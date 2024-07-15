import streamlit as st
import plotly.graph_objects as go
from utils.db_utils import get_projects
from datetime import date

st.title('프로젝트 보기')

projects = get_projects()

for project in projects:
    with st.expander(f"프로젝트: {project.name}", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("매출", f"{project.revenue:,}원")
            st.metric("예산", f"{project.budget:,}원")
            st.metric("순이익", f"{project.revenue - project.budget:,}원", delta=f"{project.revenue - project.budget:,}원")
        with col2:
            st.info(f"**프로젝트 관리자:** {project.manager}")
            st.info(f"**프로젝트 기간:** {project.start_date.strftime('%Y-%m-%d')} ~ {project.end_date.strftime('%Y-%m-%d')}")

        st.subheader("역할 및 테스크")
        
        # 역할 분포 파이 차트
        role_names = [role.name for role in project.roles]
        role_percentages = [role.percentage for role in project.roles]
        fig = go.Figure(data=[go.Pie(labels=role_names, values=role_percentages)])
        fig.update_layout(title="역할 분포")
        st.plotly_chart(fig)

        for role in project.roles:
            with st.expander(f"역할: {role.name} ({role.percentage}%)", expanded=False):
                st.write(f"**책임:** {role.responsibility}")
                
                # 테스크 진행 상황 차트
                task_names = [task.name for task in role.tasks]
                task_progress = [task.get_progress() for task in role.tasks]
                fig = go.Figure(data=[go.Bar(x=task_names, y=task_progress)])
                fig.update_layout(title="테스크 진행 상황", yaxis_title="진행률 (%)")
                st.plotly_chart(fig)

                for task in role.tasks:
                    with st.expander(f"테스크: {task.name} ({task.percentage}%)", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**기간:** {task.start_date.strftime('%Y-%m-%d')} ~ {task.end_date.strftime('%Y-%m-%d')}")
                            st.write(f"**상태:** {task.get_status()}")
                        with col2:
                            st.write(f"**진행률:** {task.get_progress()}%")
                            st.progress(task.get_progress() / 100)
                        
                        # 간트 차트
                        fig = go.Figure(data=[go.Bar(
                            x=[(task.end_date - task.start_date).days],
                            y=[task.name],
                            orientation='h',
                            base=date.toordinal(task.start_date),
                            marker_color='rgb(0, 153, 204)'
                        )])
                        fig.update_layout(title="테스크 일정", xaxis_title="날짜", yaxis_title="테스크")
                        fig.update_xaxes(
                            tickformat='%Y-%m-%d',
                            tickvals=[date.toordinal(d) for d in [task.start_date, task.end_date]],
                            ticktext=[task.start_date.strftime('%Y-%m-%d'), task.end_date.strftime('%Y-%m-%d')]
                        )
                        st.plotly_chart(fig)
                        
                        st.write("**참여 직원:**")
                        for allocation in task.allocations:
                            employee = allocation.employee
                            st.write(f"- {employee.name} ({allocation.percentage}%)")

    st.markdown("---")