import streamlit as st
from utils.data_management import SessionLocal, projects_table
from sqlalchemy.orm import sessionmaker

def display():
    st.header("프로젝트 기준으로 보기")

    session = SessionLocal()
    projects = session.query(projects_table).all()
    session.close()

    for project in projects:
        st.write(f"프로젝트 이름: {project.name}, 비용: {project.cost}, 예산: {project.budget}, 마진: {project.margin}")
