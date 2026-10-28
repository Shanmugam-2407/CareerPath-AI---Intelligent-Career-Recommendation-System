"""
Tasks Page: Displays daily time-budgeted study tasks with interactive completion checkboxes.
"""
import streamlit as st
from frontend.utils.api_client import APIClient

client = APIClient()


def render_tasks_page():
    st.markdown("## ✅ Daily Study Tasks & Practice Exercises")
    st.markdown("Daily schedule divided into Theory, Hands-on Coding, and Applied Practice.")

    roadmap_data = st.session_state.get("roadmap")
    if not roadmap_data:
        from utils.helpers import load_json
        from utils.constants import DEFAULT_ROADMAP
        stored = load_json(DEFAULT_ROADMAP, default=None)
        if stored:
            roadmap_data = stored
            st.session_state["roadmap"] = stored

    if not roadmap_data:
        st.info("💡 Generate your roadmap first to access scheduled daily tasks.")
        return

    tasks = roadmap_data.get("daily_tasks", [])
    if not tasks:
        st.warning("No daily tasks currently loaded.")
        return

    # Load current progress
    progress = client.get_progress()
    completed_task_titles = set(progress.get("completed_tasks", []))

    st.markdown(f"**Total Tasks:** {len(tasks)} | **Completed:** {len(completed_task_titles)}")

    newly_checked = []

    type_colors = {
        "Theory": "#0284c7",
        "Coding": "#7c3aed",
        "Practice": "#059669"
    }

    for idx, task in enumerate(tasks):
        title = task.get("task_title", f"Task {idx+1}")
        t_type = task.get("task_type", "Coding")
        duration = task.get("estimated_duration", "1 hour")
        difficulty = task.get("difficulty", "Intermediate")
        desc = task.get("description", "")
        outcome = task.get("expected_outcome", "")
        topic = task.get("topic", "")

        is_completed = title in completed_task_titles
        badge_color = type_colors.get(t_type, "#475569")

        st.markdown(
            f"""
            <div style="border-left: 4px solid {badge_color}; background-color: #0f172a; padding: 12px 18px; border-radius: 6px; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 700; font-size: 1.1rem; color: #f8fafc;">{title}</span>
                    <div>
                        <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; margin-right: 6px;">{t_type}</span>
                        <span style="background-color: #1e293b; color: #94a3b8; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #334155;">⏱️ {duration}</span>
                        <span style="background-color: #1e293b; color: #cbd5e1; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #334155; margin-left: 4px;">{difficulty}</span>
                    </div>
                </div>
                <p style="color: #cbd5e1; margin: 8px 0 4px 0; font-size: 0.9rem;">{desc}</p>
                <div style="font-size: 0.82rem; color: #38bdf8;">🎯 <strong>Expected Outcome:</strong> {outcome}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        checked = st.checkbox(f"Mark '{title}' as Completed", value=is_completed, key=f"task_{idx}")
        if checked:
            newly_checked.append(title)

    st.markdown("---")
    if st.button("💾 Synchronize Task Progress", type="primary"):
        with st.spinner("Updating progress.json..."):
            client.update_progress(completed_tasks=newly_checked)
            st.success(f"Progress synchronized! {len(newly_checked)} tasks marked complete.")
            st.rerun()
