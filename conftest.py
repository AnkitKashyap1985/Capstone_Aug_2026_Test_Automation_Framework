import inspect

import  pandas as pd
from sqlalchemy import create_engine,text
import cx_Oracle
import logging
from test_configuration.etl_config import *
import pytest

logging.basicConfig(
    filename='test_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s-%(levelname)s-%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture()
def connect_mysql_database():
    logger.info("mysql databse connection is being established..")
    mysql_conn = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATBASE}")
    logger.info("mysql databse connection has been established..")
    yield mysql_conn
    logger.info("mysql databse connection has been terminated..")


@pytest.fixture()
def connect_oracle_database():
    logger.info("oracle databse connection is being established..")
    oracle_conn = create_engine(
        f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")
    logger.info("oracle databse connection has been established..")
    yield oracle_conn
    logger.info("oracle databse connection has been terminated..")

