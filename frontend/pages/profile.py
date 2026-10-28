"""
Profile Page: Candidate information entry form, skill selector, and free-text career prompt.
"""
import streamlit as st
from utils.constants import CANONICAL_SKILLS, CAREER_DOMAINS
from frontend.utils.api_client import APIClient

client = APIClient()


def render_profile_page():
    st.markdown("## 👤 Candidate Profile & Skills Assessment")
    st.markdown("Enter your academic background, technical proficiencies, time commitment, and aspirations.")

    # Pre-populate sample profile button
    col_demo1, col_demo2 = st.columns([1, 4])
    with col_demo1:
        if st.button("✨ Load Example Profile", help="Populates example: final-year B.Tech IT student aiming for Data Scientist"):
            st.session_state["p_name"] = "Alex Morgan"
            st.session_state["p_edu"] = "Final-Year B.Tech IT Student"
            st.session_state["p_exp"] = "Beginner"
            st.session_state["p_skills"] = ["Python", "SQL", "HTML", "CSS"]
            st.session_state["p_interests"] = "AI, Data Science, Machine Learning, Statistical Analysis"
            st.session_state["p_goal"] = "Data Scientist"
            st.session_state["p_domain"] = "Data Science"
            st.session_state["p_hours"] = 3.0
            st.session_state["p_timeline"] = 6
            st.session_state["p_projects"] = "Academic bookstore database in SQL, simple portfolio website in HTML/CSS."
            st.session_state["p_prompt"] = "I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months."
            st.rerun()

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", value=st.session_state.get("p_name", ""))
            education = st.text_input(
                "Current Qualification / Education",
                value=st.session_state.get("p_edu", ""),
                placeholder="e.g. B.Tech Computer Science, BCA, B.Sc Mathematics"
            )
            experience_level = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Experienced / Transitioning"],
                index=0
            )
            career_goal = st.text_input(
                "Specific Career Goal / Target Title",
                value=st.session_state.get("p_goal", "Data Scientist"),
                placeholder="e.g. Data Scientist, AI Engineer, Backend Developer"
            )
            preferred_domain = st.selectbox(
                "Preferred Domain",
                CAREER_DOMAINS,
                index=0
            )

        with col2:
            study_hours = st.slider(
                "Available Study Hours / Day",
                min_value=0.5,
                max_value=12.0,
                value=float(st.session_state.get("p_hours", 3.0)),
                step=0.5
            )
            timeline_months = st.slider(
                "Target Timeline (Months)",
                min_value=1,
                max_value=24,
                value=int(st.session_state.get("p_timeline", 6)),
                step=1
            )
            interests = st.text_input(
                "Technical Interests & Passions",
                value=st.session_state.get("p_interests", ""),
                placeholder="e.g. Deep Learning, Data Analytics, Cloud Systems"
            )
            current_projects = st.text_area(
                "Previous / Current Projects (Optional)",
                value=st.session_state.get("p_projects", ""),
                placeholder="Briefly describe what you've built before...",
                height=70
            )

        st.markdown("### 🛠️ Existing Technical Skills & Programming Languages")
        default_skills = st.session_state.get("p_skills", ["Python", "SQL"])
        selected_skills = st.multiselect(
            "Select known skills (type to search)",
            options=CANONICAL_SKILLS,
            default=[s for s in default_skills if s in CANONICAL_SKILLS]
        )

        st.markdown("### 💬 Free-Text Career Description / Prompt (Optional NLP Extraction)")
        free_text = st.text_area(
            "Describe your background and goals in your own words:",
            value=st.session_state.get("p_prompt", ""),
            placeholder="e.g. I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months.",
            height=100
        )

        submitted = st.form_submit_button("🚀 Save Profile & Run ML Career Analysis", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
            return
        if not education.strip():
            st.error("Please enter your qualification.")
            return
        if not selected_skills and not free_text.strip():
            st.error("Please select at least one skill or describe your skills in the text box.")
            return

        profile_payload = {
            "name": name,
            "education": education,
            "experience_level": experience_level,
            "career_goal": career_goal,
            "preferred_domain": preferred_domain,
            "study_hours": study_hours,
            "timeline_months": timeline_months,
            "interests": interests,
            "current_projects": current_projects,
            "skills": selected_skills,
            "free_text": free_text
        }

        with st.spinner("Processing NLP extraction and saving profile..."):
            saved = client.save_profile(profile_payload)
            st.session_state["profile"] = saved
            st.session_state["selected_domain"] = career_goal or preferred_domain
            st.success("✅ Profile successfully processed and saved!")
            st.info("Navigate to **🤖 ML Career Prediction** or **🗺️ Personalized Roadmap** from the sidebar to view your results.")
