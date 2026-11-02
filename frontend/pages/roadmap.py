"""
Roadmap Page: Displays personalized month-by-month and week-by-week learning roadmap.
Features interactive month filters, milestone tracking, and 1-click Markdown/JSON export.
"""
import json
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html
from frontend.components.cards import render_metric_card
from utils.helpers import load_json
from utils.constants import DEFAULT_ROADMAP

client = APIClient()


def render_roadmap_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">🗺️ Personalized Chronological <span class="gradient-text">Learning Roadmap</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Calibrated strictly to your target career, existing technical baseline, and daily study capacity.
            </p>
        </div>
        """
    )

    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
        stored = load_json(DEFAULT_ROADMAP, default=None)
        if stored:
            roadmap_data = stored
            st.session_state["roadmap"] = stored

    if not roadmap_data:
        render_html(
            """
            <div class="saas-card" style="text-align: center; padding: 40px 20px;">
                <div style="font-size: 2.5rem; margin-bottom: 12px;">🗺️</div>
                <h3 style="margin-bottom: 8px;">No Learning Roadmap Generated Yet</h3>
                <p style="color: #94a3b8; max-width: 500px; margin: 0 auto 20px auto;">
                    Generate your personalized curriculum by completing the candidate assessment and running the career analysis.
                </p>
            </div>
            """
        )
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("🚀 Generate Sample 6-Month Roadmap", type="primary", use_container_width=True):
                sample_profile = {
                    "name": "Alex Morgan",
                    "education": "Final-Year B.Tech IT Student",
                    "experience_level": "Beginner",
                    "target_career": "Data Scientist",
                    "study_hours": 3.0,
                    "timeline_months": 6,
                    "skills": ["Python", "SQL", "HTML", "CSS"],
                    "free_text": "I want to become a Data Scientist within 6 months."
                }
                with st.spinner("Synthesizing comprehensive curriculum..."):
                    generated = client.generate_roadmap(sample_profile, "Data Scientist")
                    st.session_state["roadmap"] = generated
                    st.session_state["profile"] = sample_profile
                    st.success("Roadmap generated!")
                    st.rerun()

        with col_e2:
            if st.button("🤖 Go to Career Prediction", use_container_width=True):
                st.session_state["nav"] = "🤖 ML Career Prediction"
                st.rerun()
        return

    target = roadmap_data.get("target_career", "Data Science")
    timeline = roadmap_data.get("timeline_months", 6)
    hours = roadmap_data.get("available_hours_per_day", 3.0)
    roadmap_core = roadmap_data.get("roadmap", {})
    overview = roadmap_core.get("overview", roadmap_data.get("ai_explanation", ""))
    modules = roadmap_core.get("monthly_modules", [])
    total_weeks = sum(len(m.get("weeks", [])) for m in modules)

    # Top Metrics Ribbon
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Target Role", target, "Personalized Track", icon="🎯", accent="cyan")
    with col2:
        render_metric_card("Duration", f"{timeline} Months", f"{total_weeks} Total Sprints", icon="📅", accent="emerald")
    with col3:
        render_metric_card("Daily Commitment", f"{hours}h / day", f"{round(hours * 7, 1)}h / week", icon="⏱️", accent="purple")
    with col4:
        render_metric_card("Total Modules", f"{len(modules)} Months", "Sprint Blocks", icon="🏆", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Strategic Curriculum Overview
    overview_html = f"""
    <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.6) 100%); border-left: 4px solid #38bdf8; border-radius: 12px; padding: 18px; margin-bottom: 24px; border-top: 1px solid rgba(255,255,255,0.08); border-right: 1px solid rgba(255,255,255,0.08); border-bottom: 1px solid rgba(255,255,255,0.08);">
        <div style="font-weight: 700; color: #38bdf8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
            🎯 Strategic Curriculum Architecture
        </div>
        <p style="margin: 0; color: #f1f5f9; font-size: 0.95rem; line-height: 1.6;">{overview}</p>
    </div>
    """
    render_html(overview_html)

    # Export & Filter Row
    col_exp1, col_exp2, col_exp3 = st.columns([2, 1, 1])
    with col_exp1:
        st.markdown("### 📅 Chronological Timeline & Milestones")

    with col_exp2:
        md_content = f"# Career Roadmap: {target}\n\n**Candidate Duration:** {timeline} Months ({hours} hrs/day)\n\n## Overview\n{overview}\n\n"
        for m in modules:
            md_content += f"### {m.get('title', 'Month')}\n**Objective:** {m.get('learning_objective', '')}\n**Skills:** {', '.join(m.get('focus_skills', []))}\n\n"
            for w in m.get("weeks", []):
                md_content += f"- **{w.get('title', 'Week')}**: {', '.join(w.get('topics', []))} *(Milestone: {w.get('key_milestone', '')})*\n"
            md_content += "\n"

        st.download_button(
            label="📥 Export as Markdown",
            data=md_content,
            file_name=f"career_roadmap_{target.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_exp3:
        st.download_button(
            label="📦 Export as JSON",
            data=json.dumps(roadmap_data, indent=2),
            file_name=f"career_roadmap_{target.lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )

    # Interactive Month Filter Tabs
    month_tabs = ["All Months"] + [f"Month {m.get('month', i+1)}" for i, m in enumerate(modules)]
    selected_tab = st.radio("Filter Month View", month_tabs, horizontal=True, label_visibility="collapsed")

    render_html("<div style='height: 10px;'></div>")

    # Render Modules
    for mod in modules:
        m_num = mod.get("month", 1)
        m_label = f"Month {m_num}"

        if selected_tab != "All Months" and selected_tab != m_label:
            continue

        m_title = mod.get("title", f"Month {m_num}")
        skills = mod.get("focus_skills", [])
        obj = mod.get("learning_objective", "")
        weeks = mod.get("weeks", [])

        with st.expander(f"📌 {m_title} ({len(weeks)} Weeks)", expanded=True):
            mod_header_html = f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 14px 16px; margin-bottom: 16px;">
                <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                    🎯 Monthly Objective
                </div>
                <div style="color: #f8fafc; font-size: 0.95rem; font-weight: 500;">
                    {obj}
                </div>
            </div>
            """
            render_html(mod_header_html)

            if skills:
                pills = " ".join([
                    f'<span class="pill-badge pill-cyan">⚡ {s}</span>'
                    for s in skills
                ])
                render_html(f'<div style="margin-bottom: 16px;"><strong>Target Core Skills:</strong> {pills}</div>')

            if weeks:
                w_cols = st.columns(min(len(weeks), 4))
                for idx, w in enumerate(weeks):
                    col_target = w_cols[idx % min(len(weeks), 4)]
                    with col_target:
                        topics_html = "".join([f"<li style='margin-bottom: 4px;'>{t}</li>" for t in w.get("topics", [])])
                        week_html = f"""
                        <div class="week-card">
                            <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem; margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 6px;">
                                {w.get('title', f'Week {idx+1}')}
                            </div>
                            <div style="font-size: 0.8rem; color: #cbd5e1; margin-bottom: 10px;">
                                <ul style="padding-left: 18px; margin: 0;">
                                    {topics_html}
                                </ul>
                            </div>
                            <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 6px 10px; border-radius: 4px; font-size: 0.74rem; color: #34d399;">
                                🏁 <strong>Milestone:</strong> {w.get('key_milestone', 'Completed')}
                            </div>
                        </div>
                        """
                        render_html(week_html)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Next step action
    col_n1, col_n2 = st.columns([2, 3])
    with col_n1:
        if st.button("👉 Proceed to Daily Tasks & Practice", type="primary", use_container_width=True):
            st.session_state["nav"] = "✅ Daily Tasks & Practice"
            st.rerun()
    with col_n2:
        st.caption("View your time-budgeted daily study sessions divided into Theory, Hands-on Coding, and Applied Practice.")
