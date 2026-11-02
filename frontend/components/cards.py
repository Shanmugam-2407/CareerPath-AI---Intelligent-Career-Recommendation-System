"""
Streamlit Card, Badge, and Interactive UI Components.
Implements modern SaaS-style glassmorphism cards, tiered project cards,
interactive skill badges, and progress milestones.
"""
import streamlit as st
from typing import List, Dict, Any, Optional
from frontend.utils.ui_helpers import render_html


def render_workflow_stepper(active_page: str):
    """Renders a responsive 6-step interactive visual wizard at the top of the page."""
    steps = [
        ("Overview", "🏠 Overview"),
        ("Profile", "👤 Profile"),
        ("Prediction", "🤖 Prediction"),
        ("Roadmap", "🗺️ Roadmap"),
        ("Tasks", "✅ Tasks"),
        ("Projects", "🚀 Projects"),
        ("Progress", "📈 Progress")
    ]

    active_idx = 0
    for idx, (key, label) in enumerate(steps):
        if key.lower() in active_page.lower():
            active_idx = idx
            break

    stepper_html = '<div class="stepper-container">'
    for idx, (key, label) in enumerate(steps):
        status_class = ""
        if idx < active_idx:
            status_class = "completed"
            circle_content = "✓"
        elif idx == active_idx:
            status_class = "active"
            circle_content = str(idx + 1)
        else:
            circle_content = str(idx + 1)

        stepper_html += f"""<div class="step-item {status_class}"><div class="step-circle">{circle_content}</div><span>{label}</span></div>"""
        if idx < len(steps) - 1:
            divider_class = "filled" if idx < active_idx else ""
            stepper_html += f'<div class="step-divider {divider_class}"></div>'

    stepper_html += '</div>'
    render_html(stepper_html)


def render_metric_card(
    title: str,
    value: str,
    subtext: str = "",
    delta: Optional[str] = None,
    icon: str = "📊",
    accent: str = "cyan"
):
    """Renders an interactive high-contrast metric card with glowing accent."""
    accents = {
        "cyan": ("#06b6d4", "rgba(6, 182, 212, 0.2)"),
        "sky": ("#38bdf8", "rgba(56, 189, 248, 0.2)"),
        "emerald": ("#10b981", "rgba(16, 185, 129, 0.2)"),
        "purple": ("#8b5cf6", "rgba(139, 92, 246, 0.2)"),
        "amber": ("#f59e0b", "rgba(245, 158, 11, 0.2)"),
        "rose": ("#f43f5e", "rgba(244, 63, 94, 0.2)")
    }
    color, glow = accents.get(accent, ("#38bdf8", "rgba(56, 189, 248, 0.2)"))

    delta_html = ""
    if delta:
        delta_html = f'<span style="background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700; margin-left: 8px;">{delta}</span>'

    card_html = f"""
    <div class="metric-card-pro" style="border-left: 4px solid {color};">
        <div class="metric-label-pro">
            <span>{icon}</span>
            <span>{title}</span>
            {delta_html}
        </div>
        <div class="metric-value-pro" style="color: {color};">{value}</div>
        <div class="metric-subtext-pro">
            <span>{subtext}</span>
        </div>
    </div>
    """
    render_html(card_html)


def render_skill_badges(known_skills: List[str], missing_skills: List[str]):
    """Renders visual pills for already known vs missing skills with clean categorized chips."""
    col1, col2 = st.columns(2)

    with col1:
        known_header = f"""
        <div style="background: rgba(6, 78, 59, 0.2); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #34d399; font-size: 0.95rem;">
                    ✅ Verified Mastered Skills
                </div>
                <span class="pill-badge pill-emerald">{len(known_skills)} Skills</span>
            </div>
        """
        if known_skills:
            badges = "".join([
                f'<span style="background-color: rgba(6, 78, 59, 0.6); color: #6ee7b7; padding: 5px 11px; border-radius: 8px; font-size: 0.82rem; font-weight: 600; display: inline-block; margin: 3px; border: 1px solid rgba(16, 185, 129, 0.4);">✓ {s}</span>'
                for s in known_skills
            ])
            known_html = known_header + f'<div style="line-height: 1.8;">{badges}</div></div>'
        else:
            known_html = known_header + '<div style="color: #94a3b8; font-size: 0.85rem;">No prior domain matching skills detected.</div></div>'
        render_html(known_html)

    with col2:
        missing_header = f"""
        <div style="background: rgba(69, 10, 10, 0.2); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #f87171; font-size: 0.95rem;">
                    🎯 Missing Skills (Target Curriculum)
                </div>
                <span class="pill-badge pill-rose">{len(missing_skills)} Needed</span>
            </div>
        """
        if missing_skills:
            badges = "".join([
                f'<span style="background-color: rgba(69, 10, 10, 0.6); color: #fca5a5; padding: 5px 11px; border-radius: 8px; font-size: 0.82rem; font-weight: 600; display: inline-block; margin: 3px; border: 1px solid rgba(239, 68, 68, 0.4);">⚡ {s}</span>'
                for s in missing_skills
            ])
            missing_html = missing_header + f'<div style="line-height: 1.8;">{badges}</div></div>'
        else:
            missing_html = missing_header + '<div style="color: #34d399; font-size: 0.85rem;">Candidate already covers 100% of domain prerequisites!</div></div>'
        render_html(missing_html)


