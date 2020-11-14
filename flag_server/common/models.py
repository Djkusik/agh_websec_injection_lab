import datetime

from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, aliased


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    name = Column(String, unique=True, nullable=False)
    password = Column(String)
    
    tasks = relationship(
                'Task',
                secondary='solutions',
                back_populates='users'
            )

    def __repr__(self):
        return f'{self.name} :: {len(self.tasks)} task/s solved ({sum([t.points for t in self.tasks])} points)'


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, Sequence('task_id_seq'), primary_key=True)

    name = Column(String, unique=True, nullable=False)
    lab_no = Column(Integer, unique=False)
    flag = Column(String)
    points = Column(Integer, default=0)

    users = relationship(
                'User',
                secondary='solutions',
                back_populates='tasks'
            )

    def __repr__(self):
        return f'{self.name} :: <{self.points} | {self.lab_no}> solved {len(self.users)} times'


class Solutions(Base):
    __tablename__ == 'solutions'
    id = Column(Integer, Sequence('solution_id_seq'), primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))

    user = relationship(User, backref=backref('solutions', cascade='all, delete-orphan'))
    task = relationship(Task, backref=backref('solutions', cascade='all, delete-orphan'))

    solve_time = Column(DateTime, default=datetime.datetime.utcnow)