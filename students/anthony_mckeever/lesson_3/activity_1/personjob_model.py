"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import sys
import logging
from datetime import datetime

from peewee import SqliteDatabase
from peewee import IntegrityError
from peewee import Model

from peewee import CharField
from peewee import DateField
from peewee import DecimalField
from peewee import ForeignKeyField

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Define Person table...')
    
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)
    
    logger.info("Table defined successfully.")

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    logger.info('Define Job table...')

    job_id = CharField(primary_key=True, max_length=4)
    job_name = CharField(max_length = 30)

    logger.info("Table defined successfully.")

class PersonToJob(BaseModel):
    logger.info('Define PersonToJob table...')

    person_name = ForeignKeyField(Person, to_field="person_name")
    job_id = ForeignKeyField(Job, to_field="job_id")

    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')

    salary = DecimalField(max_digits = 7, decimal_places = 2)
    duration_days = DecimalField(max_digits=7, decimal_places=0, null=True)

    logger.info("Table defined successfully.")

class Department(BaseModel):
    logger.info('Define Department table...')

    department_name = CharField(max_length=30)
    department_id = CharField(primary_key=True, max_length=4)
    manager = ForeignKeyField(Person, to_field='person_name', null=True)

    logger.info("Table defined successfully.")

class PersonToDepartment(BaseModel):
    logger.info('Define PersonToDepartment table...')

    person = ForeignKeyField(Person, to_field="person_name", null=False)
    department = ForeignKeyField(Department, to_field="department_id", null=False)
 
    logger.info("Table defined successfully.")

people = [{"name": "Kima",     "town": "Yukayosha",           "nickname": None},
          {"name": "Delilah",  "town": "Misty Autumn",        "nickname": "Lilah"},
          {"name": "Astra",    "town": "Almia",               "nickname": None},
          {"name": "Cresenta", "town": "Almia",               "nickname": "Cressy"},
          {"name": "Katie",    "town": "Lovel",               "nickname": "Kate"},
          {"name": "Mayrina",  "town": "Collette",            "nickname": "Mari"},
          {"name": "Kayomi",   "town": "New Sophiesville",    "nickname": "Yomi"},
          {"name": "Svetlana", "town": "Kiev",                "nickname": "Lana"},
          {"name": "Phoebe",   "town": "Ekiya Space Station", "nickname": None}]

jobs = [{"title": "Temporal Analyst I",     "id": "TA01"},
        {"title": "Temporal Developer I",   "id": "TD01"},
        {"title": "Temporal Facilitator I", "id": "TF01"},
        {"title": "Deep Field Operative",   "id": "DFO1"},
        {"title": "Near Field Operative",   "id": "NFO1"},
        {"title": "Temporal Debugger",      "id": "TDBR"},
        {"title": "Researcher III",         "id": "RES3"}]

people_jobs = [{"name": "Kima",     "job": "TF01", "start": "2323-04-13", "end": "2353-05-30", "salary": "7000"},
               {"name": "Delilah",  "job": "TD01", "start": "2150-10-04", "end": "2353-05-30", "salary": "7000"},
               {"name": "Astra",    "job": "TA01", "start": "0012-06-19", "end": "2353-05-30", "salary": "7500"},
               {"name": "Cresenta", "job": "DFO1", "start": "2153-08-23", "end": "2153-09-08", "salary": "8231"},
               {"name": "Katie",    "job": "TDBR", "start": "2170-12-26", "end": "2353-05-30", "salary": "6500"},
               {"name": "Mayrina",  "job": "NFO1", "start": "2130-03-13", "end": "2167-02-14", "salary": "5000"},
               {"name": "Kayomi",   "job": "NFO1", "start": "2103-11-01", "end": "2117-04-05", "salary": "5000"},
               {"name": "Svetlana", "job": "TDBR", "start": "1961-05-23", "end": "2353-05-30", "salary": "6000"},
               {"name": "Phoebe",   "job": "RES3", "start": "2149-01-20", "end": "2154-01-19", "salary": "4600"}]

