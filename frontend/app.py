"""
Streamlit Main Application Entrypoint.
Production-grade AI-Powered Personalized Career Path Generator dashboard.
Features modern SaaS design, interactive state management, and real-time backend synchronization.
"""
import sys
from pathlib import Path

# Ensure workspace root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from frontend.styles.theme import get_custom_css
from frontend.utils.ui_helpers import render_html
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import render_workflow_stepper, render_metric_card, render_feature_card
from frontend.pages.profile import render_profile_page
from frontend.pages.career_prediction import render_career_prediction_page
from frontend.pages.roadmap import render_roadmap_page
from frontend.pages.tasks import render_tasks_page
from frontend.pages.projects import render_projects_page
from frontend.pages.progress import render_progress_page
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="CareerPath AI — Intelligent Career & Learning Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Master SaaS Theme
render_html(get_custom_css())

client = APIClient()


def render_app_header(selected_nav: str):
    """Renders the modern topbar with live system diagnostics and active candidate identity."""
    is_connected = client.check_health()
    status_text = "FastAPI Connected" if is_connected else "Local Engine Active"
    status_class = "pill-emerald" if is_connected else "pill-cyan"
    status_icon = "🟢" if is_connected else "⚡"

    profile = st.session_state.get("profile")
    candidate_badge = ""
    if profile and profile.get("name"):
        candidate_badge = f"""<div style="display: flex; align-items: center; gap: 8px; background: rgba(30, 41, 59, 0.7); padding: 5px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);"><span style="font-size: 0.82rem; color: #cbd5e1;">Candidate:</span><span style="font-weight: 700; color: #38bdf8; font-size: 0.85rem;">{profile.get('name')}</span></div>"""

    header_html = f"""
    <div class="app-topbar">
        <div class="app-branding">
            <div class="app-logo-badge">🚀</div>
            <div class="app-title-group">
                <h2>CareerPath <span class="gradient-text">AI</span></h2>
                <p>Enterprise Adaptive Career Recommendation & Roadmap Engine</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            {candidate_badge}
            <div class="app-status-pill {status_class}">
                <span class="pulse-dot"></span>
                <span>{status_icon} {status_text}</span>
            </div>
        </div>
    </div>
    """
    render_html(header_html)

    # Render interactive progress stepper
    render_workflow_stepper(selected_nav)


