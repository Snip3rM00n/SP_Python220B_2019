# Advanced Programming In Python - Lesson 5 Assignment 1: Customer NoSQL DB
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 11/20/2019
# End Date:

"""
Customer and Product Database Helper

Helps connect to and read content from the Customer and Product NoSQL databases
"""

import csv
import os.path

from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def ingest_file(database, directory, file_name, collection):
    file_path = os.path.join(directory, file_name)
    db_collection = database[collection]
    errors = 0

    try:
        with open(file_path) as open_file:
            contents = csv.DictReader(open_file)
            for row in contents:
                try:
                    db_collection.insert_one(row)
                except Exception as exception:
                    print(exception)
                    errors += 1
    except Exception as ex:
        print(ex)

    return errors, db_collection.count()


def import_data(directory_name, product_file, customer_file, rentals_file):
    mongo = MongoDBConnection()

    product_errors, customer_errors, rentals_errors = 0, 0, 0
    products, customers, rentals = 0, 0, 0
    
    with mongo:
        database = mongo.connection.hp_norton
        product_errors, products = ingest_file(database,
                                               directory_name,
                                               product_file,
                                               "products")
        customer_errors, customers = ingest_file(database,
                                                 directory_name,
                                                 customer_file,
                                                 "customers")
        rentals_errors, rentals = ingest_file(database,
                                              directory_name,
                                              rentals_file,
                                              "rentals")
    
    records = (products, customers, rentals)
    errors = (product_errors, customer_errors, rentals_errors)
    return records, errors
