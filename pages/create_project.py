import streamlit as st
from db.models import Project, Role, Task, Employee, Allocation
from utils.db_utils import session, add_instance, get_employees
from datetime import date

st.title('프로젝트 생성하기')

if 'category_count' not in st.session_state:
    st.session_state['category_count'] = 1

def add_category():
    if 'category_count' in st.session_state:
        st.session_state['category_count'] += 1
    else:
        st.session_state['category_count'] = 2

st.button("카테고리 추가", on_click=add_category)

with st.form("project_creation_form"):
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input('프로젝트 이름', key='project_name')
        revenue = st.number_input('매출', min_value=0, step=1000000, key='revenue')
        budget = st.number_input('예산', min_value=0, step=1000000, key='budget')
    with col2:
        manager = st.text_input('프로젝트 관리자', key='manager')
        start_date = st.date_input('프로젝트 시작일', key='start_date')
        end_date = st.date_input('프로젝트 종료일', key='end_date')

    st.header('R&R 카테고리')

    categories = []
    category_columns = st.columns(st.session_state.category_count)

    for c, category_col in enumerate(category_columns):
        with category_col:
            with st.expander(f"카테고리 {c + 1}", expanded=True):
                role_count = st.number_input(f'역할 수 (카테고리 {c + 1})', min_value=1, max_value=10, value=1, step=1, key=f'role_count_{c}')
                
                roles = []
                total_percentage = 0

                for i in range(role_count):
                    role_name = st.text_input(f'역할 이름', key=f'role_name_{c}_{i}')
                    role_percentage = st.number_input(f'비중 (%)', min_value=0, max_value=100, step=1, key=f'percentage_{c}_{i}')
                    
                    total_percentage += role_percentage
                    tasks = []

                    task_count = st.number_input(f'테스크 수 (역할 {i + 1})', min_value=1, max_value=10, value=1, step=1, key=f'task_count_{c}_{i}')

                    task_total_percentage = 0
                    for j in range(task_count):
                        task_name = st.text_input(f'테스크 이름', key=f'task_name_{c}_{i}_{j}')
                        task_percentage = st.number_input(f'테스크 비중 (%)', min_value=0, max_value=100, step=1, key=f'task_percentage_{c}_{i}_{j}')
                        task_start_date = st.date_input(f'시작일', key=f'start_date_{c}_{i}_{j}')
                        task_end_date = st.date_input(f'마감일', key=f'end_date_{c}_{i}_{j}')
                        
                        task_total_percentage += task_percentage
                        
                        employees = []
                        employee_list = get_employees()
                        employee_names = [emp.name for emp in employee_list]
                        selected_employees = st.multiselect('직원 선택', employee_names, key=f'employees_{c}_{i}_{j}')
                        
                        employee_total_percentage = 0
                        for emp_name in selected_employees:
                            emp = next(emp for emp in employee_list if emp.name == emp_name)
                            employee_percentage = st.number_input(f'{emp_name} 투입률 (%)', min_value=0, max_value=100, step=1, key=f'employee_percentage_{c}_{i}_{j}_{emp.id}')
                            employee_total_percentage += employee_percentage
                            if employee_percentage > 0:
                                employees.append({'name': emp_name, 'percentage': employee_percentage, 'id': emp.id})

                        if task_name and task_percentage > 0 and task_start_date <= task_end_date:
                            tasks.append({
                                'name': task_name, 
                                'percentage': task_percentage, 
                                'start_date': task_start_date,
                                'end_date': task_end_date,
                                'employees': employees
                            })
                        if employee_total_percentage != 100:
                            st.warning(f'테스크 {j + 1}의 직원 투입률 합계가 100%가 되어야 합니다.')

                    if task_total_percentage != 100:
                        st.warning(f'역할 {i + 1}의 테스크 비중 합계가 100%가 되어야 합니다.')

                    if role_name and role_percentage > 0 and task_total_percentage == 100:
                        roles.append({'name': role_name, 'percentage': role_percentage, 'tasks': tasks})

            if total_percentage != 100:
                st.warning('모든 역할의 비중 합계가 100%가 되어야 합니다.')

            categories.append({'roles': roles, 'total_percentage': total_percentage})

    submitted = st.form_submit_button("프로젝트 생성")

    if submitted:
        if not project_name or not manager:
            st.error('프로젝트 이름과 관리자는 필수 입력 항목입니다.')
        elif start_date > end_date:
            st.error('프로젝트 시작일이 종료일보다 늦을 수 없습니다.')
        elif any(category['total_percentage'] != 100 for category in categories):
            st.error('모든 카테고리의 역할 비중의 합이 100%가 되어야 합니다.')
        elif any(any(not role['tasks'] for role in category['roles']) for category in categories):
            st.error('모든 역할에는 최소 하나의 테스크가 있어야 합니다.')
        else:
            new_project = Project(name=project_name, revenue=revenue, budget=budget, manager=manager, start_date=start_date, end_date=end_date)
            add_instance(new_project)
            
            for category in categories:
                for role in category['roles']:
                    new_role = Role(name=role['name'], percentage=role['percentage'], project_id=new_project.id)
                    add_instance(new_role)
                    
                    for task in role['tasks']:
                        new_task = Task(
                            name=task['name'], 
                            percentage=task['percentage'], 
                            role_id=new_role.id,
                            start_date=task['start_date'],
                            end_date=task['end_date']
                        )
                        add_instance(new_task)
                        
                        for employee in task['employees']:
                            new_allocation = Allocation(task_id=new_task.id, employee_id=employee['id'], percentage=employee['percentage'])
                            add_instance(new_allocation)

            st.success('프로젝트가 성공적으로 생성되었습니다!')