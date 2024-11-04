from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
engine = create_engine(os.getenv('DATABASE_URL'))

Base = declarative_base()
session = sessionmaker()