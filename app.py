import streamlit as st
from streamlit_option_menu import option_menu
import importlib

st.set_page_config(layout="wide", page_title="프로젝트 관리 시스템")

def load_page(page_name):
    module = importlib.import_module(f"pages.{page_name}")
    module.main()

with st.sidebar:
    st.title('프로젝트 관리 시스템')
    selected = option_menu(
        menu_title=None,
        options=["프로젝트 생성", "프로젝트 보기", "직원 관리"],
        icons=["plus-circle", "list-task", "people"],
        menu_icon="cast",
        default_index=0,
    )

page_mapping = {
    "프로젝트 생성": "create_project",
    "프로젝트 보기": "view_projects",
    "직원 관리": "employee_management"
}

if selected in page_mapping:
    load_page(page_mapping[selected])
else:
    st.error("선택한 페이지를 찾을 수 없습니다.")

st.sidebar.markdown("---")
st.sidebar.info("© 2023 프로젝트 관리 시스템")