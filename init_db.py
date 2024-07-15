from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Project, Role, Task, Employee, Allocation
from datetime import date

# 데이터베이스 초기화
engine = create_engine('sqlite:///projects.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 더미 데이터 추가
def add_dummy_data():
    # 직원 추가
    employees = [
        Employee(name='홍길동'),
        Employee(name='김철수'),
        Employee(name='이영희')
    ]
    for emp in employees:
        session.add(emp)
    session.commit()

    # 프로젝트 추가
    project = Project(
        name='프로젝트 A',
        revenue=10000000,
        budget=5000000,
        manager='박매니저',
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )
    session.add(project)
    session.commit()

    # 역할 추가
    role = Role(
        name='개발',
        percentage=50,
        project_id=project.id
    )
    session.add(role)
    session.commit()

    # 테스크 추가
    task = Task(
        name='개발 작업 1',
        percentage=100,
        role_id=role.id,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 6, 30)
    )
    session.add(task)
    session.commit()

    # 할당 추가
    allocation = Allocation(
        task_id=task.id,
        employee_id=employees[0].id,
        percentage=100
    )
    session.add(allocation)
    session.commit()

if __name__ == "__main__":
    add_dummy_data()
    print("더미 데이터가 성공적으로 추가되었습니다.")