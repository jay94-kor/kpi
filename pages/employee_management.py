import streamlit as st
from utils.db_utils import session, add_instance, get_employees
from db.models import Employee

st.title('직원 관리')

employee_name = st.text_input('직원 이름')

if st.button('직원 추가'):
    new_employee = Employee(name=employee_name)
    add_instance(new_employee)
    st.success('직원이 성공적으로 추가되었습니다!')

st.header('직원 목록')
employees = get_employees()
for employee in employees:
    st.write(f'직원 이름: {employee.name}')
