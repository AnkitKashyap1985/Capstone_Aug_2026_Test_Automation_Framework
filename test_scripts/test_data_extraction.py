import inspect

import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
import logging

from common_utilities.utilities import ValidationUtility
from test_configuration.etl_config import *
import pytest

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)



oracle_conn = create_engine(f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

mysql_conn = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATBASE}")


class TestDataExtraction:
    validation_utility = ValidationUtility()


    def test_data_extraction_sales_file_stag(self):
        try:
            df_expected = pd.read_csv("test_data/sales_data.csv")
            query_actual = """select * from stag_sale"""
            df_actual = pd.read_sql(query_actual,mysql_conn)
            assert df_expected.equals(df_actual),"sale data between source and stag did not match"
        except Exception as e:
            logger.error(f"test case failed :{e}")
            pytest.fail()


'''
    def test_data_extraction_product_file_stag(self):
        df_expected = pd.read_csv("test_data/product_data_from_linux.csv")
        query_actual = """select * from stag_product"""
        df_actual = pd.read_sql(query_actual,mysql_conn)
        assert df_expected.equals(df_actual),"product data between source and stag did not match"
'''