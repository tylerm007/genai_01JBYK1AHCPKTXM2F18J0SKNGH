# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 05, 2024 16:39:02
# Database: sqlite:////tmp/tmp.vqtBxcdU5M-01JBYK1AHCPKTXM2F18J0SKNGH/DogWalkingBusiness/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Owner(SAFRSBaseX, Base):
    """
    description: Represents a dog owner who can register dogs and request walks.
    """
    __tablename__ = 'owner'
    _s_collection_name = 'Owner'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")
    WalkRequestList : Mapped[List["WalkRequest"]] = relationship(back_populates="owner")



class Walker(SAFRSBaseX, Base):
    """
    description: Represents a registered dog walker who can set availability and accept walk requests.
    """
    __tablename__ = 'walker'
    _s_collection_name = 'Walker'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    small_dog_price = Column(Float, nullable=False)
    medium_dog_price = Column(Float, nullable=False)
    large_dog_price = Column(Float, nullable=False)
    available_days = Column(String, nullable=False)
    available_times = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    WalkRequestList : Mapped[List["WalkRequest"]] = relationship(back_populates="walker")



class Dog(SAFRSBaseX, Base):
    """
    description: Represents a dog belonging to an owner, with details about their breed and size.
    """
    __tablename__ = 'dog'
    _s_collection_name = 'Dog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    size = Column(String, nullable=False)
    notes = Column(String)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)



class WalkRequest(SAFRSBaseX, Base):
    """
    description: Represents a request for a walk made by an owner for their dogs, matched to available walkers.
    """
    __tablename__ = 'walk_request'
    _s_collection_name = 'WalkRequest'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    walker_id = Column(ForeignKey('walker.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    time_slot = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("WalkRequestList"))
    walker : Mapped["Walker"] = relationship(back_populates=("WalkRequestList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="walk_request")



class Payment(SAFRSBaseX, Base):
    """
    description: Represents payment records for completed dog walks.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    walk_request_id = Column(ForeignKey('walk_request.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)

    # parent relationships (access parent)
    walk_request : Mapped["WalkRequest"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
