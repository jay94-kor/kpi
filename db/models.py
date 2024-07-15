from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date, timedelta
from calendar import monthcalendar
from collections import defaultdict

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
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

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

    def get_status(self):
        today = date.today()
        if today < self.start_date:
            return "예정"
        elif today > self.end_date:
            return "완료"
        else:
            return "진행 중"

    def get_progress(self):
        today = date.today()
        if today < self.start_date:
            return 0
        elif today > self.end_date:
            return 100
        else:
            total_days = (self.end_date - self.start_date).days
            days_passed = (today - self.start_date).days
            return min(100, int((days_passed / total_days) * 100))

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

class Calendar:
    @staticmethod
    def get_monthly_tasks(year, month, tasks):
        cal = monthcalendar(year, month)
        task_calendar = defaultdict(list)

        for task in tasks:
            start = max(task.start_date, date(year, month, 1))
            end = min(task.end_date, date(year, month, cal[-1][-1]))

            current = start
            while current <= end:
                task_calendar[current.day].append(task)
                current += timedelta(days=1)

        return cal, task_calendar

    @staticmethod
    def print_monthly_calendar(year, month, tasks):
        cal, task_calendar = Calendar.get_monthly_tasks(year, month, tasks)
        print(f"{year}년 {month}월")
        print("월 화 수 목 금 토 일")
        for week in cal:
            for day in week:
                if day == 0:
                    print("   ", end="")
                else:
                    print(f"{day:2d}", end="")
                    if day in task_calendar:
                        print("*", end="")
                    else:
                        print(" ", end="")
            print()
        
        print("\n작업 목록:")
        for day, day_tasks in task_calendar.items():
            print(f"{day}일:")
            for task in day_tasks:
                print(f"  - {task.name} ({task.get_status()}, 진행률: {task.get_progress()}%)")

def init_db():
    engine = create_engine('sqlite:///projects.db')
    Base.metadata.create_all(engine)
    return engine