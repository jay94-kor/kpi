import streamlit as st
from streamlit_option_menu import option_menu
import importlib

st.set_page_config(layout="wide", page_title="프로젝트 관리 시스템")

def load_page(page_name):
    try:
        with st.spinner(f"{page_name} 페이지를 로딩 중입니다..."):
            module = importlib.import_module(f"pages.{page_name}")
            if hasattr(module, 'main'):
                module.main()
            else:
                st.error(f"{page_name} 페이지에 main() 함수가 정의되어 있지 않습니다.")
    except ImportError:
        st.error(f"{page_name} 페이지를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"페이지 로딩 중 오류가 발생했습니다: {str(e)}")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "프로젝트 생성"

with st.sidebar:
    st.title('프로젝트 관리 시스템')
    selected = option_menu(
        menu_title=None,
        options=["프로젝트 생성", "프로젝트 보기", "직원 관리"],
        icons=["plus-circle", "list-task", "people"],
        menu_icon="cast",
        default_index=["프로젝트 생성", "프로젝트 보기", "직원 관리"].index(st.session_state.current_page),
    )

    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()

page_mapping = {
    "프로젝트 생성": "create_project",
    "프로젝트 보기": "view_projects",
    "직원 관리": "employee_management"
}

if st.session_state.current_page in page_mapping:
    load_page(page_mapping[st.session_state.current_page])
else:
    st.error("선택한 페이지를 찾을 수 없습니다.")

st.sidebar.markdown("---")
st.sidebar.info("© 2024 프로젝트 관리 시스템")