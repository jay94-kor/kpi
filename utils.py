import streamlit as st

def display_project_summary(project):
    st.success("프로젝트가 성공적으로 생성되었습니다!")
    st.subheader("프로젝트 개요")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("프로젝트명", project.name)
        st.metric("매출", f"{project.revenue:,} 원")
        st.metric("예산", f"{project.budget:,} 원")
    with col2:
        st.metric("이익금", f"{project.profit:,} 원")
        st.metric("이익률", f"{project.profit_margin:.2f}%")

def display_project_details(project):
    st.subheader("상세 정보")
    project_data = project.display_project_info()
    for key, value in project_data.items():
        if key != "카테고리와 항목":
            st.write(f"{key}: {value}")

def display_categories_and_items(project):
    st.subheader("카테고리 및 항목 목록")
    for category, items in project.categories.items():
        with st.expander(f"카테고리: {category}"):
            if items:
                for item in items:
                    st.write(f"- {item}")
            else:
                st.write("항목이 없습니다.")