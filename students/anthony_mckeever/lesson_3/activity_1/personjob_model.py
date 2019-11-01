"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

# if you wanted to use heroku postgres:
#
# psycopg2
#
# parse.uses_netloc.append("postgres")
# url = parse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
# database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
# database = conn.cursor()
#
# Also consider elephantsql.com (be sure to use configparser for PWß)

logger.info('This means we can easily switch to a different database')

logger.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)

    @property
    def duration(self):
        if self.start_date is not None and self.end_date is not None:
            formatter = "%Y-%m-%d"
            return (datetime.datetime.strftime(self.start_date, formatter) -
                    datetime.datetime.strftime(self.end_date, formatter)) 

class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")
    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Department(BaseModel):
    department_name = CharField(max_length=30)
    department_number = CharField(primary_key=True, max_length=4)
    department_manager = ForeignKeyField(Person, to_field='person_name', null=True)

class PersonToDepartment(BaseModel):
    person = ForeignKeyField(Person, to_field="person_name", null=False)
    job = ForeignKeyField(Job, to_field="job_name", null=False)
    department = ForeignKeyField(Department, to_field="department_number", null=False)
    duration_days = ForeignKeyField(Job, to_field="duration", null=False)


people = [{"name": "Kima", "town": "Yukayosha", "nickname": None},
          {"name": "Delilah", "town": "Misty Autumn", "nickname": "Lilah"},
          {"name": "Astra", "town": "Almia", "nickname": None},
          {"name": "Cresenta", "town": "Almia", "nickname": "Cressy"},
          {"name": "Katie", "town": "Lovel", "nickname": "Kate"},
          {"name": "Mayrina", "town": "Collette", "nickname": "Mari"},
          {"name": "Kayomi", "town": "New Sophiesville", "nickname": "Yomi"},
          {"name": "Svetlana", "town": "Kiev", "nickname": "Lana"},
          {"name": "Phoebe", "town": "Ekiya Space Station", "nickname": None}]

jobs = [{"title": "Temporal Analyst", "start": "0012-06-19", "end":"2353-05-30", "salary": 7500},
        {"title": "Temporal Developer", "start": "2150-10-04", "end":"2353-05-30", "salary": 7000},
        {"title": "Temporal Facilitator", "start": "2323-04-13", "end":"2353-05-30", "salary": 7000},
        {"title": "Deep Field Operative", "start": "2153-08-23", "end":"2153-09-08", "salary": 8231},
        {"title": "Near Field Operative", "start": "2130-03-13", "end":"2167-02-14", "salary": 5000},
        {"title": "Temporal Debugger", "start": "2170-12-26", "end":"2353-05-30", "salary": 6000},
        {"title": "Researcher", "start": "2149-01-20", "end":"2154-01-19", "salary": 4000}]

depts = [{"department_name": "Temporal Integrity", "department_number": "T832", "department_manager": "Kima"},
         {"department_name": "Astrometic Intelligence", "department_number": "A149", "department_manager": "Mayrina"},
         {"department_name": "Temporal Refactory", "department_number": "T956", "department_manager": "Katie"},
         {"department_name": "Forbidden Weaponry", "department_number": "S004", "department_manager": "Phoebe"}]

relations = [{"name": "Kima", "title": "Temporal Facilitator", "department": "T832"},
             {"name": "Astra", "title": "Temporal Analyst", "department": "T832"},
             {"name": "Delilah", "title": "Temporal Developer", "department": "T832"},
             {"name": "Cresenta", "title": "Deep Field Operative", "department": "A149"},
             {"name": "Mayrina", "title": "Near Field Operative", "department": "A149"},
             {"name": "Kayomi", "title": "Near Field Operative", "department": "A149"},
             {"name": "Phoebe", "title": "Researcher", "department": "S004"},
             {"name": "Katie", "title": "Temporal Debugger", "department": "T956"},
             {"name": "Svetlana", "title": "Temporal Debugger", "department": "T956"}]