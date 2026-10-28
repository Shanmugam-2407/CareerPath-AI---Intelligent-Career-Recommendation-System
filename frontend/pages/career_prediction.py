"""
Career Prediction & Skill Gap Page: Shows ML domain predictions, probabilities, and skill gap analysis.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.components.charts import (
    render_domain_prediction_chart,
    render_skill_match_gauge,
    render_skill_gap_bar
)
from frontend.components.cards import render_metric_card, render_skill_badges

client = APIClient()


def render_career_prediction_page():
    st.markdown("## 🤖 ML Career Domain Prediction & Skill Gap")

    profile = st.session_state.get("profile")
    if not profile:
        st.warning("⚠️ No active profile found. Please fill out your profile first.")
        if st.button("Go to User Profile"):
            st.session_state["nav"] = "👤 User Profile & Skills"
            st.rerun()
        return

    skills = profile.get("normalized_skills") or profile.get("skills", [])
    interests = profile.get("interests", "")
    education = profile.get("education", "")
    free_text = profile.get("free_text", "")
    target = profile.get("career_goal") or profile.get("preferred_domain") or "Data Science"

    with st.spinner("Running ML classifier & NLP skill gap analysis..."):
        pred_res = client.predict_career(
            skills=skills,
            interests=interests,
            education=education,
            free_text=free_text
        )
        gap_res = client.analyze_skill_gap(
            user_skills=skills,
            target_career=target,
            free_text=free_text
        )
        st.session_state["prediction"] = pred_res
        st.session_state["skill_gap"] = gap_res

    rec_career = pred_res.get("recommended_career", "Data Science")
    confidence = pred_res.get("confidence_score", 0.85)
    match_pct = gap_res.get("match_percentage", 65.0)

    # Top Metric Banner
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Recommended Career", rec_career, f"Target: {target}")
    with col2:
        render_metric_card("ML Career Confidence", f"{int(confidence * 100)}%", pred_res.get("model_used", "ML Model"))
    with col3:
        render_metric_card("Skill Match Percentage", f"{match_pct}%", f"{gap_res.get('known_count', 0)} of {gap_res.get('total_required_count', 0)} skills met")

    st.markdown("---")

    # Visual Charts
    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        render_domain_prediction_chart(pred_res.get("rankings", []))
    with col_chart2:
        render_skill_match_gauge(match_pct)

    st.markdown("---")

    # Skill Gap Section
    st.markdown("### 🔍 In-Depth Skill Gap & Requirement Breakdown")
    render_skill_badges(
        known_skills=gap_res.get("already_known", []),
        missing_skills=gap_res.get("missing_skills", [])
    )

    st.markdown("#### 🚀 Next Recommended Career Step")
    st.info(f"💡 **Actionable Step:** {gap_res.get('next_step', 'Focus on foundational topics.')}")

    st.markdown("---")
    col_btn1, col_btn2 = st.columns([2, 3])
    with col_btn1:
        if st.button("🗺️ Generate Full AI Learning Roadmap", type="primary", use_container_width=True):
            with st.spinner("Synthesizing personalized timeline, weekly plan, daily tasks, and projects..."):
                roadmap = client.generate_roadmap(profile, target)
                st.session_state["roadmap"] = roadmap
                st.success("🎉 Roadmap successfully generated!")
                st.info("Check the **Personalized Roadmap**, **Daily Tasks**, and **Portfolio Projects** tabs!")
