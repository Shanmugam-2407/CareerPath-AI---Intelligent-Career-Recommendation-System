"""
Streamlit Card and Badge UI components.
"""
import streamlit as st


def render_metric_card(title: str, value: str, subtext: str = "", delta: str = None):
    """Renders a styled metric card."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 18px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            margin-bottom: 15px;
        ">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #38bdf8; margin: 4px 0;">{value}</div>
            <div style="font-size: 0.82rem; color: #cbd5e1;">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_skill_badges(known_skills: list, missing_skills: list):
    """Renders visual pills for already known vs missing skills."""
    st.markdown("#### Skill Inventory Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Already Mastered ({len(known_skills)})**")
        if known_skills:
            badges_html = " ".join([
                f'<span style="background-color: #064e3b; color: #6ee7b7; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 3px 2px; border: 1px solid #059669;">✓ {s}</span>'
                for s in known_skills
            ])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.info("No prior matching skills detected.")

    with col2:
        st.markdown(f"**Missing Skills to Learn ({len(missing_skills)})**")
        if missing_skills:
            badges_html = " ".join([
                f'<span style="background-color: #450a0a; color: #fca5a5; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 3px 2px; border: 1px solid #dc2626;">❌ {s}</span>'
                for s in missing_skills
            ])
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.success("You have covered all core skills for this domain!")


def render_project_card(project: dict):
    """Renders a comprehensive portfolio project card."""
    level = project.get("level", "Project")
    title = project.get("project_title", "Untitled Project")
    level_colors = {
        "Mini Project": ("#0284c7", "#e0f2fe"),
        "Intermediate Project": ("#7c3aed", "#ede9fe"),
        "Capstone Project": ("#059669", "#d1fae5")
    }
    badge_bg, badge_fg = level_colors.get(level, ("#475569", "#f1f5f9"))

    with st.expander(f"📁 {level}: {title}", expanded=(level == "Mini Project")):
        st.markdown(
            f"""
            <span style="background-color: {badge_bg}; color: white; padding: 3px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: bold;">
                {level}
            </span>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"**Problem Statement:** {project.get('problem_statement', '')}")
        st.markdown(f"**Objective:** {project.get('objective', '')}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Key Features:**")
            for f in project.get("features", []):
                st.markdown(f"- {f}")
            st.markdown(f"**Dataset:** `{project.get('dataset_requirement', 'Standard')}`")

        with col_b:
            st.markdown("**Technologies Used:**")
            tech_badges = " ".join([
                f'<span style="background-color: #1e293b; color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #334155; margin: 2px;">{t}</span>'
                for t in project.get("technologies", [])
            ])
            st.markdown(tech_badges, unsafe_allow_html=True)
            st.markdown(f"**ML/AI Approach:** {project.get('ml_ai_approach', 'Standard ML')}")

        st.markdown("**Development Steps:**")
        for i, step in enumerate(project.get("development_steps", []), 1):
            st.markdown(f"{i}. {step}")

        st.info(f"**Expected Output:** {project.get('expected_output', '')}")
        st.success(f"**Resume Bullet:** *\"{project.get('resume_value', '')}\"*")
