import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from db.models import Project, Role, Task, Employee, Allocation

engine = create_engine('sqlite:///projects.db')

def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

def main():
    st.title('데이터베이스 뷰어')

    table_options = ['projects', 'roles', 'tasks', 'employees', 'allocations']
    selected_table = st.selectbox('테이블 선택', table_options)

    if selected_table:
        data = load_data(selected_table)
        st.write(f'**{selected_table}** 테이블 데이터')
        st.dataframe(data)

if __name__ == "__main__":
    main()