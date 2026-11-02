"""
Tasks Page: Displays daily time-budgeted study tasks with category filters,
interactive completion checkboxes, study focus timer, and progress synchronization.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html
from frontend.components.cards import render_metric_card
from utils.helpers import load_json
from utils.constants import DEFAULT_ROADMAP

client = APIClient()


def render_tasks_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">✅ Daily Study Tasks & <span class="gradient-text">Practice Exercises</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Personalized study sessions calibrated strictly into Theory, Hands-on Coding, and Applied Practice.
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
                <div style="font-size: 2.5rem; margin-bottom: 12px;">✅</div>
                <h3 style="margin-bottom: 8px;">No Study Tasks Currently Loaded</h3>
                <p style="color: #94a3b8; max-width: 500px; margin: 0 auto 20px auto;">
                    Generate your career roadmap first to access scheduled daily tasks tailored to your hours.
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
            if st.button("🤖 Run Career Prediction", use_container_width=True):
                st.session_state["nav"] = "🤖 ML Career Prediction"
                st.rerun()
        return

    tasks = roadmap_data.get("daily_tasks", [])
    if not tasks:
        st.warning("No daily tasks currently loaded.")
        return

    # Load current progress
    progress = client.get_progress()
    completed_task_titles = set(progress.get("completed_tasks", []))
    total_tasks = len(tasks)
    done_count = len([t for t in tasks if t.get("task_title") in completed_task_titles])
    completion_rate = (done_count / total_tasks * 100.0) if total_tasks > 0 else 0.0

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Total Tasks", str(total_tasks), "Structured Sessions", icon="📋", accent="cyan")
    with col2:
        render_metric_card("Completed", str(done_count), f"{total_tasks - done_count} remaining", icon="✅", accent="emerald")
    with col3:
        render_metric_card("Completion Rate", f"{completion_rate:.1f}%", "Goal Progress", icon="📈", accent="purple")
    with col4:
        render_metric_card("Daily Budget", f"{roadmap_data.get('available_hours_per_day', 3.0)}h", "Study Time", icon="⏱️", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Interactive Study Focus / Pomodoro Timer Widget
    with st.expander("⏱️ Interactive Study Focus Timer (25-Minute Sprint)", expanded=False):
        t_col1, t_col2, t_col3 = st.columns([1, 1, 2])
        with t_col1:
            timer_box_html = """
            <div style="text-align: center; background: rgba(15, 23, 42, 0.7); border-radius: 10px; padding: 12px; border: 1px solid rgba(56, 189, 248, 0.3);">
                <div style="font-size: 2rem; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono', monospace;">25:00</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Sprint Block</div>
            </div>
            """
            render_html(timer_box_html)
        with t_col2:
            render_html("<div style='height: 4px;'></div>")
            if st.button("▶️ Start Focus Sprint", use_container_width=True):
                st.toast("🎯 25-minute study sprint active! Stay focused.")
            if st.button("🔄 Reset Timer", use_container_width=True):
                st.toast("Timer reset.")
        with t_col3:
            st.caption("Use deep-work sprints for each theory or coding task. Eliminate distractions, run 25 minutes of high focus, then take a 5-minute break.")

    render_html("<div style='height: 10px;'></div>")

    # Filter Tabs
    filter_tabs = ["All Tasks", "📖 Theory", "💻 Coding", "⚡ Practice"]
    selected_type = st.radio("Filter Task Category", filter_tabs, horizontal=True, label_visibility="collapsed")

    type_map = {
        "📖 Theory": "Theory",
        "💻 Coding": "Coding",
        "⚡ Practice": "Practice"
    }

    type_meta = {
        "Theory": {"color": "#0284c7", "bg": "rgba(2, 132, 199, 0.15)", "icon": "📖"},
        "Coding": {"color": "#7c3aed", "bg": "rgba(124, 58, 237, 0.15)", "icon": "💻"},
        "Practice": {"color": "#059669", "bg": "rgba(5, 150, 105, 0.15)", "icon": "⚡"}
    }

    render_html("<div style='height: 10px;'></div>")

    newly_checked = []

    for idx, task in enumerate(tasks):
        title = task.get("task_title", f"Task {idx+1}")
        t_type = task.get("task_type", "Coding")
        duration = task.get("estimated_duration", "1 hour")
        difficulty = task.get("difficulty", "Intermediate")
        desc = task.get("description", "")
        outcome = task.get("expected_outcome", "")
        topic = task.get("topic", "")

        if selected_type != "All Tasks" and type_map.get(selected_type) != t_type:
            if title in completed_task_titles:
                newly_checked.append(title)
            continue

        is_completed = title in completed_task_titles
        meta = type_meta.get(t_type, type_meta["Coding"])

        done_badge = "✓ COMPLETED" if is_completed else "PENDING"
        done_color = "#34d399" if is_completed else "#94a3b8"

        task_html = f"""
        <div style="
            border-left: 4px solid {meta['color']};
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.7) 100%);
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding: 16px 20px;
            border-radius: 12px;
            margin-top: 14px;
            margin-bottom: 6px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; margin-bottom: 4px;">
                        {meta['icon']} {title}
                    </div>
                    <div style="font-size: 0.78rem; color: #38bdf8; font-weight: 600;">
                        📌 Topic: {topic}
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                    <span style="background: {meta['bg']}; color: {meta['color']}; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; border: 1px solid {meta['color']}40;">
                        {t_type}
                    </span>
                    <span style="background: rgba(30, 41, 59, 0.8); color: #cbd5e1; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.1);">
                        ⏱️ {duration}
                    </span>
                    <span style="background: rgba(30, 41, 59, 0.8); color: #cbd5e1; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid rgba(255, 255, 255, 0.1);">
                        📊 {difficulty}
                    </span>
                    <span style="font-size: 0.72rem; font-weight: 700; color: {done_color}; margin-left: 4px;">
                        {done_badge}
                    </span>
                </div>
            </div>
            <p style="color: #cbd5e1; margin: 10px 0 8px 0; font-size: 0.92rem; line-height: 1.5;">{desc}</p>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.15);">
                🎯 <strong>Expected Outcome:</strong> {outcome}
            </div>
        </div>
        """
        render_html(task_html)

        checked = st.checkbox(
            f"Mark as Completed: {title}",
            value=is_completed,
            key=f"task_chk_{idx}"
        )
        if checked:
            newly_checked.append(title)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Sync progress action bar
    col_s1, col_s2 = st.columns([2, 3])
    with col_s1:
        if st.button("💾 Synchronize Task Progress", type="primary", use_container_width=True):
            with st.spinner("Saving progress to progress.json..."):
                client.update_progress(completed_tasks=newly_checked)
                st.toast(f"🎉 Synchronized! {len(newly_checked)} tasks completed.")
                st.rerun()

    with col_s2:
        if st.button("👉 Proceed to Portfolio Projects", use_container_width=True):
            st.session_state["nav"] = "🚀 Portfolio Projects"
            st.rerun()