depts = [{"name": "Temporal Integrity",      "number": "T832", "manager": "Kima"},
         {"name": "Astrometic Intelligence", "number": "A149", "manager": "Mayrina"},
         {"name": "Temporal Refactory",      "number": "T956", "manager": "Katie"},
         {"name": "Forbidden Weaponry",      "number": "S004", "manager": "Phoebe"}]

relations = [{"name": "Kima",     "department": "T832"},
             {"name": "Astra",    "department": "T832"},
             {"name": "Delilah",  "department": "T832"},
             {"name": "Cresenta", "department": "A149"},
             {"name": "Mayrina",  "department": "A149"},
             {"name": "Kayomi",   "department": "A149"},
             {"name": "Phoebe",   "department": "S004"},
             {"name": "Katie",    "department": "T956"},
             {"name": "Svetlana", "department": "T956"}]

def populate_people(list_people):
    logger.info("Start populating people")

    for person in list_people:
        try:
            current = Person.get_or_create(person_name=person["name"],
                                           lives_in_town=person["town"],
                                           nickname=person["nickname"])
            logger.debug('Saved Person: %s', current)
        except IntegrityError as ie:
            logger.debug("Failed to save person: %d", person)
            logger.error(ie)
    
    logger.info("Finished populating people")

def populate_jobs(list_jobs):
    logger.info("Start populating jobs")

    for job in list_jobs:
        try:
            current = Job.get_or_create(job_id=job["id"],
                                        job_name=job["title"])
            logger.debug('Saved Job: %s', current)
        except IntegrityError as ie:
            logger.debug("Failed to save job: %d", job)
            logger.error(ie)

    logger.info("Finished populating jobs")

def populate_person_to_job(list_pj):
    logger.info("Start populating PersonToJob")

    for pj in list_pj:
        try:
            duration = None
            start = pj.get("start")
            end = pj.get("end")
                        
            if start is not None and end is not None:
                formatter = "%Y-%m-%d"
                start_date = datetime.strptime(start, formatter)
                end_date = datetime.strptime(end, formatter)
                duration = (end_date - start_date).days

            person = Person.get(Person.person_name == pj["name"])
            job = Job.get(Job.job_id == pj["job"])

            current = PersonToJob.get_or_create(person_name=person.person_name,
                                                job_id=job.job_id,
                                                start_date=start,
                                                end_date=end,
                                                salary=pj["salary"],
                                                duration_days=duration)

            logger.debug('Saved PersonToJob: %s', current)
        except IntegrityError as ie:
            logger.debug("Failed to save PersonToJob: %d", pj)
            logger.error(ie)

    logger.info("Finished populating PersonToJob")

def populate_departments(list_depts):
    logger.info("Start populating departments")

    for dept in list_depts:
        try:
            current = Department.get_or_create(department_name=dept["name"],
                                               department_id=dept["number"],
                                               manager=dept["manager"])
            logger.debug('Saved Department: %s', current)
        except IntegrityError as ie:
            logger.debug("Failed to save Department: %d", dept)
            logger.error(ie)

    logger.info("Finished populating departments")

def populate_relations(list_relation):
    logger.info("Start populating PeopleToDepartment")
    for relation in list_relation:
        person = Person.get(Person.person_name == relation["name"])
        dept = Department.get(Department.department_id == relation["department"])        
        
        PersonToDepartment.get_or_create(person=person.person_name,
                                         department=dept.department_id)

    logger.info("Finished populating PeopleToDepartment")

def main():
    try:
        logger.info("Initialize database...")
        database.create_tables([Person, Job, PersonToJob,
                                Department, PersonToDepartment])
        logger.info("Database initialized successfully.")
        
    except IntegrityError as ie:
        logger.error(ie)
        logger.info("Failed to initialize database.  Exiting.")

        sys.exit()

    populate_people(people)
    populate_jobs(jobs)
    populate_person_to_job(people_jobs)
    populate_departments(depts)
    populate_relations(relations)

if __name__ == "__main__":
    main()
