import streamlit as st
from project import Project
from steps import project_overview, category_setup, item_setup

st.title("프로젝트 관리 시스템")

# 초기 세션 상태 설정
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'project' not in st.session_state:
    st.session_state.project = None

# 현재 단계에 따라 적절한 내용 표시
if st.session_state.step == 1:
    project_overview.show()
elif st.session_state.step == 2:
    category_setup.show()
elif st.session_state.step == 3:
    item_setup.show()

# 네비게이션 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.step > 1:
        if st.button("이전"):
            st.session_state.step -= 1
            st.experimental_rerun()

with col3:
    if st.session_state.step < 3:
        if st.button("다음"):
            st.session_state.step += 1
            st.experimental_rerun()
    elif st.session_state.step == 3:
        if st.button("완료"):
            st.success("프로젝트 설정이 완료되었습니다!")