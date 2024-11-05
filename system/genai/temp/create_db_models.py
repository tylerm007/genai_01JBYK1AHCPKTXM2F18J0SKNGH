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
    """description: Represents a registered dog walker who can set availability and accept walk requests."""
    __tablename__ = 'walker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    small_dog_price = Column(Float, nullable=False)
    medium_dog_price = Column(Float, nullable=False)
    large_dog_price = Column(Float, nullable=False)
    available_days = Column(String, nullable=False)  # "Mon,Tues,..."
    available_times = Column(String, nullable=False)  # "morning,afternoon"
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)


class Owner(Base):
    """description: Represents a dog owner who can register dogs and request walks."""
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)


class Dog(Base):
    """description: Represents a dog belonging to an owner, with details about their breed and size."""
    __tablename__ = 'dog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    size = Column(String, nullable=False)  # small, medium, large
    notes = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)


class WalkRequest(Base):
    """description: Represents a request for a walk made by an owner for their dogs, matched to available walkers."""
    __tablename__ = 'walk_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    walker_id = Column(Integer, ForeignKey('walker.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    time_slot = Column(String, nullable=False)  # morning, afternoon
    status = Column(String, nullable=False, default='pending')  # pending, confirmed, rejected
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)


class Payment(Base):
    """description: Represents payment records for completed dog walks."""
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    walk_request_id = Column(Integer, ForeignKey('walk_request.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

from datetime import date

walker_1 = Walker(
    first_name='John',
    last_name='Doe',
    postal_code='12345',
    phone='123-456-7890',
    email='john.doe@example.com',
    max_dogs_per_walk=5,
    small_dog_price=15.00,
    medium_dog_price=20.00,
    large_dog_price=25.00,
    available_days='Mon,Tues,Wed',
    available_times='morning,afternoon',
    created_by='system'
)

owner_1 = Owner(
    name='Jane Smith',
    address='456 Elm St',
    phone='987-654-3210',
    email='jane.smith@example.com',
    created_by='system'
)

dog_1 = Dog(
    owner_id=1,
    name='Buddy',
    breed='Golden Retriever',
    size='large',
    notes='Very friendly',
    created_by='system'
)

dog_2 = Dog(
    owner_id=1,
    name='Bella',
    breed='Beagle',
    size='medium',
    notes='Loves treats',
    created_by='system'
)

walk_request_1 = WalkRequest(
    owner_id=1,
    walker_id=1,
    scheduled_date=date(2023, 10, 21),
    time_slot='morning',
    status='pending',
    created_by='system'
)

payment_1 = Payment(
    walk_request_id=1,
    amount=35.00,
    payment_date=date(2023, 10, 21),
    created_by='system'
)


session.add_all([walker_1, owner_1, dog_1, dog_2, walk_request_1, payment_1])
session.commit()
