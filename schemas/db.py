from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

SQL_URL = 'sqlite:///youdb.db'

engine = create_engine(SQL_URL, echo = True)
