import streamlit as st
from utils.data_management import SessionLocal, rr_categories_table, rr_items_table
from sqlalchemy import insert, select, func
from sqlalchemy.exc import SQLAlchemyError

def display_rr_form():
    st.subheader("R&R 카테고리 추가")
    category_name = st.text_input("카테고리 이름")
    category_weight = st.number_input("카테고리 가중치", min_value=0.0, max_value=1.0, step=0.1)

    if st.button("카테고리 저장"):
        session = SessionLocal()
        try:
            # 카테고리 가중치 검증
            total_weight = session.execute(select(func.sum(rr_categories_table.c.weight))).scalar() or 0
            if total_weight + category_weight > 1.0:
                st.error("카테고리 가중치의 합이 100%를 초과할 수 없습니다.")
            else:
                stmt = insert(rr_categories_table).values(name=category_name, weight=category_weight)
                session.execute(stmt)
                session.commit()
                st.success("R&R 카테고리가 저장되었습니다.")
        except SQLAlchemyError as e:
            session.rollback()
            st.error(f"데이터베이스 오류: {str(e)}")
        finally:
            session.close()

    st.subheader("R&R 항목 추가")
    session = SessionLocal()
    categories = session.execute(select(rr_categories_table)).fetchall()
    session.close()

    category_options = {category.name: category.id for category in categories}
    selected_category = st.selectbox("카테고리 선택", list(category_options.keys()))
    item_name = st.text_input("항목 이름")
    item_weight = st.number_input("항목 가중치", min_value=0.0, max_value=1.0, step=0.1)
    start_date = st.date_input("시작일")
    end_date = st.date_input("종료일")

    if st.button("항목 저장"):
        session = SessionLocal()
        try:
            # 항목 가중치 검증
            total_item_weight = session.execute(
                select(func.sum(rr_items_table.c.weight))
                .where(rr_items_table.c.category_id == category_options[selected_category])
            ).scalar() or 0
            if total_item_weight + item_weight > 1.0:
                st.error("항목 가중치의 합이 100%를 초과할 수 없습니다.")
            else:
                stmt = insert(rr_items_table).values(
                    category_id=category_options[selected_category],
                    name=item_name,
                    weight=item_weight,
                    start_date=start_date,
                    end_date=end_date
                )
                session.execute(stmt)
                session.commit()
                st.success("R&R 항목이 저장되었습니다.")
        except SQLAlchemyError as e:
            session.rollback()
            st.error(f"데이터베이스 오류: {str(e)}")
        finally:
            session.close()