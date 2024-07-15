import streamlit as st
import pandas as pd
from utils.data_management import SessionLocal, projects_table, rr_items_table, employee_project_table, employees_table, rr_categories_table
from sqlalchemy import select, join, func

def display():
    st.header("프로젝트 기준으로 보기")

    with SessionLocal() as session:
        # 프로젝트, R&R 항목, 직원 정보를 조인하여 가져옵니다
        stmt = select(
            projects_table, 
            rr_categories_table,
            rr_items_table, 
            employees_table, 
            employee_project_table.c.allocation_rate
        ).select_from(
            join(projects_table, employee_project_table, projects_table.c.id == employee_project_table.c.project_id)
            .join(rr_items_table, rr_items_table.c.id == employee_project_table.c.rr_item_id)
            .join(rr_categories_table, rr_categories_table.c.id == rr_items_table.c.category_id)
            .join(employees_table, employees_table.c.id == employee_project_table.c.employee_id)
        )
        results = session.execute(stmt).fetchall()

        # 프로젝트별로 데이터를 그룹화합니다
        projects_data = {}
        for row in results:
            project = row.projects
            if project.id not in projects_data:
                projects_data[project.id] = {
                    "name": project.name,
                    "cost": project.cost,
                    "budget": project.budget,
                    "margin": project.margin,
                    "categories": {}
                }
            
            category = row.rr_categories
            if category.id not in projects_data[project.id]["categories"]:
                projects_data[project.id]["categories"][category.id] = {
                    "name": category.name,
                    "items": {}
                }
            
            item = row.rr_items
            if item.id not in projects_data[project.id]["categories"][category.id]["items"]:
                projects_data[project.id]["categories"][category.id]["items"][item.id] = {
                    "name": item.name,
                    "employees": []
                }
            
            projects_data[project.id]["categories"][category.id]["items"][item.id]["employees"].append({
                "name": row.employees.name,
                "allocation_rate": row.allocation_rate
            })

        # 프로젝트 정보를 표시합니다
        for project_id, project_data in projects_data.items():
            st.subheader(f"프로젝트: {project_data['name']}")
            
            for category_id, category_data in project_data["categories"].items():
                st.write(f"- {category_data['name']}")
                for item_id, item_data in category_data["items"].items():
                    st.write(f"  - {item_data['name']}")
                    for employee in item_data["employees"]:
                        st.write(f"    - {employee['name']} (할당률: {employee['allocation_rate']*100:.1f}%)")
            
            st.write("---")

        # 프로젝트 진행 상황을 시각화합니다
        st.subheader("프로젝트 진행 상황")
        progress_data = []
        for project_id, project_data in projects_data.items():
            total_allocation = sum(employee["allocation_rate"] for category in project_data["categories"].values() 
                                   for item in category["items"].values() 
                                   for employee in item["employees"])
            progress_data.append({"name": project_data["name"], "progress": total_allocation})

        progress_df = pd.DataFrame(progress_data)
        st.bar_chart(progress_df.set_index("name"))