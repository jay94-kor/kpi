import streamlit as st

st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Select a page:', ['Create Project', 'View Projects', 'Employee Management'])

if page == 'Create Project':
    from pages.create_project import *
elif page == 'View Projects':
    from pages.view_projects import *
elif page == 'Employee Management':
    from pages.employee_management import *
