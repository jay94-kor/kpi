import streamlit as st
from utils.db_utils import get_projects

st.title('프로젝트 보기')

projects = get_projects()

for project in projects:
    st.header(f'프로젝트 이름: {project.name}')
    st.write(f'매출: {project.revenue}')
    st.write(f'예산: {project.budget}')
    st.write(f'순이익: {project.revenue - project.budget}')
    st.write(f'프로젝트 관리자: {project.manager}')

    for role in project.roles:
        st.subheader(f'Role: {role.name} ({role.percentage}%)')
        st.write(f'책임: {role.responsibility}')
        
        for task in role.tasks:
            st.write(f'Task: {task.name} ({task.percentage}%)')
            for allocation in task.allocations:
                employee = allocation.employee
                st.write(f'  Employee: {employee.name} ({allocation.percentage}%)')
