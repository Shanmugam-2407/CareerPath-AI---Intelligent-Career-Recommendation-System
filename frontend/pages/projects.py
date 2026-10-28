"""
Projects Page: Displays tiered portfolio projects (Mini, Intermediate, Capstone)
with complete technical specifications and resume points.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.components.cards import render_project_card

client = APIClient()


def render_projects_page():
    st.markdown("## 🚀 Tiered Portfolio Projects")
    st.markdown("Build production-ready, resume-grade projects that prove end-to-end competency to recruiters.")

    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
        from utils.helpers import load_json
        from utils.constants import DEFAULT_ROADMAP
        stored = load_json(DEFAULT_ROADMAP, default=None)
        if stored:
            roadmap_data = stored
            st.session_state["roadmap"] = stored

    if not roadmap_data:
        st.info("💡 Generate your career roadmap first to view recommended portfolio projects.")
        return

    projects = roadmap_data.get("projects", [])
    if not projects:
        st.warning("No projects currently generated.")
        return

    # Check progress
    progress = client.get_progress()
    completed_projects = set(progress.get("completed_projects", []))

    for p in projects:
        render_project_card(p)

    st.markdown("---")
    st.markdown("### 🏆 Project Completion Tracking")
    project_titles = [p.get("project_title") for p in projects]
    checked_projects = []

    for title in project_titles:
        is_done = title in completed_projects
        if st.checkbox(f"Completed Project: {title}", value=is_done, key=f"proj_{title}"):
            checked_projects.append(title)

    if st.button("💾 Synchronize Project Milestones", type="primary"):
        with st.spinner("Updating progress.json..."):
            client.update_progress(completed_projects=checked_projects)
            st.success(f"Project milestones saved! {len(checked_projects)} completed.")
            st.rerun()
