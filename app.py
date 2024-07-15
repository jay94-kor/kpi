import streamlit as st
from streamlit_option_menu import option_menu
from pages import employees_view, projects_view, admin_view
from utils.data_management import init_db

# 데이터베이스 초기화
init_db()

st.title("프로젝트 KPI 관리 웹 서비스")

# 사이드바 메뉴 생성
menu = option_menu(
    menu_title="메뉴", 
    options=["직원 기준으로 보기", "프로젝트 기준으로 보기", "관리자 페이지"],
    icons=["people", "folder", "gear"],
    menu_icon="cast",
    default_index=0,
)

# 페이지 라우팅
if menu == "직원 기준으로 보기":
    employees_view.display()
elif menu == "프로젝트 기준으로 보기":
    projects_view.display()
elif menu == "관리자 페이지":
    admin_view.display()