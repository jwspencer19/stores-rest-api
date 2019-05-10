from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = "postgres://postgres:docker@localhost:5432/postgres"

db = create_engine(db_string)
base = declarative_base()


class UserModel(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80))
    password = Column(String(80))


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# Create
test1 = UserModel(username="username1", password="password1")
session.add(test1)
session.commit()
