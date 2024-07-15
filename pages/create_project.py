import streamlit as st
from db.models import Project, Role, Task, Employee, Allocation
from utils.db_utils import session, add_instance, get_employees

st.title('프로젝트 생성하기')

project_name = st.text_input('프로젝트 이름')
revenue = st.number_input('매출', min_value=0.0)
budget = st.number_input('예산', min_value=0.0)
manager = st.text_input('프로젝트 관리자')

st.header('R&R 카테고리 추가')
roles = []
total_percentage = 0

for i in range(5):
    with st.expander(f'Role {i + 1}'):
        role_name = st.text_input(f'역할 이름 {i + 1}', key=f'role_name_{i}')
        responsibility = st.text_area(f'책임 {i + 1}', key=f'responsibility_{i}')
        percentage = st.number_input(f'비중 (%) {i + 1}', min_value=0.0, max_value=100.0, key=f'percentage_{i}')
        total_percentage += percentage
        
        tasks = []
        task_total_percentage = 0
        for j in range(5):
            with st.expander(f'Task {j + 1} for Role {i + 1}'):
                task_name = st.text_input(f'테스크 이름 {j + 1}', key=f'task_name_{i}_{j}')
                task_percentage = st.number_input(f'테스크 비중 (%) {j + 1}', min_value=0.0, max_value=100.0, key=f'task_percentage_{i}_{j}')
                task_total_percentage += task_percentage
                
                employees = []
                employee_total_percentage = 0
                employee_list = get_employees()
                for k in range(len(employee_list)):
                    employee_name = st.text_input(f'직원 이름 {k + 1}', value=employee_list[k].name, key=f'employee_name_{i}_{j}_{k}', disabled=True)
                    employee_percentage = st.number_input(f'투입률 (%) {k + 1}', min_value=0.0, max_value=100.0, key=f'employee_percentage_{i}_{j}_{k}')
                    employee_total_percentage += employee_percentage
                    if employee_percentage > 0:
                        employees.append({'name': employee_name, 'percentage': employee_percentage, 'id': employee_list[k].id})
                
                if task_name and task_percentage > 0 and employee_total_percentage == 100:
                    tasks.append({'name': task_name, 'percentage': task_percentage, 'employees': employees})

        if role_name and responsibility and percentage > 0 and task_total_percentage == 100:
            roles.append({'name': role_name, 'responsibility': responsibility, 'percentage': percentage, 'tasks': tasks})

if st.button('생성'):
    if total_percentage == 100:
        new_project = Project(name=project_name, revenue=revenue, budget=budget, manager=manager)
        add_instance(new_project)
        
        for role in roles:
            new_role = Role(name=role['name'], responsibility=role['responsibility'], percentage=role['percentage'], project_id=new_project.id)
            add_instance(new_role)
            
            for task in role['tasks']:
                new_task = Task(name=task['name'], percentage=task['percentage'], role_id=new_role.id)
                add_instance(new_task)
                
                for employee in task['employees']:
                    new_allocation = Allocation(task_id=new_task.id, employee_id=employee['id'], percentage=employee['percentage'])
                    add_instance(new_allocation)

        st.success('프로젝트가 성공적으로 생성되었습니다!')
    else:
        st.error('R&R 카테고리의 비중의 합이 100%가 되어야 합니다.')
