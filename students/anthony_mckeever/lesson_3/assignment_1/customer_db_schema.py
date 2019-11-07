# Advanced Programming In Python - Lesson 3 Assigmnet 1: Automated Testing
# RedMine Issue - SchoolOps-13
# Code Poet: Anthony McKeever
# Start Date: 11/06/2019
# End Date:

import sys
import logging
import datetime
import argparse

from peewee import SqliteDatabase
from peewee import IntegrityError
from peewee import Model

from peewee import CharField
from peewee import BitField
from peewee import DateField
from peewee import DateTimeField
from peewee import DecimalField
from peewee import ForeignKeyField

parser = argparse.ArgumentParser(description='Create Customers DB')
parser.add_argument('--log-errors', action="store_true", help="Display errors in log.")

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info("Initializing database...")

DATABASE = SqliteDatabase("customers.db")
DATABASE.connect()
DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

LOGGER.info("Database initialized successfully.")


class BaseModel(Model):
    class Meta:
        database = DATABASE

class Customers(BaseModel):
    customer_id = CharField(primary_key=True, unique=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=200)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=30)
    status = BitField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_modified = DateTimeField(default=datetime.datetime.now)


def set_logging():
    args = parser.parse_args()

    if args.log_errors:
        LOGGER.setLevel(logging.ERROR)

def main():
    set_logging()
    LOGGER.info("Creating tables...")
    
    try:
        DATABASE.create_tables([Customers])
    except IntegrityError as ie:
        LOGGER.error(ie)
        LOGGER.info("Failed to create tables.")

        if LOGGER.level < logging.ERROR:
            LOGGER.info("To view the error run again with --log-errors")
    

if __name__ == "__main__":
    main()