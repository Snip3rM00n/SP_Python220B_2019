import sys
import logging
import datetime
import argparse

from peewee import SqliteDatabase
from peewee import IntegrityError
from peewee import Model

from customer_db_schema import Customers

def add_customer(customer_id, first_name, last_name, address, ptn, email, status, credit_limit):
    try:
        use_status = 1 if status.lower() == "active" else 0
        current = Customers.get_or_create(customer_id=customer_id,
                                          first_name=first_name,
                                          last_name=last_name,
                                          home_address=address,
                                          phone_number=ptn,
                                          email_address=email,
                                          status=use_status,
                                          credit_limit=credit_limit)
        print(current)
    except IntegrityError as ie:
        print(ie)

add_customer("fuck", "shit", "bitches", "hoes", "jizz", "dick", "active", 234.00)