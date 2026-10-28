"""
Streamlit Main Application Entrypoint.
Production-style AI-Powered Personalized Career Path Generator dashboard.
"""
import sys
from pathlib import Path

# Ensure workspace root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.pages.profile import render_profile_page
from frontend.pages.career_prediction import render_career_prediction_page
from frontend.pages.roadmap import render_roadmap_page
from frontend.pages.tasks import render_tasks_page
from frontend.pages.projects import render_projects_page
from frontend.pages.progress import render_progress_page
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="AI-Powered Personalized Career Path Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, h4 {
            color: #f8fafc;
            font-weight: 700;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
        }
    </style>
    """,
    unsafe_allow_html=True
)


def render_home_page():
    st.markdown("# 🚀 AI-Powered Personalized Career Path Generator")
    st.markdown(
        """
        ### Bridge the gap between where you are and your dream tech role.
        An enterprise portfolio-grade system combining **Machine Learning classification**, **NLP skill-gap extraction**,
        and **pluggable AI roadmap synthesis** to build an adaptive learning curriculum.
        """
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            #### 1. ML Domain Prediction
            - Multi-class classification across 11 domains
            - TF-IDF + XGBoost & Logistic Regression
            - Confidence probability distributions
            """
        )
    with col2:
        st.markdown(
            """
            #### 2. NLP Skill-Gap Analysis
            - Automated skill extraction from free-form text
            - Canonical taxonomy normalization
            - Interactive Plotly match metrics
            """
        )
    with col3:
        st.markdown(
            """
            #### 3. AI Learning Architecture
            - Structured monthly & weekly roadmaps
            - Daily tasks calibrated to your study hours
            - Resume-ready Mini, Intermediate & Capstone projects
            """
        )

    st.markdown("---")

    st.markdown("### 📋 Architecture & Data Flow")
    st.code(
        """
Candidate Profile Form (Streamlit)
          ↓
FastAPI Validation & Endpoints (Pydantic)
          ↓
ML Prediction Engine (Scikit-Learn / XGBoost / Joblib)
          ↓
NLP Skill Extraction & Skill Gap Engine
          ↓
AI Service Abstraction (Adaptive Roadmap, Tasks & Projects)
          ↓
Local JSON Storage (user_profile.json, roadmap.json, progress.json)
          ↓
Interactive Plotly Visualizations & Adaptive Progress Tracker
        """,
        language="text"
    )

    st.markdown("---")
    c_btn, _ = st.columns([2, 3])
    with c_btn:
        if st.button("🚀 Start Career Analysis", type="primary", use_container_width=True):
            st.session_state["nav"] = "👤 User Profile & Skills"
            st.rerun()


def main():
    # Handle programmatic navigation
    if "nav" in st.session_state:
        selected_nav = st.session_state.pop("nav")
    else:
        selected_nav = render_sidebar()

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
