from sqlalchemy.orm import sessionmaker
from db.models import init_db, Project, Role, Task, Employee, Allocation

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

def add_instance(instance):
    session.add(instance)
    session.commit()

def get_projects():
    return session.query(Project).all()

def get_employees():
    return session.query(Employee).all()