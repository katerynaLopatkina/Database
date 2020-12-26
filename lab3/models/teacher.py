
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, String, Date, UniqueConstraint

from models.base_model import Base

teacher_subject_links = Table('teacher_subject', Base.metadata,
                              Column('id_teacher', Integer, ForeignKey('teacher.id', ondelete="CASCADE")),
                              Column('id_subject', Integer, ForeignKey('subject.id', ondelete="CASCADE")),
                              UniqueConstraint('id_teacher', 'id_subject', name='unique_teacher_subject')
                              )


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

    def __init__(self, id, first_name, last_name, phone_number):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def __repr__(self):
        return "<Teacher(id={}, first_name='{}', last_name='{}', phone_number='{}')>" \
            .format(self.id, self.first_name, self.last_name, self.phone_number)
