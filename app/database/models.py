"""Models for the database"""
from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import ARRAY

from .instance import db_instance

Base = db_instance.base


def string_uuid():
    return str(uuid4())


class ClickInputTable(Base):
    __tablename__ = "clickInputTable"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    page_uuid = Column(
        String(10),
        nullable=False
    )
    coordinates = Column(
        ARRAY(Integer)
    )


Base.metadata.create_all(db_instance._engine)