def render_home_page():
    """Renders the modern SaaS homepage with interactive demo personas and architecture overview."""
    # Hero Section
    hero_html = """
    <div class="saas-card saas-card-glow" style="text-align: center; padding: 36px 20px; margin-bottom: 24px;">
        <div style="display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; color: #38bdf8; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
            Next-Gen Career Intelligence
        </div>
        <h1 style="font-size: 2.6rem; font-weight: 800; margin-bottom: 14px; letter-spacing: -0.03em;">
            Bridge the Gap to Your <span class="gradient-text">Dream Tech Career</span>
        </h1>
        <p style="font-size: 1.1rem; color: #94a3b8; max-width: 780px; margin: 0 auto 24px auto; line-height: 1.6;">
            An intelligent system combining <strong>ML multi-class domain classification</strong>,
            <strong>NLP skill-gap taxonomy normalization</strong>, and <strong>adaptive AI curriculum synthesis</strong>
            calibrated to your daily study capacity.
        </p>
    </div>
    """
    render_html(hero_html)

    # Metrics Summary Ribbon
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        render_metric_card("Tech Verticals", "11 Domains", "From AI to DevOps", icon="🎯", accent="cyan")
    with col_m2:
        render_metric_card("ML Accuracy", "98.5%", "Benchmarked Models", icon="🤖", accent="emerald")
    with col_m3:
        render_metric_card("Skill Taxonomy", "75+ Skills", "Canonical Aliases", icon="🔍", accent="purple")
    with col_m4:
        render_metric_card("Persistence", "0 External DB", "Thread-safe Atomic JSON", icon="⚡", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Interactive Guided Launchpad: 4 1-Click Preset Roles
    st.markdown("### ⚡ Interactive Guided Launchpad (1-Click Presets)")
    st.markdown("Test the engine immediately with realistic pre-configured profiles or create your own custom assessment.")

    pcol1, pcol2, pcol3, pcol4 = st.columns(4)

    with pcol1:
        card1_html = """
        <div class="saas-card" style="padding: 16px; height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
            <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem;">Data Scientist</div>
            <div style="font-size: 0.78rem; color: #cbd5e1; margin: 4px 0 10px 0;">Final-Year B.Tech IT student knowing Python & SQL, targeting Data Science.</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 12px;">3 hrs/day • 6 Months</div>
        </div>
        """
        render_html(card1_html)
        if st.button("🚀 Load Alex (Data Science)", use_container_width=True, key="preset_ds"):
            _load_preset(
                name="Alex Morgan",
                edu="Final-Year B.Tech IT Student",
                exp="Beginner",
                skills=["Python", "SQL", "HTML", "CSS"],
                interests="AI, Data Science, Machine Learning, Statistical Modeling",
                goal="Data Scientist",
                domain="Data Science",
                hours=3.0,
                timeline=6,
                prompt="I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months."
            )

    with pcol2:
        card2_html = """
        <div class="saas-card" style="padding: 16px; height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">💻</div>
            <div style="font-weight: 700; color: #818cf8; font-size: 0.95rem;">Full-Stack Engineer</div>
            <div style="font-size: 0.78rem; color: #cbd5e1; margin: 4px 0 10px 0;">Junior developer with JavaScript & HTML/CSS aiming to master React, Node & Next.js.</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 12px;">2.5 hrs/day • 4 Months</div>
        </div>
        """
        render_html(card2_html)
        if st.button("🚀 Load Jordan (Fullstack)", use_container_width=True, key="preset_fs"):
            _load_preset(
                name="Jordan Lee",
                edu="BCA Graduate",
                exp="Intermediate",
                skills=["JavaScript", "HTML", "CSS", "Git", "GitHub"],
                interests="Modern Web Apps, Serverless, Microservices, UI Design",
                goal="Full Stack Developer",
                domain="Web Development",
                hours=2.5,
                timeline=4,
                prompt="I am a BCA graduate with good knowledge of JavaScript and frontend styling. I want to become a modern Full Stack Web Developer mastering React, Node.js, and databases within 4 months."
            )

    with pcol3:
        card3_html = """
        <div class="saas-card" style="padding: 16px; height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">☁️</div>
            <div style="font-weight: 700; color: #34d399; font-size: 0.95rem;">DevOps Specialist</div>
            <div style="font-size: 0.78rem; color: #cbd5e1; margin: 4px 0 10px 0;">Systems administrator knowing Linux & Python, transitioning into Cloud/DevOps.</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 12px;">3 hrs/day • 6 Months</div>
        </div>
        """
        render_html(card3_html)
        if st.button("🚀 Load Samira (DevOps)", use_container_width=True, key="preset_devops"):
            _load_preset(
                name="Samira Patel",
                edu="B.S. Information Systems",
                exp="Experienced / Transitioning",
                skills=["Linux", "Python", "Git", "GitHub", "REST API"],
                interests="Infrastructure as Code, Kubernetes, CI/CD pipelines, Cloud Architecture",
                goal="DevOps Engineer",
                domain="DevOps",
                hours=3.0,
                timeline=6,
                prompt="I have worked in system administration and know Linux shell and Python scripting. I want to transition into a Cloud DevOps role mastering Docker, Kubernetes, CI/CD, and AWS."
            )

    with pcol4:
        card4_html = """
        <div class="saas-card" style="padding: 16px; height: 100%;">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🛡️</div>
            <div style="font-weight: 700; color: #f43f5e; font-size: 0.95rem;">Cybersecurity Analyst</div>
            <div style="font-size: 0.78rem; color: #cbd5e1; margin: 4px 0 10px 0;">Networking student aiming for penetration testing, SIEM, and SOC operations.</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-bottom: 12px;">4 hrs/day • 5 Months</div>
        </div>
        """
        render_html(card4_html)
        if st.button("🚀 Load Marcus (Security)", use_container_width=True, key="preset_sec"):
            _load_preset(
                name="Marcus Vance",
                edu="B.Tech Computer Science (3rd Year)",
                exp="Beginner",
                skills=["Linux", "Python", "Git"],
                interests="Penetration Testing, Ethical Hacking, Threat Hunting, SOC Operations",
                goal="Cybersecurity Analyst",
                domain="Cybersecurity",
                hours=4.0,
                timeline=5,
                prompt="I am a Computer Science student with a strong interest in cyber defense. I know Linux and basic Python. I want to prepare for a SOC and Cybersecurity Analyst role."
            )

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Core Capabilities
    st.markdown("### 🏛️ The 4 Core Architectural Engines")
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)

    with fcol1:
        render_feature_card(
            "🤖",
            "ML Domain Classifier",
            "Multi-class classification trained on balanced domain profiles with TF-IDF and Logistic / XGBoost models.",
            badge="Scikit-Learn"
        )
    with fcol2:
        render_feature_card(
            "🔍",
            "NLP Skill-Gap Engine",
            "Boundary-safe tokenization and canonical alias normalization calculating exact mathematical skill match %.",
            badge="NLP Taxonomy"
        )
    with fcol3:
        render_feature_card(
            "🗺️",
            "AI Learning Engine",
            "Generates adaptive month-by-month roadmaps, daily theory/code/practice tasks, and 3-tiered portfolio projects.",
            badge="AI Planner"
        )
    with fcol4:
        render_feature_card(
            "⚡",
            "Zero-DB Storage",
            "Thread-safe atomic local JSON persistence for user profiles, roadmaps, and progress without external database setup.",
            badge="Local JSON"
        )

    render_html("<div style='height: 15px;'></div>")

    # Start button CTA
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("🚀 Start Custom Career Assessment Now", type="primary", use_container_width=True):
            st.session_state["nav"] = "👤 Candidate Profile & Skills"
            st.rerun()


