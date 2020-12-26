from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Table, String, Date, UniqueConstraint
from models.base_model import Base
from models.student import student_subject_links
from models.teacher import teacher_subject_links

subject_group_links = Table('subject_group', Base.metadata,
                            Column('id_group', Integer, ForeignKey('group.id', ondelete="CASCADE")),
                            Column('id_subject', Integer, ForeignKey('subject.id', ondelete="CASCADE")),
                            UniqueConstraint('id_group', 'id_subject', name='unique_group_subject')
                            )


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(Integer)

    students = relationship("Student", secondary=student_subject_links, backref="subjects")
    teachers = relationship("Teacher", secondary=teacher_subject_links, backref="subjects")
    groups = relationship("Group", secondary=subject_group_links, backref="subjects")

    def __init__(self, id, name, time):
        self.id = id
        self.name = name
        self.time = time

    def __repr__(self):
        return "<Subject(id={}, name='{}', time='{}')>" \
            .format(self.id, self.name, self.time)
