import inspect
import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
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


class TestDataTransformation:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    def test_data_transformation_for_filter_sales_data(self, connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_expected = """select sales_id,product_id,store_id,quantity,price,sale_date,region from stag_sales  where sale_date>='2026-09-01'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from filtered_sales"""
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

    def test_data_transformation_for_router_high_sales_data(self, connect_mysql_database):
        pass

    def test_data_transformation_for_router_low_sales_data(self, connect_mysql_database):
        pass

    def test_data_transformation_for_aggregator_sales(self, connect_mysql_database):
        pass

    def test_data_transformation_for_joiner(self, connect_mysql_database):
        pass

    def test_data_transformation_aggregator_inventory(self, connect_mysql_database):
        pass