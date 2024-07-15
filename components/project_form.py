import streamlit as st
from utils.data_management import SessionLocal, projects_table
from sqlalchemy import insert

def display_project_form():
    project_name = st.text_input("프로젝트 명")
    project_cost = st.number_input("프로젝트 비용", min_value=0.0)
    project_budget = st.number_input("프로젝트 예산", min_value=0.0)
    project_margin = project_budget - project_cost

    st.write(f"프로젝트 마진: {project_margin}")

    if st.button("프로젝트 저장"):
        session = SessionLocal()
        stmt = insert(projects_table).values(
            name=project_name, cost=project_cost, budget=project_budget, margin=project_margin
        )
        session.execute(stmt)
        session.commit()
        session.close()
        st.success("프로젝트가 저장되었습니다.")
