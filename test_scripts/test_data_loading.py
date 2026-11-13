import inspect
import  pandas as pd
from sqlalchemy import create_engine,text
import logging

from common_utilities.utilities import ValidationUtility, BaseUtility
from test_configuration.etl_config import *
import pytest

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataLoading:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()



    def test_data_loading_for_monthly_sales_summary(self, connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_expected = """select product_id,month,year,total_sales from monthly_sales_summary_source order by product_id"""
            query_actual = """select product_id,month,year,total_sales from monthly_sales_summary order by product_id"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_mysql_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_mysql_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()


    def test_data_loading_for_fact_inventory(self, connect_mysql_database):
        pass

    def test_data_loading_for_fact_sales(self, connect_mysql_database):
        pass

    def test_data_loading_for_inventory_level_by_stores(self, connect_mysql_database):
        pass