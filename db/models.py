from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    revenue = Column(Float, nullable=False)
    budget = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    manager = Column(String, nullable=False)
    roles = relationship('Role', back_populates='project')

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String, nullable=False)
    responsibility = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    project = relationship('Project', back_populates='roles')
    tasks = relationship('Task', back_populates='role')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    role = relationship('Role', back_populates='tasks')
    allocations = relationship('Allocation', back_populates='task')

    @property
    def duration(self):
        return (self.end_date - self.start_date).days

    @property
    def is_completed(self):
        return date.today() > self.end_date

    @property
    def is_difficult(self):
        # 예: 7일 이상의 작업을 어려운 작업으로 간주
        return self.duration >= 7

    @property
    def accumulated_kpi(self):
        if self.is_completed:
            return self.percentage
        return 0

    @property
    def expected_kpi(self):
        if not self.is_completed:
            return self.percentage
        return 0

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    allocations = relationship('Allocation', back_populates='employee')

    def get_accumulated_kpi(self):
        return sum(allocation.task.accumulated_kpi * allocation.percentage / 100
                   for allocation in self.allocations)

    def get_expected_kpi(self):
        return sum(allocation.task.expected_kpi * allocation.percentage / 100
                   for allocation in self.allocations)

class Allocation(Base):
    __tablename__ = 'allocations'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    percentage = Column(Float, nullable=False)
    task = relationship('Task', back_populates='allocations')
    employee = relationship('Employee', back_populates='allocations')

def init_db():
    engine = create_engine('sqlite:///projects.db')
    Base.metadata.create_all(engine)
    return engine