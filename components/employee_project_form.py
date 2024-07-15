import streamlit as st
from utils.data_management import SessionLocal, employees_table, projects_table, rr_items_table, employee_project_table
from sqlalchemy import insert, select, func
from sqlalchemy.exc import SQLAlchemyError

def display_employee_project_form():
    try:
        with SessionLocal() as session:
            employees = session.execute(select(employees_table)).fetchall()
            projects = session.execute(select(projects_table)).fetchall()
            rr_items = session.execute(select(rr_items_table)).fetchall()

            employee_options = {employee.name: employee.id for employee in employees}
            project_options = {project.name: project.id for project in projects}
            rr_item_options = {item.name: item.id for item in rr_items}

            selected_employee = st.selectbox("직원 선택", list(employee_options.keys()))
            selected_project = st.selectbox("프로젝트 선택", list(project_options.keys()))
            selected_rr_item = st.selectbox("R&R 항목 선택", list(rr_item_options.keys()))
            allocation_rate = st.number_input("할당률", min_value=0.0, max_value=1.0, step=0.1)

            if st.button("직원 프로젝트 할당"):
                if not selected_employee or not selected_project or not selected_rr_item:
                    st.error("모든 필드를 선택해주세요.")
                    return

                # 현재 직원의 총 할당률 확인
                current_allocation = session.execute(
                    select(func.sum(employee_project_table.c.allocation_rate))
                    .where(employee_project_table.c.employee_id == employee_options[selected_employee])
                ).scalar() or 0

                if current_allocation + allocation_rate > 1.0:
                    st.error(f"총 할당률이 100%를 초과합니다. 현재 할당률: {current_allocation*100}%")
                    return

                # 항목별 투입률 검증
                item_allocation = session.execute(
                    select(func.sum(employee_project_table.c.allocation_rate))
                    .where(employee_project_table.c.rr_item_id == rr_item_options[selected_rr_item])
                ).scalar() or 0

                if item_allocation + allocation_rate > 1.0:
                    st.error(f"항목의 총 투입률이 100%를 초과합니다. 현재 투입률: {item_allocation*100}%")
                    return

                try:
                    stmt = insert(employee_project_table).values(
                        employee_id=employee_options[selected_employee],
                        project_id=project_options[selected_project],
                        rr_item_id=rr_item_options[selected_rr_item],
                        allocation_rate=allocation_rate
                    )
                    session.execute(stmt)
                    session.commit()
                    st.success("직원이 프로젝트에 할당되었습니다.")
                except SQLAlchemyError as e:
                    session.rollback()
                    st.error(f"데이터베이스 오류: {str(e)}")
    except Exception as e:
        st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")