import sys
import logging
import datetime
import argparse

from peewee import SqliteDatabase
from peewee import IntegrityError

from customer_db_schema import Customers

parser = argparse.ArgumentParser(description='Create Customers DB')
parser.add_argument('--log-errors', action="store_true", help="Display errors in log.")

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def set_logging():
    args = parser.parse_args()

    if args.log_errors:
        LOGGER.setLevel(logging.ERROR)

def init_database():
    LOGGER.info("Initializing database...")

    database = SqliteDatabase("customers.db")
    database.connect()
    database.execute_sql("PRAGMA foreign_keys = ON;")

    LOGGER.info("Database initialized successfully.")

    return database

def create_tabels(database):
    LOGGER.info("Creating tables...")
    
    try:
        database.create_tables([Customers])
    except IntegrityError as ie:
        LOGGER.error(ie)
        LOGGER.info("Failed to create tables.")

        if LOGGER.level < logging.ERROR:
            LOGGER.info("To view the error run again with --log-errors")

def main():
    set_logging()
    database = init_database()
    create_tabels(database)


if __name__ == "__main__":
    main()
