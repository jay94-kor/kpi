from sqlalchemy import func, select
from utils.data_management import projects_table, employee_project_table, employees_table, rr_items_table

def calculate_project_kpi(session, project_id):
    # 프로젝트 기본 정보 조회
    project = session.execute(select(projects_table).where(projects_table.c.id == project_id)).fetchone()
    
    # 프로젝트에 할당된 총 인원 수
    total_employees = session.execute(
        select(func.count(func.distinct(employee_project_table.c.employee_id)))
        .where(employee_project_table.c.project_id == project_id)
    ).scalar()

    # 프로젝트의 총 할당률
    total_allocation = session.execute(
        select(func.sum(employee_project_table.c.allocation_rate))
        .where(employee_project_table.c.project_id == project_id)
    ).scalar() or 0

    # R&R 항목 완료율 계산
    rr_items_completion = session.execute(
        select(
            rr_items_table.c.id,
            rr_items_table.c.name,
            func.sum(employee_project_table.c.allocation_rate).label('total_allocation')
        )
        .select_from(
            rr_items_table.join(employee_project_table, rr_items_table.c.id == employee_project_table.c.rr_item_id)
        )
        .where(employee_project_table.c.project_id == project_id)
        .group_by(rr_items_table.c.id, rr_items_table.c.name)
    ).fetchall()

    # KPI 계산
    budget_utilization = project.cost / project.budget if project.budget > 0 else 0
    resource_utilization = total_allocation / total_employees if total_employees > 0 else 0
    
    return {
        "project_name": project.name,
        "budget_utilization": budget_utilization,
        "resource_utilization": resource_utilization,
        "total_employees": total_employees,
        "total_allocation": total_allocation,
        "rr_items_completion": [
            {"name": item.name, "completion_rate": item.total_allocation}
            for item in rr_items_completion
        ]
    }