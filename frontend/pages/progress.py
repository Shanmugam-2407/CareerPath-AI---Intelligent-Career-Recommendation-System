"""
Progress Page: Interactive analytics dashboard tracking overall curriculum completion,
mastered skills, daily tasks, tiered projects, adaptive AI recommendations,
and historical generation audit trail.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html
from frontend.components.charts import render_overall_progress_chart
from frontend.components.cards import render_metric_card
from utils.helpers import load_json
from utils.constants import DEFAULT_ROADMAP

client = APIClient()


def render_progress_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">📈 Progress Dashboard & <span class="gradient-text">Adaptive AI Engine</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Track your real-time learning momentum and receive dynamic next-step suggestions as you master topics.
            </p>
        </div>
        """
    )

    progress = client.get_progress()
    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
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
        render_metric_card("Overall Completion", f"{overall_pct:.1f}%", "Weighted Progress", icon="📈", accent="cyan")
    with col2:
        render_metric_card("Mastered Skills", str(len(completed_skills)), f"{len(remaining_skills)} remaining", icon="🛠️", accent="emerald")
    with col3:
        render_metric_card("Tasks Completed", str(len(completed_tasks)), "Study Sessions", icon="✅", accent="purple")
    with col4:
        render_metric_card("Projects Delivered", str(len(completed_projects)), "Portfolio Milestones", icon="🏆", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Chart and Adaptive AI Engine Banner
    col_chart, col_adaptive = st.columns([2, 3])
    with col_chart:
        render_overall_progress_chart(overall_pct)

    with col_adaptive:
        action_title = adaptive.get('action', 'Next Adaptive Step')
        difficulty = adaptive.get('difficulty', 'Intermediate')
        rec_text = adaptive.get('recommendation', 'Continue steady progress on your daily tasks and project milestones.')

        adaptive_html = f"""
        <div style="
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(15, 23, 42, 0.85) 100%);
            border: 1px solid rgba(99, 102, 241, 0.35);
            border-radius: 14px;
            padding: 22px;
            height: 100%;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.4rem;">🧠</span>
                    <span style="font-weight: 800; color: #818cf8; font-size: 1.05rem;">Adaptive AI Recommendation</span>
                </div>
                <span class="pill-badge pill-indigo">{difficulty} Level</span>
            </div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                ⚡ Trigger: {action_title}
            </div>
            <p style="color: #f1f5f9; margin: 8px 0 16px 0; font-size: 0.95rem; line-height: 1.6;">
                {rec_text}
            </p>
            <div style="background: rgba(15, 23, 42, 0.5); padding: 8px 12px; border-radius: 6px; font-size: 0.76rem; color: #94a3b8; border: 1px solid rgba(255, 255, 255, 0.06);">
                💡 The adaptive engine automatically unlocks specialized advanced topics as prerequisites are marked complete.
            </div>
        </div>
        """
        render_html(adaptive_html)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Interactive Skill Mastery Checklist
    st.markdown("### 🎯 Interactive Skill Mastery Checklist")
    st.markdown("Check skills as you learn and practice them to dynamically update your completion score and trigger new AI recommendations:")

    all_domain_skills = sorted(list(set(completed_skills + remaining_skills)))
    if not all_domain_skills and roadmap_data:
        all_domain_skills = roadmap_data.get("skill_gap", {}).get("required_skills", [])

    if all_domain_skills:
        search_query = st.text_input("🔍 Search within skills checklist:", "", placeholder="Type skill name to filter...")

        displayed_skills = [
            s for s in all_domain_skills
            if not search_query or search_query.lower() in s.lower()
        ]

        cols = st.columns(3)
        updated_skills = []

        for i, skill in enumerate(displayed_skills):
            c_idx = i % 3
            with cols[c_idx]:
                checked = st.checkbox(
                    skill,
                    value=(skill in completed_skills),
                    key=f"skill_chk_dash_{skill}"
                )
                if checked:
                    updated_skills.append(skill)

        if search_query:
            for s in all_domain_skills:
                if s not in displayed_skills and s in completed_skills:
                    updated_skills.append(s)

        render_html("<div style='height: 12px;'></div>")

        col_up1, col_up2 = st.columns([2, 3])
        with col_up1:
            if st.button("🔄 Recalculate Adaptive Progression", type="primary", use_container_width=True):
                with st.spinner("Re-evaluating mastery metrics and adaptive triggers..."):
                    client.update_progress(completed_skills=updated_skills)
                    st.toast("🎉 Progression state and adaptive triggers recalculated!")
                    st.rerun()
    else:
        st.info("💡 No domain skills loaded yet. Generate your roadmap to populate the checklist.")

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Generation Audit History
    with st.expander("📜 Historical Generation Audit Trail (storage/history/generations.json)", expanded=False):
        history = client.get_generation_history()
        if history:
            st.markdown(f"Found **{len(history)}** previous roadmap synthesis events:")
            for item in reversed(history[-10:]):
                ts = item.get("timestamp", "N/A")
                t_career = item.get("target_career", "Career")
                t_line = item.get("timeline_months", 6)
                t_hours = item.get("study_hours", 3.0)
                hist_html = f"""
                <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #38bdf8; font-size: 0.88rem;">🎯 {t_career}</span>
                        <span style="font-size: 0.75rem; color: #94a3b8;">📅 {ts}</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 4px;">
                        Study: {t_hours}h/day • Timeline: {t_line} Months • ID: <code>{item.get('generation_id', 'N/A')[:8]}...</code>
                    </div>
                </div>
                """
                render_html(hist_html)
        else:
            st.caption("No historical generation events recorded yet.")
