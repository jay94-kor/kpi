import streamlit as st
import pandas as pd

def show():
    st.header("카테고리 설정")
    
    if 'project' not in st.session_state or st.session_state.project is None:
        st.warning("먼저 프로젝트를 생성해주세요.")
        return

    project = st.session_state.project

    if 'categories' not in st.session_state:
        st.session_state.categories = []

    def add_category():
        category_name = st.session_state["category_input"]
        if category_name and category_name not in [cat['name'] for cat in st.session_state.categories]:
            st.session_state.categories.append({"name": category_name, "weight": 0})
            project.add_category(category_name)
            st.success(f"{category_name} 카테고리가 추가되었습니다.")
            st.experimental_rerun()

    category_name = st.text_input("카테고리명", key="category_input", value="")
    if st.button("카테고리 추가"):
        add_category()

    st.subheader("카테고리 비중 설정")
    
    if st.session_state.categories:
        total_weight = 0
        for i, category in enumerate(st.session_state.categories[:-1]):  # 마지막 카테고리 제외
            weight = st.number_input(f"{category['name']} 비중 (%)", 
                                     min_value=0, 
                                     max_value=100-total_weight, 
                                     value=int(category['weight']),
                                     key=f"weight_{i}")
            category['weight'] = weight
            total_weight += weight

        # 마지막 카테고리 비중 표시 (수정 불가)
        if len(st.session_state.categories) > 0:
            last_category = st.session_state.categories[-1]
            last_category['weight'] = 100 - total_weight
            st.text(f"{last_category['name']} 비중: {last_category['weight']}% (자동 계산)")

        # 카테고리 및 비중 표시
        df = pd.DataFrame(st.session_state.categories)
        st.table(df)

        if st.button("카테고리 설정 완료"):
            for category in st.session_state.categories:
                project.add_category(category['name'], category['weight'])
            st.success("카테고리 설정이 완료되었습니다.")
    else:
        st.warning("카테고리를 추가해주세요.")