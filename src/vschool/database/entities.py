from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, Text,
                        DECIMAL, DATETIME, func, ForeignKey,
                        CheckConstraint, PrimaryKeyConstraint, 
                        ForeignKeyConstraint)
from decimal import Decimal
from datetime import datetime

# Define the base class for ORM models
Base = declarative_base()

class SerializerMixin:
    def to_dict(self):
        ret = {}
        for c in self.__table__.columns:
            if isinstance(getattr(self, c.name), datetime):
                ret[c.name] = getattr(self, c.name).strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(getattr(self, c.name), Decimal):
                ret[c.name] = float(getattr(self, c.name))
            else:
                ret[c.name] = getattr(self, c.name)
        return ret

# Define the ORM model
class Course(Base, SerializerMixin):
    __tablename__ = 'Course'

    course_id = Column(Text, nullable=False)
    class_id = Column(Integer, nullable=False)
    course_name = Column(Text, nullable=False)
    department = Column(Text, nullable=False)
    teacher = Column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("length(course_id) = 8 AND course_id GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'"),
        PrimaryKeyConstraint('course_id', 'class_id', name='pk_course'),
    )

class Schedule(Base, SerializerMixin):
    __tablename__ = 'Schedule'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Text, nullable=False)
    class_id = Column(Integer, nullable=False)
    start_week = Column(Integer, nullable=False)
    end_week = Column(Integer, nullable=False)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    location = Column(Text, nullable=False)
    frequency = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['course_id', 'class_id'], ['Course.course_id', 'Course.class_id']),
    )