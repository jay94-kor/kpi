import streamlit as st
from components import project_form, employee_form

def display():
    st.header("관리자 페이지")
    
    st.subheader("프로젝트 추가")
    project_form.display_project_form()
    
    st.subheader("직원 추가")
    employee_form.display_employee_form()
