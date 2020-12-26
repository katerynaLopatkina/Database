from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.subject import subject_group_links

from models.base_model import Base


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("Student", cascade="all, delete", passive_deletes=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Group(id ='{}', name ='{}')>" \
            .format(self.id, self.name)
