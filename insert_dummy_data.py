import logging
from datetime import date, timedelta
from utils.data_management import SessionLocal, projects_table, employees_table, rr_categories_table, rr_items_table, employee_project_table
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_data(employees, projects, rr_categories, rr_items, employee_projects):
    # 직원 데이터 검증
    if not all(isinstance(e['name'], str) for e in employees):
        raise ValueError("모든 직원 이름은 문자열이어야 합니다.")

    # 프로젝트 데이터 검증
    if not all(p['budget'] >= p['cost'] for p in projects):
        raise ValueError("모든 프로젝트의 예산은 비용보다 크거나 같아야 합니다.")

    # R&R 카테고리 데이터 검증
    if abs(sum(c['weight'] for c in rr_categories) - 1.0) > 0.001:
        raise ValueError("R&R 카테고리의 가중치 합은 1이어야 합니다.")

    # R&R 항목 데이터 검증
    for item in rr_items:
        if item['start_date'] >= item['end_date']:
            raise ValueError("R&R 항목의 시작일은 종료일보다 앞서야 합니다.")

    # 직원-프로젝트 할당 데이터 검증
    employee_allocations = {}
    for ep in employee_projects:
        employee_id = ep['employee_id']
        if employee_id not in employee_allocations:
            employee_allocations[employee_id] = 0
        employee_allocations[employee_id] += ep['allocation_rate']

    if any(allocation > 1.0 for allocation in employee_allocations.values()):
        raise ValueError("어떤 직원의 총 할당률도 100%를 초과할 수 없습니다.")

    return True

def insert_dummy_data():
    logger.info("더미 데이터 삽입 시작")
    session = SessionLocal()

    employees = [
        {"name": "김철수"},
        {"name": "이영희"},
        {"name": "박민수"},
    ]

    projects = [
        {"name": "프로젝트 A", "cost": 1000000, "budget": 1500000, "margin": 500000},
        {"name": "프로젝트 B", "cost": 2000000, "budget": 2500000, "margin": 500000},
        {"name": "프로젝트 C", "cost": 3000000, "budget": 4000000, "margin": 1000000},
    ]

    rr_categories = [
        {"name": "기획", "weight": 0.3},
        {"name": "개발", "weight": 0.5},
        {"name": "테스트", "weight": 0.2},
    ]

    rr_items = [
        {"category_id": 1, "name": "요구사항 분석", "weight": 0.5, "start_date": date.today(), "end_date": date.today() + timedelta(days=30)},
        {"category_id": 1, "name": "설계", "weight": 0.5, "start_date": date.today() + timedelta(days=31), "end_date": date.today() + timedelta(days=60)},
        {"category_id": 2, "name": "프론트엔드 개발", "weight": 0.5, "start_date": date.today() + timedelta(days=61), "end_date": date.today() + timedelta(days=90)},
        {"category_id": 2, "name": "백엔드 개발", "weight": 0.5, "start_date": date.today() + timedelta(days=61), "end_date": date.today() + timedelta(days=90)},
    ]

    try:
        for employee in employees:
            stmt = insert(employees_table).values(**employee)
            session.execute(stmt)

        for project in projects:
            stmt = insert(projects_table).values(**project)
            session.execute(stmt)

        for category in rr_categories:
            stmt = insert(rr_categories_table).values(**category)
            session.execute(stmt)

        for item in rr_items:
            stmt = insert(rr_items_table).values(**item)
            session.execute(stmt)

        session.commit()
        logger.info("더미 데이터 삽입 완료")
    except SQLAlchemyError as e:
        logger.error(f"데이터베이스 오류 발생: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    insert_dummy_data()