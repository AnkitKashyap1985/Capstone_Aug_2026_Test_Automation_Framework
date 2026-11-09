import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
import logging
from test_configuration.etl_config import *
import pytest
import os

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

oracle_conn = create_engine(f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

mysql_conn = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATBASE}")


class BaseUtility:
    # encasulation
    def __read_file(self,file_path,file_type):
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "json":
            df = pd.read_json(file_path)
        elif file_type == "xml":
            df = pd.read_json(file_path,xpath=".//item")
        else:
            raise ValueError(f"unsupported file type {file_type}")
        return df

    #abstraction
    def read_file(self,file_path,file_type):
        return self.__read_file(file_path,file_type)

#Inheritance
class ValidationUtility(BaseUtility):

    def execute_validation(self,validation_type,test_case_name,file_path,file_type,query_actual,dbconn_actual):
        try:
            if validation_type == "FILE_TO_DB":
                df_expected = self.read_file(file_path,file_type)
                logger.info(f"expected data :{df_expected}")
                df_actual = pd.read_sql(query_actual,dbconn_actual)
                logger.info(f"actual data :{df_actual}")
                # expected minus actual
                df_extra_expected = df_expected[~df_expected.apply(tuple,axis=1).isin(df_actual.apply(tuple,axis=1))]

                # actual minus expected
                df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

                if not df_extra_expected.empty or not df_extra_actual.empty :
                    os.makedirs("differences",exist_ok=True)

                    if not df_extra_expected.empty:
                        df_extra_expected.to_csv(f"differences_{test_case_name}.csv",index=False)

                    if not df_extra_actual.empty:
                        df_extra_actual.to_csv(f"differences_{test_case_name}.csv",index=False)


                # Assertion
                assert df_actual.equals(df_expected),f"{test_case_name} failed"
                logger.info(f"{test_case_name} passed")

        except Exception as e:
            logger.error(f"{test_case_name} validation failed {e}")
            pytest.fail()