def render_project_card(project: Dict[str, Any]):
    """Renders a comprehensive, production-grade portfolio project card."""
    level = project.get("level", "Project")
    title = project.get("project_title", "Untitled Project")

    tier_meta = {
        "Mini Project": {
            "color": "#0284c7",
            "bg": "rgba(2, 132, 199, 0.15)",
            "border": "rgba(2, 132, 199, 0.35)",
            "icon": "⚡",
            "phase": "Foundation Milestone (Month 1-2)"
        },
        "Intermediate Project": {
            "color": "#8b5cf6",
            "bg": "rgba(139, 92, 246, 0.15)",
            "border": "rgba(139, 92, 246, 0.35)",
            "icon": "🚀",
            "phase": "Applied System Milestone (Month 3-4)"
        },
        "Capstone Project": {
            "color": "#10b981",
            "bg": "rgba(16, 185, 129, 0.15)",
            "border": "rgba(16, 185, 129, 0.35)",
            "icon": "🏆",
            "phase": "Enterprise Production Milestone (Month 5-6)"
        }
    }

    meta = tier_meta.get(level, tier_meta["Mini Project"])

    with st.expander(f"{meta['icon']} {level}: {title}", expanded=(level == "Mini Project")):
        card_header = f"""
        <div style="
            display: flex; justify-content: space-between; align-items: center;
            background: {meta['bg']}; border: 1px solid {meta['border']};
            border-radius: 10px; padding: 12px 16px; margin-bottom: 16px;
        ">
            <div style="font-weight: 700; color: {meta['color']}; font-size: 1.05rem;">
                {meta['icon']} {level} — <span style="color: #f8fafc;">{title}</span>
            </div>
            <div style="font-size: 0.8rem; color: #cbd5e1; font-weight: 600;">
                {meta['phase']}
            </div>
        </div>
        """
        render_html(card_header)

        st.markdown(f"**🎯 Problem Statement:** {project.get('problem_statement', '')}")
        st.markdown(f"**💡 Primary Objective:** {project.get('objective', '')}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Key Architectural Features:**")
            for f in project.get("features", []):
                st.markdown(f"- {f}")
            st.markdown(f"**📦 Recommended Dataset:** `{project.get('dataset_requirement', 'Public Benchmark Dataset')}`")

        with col_b:
            st.markdown("**Technologies & Frameworks:**")
            tech_badges = "".join([
                f'<span style="background-color: rgba(30, 41, 59, 0.8); color: #38bdf8; padding: 3px 9px; border-radius: 6px; font-size: 0.8rem; border: 1px solid rgba(56, 189, 248, 0.3); margin: 3px; display: inline-block;">{t}</span>'
                for t in project.get("technologies", [])
            ])
            render_html(f'<div style="line-height: 2; margin-bottom: 8px;">{tech_badges}</div>')
            st.markdown(f"**🧠 Approach & Architecture:** {project.get('ml_ai_approach', 'Production ML Pipeline')}")

        st.markdown("---")
        st.markdown("**🛠️ Step-by-Step Implementation Guide:**")
        steps = project.get("development_steps", [])
        for i, step in enumerate(steps, 1):
            st.markdown(f"**{i}.** {step}")

        deliverable_html = f"""
        <div style="background: rgba(15, 23, 42, 0.6); border-left: 4px solid {meta['color']}; border-radius: 6px; padding: 12px; margin: 12px 0;">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">EXPECTED DELIVERABLE</div>
            <div style="color: #f8fafc; font-size: 0.92rem; margin-top: 4px;">{project.get('expected_output', '')}</div>
        </div>
        """
        render_html(deliverable_html)

        resume_bullet = project.get("resume_value", "")
        resume_html = f"""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 14px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: #34d399; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em;">💼 Resume Ready Bullet</span>
                <span style="font-size: 0.75rem; color: #94a3b8;">Copy & Paste to Experience Section</span>
            </div>
            <div style="color: #e2e8f0; font-style: italic; font-size: 0.9rem; line-height: 1.4;">
                "{resume_bullet}"
            </div>
        </div>
        """
        render_html(resume_html)


def render_feature_card(icon: str, title: str, description: str, badge: str = ""):
    """Renders a feature showcase card for the home/overview page."""
    badge_html = f'<span class="pill-badge pill-cyan">{badge}</span>' if badge else ""
    card_html = f"""
    <div class="saas-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div style="font-size: 2rem;">{icon}</div>
            {badge_html}
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 8px;">{title}</div>
        <div style="font-size: 0.88rem; color: #94a3b8; line-height: 1.5;">{description}</div>
    </div>
    """
    render_html(card_html)
