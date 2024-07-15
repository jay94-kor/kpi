import streamlit as st
import pandas as pd
from utils.data_management import SessionLocal, employees_table, projects_table, rr_items_table, employee_project_table, rr_categories_table
from sqlalchemy import select, join, func

def display():
    st.header("직원 기준으로 보기")

    with SessionLocal() as session:
        # 직원, 프로젝트, R&R 항목 정보를 조인하여 가져옵니다
        stmt = select(
            employees_table, 
            projects_table, 
            rr_categories_table,
            rr_items_table, 
            employee_project_table.c.allocation_rate
        ).select_from(
            join(employees_table, employee_project_table, employees_table.c.id == employee_project_table.c.employee_id)
            .join(projects_table, projects_table.c.id == employee_project_table.c.project_id)
            .join(rr_items_table, rr_items_table.c.id == employee_project_table.c.rr_item_id)
            .join(rr_categories_table, rr_categories_table.c.id == rr_items_table.c.category_id)
        )
        results = session.execute(stmt).fetchall()

        # 직원별로 데이터를 그룹화합니다
        employees_data = {}
        for row in results:
            employee = row.employees
            if employee.id not in employees_data:
                employees_data[employee.id] = {
                    "name": employee.name,
                    "projects": {}
                }
            
            project = row.projects
            if project.id not in employees_data[employee.id]["projects"]:
                employees_data[employee.id]["projects"][project.id] = {
                    "name": project.name,
                    "categories": {}
                }
            
            category = row.rr_categories
            if category.id not in employees_data[employee.id]["projects"][project.id]["categories"]:
                employees_data[employee.id]["projects"][project.id]["categories"][category.id] = {
                    "name": category.name,
                    "items": []
                }
            
            employees_data[employee.id]["projects"][project.id]["categories"][category.id]["items"].append({
                "name": row.rr_items.name,
                "allocation_rate": row.allocation_rate
            })

        # 직원 정보를 표시합니다
        for employee_id, employee_data in employees_data.items():
            st.subheader(f"직원: {employee_data['name']}")
            
            for project_id, project_data in employee_data["projects"].items():
                st.write(f"**프로젝트: {project_data['name']}**")
                for category_id, category_data in project_data["categories"].items():
                    st.write(f"- {category_data['name']}")
                    for item in category_data["items"]:
                        st.write(f"  - {item['name']} (할당률: {item['allocation_rate']*100:.1f}%)")
            
            st.write("---")

        # 직원별 총 할당률을 시각화합니다
        st.subheader("직원별 총 할당률")
        allocation_data = []
        for employee_id, employee_data in employees_data.items():
            total_allocation = sum(item["allocation_rate"] for project in employee_data["projects"].values() 
                                   for category in project["categories"].values() 
                                   for item in category["items"])
            allocation_data.append({"name": employee_data["name"], "allocation": total_allocation})

        allocation_df = pd.DataFrame(allocation_data)
        st.bar_chart(allocation_df.set_index("name"))