# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


class Walker(Base):
    """description: Table for storing dog walker information."""
    __tablename__ = 'walker'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    rate_small = Column(Float, nullable=False)
    rate_medium = Column(Float, nullable=False)
    rate_large = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.datetime.now)
    created_by = Column(String)


class Owner(Base):
    """description: Table for registering dog owners."""
    __tablename__ = 'owner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.datetime.now)
    created_by = Column(String)


class Dog(Base):
    """description: Table for storing dog information related to owners."""
    __tablename__ = 'dog'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    size = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.datetime.now)
    created_by = Column(String)


class Walk(Base):
    """description: Table for storing walk requests and confirmations."""
    __tablename__ = 'walk'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    walker_id = Column(Integer, ForeignKey('walker.id'))
    dog_id = Column(Integer, ForeignKey('dog.id'))
    day_of_week = Column(String, nullable=False)
    time_of_day = Column(String, nullable=False)
    status = Column(String, nullable=False)  # Possible values: 'requested', 'confirmed', 'rejected'
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.datetime.now)
    created_by = Column(String)


class Payment(Base):
    """description: Table for recording payments made by owners to walkers for walks."""
    __tablename__ = 'payment'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    walk_id = Column(Integer, ForeignKey('walk.id'))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    amount = Column(Float, nullable=False)
    date_paid = Column(DateTime, default=datetime.datetime.now)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.datetime.now)
    created_by = Column(String)


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

# Walkers
date1 = datetime.datetime(2023, 10, 15)
walker1 = Walker(first_name='John', last_name='Doe', postal_code='12345', phone='555-1010', 
                 email='johndoe@example.com', max_dogs_per_walk=3, rate_small=10.0, rate_medium=15.0, rate_large=20.0,
                 created_date=date1, created_by='admin')
walker2 = Walker(first_name='Jane', last_name='Smith', postal_code='54321', phone='555-2020', 
                 email='janesmith@example.com', max_dogs_per_walk=4, rate_small=12.0, rate_medium=18.0, rate_large=25.0,
                 created_date=date1, created_by='admin')

# Owners
date2 = datetime.datetime(2023, 11, 10)
owner1 = Owner(name='Emily Jones', address='123 Elm St', phone='555-3030', 
               email='emilyjones@example.com', created_date=date2, created_by='admin')
owner2 = Owner(name='Michael Brown', address='456 Oak Ave', phone='555-4040', 
               email='michaelbrown@example.com', created_date=date2, created_by='admin')

# Dogs
dog1 = Dog(owner_id=1, name='Rex', breed='Labrador', size='large', notes='Friendly', 
            created_date=date2, created_by='owner')
dog2 = Dog(owner_id=1, name='Bella', breed='Beagle', size='medium', notes='Loves to play', 
            created_date=date2, created_by='owner')
dog3 = Dog(owner_id=2, name='Charlie', breed='Poodle', size='small', notes='Very active', 
            created_date=date2, created_by='owner')

# Walks
date3 = datetime.datetime(2023, 12, 5)
walk1 = Walk(walker_id=1, dog_id=1, day_of_week='Mon', time_of_day='morning', status='requested', 
             created_date=date3, created_by='owner')
walk2 = Walk(walker_id=2, dog_id=3, day_of_week='Wed', time_of_day='afternoon', status='confirmed', 
             created_date=date3, created_by='owner')

# Payments
payment1 = Payment(walk_id=2, owner_id=2, amount=25.0, date_paid=date3, created_date=date3, created_by='system')




session.add_all([date1, walker1, walker2, date2, owner1, owner2, dog1, dog2, dog3, date3, walk1, walk2, payment1])
session.commit()
