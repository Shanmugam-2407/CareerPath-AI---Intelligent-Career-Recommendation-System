"""
Progress Page: Interactive dashboard tracking overall curriculum progress,
completed skills/tasks/projects, and displaying adaptive AI recommendations.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.components.charts import render_overall_progress_chart
from frontend.components.cards import render_metric_card

client = APIClient()


def render_progress_page():
    st.markdown("## 📈 Progress Dashboard & Adaptive Recommendations")
    st.markdown("Track your learning momentum and receive dynamic AI suggestions as you master skills.")

    progress = client.get_progress()
    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
        from utils.helpers import load_json
        from utils.constants import DEFAULT_ROADMAP
        stored = load_json(DEFAULT_ROADMAP, default=None)
        if stored:
            roadmap_data = stored
            st.session_state["roadmap"] = stored

    overall_pct = progress.get("overall_completion_percentage", 0.0)
    completed_skills = progress.get("completed_skills", [])
    remaining_skills = progress.get("remaining_skills", [])
    completed_tasks = progress.get("completed_tasks", [])
    completed_projects = progress.get("completed_projects", [])
    adaptive = progress.get("adaptive_recommendation", {})

    # Top summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Overall Completion", f"{overall_pct:.1f}%", "Weighted Progress")
    with col2:
        render_metric_card("Mastered Skills", str(len(completed_skills)), f"{len(remaining_skills)} remaining")
    with col3:
        render_metric_card("Completed Tasks", str(len(completed_tasks)), "Daily Study Goals")
    with col4:
        render_metric_card("Projects Delivered", str(len(completed_projects)), "Portfolio Milestones")

    st.markdown("---")

    # Chart and Adaptive Banner
    col_chart, col_adaptive = st.columns([2, 3])
    with col_chart:
        render_overall_progress_chart(overall_pct)

    with col_adaptive:
        st.markdown("### 🧠 Adaptive Learning Engine")
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid #4338ca; border-radius: 8px; padding: 18px; margin-top: 10px;">
                <span style="background-color: #4f46e5; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">
                    {adaptive.get('action', 'Next Action')}
                </span>
                <p style="color: #e0e7ff; margin: 10px 0; font-size: 0.95rem; line-height: 1.4;">
                    {adaptive.get('recommendation', 'Continue daily lessons.')}
                </p>
                <div style="font-size: 0.8rem; color: #a5b4fc;">
                    Level: <strong>{adaptive.get('difficulty', 'Intermediate')}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Interactive Skill Mastery Checkbox Checklist
    st.markdown("### 🎯 Skill Mastery Checklist")
    st.markdown("Mark skills as you master them to dynamically update your progress and trigger adaptive suggestions:")

    all_domain_skills = sorted(list(set(completed_skills + remaining_skills)))
    if not all_domain_skills and roadmap_data:
        all_domain_skills = roadmap_data.get("skill_gap", {}).get("required_skills", [])

    if all_domain_skills:
        cols = st.columns(3)
        updated_skills = []
        for i, skill in enumerate(all_domain_skills):
            c_idx = i % 3
            with cols[c_idx]:
                checked = st.checkbox(skill, value=(skill in completed_skills), key=f"skill_chk_{skill}")
                if checked:
                    updated_skills.append(skill)

        if st.button("🔄 Recalculate Adaptive Progression", type="primary"):
            with st.spinner("Updating progression state..."):
                updated = client.update_progress(completed_skills=updated_skills)
                st.success("Progression state refreshed!")
                st.rerun()
    else:
        st.info("No active skills to display. Please generate a roadmap first.")
