import inspect
import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
import logging
import os

from common_utilities.utilities import ValidationUtility, BaseUtility
from test_configuration.etl_config import *
import pytest

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataExtraction:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()


    def test_data_extraction_supplier_file_stag(self,connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from stag_supplier"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/supplier_data.json",
                                                       file_type="json",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_mysql_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    def test_data_extraction_inventory_file_stag(self,connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from stag_inventory"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/inventory_data.xml",
                                                       file_type="xml",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_mysql_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()


    def test_data_extraction_product_file_stag(self, connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            # Download only if the file is not already available locally
            if not os.path.exists(LOCAL_FILE_PATH):
                logger.info("Local file not found. Downloading from Linux server...")
                self.base_utility.linux_utility_download_file_from_linux_server()
            else:
                logger.info(f"File already exists: {LOCAL_FILE_PATH}. Skipping download.")
            query_actual = """select * from stag_product"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path=LOCAL_FILE_PATH,
                                                       file_type="csv",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_mysql_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    def test_data_extraction_sales_file_stag(self, connect_mysql_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")

        try:
            query_actual = """select * from stag_sales"""
            self.validation_utility.execute_validation(validation_type="S3_TO_DB",
                                                       test_case_name=test_case_name,
                                                       bucket_name=BUCKET_NAME,
                                                       file_key=FILE_KEY,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_mysql_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    def test_data_extraction_stores_db_stag(self, connect_mysql_database,connect_oracle_database):
        pass