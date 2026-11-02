"""
Projects Page: Displays tiered portfolio projects (Mini, Intermediate, Capstone)
with complete technical specifications, dataset requirements, and resume bullet points.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html
from frontend.components.cards import render_metric_card, render_project_card
from utils.helpers import load_json
from utils.constants import DEFAULT_ROADMAP

client = APIClient()


def render_projects_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">🚀 Tiered Portfolio <span class="gradient-text">Project Engine</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Build production-ready, resume-grade systems that demonstrate end-to-end competency to hiring managers.
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
                <div style="font-size: 2.5rem; margin-bottom: 12px;">📁</div>
                <h3 style="margin-bottom: 8px;">No Portfolio Projects Generated Yet</h3>
                <p style="color: #94a3b8; max-width: 500px; margin: 0 auto 20px auto;">
                    Generate your career roadmap to receive tailored Mini, Intermediate, and Capstone projects.
                </p>
            </div>
            """
        )
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("🗺️ Go to Roadmap Generation", type="primary", use_container_width=True):
                st.session_state["nav"] = "🗺️ Personalized Roadmap"
                st.rerun()
        with col_e2:
            if st.button("👤 View Candidate Profile", use_container_width=True):
                st.session_state["nav"] = "👤 Candidate Profile & Skills"
                st.rerun()
        return

    projects = roadmap_data.get("projects", [])
    if not projects:
        st.warning("No projects currently loaded.")
        return

    # Check progress
    progress = client.get_progress()
    completed_projects = set(progress.get("completed_projects", []))
    total_projects = len(projects)
    done_count = len([p for p in projects if p.get("project_title") in completed_projects])

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Portfolio Projects", str(total_projects), "3-Tiered Scope", icon="📁", accent="cyan")
    with col2:
        render_metric_card("Delivered", str(done_count), f"{total_projects - done_count} remaining", icon="🏆", accent="emerald")
    with col3:
        render_metric_card("Resume Bullets", f"{total_projects} Ready", "Impact-Driven", icon="💼", accent="purple")
    with col4:
        render_metric_card("Target Career", roadmap_data.get("target_career", "Data Science"), "Specialization", icon="🎯", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Filter by Tier
    filter_tabs = ["All Tiers", "⚡ Mini Project", "🚀 Intermediate Project", "🏆 Capstone Project"]
    selected_tier = st.radio("Filter Project Tier", filter_tabs, horizontal=True, label_visibility="collapsed")

    tier_map = {
        "⚡ Mini Project": "Mini Project",
        "🚀 Intermediate Project": "Intermediate Project",
        "🏆 Capstone Project": "Capstone Project"
    }

    # Render Project Cards
    for p in projects:
        level = p.get("level", "")
        if selected_tier != "All Tiers" and tier_map.get(selected_tier) != level:
            continue
        render_project_card(p)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Milestone Synchronization Form
    st.markdown("### 🏆 Project Completion & Milestone Synchronization")
    st.markdown("Check off projects as you implement and publish them to your GitHub portfolio:")

    project_titles = [p.get("project_title") for p in projects]
    checked_projects = []

    c_cols = st.columns(len(project_titles) if project_titles else 1)
    for idx, title in enumerate(project_titles):
        is_done = title in completed_projects
        with c_cols[idx]:
            if st.checkbox(f"Completed: {title}", value=is_done, key=f"proj_chk_{title}"):
                checked_projects.append(title)

    render_html("<div style='height: 12px;'></div>")

    col_btn1, col_btn2 = st.columns([2, 3])
    with col_btn1:
        if st.button("💾 Synchronize Project Milestones", type="primary", use_container_width=True):
            with st.spinner("Saving progress to progress.json..."):
                client.update_progress(completed_projects=checked_projects)
                st.toast(f"🎉 Project milestones saved! {len(checked_projects)} completed.")
                st.rerun()

    with col_btn2:
        if st.button("👉 Proceed to Progress Dashboard", use_container_width=True):
            st.session_state["nav"] = "📈 Progress Dashboard"
            st.rerun()
