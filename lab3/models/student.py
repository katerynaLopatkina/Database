from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, String, Date, UniqueConstraint
from models.base_model import Base

student_subject_links = Table('student_subject', Base.metadata,
                              Column('id_student', Integer, ForeignKey('student.id', ondelete="CASCADE")),
                              Column('id_subject', Integer, ForeignKey('subject.id', ondelete="CASCADE")),
                              UniqueConstraint('id_student', 'id_subject', name='unique_student_subject')
                              )


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    sex = Column(String)
    date_of_birth = Column(Date)
    id_group = Column(Integer, ForeignKey('group.id', ondelete="CASCADE"))

    def __init__(self, id, first_name, last_name, sex, date_of_birth, id_group):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.id_group = id_group

    def __repr__(self):
        return "<Student(id={}, first_name='{}', last_name='{}', sex={}, date_of_birth='{}', id_group={})>" \
            .format(self.id, self.first_name, self.last_name, self.sex, self.date_of_birth, self.id_group)
