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
    __tablename__ = 'walker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer)
    price_per_walk_small = Column(Float)
    price_per_walk_medium = Column(Float)
    price_per_walk_large = Column(Float)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, onupdate=datetime.now())
    created_by = Column(String)



class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, onupdate=datetime.now())
    created_by = Column(String)



class Dog(Base):
    __tablename__ = 'dog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    size = Column(Enum('small', 'medium', 'large', name='dog_size'), nullable=False)
    notes = Column(String)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, onupdate=datetime.now())
    created_by = Column(String)



class WalkRequest(Base):
    __tablename__ = 'walk_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    walker_id = Column(Integer, ForeignKey('walker.id'))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    requested_date = Column(Date, nullable=False)
    time_of_day = Column(Enum('morning', 'afternoon', name='time_of_day'), nullable=False)
    status = Column(Enum('pending', 'confirmed', 'rejected', name='walk_status'), default='pending')
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, onupdate=datetime.now())
    created_by = Column(String)



# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

from datetime import date, datetime

# Create Walkers
dog_walker_1 = Walker(
    first_name="John",
    last_name="Doe",
    postal_code="12345",
    phone="555-1234",
    email="john.doe@example.com",
    max_dogs_per_walk=4,
    price_per_walk_small=15.0,
    price_per_walk_medium=20.0,
    price_per_walk_large=25.0,
    created_by="Admin"
)
dog_walker_2 = Walker(
    first_name="Jane",
    last_name="Smith",
    postal_code="23456",
    phone="555-5678",
    email="jane.smith@example.com",
    max_dogs_per_walk=3,
    price_per_walk_small=12.0,
    price_per_walk_medium=18.0,
    price_per_walk_large=30.0,
    created_by="Admin"
)

# Create Owners
owner_1 = Owner(
    name="Alice Johnson",
    address="789 Apple St",
    phone="555-8765",
    email="alice.johnson@example.com",
    created_by="Admin"
)
owner_2 = Owner(
    name="Bob Brown",
    address="321 Orange Ave",
    phone="555-4321",
    email="bob.brown@example.com",
    created_by="Admin"
)

# Create Dogs for Owners
dog_1 = Dog(
    owner_id=1,  # Owner 1
    name="Fido",
    breed="Dalmatian",
    size="medium",
    notes="Very playful",
    created_by="Alice Johnson"
)
dog_2 = Dog(
    owner_id=2,  # Owner 2
    name="Rex",
    breed="German Shepherd",
    size="large",
    notes="Needs lots of exercises",
    created_by="Bob Brown"
)

dog_3 = Dog(
    owner_id=1,  # Owner 1
    name="Spot",
    breed="Beagle",
    size="small",
    notes="Loves attention",
    created_by="Alice Johnson"
)

# Create Walk Requests
walk_request_1 = WalkRequest(
    walker_id=1,  # Walker 1
    owner_id=1,  # Owner 1
    requested_date=date(2023, 10, 22),
    time_of_day="morning",
    status="pending",
    created_by="Alice Johnson"
)

walk_request_2 = WalkRequest(
    walker_id=2,  # Walker 2
    owner_id=2,  # Owner 2
    requested_date=date(2023, 10, 23),
    time_of_day="afternoon",
    status="confirmed",
    created_by="Bob Brown"
)


session.add_all([dog_walker_1, dog_walker_2, owner_1, owner_2, dog_1, dog_2, dog_3, walk_request_1, walk_request_2])
session.commit()
