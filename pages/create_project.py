import streamlit as st
from db.models import Project, Role, Task, Employee, Allocation
from utils.db_utils import session, add_instance, get_employees
from datetime import date

st.title('프로젝트 생성하기')

if 'category_count' not in st.session_state:
    st.session_state['category_count'] = 2

if 'categories' not in st.session_state:
    st.session_state['categories'] = [{'name': '', 'percentage': 0, 'items': [{'name': '', 'percentage': 0}]} for _ in range(st.session_state['category_count'])]

def add_category():
    st.session_state['category_count'] += 1
    st.session_state['categories'].append({'name': '', 'percentage': 0, 'items': [{'name': '', 'percentage': 0}]})

def remove_category(index):
    if st.session_state['category_count'] > 1:
        st.session_state['category_count'] -= 1
        st.session_state['categories'].pop(index)

def add_item(category_index):
    st.session_state['categories'][category_index]['items'].append({'name': '', 'percentage': 0})

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
                category_name = st.text_input(f'카테고리 이름', key=f'category_name_{c}')
                category_percentage = st.number_input(f'카테고리 비중 (%)', min_value=0, max_value=100, step=1, key=f'category_percentage_{c}')
                
                if len(st.session_state['categories']) <= c:
                    st.session_state['categories'].append({'name': category_name, 'percentage': category_percentage, 'items': [{'name': '', 'percentage': 0}]})
                else:
                    st.session_state['categories'][c]['name'] = category_name
                    st.session_state['categories'][c]['percentage'] = category_percentage

    total_percentage = sum(category['percentage'] for category in st.session_state['categories'])
    remaining_percentage = 100 - total_percentage
    st.write(f"현재 비중 합계: {total_percentage}%, 남은 비중: {remaining_percentage}%")

    submitted = st.form_submit_button("카테고리 설정 완료")

for c in range(st.session_state['category_count']):
    st.button("카테고리 삭제", on_click=remove_category, args=(c,))

if submitted:
    if total_percentage != 100:
        st.error('모든 카테고리의 비중 합계가 100%가 되어야 합니다.')
    else:
        st.success('카테고리 설정이 완료되었습니다. 이제 항목을 추가하세요.')

        for c, category in enumerate(st.session_state['categories']):
            st.header(f"카테고리 {c + 1}: {category['name']} ({category['percentage']}%)")
            for i, item in enumerate(category['items']):
                item_name = st.text_input(f'항목 이름', key=f'item_name_{c}_{i}')
                item_percentage = st.number_input(f'항목 비중 (%)', min_value=0, max_value=100, step=1, key=f'item_percentage_{c}_{i}')
                st.session_state['categories'][c]['items'][i]['name'] = item_name
                st.session_state['categories'][c]['items'][i]['percentage'] = item_percentage

            st.button("항목 추가하기", on_click=add_item, args=(c,))

            if st.button(f"카테고리 {c + 1} 설정 완료"):
                break

    if st.button("프로젝트 생성"):
        if not project_name or not manager:
            st.error('프로젝트 이름과 관리자는 필수 입력 항목입니다.')
        elif start_date > end_date:
            st.error('프로젝트 시작일이 종료일보다 늦을 수 없습니다.')
        else:
            new_project = Project(name=project_name, revenue=revenue, budget=budget, manager=manager, start_date=start_date, end_date=end_date)
            add_instance(new_project)
            
            for category in st.session_state['categories']:
                for item in category['items']:
                    new_role = Role(name=item['name'], percentage=item['percentage'], project_id=new_project.id)
                    add_instance(new_role)

            st.success('프로젝트가 성공적으로 생성되었습니다!')