import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from db.models import Project, Role, Task, Employee, Allocation

# 데이터베이스 연결
engine = create_engine('sqlite:///projects.db')

# 데이터베이스 테이블을 DataFrame으로 변환하는 함수
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Streamlit 애플리케이션
st.title('데이터베이스 뷰어')

# 테이블 선택
table_options = ['projects', 'roles', 'tasks', 'employees', 'allocations']
selected_table = st.selectbox('테이블 선택', table_options)

# 선택한 테이블의 데이터 로드 및 표시
if selected_table:
    data = load_data(selected_table)
    st.write(f'**{selected_table}** 테이블 데이터')
    st.dataframe(data)