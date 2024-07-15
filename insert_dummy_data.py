from utils.data_management import SessionLocal, projects_table, employees_table
from sqlalchemy import insert

def insert_dummy_data():
    print("더미 데이터 삽입 중...")
    session = SessionLocal()

    # 직원 더미 데이터
    employees = [
        {"name": "김철수"},
        {"name": "이영희"},
        {"name": "박민수"},
    ]

    # 프로젝트 더미 데이터
    projects = [
        {"name": "프로젝트 A", "cost": 1000000, "budget": 1500000, "margin": 500000},
        {"name": "프로젝트 B", "cost": 2000000, "budget": 2500000, "margin": 500000},
        {"name": "프로젝트 C", "cost": 3000000, "budget": 4000000, "margin": 1000000},
    ]

    try:
        # 직원 데이터 삽입
        for employee in employees:
            stmt = insert(employees_table).values(**employee)
            session.execute(stmt)

        # 프로젝트 데이터 삽입
        for project in projects:
            stmt = insert(projects_table).values(**project)
            session.execute(stmt)

        session.commit()
        print("더미 데이터 삽입 완료.")
    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    insert_dummy_data()