def _load_preset(name, edu, exp, skills, interests, goal, domain, hours, timeline, prompt):
    """Helper to load preset candidate profiles into session state and save."""
    st.session_state["p_name"] = name
    st.session_state["p_edu"] = edu
    st.session_state["p_exp"] = exp
    st.session_state["p_skills"] = skills
    st.session_state["p_interests"] = interests
    st.session_state["p_goal"] = goal
    st.session_state["p_domain"] = domain
    st.session_state["p_hours"] = hours
    st.session_state["p_timeline"] = timeline
    st.session_state["p_prompt"] = prompt

    payload = {
        "name": name,
        "education": edu,
        "experience_level": exp,
        "career_goal": goal,
        "preferred_domain": domain,
        "study_hours": hours,
        "timeline_months": timeline,
        "interests": interests,
        "skills": skills,
        "free_text": prompt
    }
    saved = client.save_profile(payload)
    st.session_state["profile"] = saved
    st.session_state["selected_domain"] = goal or domain
    st.session_state["nav"] = "🤖 ML Career Prediction"
    st.rerun()


def main():
    """Main routing and rendering controller."""
    # Read navigation state
    if "nav" in st.session_state:
        selected_nav = st.session_state.pop("nav")
    else:
        selected_nav = render_sidebar()

    # Render header and stepper
    render_app_header(selected_nav)

    # Route to appropriate page
    if "Overview" in selected_nav:
        render_home_page()
    elif "Profile" in selected_nav:
        render_profile_page()
    elif "Prediction" in selected_nav:
        render_career_prediction_page()
    elif "Roadmap" in selected_nav:
        render_roadmap_page()
    elif "Tasks" in selected_nav:
        render_tasks_page()
    elif "Projects" in selected_nav:
        render_projects_page()
    elif "Progress" in selected_nav:
        render_progress_page()


if __name__ == "__main__":
    main()
