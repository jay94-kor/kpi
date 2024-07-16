import streamlit as st
from project import Project
from utils import display_project_summary, display_project_details

def show():
    st.header("프로젝트 개요")
    
    project_name = st.text_input("프로젝트명")
    project_revenue = st.number_input("프로젝트 매출", min_value=0)
    project_budget = st.number_input("프로젝트 예산", min_value=0, max_value=project_revenue)

    if st.button("프로젝트 생성"):
        if project_budget <= project_revenue:
            project = Project(project_name, project_revenue, project_budget)
            st.session_state.project = project
            
            display_project_summary(project)
            display_project_details(project)
        else:
            st.error("예산은 매출보다 클 수 없습니다.")