import streamlit as st
from utils.data_management import SessionLocal, employees_table
from sqlalchemy.orm import sessionmaker

def display():
    st.header("직원 기준으로 보기")

    session = SessionLocal()
    employees = session.query(employees_table).all()
    session.close()

    for employee in employees:
        st.write(f"직원 이름: {employee.name}")
