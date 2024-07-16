import streamlit as st
from db.models import Project, Role, Task, Employee, Allocation
from utils.db_utils import session, add_instance, get_employees
from datetime import date

def main():
    st.title('프로젝트 생성하기')

    if 'category_count' not in st.session_state:
        st.session_state['category_count'] = 2

    if 'categories' not in st.session_state:
        st.session_state['categories'] = [{'name': '', 'percentage': 0, 'items': []} for _ in range(st.session_state['category_count'])]

    def add_category():
        st.session_state['category_count'] += 1
        st.session_state['categories'].append({'name': '', 'percentage': 0, 'items': []})

    def remove_category(index):
        if st.session_state['category_count'] > 1:
            st.session_state['category_count'] -= 1
            st.session_state['categories'].pop(index)

    def add_item(category_index):
        st.session_state['categories'][category_index]['items'].append({'name': '', 'percentage': 0})

    def remove_item(category_index, item_index):
        st.session_state['categories'][category_index]['items'].pop(item_index)

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

        for c, category in enumerate(st.session_state['categories']):
            with st.expander(f"카테고리 {c + 1}", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    category['name'] = st.text_input(f'카테고리 이름', value=category['name'], key=f'category_name_{c}')
                with col2:
                    category['percentage'] = st.number_input(f'카테고리 비중 (%)', min_value=0, max_value=100, value=category['percentage'], step=1, key=f'category_percentage_{c}')
                
                st.subheader('항목')
                for i, item in enumerate(category['items']):
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        item['name'] = st.text_input('항목 이름', value=item['name'], key=f'item_name_{c}_{i}')
                    with col2:
                        item['percentage'] = st.number_input('항목 비중 (%)', min_value=0, max_value=100, value=item['percentage'], step=1, key=f'item_percentage_{c}_{i}')

        submitted = st.form_submit_button("프로젝트 생성")

        if submitted:
            if not project_name or not manager:
                st.error('프로젝트 이름과 관리자는 필수 입력 항목입니다.')
            elif start_date > end_date:
                st.error('프로젝트 시작일이 종료일보다 늦을 수 없습니다.')
            elif sum(category['percentage'] for category in st.session_state['categories']) != 100:
                st.error('모든 카테고리의 비중 합계가 100%가 되어야 합니다.')
            else:
                new_project = Project(name=project_name, revenue=revenue, budget=budget, manager=manager, start_date=start_date, end_date=end_date)
                add_instance(new_project)
                
                for category in st.session_state['categories']:
                    for item in category['items']:
                        new_role = Role(name=item['name'], percentage=item['percentage'], project_id=new_project.id)
                        add_instance(new_role)

                st.success('프로젝트가 성공적으로 생성되었습니다!')
                st.write("### 새로 생성된 프로젝트 정보")
                st.write(f"**프로젝트 이름:** {new_project.name}")
                st.write(f"**관리자:** {new_project.manager}")
                st.write(f"**기간:** {new_project.start_date} ~ {new_project.end_date}")
                st.write(f"**매출:** {new_project.revenue:,}원")
                st.write(f"**예산:** {new_project.budget:,}원")
                
                st.session_state['categories'] = [{'name': '', 'percentage': 0, 'items': []} for _ in range(2)]
                st.session_state['category_count'] = 2

    if st.button("카테고리 추가"):
        add_category()

    for c, category in enumerate(st.session_state['categories']):
        if st.button(f"카테고리 {c+1} 삭제"):
            remove_category(c)
        
        for i, item in enumerate(category['items']):
            if st.button(f"항목 삭제 (카테고리 {c+1}, 항목 {i+1})"):
                remove_item(c, i)
        
        if st.button(f"항목 추가 (카테고리 {c+1})"):
            add_item(c)

if __name__ == "__main__":
    main()