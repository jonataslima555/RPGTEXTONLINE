from peewee import SqliteDatabase
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DB_NAME = getenv('DB_NAME')

db = SqliteDatabase(DB_NAME)

from models import *
