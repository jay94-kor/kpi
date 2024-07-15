import streamlit as st
from utils.data_management import SessionLocal, employees_table
from sqlalchemy import insert

def display_employee_form():
    employee_name = st.text_input("직원 이름")

    if st.button("직원 저장"):
        session = SessionLocal()
        stmt = insert(employees_table).values(name=employee_name)
        session.execute(stmt)
        session.commit()
        session.close()
        st.success("직원이 저장되었습니다.")
