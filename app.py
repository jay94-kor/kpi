import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# 프로젝트 클래스 정의
class Project:
    def __init__(self, name, revenue, budget):
        self.name = name
        self.revenue = revenue
        self.budget = budget
        self.profit = self.calculate_profit()
        self.profit_margin = self.calculate_profit_margin()
        self.categories = {}

    def calculate_profit(self):
        return self.revenue - self.budget

    def calculate_profit_margin(self):
        if self.revenue == 0:
            return 0
        return (self.profit / self.revenue) * 100

    def add_category(self, category_name):
        if category_name not in self.categories:
            self.categories[category_name] = []

    def add_item_to_category(self, category_name, item_name):
        if category_name in self.categories:
            self.categories[category_name].append(item_name)
        else:
            self.categories[category_name] = [item_name]

    def display_project_info(self):
        st.write(f"프로젝트명: {self.name}")
        st.write(f"프로젝트 매출: {self.revenue}")
        st.write(f"프로젝트 예산: {self.budget}")
        st.write(f"이익금: {self.profit}")
        st.write(f"이익률: {self.profit_margin:.2f}%")
        st.write(f"카테고리와 항목: {self.categories}")

# Streamlit 인터페이스 설정
st.title("프로젝트 관리 시스템")

# 프로젝트 정보 입력
project_name = st.text_input("프로젝트명")
project_revenue = st.number_input("프로젝트 매출", min_value=0)
project_budget = st.number_input("프로젝트 예산", min_value=0)

if st.button("프로젝트 생성"):
    project = Project(project_name, project_revenue, project_budget)
    st.session_state['project'] = project

# 카테고리 및 항목 추가
if 'project' in st.session_state:
    project = st.session_state['project']
    
    st.subheader("카테고리 추가")
    category_name = st.text_input("카테고리명")
    if st.button("카테고리 추가"):
        project.add_category(category_name)
        st.success(f"{category_name} 카테고리가 추가되었습니다.")
    
    st.subheader("항목 추가")
    if project.categories:
        selected_category = option_menu(
            "카테고리를 선택하세요",
            options=list(project.categories.keys()),
            icons=["folder" for _ in project.categories],  # 각 카테고리에 대한 아이콘
            menu_icon="list",
            default_index=0,
        )
        item_name = st.text_input("항목명")
        if st.button("항목 추가"):
            project.add_item_to_category(selected_category, item_name)
            st.success(f"{item_name} 항목이 {selected_category} 카테고리에 추가되었습니다.")
    else:
        st.warning("먼저 카테고리를 추가해주세요.")

    # 프로젝트 정보 출력
    project.display_project_info()
    
    # DataFrame으로 정보 표시
    project_data = {
        '프로젝트명': [project.name],
        '매출': [project.revenue],
        '예산': [project.budget],
        '이익금': [project.profit],
        '이익률': [f"{project.profit_margin:.2f}%"]
    }

    df = pd.DataFrame(project_data)
    st.dataframe(df)