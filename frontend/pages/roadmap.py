"""
Roadmap Page: Displays personalized month-by-month and week-by-week learning roadmap.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.components.cards import render_metric_card

client = APIClient()


def render_roadmap_page():
    st.markdown("## 🗺️ Personalized Chronological Learning Roadmap")

    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
        # Check storage via client
        from utils.helpers import load_json
        from utils.constants import DEFAULT_ROADMAP
        stored = load_json(DEFAULT_ROADMAP, default=None)
        if stored:
            roadmap_data = stored
            st.session_state["roadmap"] = stored

    if not roadmap_data:
        st.info("💡 No roadmap generated yet. Complete your profile and click 'Generate Full AI Learning Roadmap'.")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Go to Career Prediction"):
                st.session_state["nav"] = "🤖 ML Career Prediction"
                st.rerun()
        return

    target = roadmap_data.get("target_career", "Data Science")
    timeline = roadmap_data.get("timeline_months", 6)
    hours = roadmap_data.get("available_hours_per_day", 3.0)
    roadmap_core = roadmap_data.get("roadmap", {})
    overview = roadmap_core.get("overview", roadmap_data.get("ai_explanation", ""))

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Target Role", target, "Personalized Track")
    with col2:
        render_metric_card("Duration", f"{timeline} Months", f"{timeline * 4} Total Weeks")
    with col3:
        render_metric_card("Study Commitment", f"{hours} hrs/day", f"{round(hours * 7, 1)} hrs/week")

    st.markdown("### 🎯 Strategic Curriculum Overview")
    st.markdown(
        f"""
        <div style="background-color: #0f172a; padding: 15px; border-left: 4px solid #38bdf8; border-radius: 6px; margin-bottom: 20px;">
            <p style="margin: 0; color: #e2e8f0; font-size: 0.95rem;">{overview}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📅 Monthly Modules & Weekly Plan")
    modules = roadmap_core.get("monthly_modules", [])

    for mod in modules:
        m_num = mod.get("month", 1)
        m_title = mod.get("title", f"Month {m_num}")
        skills = mod.get("focus_skills", [])
        obj = mod.get("learning_objective", "")

        with st.expander(f"📌 {m_title}", expanded=(m_num == 1)):
            st.markdown(f"**🎯 Learning Objective:** {obj}")
            if skills:
                pills = " ".join([
                    f'<span style="background-color: #0369a1; color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; margin: 2px;">{s}</span>'
                    for s in skills
                ])
                st.markdown(f"**Focus Skills:** {pills}", unsafe_allow_html=True)

            st.markdown("---")
            weeks = mod.get("weeks", [])
            w_cols = st.columns(len(weeks) if weeks else 1)

            for idx, w in enumerate(weeks):
                with w_cols[idx]:
                    st.markdown(f"**{w.get('title', f'Week {idx+1}')}**")
                    for t in w.get("topics", []):
                        st.markdown(f"- {t}")
                    st.caption(f"🏁 *Milestone:* {w.get('key_milestone', 'Milestone completed')}")
