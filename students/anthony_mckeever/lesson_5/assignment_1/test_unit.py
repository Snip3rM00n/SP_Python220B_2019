# Advanced Programming In Python - Lesson 5 Assignment 1: Customer NoSQL DB
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 11/20/2019
# End Date:

from unittest import TestCase
from unittest import mock
from unittest.mock import patch
from unittest.mock import MagicMock

import pymongo
from pymongo.errors import DuplicateKeyError

import database as Database

class TestDatabase(TestCase):

    def setUp(self):
        Database.LOGGER = MagicMock()

    def test_format_row_integers(self):
        row = {"test_string": "three", "test_int": "3", "test_dec": "3.14"}
        row = Database.format_row_integers(row)

        self.assertEqual("three", row["test_string"])
        self.assertEqual(3, row["test_int"])
        self.assertEqual("3.14", row["test_dec"])
    
    def test_ingest_file_golden_path(self):
        contents = str("test1,test2,test3" + 
                       "\nval1:1,val1:2,val1:3" + 
                       "\nval2:1,val2:2,val2:3" + 
                       "\nval3:1,val3:2,val3:3")
        open_mock = mock.mock_open(read_data=contents)

        with patch("builtins.open", open_mock):
            Database.MongoDBConnection = MagicMock()
            pymongo.database.Collection = MagicMock()
            pymongo.database.Collection.insert_one = MagicMock()

            ingest_val = Database.ingest_file(Database.MongoClient(),
                                              ".",
                                              "file",
                                              "test")
            self.assertEqual(2, len(ingest_val))
            self.assertEqual(0, ingest_val[0])  # Validate no errors occured.


    #def test_ingest_file_duplicate_key(self):
    #    contents = str("test1,test2,test3" + 
    #                   "\nval1:1,val1:2,val1:3")
    #    open_mock = mock.mock_open(read_data=contents)
#
    #    with patch("builtins.open", open_mock):
    #        Database.MongoDBConnection = MagicMock()
    #        Database.MongoDBConnection().hp_norton = MagicMock()
    #        Database.MongoDBConnection().hp_norton["test"] = MagicMock()
    #        Database.MongoDBConnection().hp_norton["test"].insert_one = MagicMock()
    #        Database.MongoDBConnection().hp_norton["test"].insert_one.side_effect = [DuplicateKeyError("Test")]
#
    #        ingest_val = Database.ingest_file(Database.MongoClient(),
    #                                          ".",
    #                                          "file",
    #                                          "test")
#
    #        self.assertEqual(2, len(ingest_val))
    #        self.assertEqual(1, ingest_val[0])
            
    def test_ingest_file_not_found(self):
        open_mock = mock.mock_open()
        open_mock.side_effect = [FileNotFoundError("test")]

        with patch("builtins.open", open_mock):
            #pymongo.database.Collection = MagicMock()

            ingest_val = Database.ingest_file(Database.MongoClient(),
                                              ".",
                                              "file",
                                              "test")

            self.assertEqual(2, len(ingest_val))
            self.assertEqual(1, ingest_val[0])

    def test_import_data(self):
        with patch("database.ingest_file") as ingest_mock:
            #pymongo.database.Collection = MagicMock()

            ingest_mock.return_value = ((1, 2, 3), (4, 5, 6))
            values = Database.import_data(".", ".", ".", ".")

            self.assertEqual(3, len(values[0]))
            self.assertEqual(3, len(values[1]))

    #@mock.patch("pymongo.collection.Collection.find")
    def test_show_available_products(self):
        output = {"_id": "test", "test1": "test"}
        #mock_find.return_value = [output]
        #Database.MongoDBConnection = MagicMock()

        products = Database.show_available_products()
        self.assertEqual(products["test"], {"test1": "test"})