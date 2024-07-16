from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Project, Role, Task, Employee, Allocation
from datetime import date
import random

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
        Employee(name='이영희'),
        Employee(name='박지민'),
        Employee(name='최유진')
    ]
    for emp in employees:
        session.add(emp)
    session.commit()

    # 프로젝트 추가
    projects = [
        Project(
            name='웹 애플리케이션 개발',
            revenue=100000000,
            budget=80000000,
            manager='박매니저',
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        ),
        Project(
            name='모바일 앱 리뉴얼',
            revenue=50000000,
            budget=40000000,
            manager='김매니저',
            start_date=date(2023, 3, 1),
            end_date=date(2023, 9, 30)
        )
    ]
    for project in projects:
        session.add(project)
    session.commit()

    # 역할 및 테스크 추가
    roles_and_tasks = [
        {
            'role': {'name': '프론트엔드 개발', 'percentage': 40, 'project_id': projects[0].id},
            'tasks': [
                {'name': 'UI 디자인', 'percentage': 30, 'start_date': date(2023, 1, 1), 'end_date': date(2023, 3, 31)},
                {'name': '프론트엔드 구현', 'percentage': 70, 'start_date': date(2023, 4, 1), 'end_date': date(2023, 12, 31)}
            ]
        },
        {
            'role': {'name': '백엔드 개발', 'percentage': 60, 'project_id': projects[0].id},
            'tasks': [
                {'name': 'API 설계', 'percentage': 20, 'start_date': date(2023, 1, 1), 'end_date': date(2023, 2, 28)},
                {'name': '데이터베이스 구축', 'percentage': 30, 'start_date': date(2023, 3, 1), 'end_date': date(2023, 5, 31)},
                {'name': '백엔드 구현', 'percentage': 50, 'start_date': date(2023, 6, 1), 'end_date': date(2023, 12, 31)}
            ]
        },
        {
            'role': {'name': 'UI/UX 디자인', 'percentage': 50, 'project_id': projects[1].id},
            'tasks': [
                {'name': '사용자 리서치', 'percentage': 30, 'start_date': date(2023, 3, 1), 'end_date': date(2023, 4, 30)},
                {'name': '디자인 시안 작업', 'percentage': 70, 'start_date': date(2023, 5, 1), 'end_date': date(2023, 8, 31)}
            ]
        },
        {
            'role': {'name': '앱 개발', 'percentage': 50, 'project_id': projects[1].id},
            'tasks': [
                {'name': '기존 코드 분석', 'percentage': 20, 'start_date': date(2023, 3, 1), 'end_date': date(2023, 4, 30)},
                {'name': '앱 리뉴얼 구현', 'percentage': 80, 'start_date': date(2023, 5, 1), 'end_date': date(2023, 9, 30)}
            ]
        }
    ]

    for role_and_tasks in roles_and_tasks:
        role = Role(**role_and_tasks['role'])
        session.add(role)
        session.commit()

        for task_data in role_and_tasks['tasks']:
            task = Task(**task_data, role_id=role.id)
            session.add(task)
            session.commit()

            # 랜덤하게 직원 할당
            num_employees = random.randint(1, 3)
            selected_employees = random.sample(employees, num_employees)
            for employee in selected_employees:
                allocation = Allocation(
                    task_id=task.id,
                    employee_id=employee.id,
                    percentage=100 // num_employees
                )
                session.add(allocation)
        
        session.commit()

if __name__ == "__main__":
    add_dummy_data()
    print("더미 데이터가 성공적으로 추가되었습니다.")