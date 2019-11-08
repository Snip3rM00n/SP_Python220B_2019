import sys
import csv
import logging
import datetime
import argparse

from itertools import islice

from peewee import SqliteDatabase
from peewee import IntegrityError

from customer_db_schema import Customers

parser = argparse.ArgumentParser(description='Create Customers DB')
parser.add_argument('--debug', type=int, default=0,
                    help="Display errors in log.")
parser.add_argument('--import-file', type=str, default=None,
                    help="A CSV of customers to import.")
parser.add_argument('--import-bandwidth', type=int, default=5,
                    help="Max customers to hold in memory during import")

def set_logging(level):
    log_level = parse_log_level(level)

    formatter = str("%(asctime)s %(filename)s:%(lineno)-3d " +
                    "%(levelname)s %(message)s")
    log_format = logging.Formatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    logger.addHandler(console_handler)

def parse_log_level(level):
    """
    Parses the logging level from the debug integer as set in the arguments.

    :level: The logging level to parse.
    """
    log_levels = {0: logging.INFO,
                  1: logging.ERROR,
                  2: logging.DEBUG}

    log_level = log_levels.get(level)

    if log_level is None:
        raise ValueError(f"Logging level {level} has no implementation.")

    return log_level

def init_database():
    logging.info("Initializing database...")

    database = SqliteDatabase("customers.db")
    database.connect()
    database.execute_sql("PRAGMA foreign_keys = ON;")

    logging.info("Database initialized successfully.")

    return database

def create_tabels(database):
    logging.info("Creating tables...")
    
    try:
        database.create_tables([Customers])
    except IntegrityError as ie:
        log_error(ie, "Failed to create tables.", should_exit=True)

def import_customers(database, file):
    with open(file, "r") as in_file:
        contents = list(islice(in_file, 5))
        
        while len(contents) > 0:
            write_customers(database, contents)
            contents = list(islice(in_file, 5))

def write_customers(database, customer_list):
    for customer in customer_list:
        try:
            customer = customer.split(',')
            current = Customers.get_or_create(customer_id=customer[0],
                                              first_name=customer[1],
                                              last_name=customer[2],
                                              home_address=customer[3],
                                              phone_number=customer[4],
                                              email_address=customer[5],
                                              status=customer[6],
                                              credit_limit=customer[7])
            logging.info("Customer written successfully.")
            logging.debug(current)
        except IntegrityError as ie:
            log_error(ie, "Failed to write customer.", should_exit=False)
            logging.debug(customer)

def log_error(error, msg, should_exit):
    logging.error(error)
    logging.info(msg)

    if should_exit:
        logging.info("Terminating application...")

def main(args):
    set_logging(args.debug)
    database = init_database()
    create_tabels(database)

    if args.import_file is not None:
        import_customers(database, args.import_file)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
