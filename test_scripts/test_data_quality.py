import inspect
import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
import logging
import os
import pytest

from common_utilities.utilities import ValidationUtility, BaseUtility, FileUtility, DataQuality
from test_configuration.etl_config import *
import pytest

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataQuality:
    file_utility = FileUtility()
    data_quality_utility = DataQuality()


    def test_data_quality_file_existence_of_inventory_data_xml_file(self):
        try:
            file_status = self.file_utility.check_file_exists("test_data/inventory_data.xml")
            assert file_status is True,"Inventory data file does not exist"
        except Exception as e:
            logger.error(f"Error while cheking file existence {e}")
            pytest.fail(f"Error while cheking file existence {e}")

    def test_data_quality_file_existence_of_supplier_data_json_file(self):
        pass

    def test_data_quality_file_existence_of_products_data_csv_file(self):
        pass


    def test_data_quality_file_size_of_inventory_data_xml_file(self):
        try:
            file_status = self.file_utility.check_file_size("test_data/inventory_data.xml")
            assert file_status is True,"Inventory data file is empty"
        except Exception as e:
            logger.error(f"Error while cheking file size {e}")
            pytest.fail(f"Error while cheking file size {e}")

    def test_data_quality_file_size_of_supplier_data_json_file(self):
        pass

    def test_data_quality_file_size_of_product_data_csv_file(self):
        pass


    def test_data_quality_duplicate_check_for_supplier_data_json_file(self):
        try:
            duplicate_status = self.data_quality_utility.check_duplicate_in_file("test_data/supplier_data.json","json")
            assert duplicate_status is True,"Supplier data file is having duplicates"
        except Exception as e:
            logger.error(f"Error while cheking duplicate in file {e}")
            pytest.fail(f"Error while cheking duplicate in file {e}")
