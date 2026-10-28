"""
Sidebar navigation and global application status component.
"""
import streamlit as st


def render_sidebar():
    """Renders the persistent left sidebar with navigation and app metadata."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #38bdf8; margin: 0;">🚀 CareerPath AI</h2>
                <p style="color: #94a3b8; font-size: 0.85rem;">Intelligent Personalized Career Engine</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        page_selection = st.radio(
            "Navigation",
            [
                "🏠 Overview & Architecture",
                "👤 User Profile & Skills",
                "🤖 ML Career Prediction",
                "🗺️ Personalized Roadmap",
                "✅ Daily Tasks & Practice",
                "🚀 Portfolio Projects",
                "📈 Progress Tracker"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### System Architecture")
        st.markdown(
            """
            - **ML:** Scikit-learn, XGBoost, Joblib
            - **NLP:** TF-IDF, Cosine Sim, Skill Extraction
            - **AI/LLM:** Pluggable Provider Interface
            - **Backend:** FastAPI & Pydantic
            - **Storage:** Local JSON (No SQL/DB)
            """
        )

        st.markdown("---")
        # Check active session profile
        profile = st.session_state.get("profile")
        if profile and profile.get("name"):
            st.success(f"👤 Candidate: **{profile.get('name')}**")
            st.caption(f"Target: {profile.get('career_goal') or 'Data Scientist'}")
            st.caption(f"Hours/day: {profile.get('study_hours')}h | Timeline: {profile.get('timeline_months')}m")
        else:
            st.info("💡 Fill your profile to generate customized path.")

        return page_selection
