import streamlit as st
from streamlit_option_menu import option_menu

def show():
    st.header("항목 설정")
    
    if 'project' not in st.session_state or st.session_state.project is None:
        st.warning("먼저 프로젝트를 생성해주세요.")
        return

    project = st.session_state.project

    def add_item():
        item_name = st.session_state.get("item_input", "")
        category = st.session_state.get("selected_category", "")
        if item_name and category:
            project.add_item_to_category(category, item_name)
            st.success(f"{item_name} 항목이 {category} 카테고리에 추가되었습니다.")
            st.experimental_rerun()

    if project.categories:
        selected_category = option_menu(
            "카테고리를 선택하세요",
            options=project.get_categories(),
            icons=["folder" for _ in project.categories],
            menu_icon="list",
            default_index=0,
            orientation="horizontal",
            key="selected_category",
        )
        item_name = st.text_input("항목명", key="item_input")
        if st.button("항목 추가"):
            add_item()

        # 카테고리와 항목 표시
        st.subheader("카테고리 및 항목 목록")
        for category in project.get_categories():
            with st.expander(f"카테고리: {category}"):
                items = project.get_items_in_category(category)
                if items:
                    for item in items:
                        st.write(f"- {item}")
                else:
                    st.write("항목이 없습니다.")
    else:
        st.warning("먼저 카테고리를 추가해주세요.")