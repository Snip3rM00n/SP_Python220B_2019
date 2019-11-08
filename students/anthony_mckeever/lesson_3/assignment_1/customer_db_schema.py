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

from peewee import BitField
from peewee import CharField
from peewee import DateField
from peewee import DecimalField
from peewee import DateTimeField

DATABASE = SqliteDatabase("customers.db")
DATABASE.connect()
DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

class BaseModel(Model):
    class Meta:
        database = DATABASE

class Customers(BaseModel):
    customer_id = CharField(primary_key=True, unique=True, max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=200, null=True)
    phone_number = CharField(max_length=20, null=True)
    email_address = CharField(max_length=30, null=True)
    status = BitField()
    credit_limit = DecimalField(max_digits=10, decimal_places=2, null=True)
    date_created = DateTimeField(default=datetime.datetime.now)
    date_modified = DateTimeField(default=datetime.datetime.now)
