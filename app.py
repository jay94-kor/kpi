import streamlit as st
import importlib
import sys
import os

st.set_page_config(layout="wide", page_title="프로젝트 관리 시스템")

def load_page(page_name):
    try:
        # 현재 디렉토리를 Python 경로에 추가
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        with st.spinner(f"{page_name} 페이지를 로딩 중입니다..."):
            module = importlib.import_module(f"pages.{page_name}")
            if hasattr(module, 'main'):
                module.main()
            else:
                st.error(f"{page_name} 페이지에 main() 함수가 정의되어 있지 않습니다.")
    except ImportError as e:
        st.error(f"{page_name} 페이지를 찾을 수 없습니다. 오류: {str(e)}")
    except Exception as e:
        st.error(f"페이지 로딩 중 오류가 발생했습니다: {str(e)}")
    finally:
        # Python 경로에서 현재 디렉토리 제거
        sys.path.pop(0)

page_mapping = {
    "프로젝트 생성": "create_project",
    "프로젝트 보기": "view_projects",
    "직원 관리": "employee_management"
}

st.sidebar.title('프로젝트 관리 시스템')

selected_page = st.sidebar.radio("페이지 선택", list(page_mapping.keys()))

if selected_page in page_mapping:
    load_page(page_mapping[selected_page])
else:
    st.error("선택한 페이지를 찾을 수 없습니다.")

st.sidebar.markdown("---")
st.sidebar.info("© 2024 프로젝트 관리 시스템")