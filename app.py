import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
 
with st.sidebar:
    st.title('프로젝트 관리 시스템')
    selected = option_menu(
        menu_title=None,
        options=["프로젝트 생성", "프로젝트 보기", "직원 관리"],
        icons=["plus-circle", "list-task", "people"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "프로젝트 생성":
    from pages.create_project import *
elif selected == "프로젝트 보기":
    from pages.view_projects import *
elif selected == "직원 관리":
    from pages.employee_management import *