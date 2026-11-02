"""
Career Prediction & Skill Gap Page: Displays ML domain predictions,
confidence distributions, interactive domain comparison sandbox,
and skill gap analysis against standard taxonomy.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from utils.constants import CAREER_DOMAINS
from frontend.utils.ui_helpers import render_html
from frontend.components.charts import (
    render_domain_prediction_chart,
    render_skill_match_gauge,
    render_skill_gap_bar
)
from frontend.components.cards import render_metric_card, render_skill_badges

client = APIClient()


def render_career_prediction_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">🤖 ML Career Domain Prediction & <span class="gradient-text">Skill Gap Analysis</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Probabilistic domain classification trained on 1,100+ profiles combined with algorithmic NLP taxonomy gap analysis.
            </p>
        </div>
        """
    )

    profile = st.session_state.get("profile")

    # Empty state handling
    if not profile:
        render_html(
            """
            <div class="saas-card" style="text-align: center; padding: 40px 20px;">
                <div style="font-size: 2.5rem; margin-bottom: 12px;">👤</div>
                <h3 style="margin-bottom: 8px;">No Active Candidate Profile Found</h3>
                <p style="color: #94a3b8; max-width: 500px; margin: 0 auto 20px auto;">
                    Please fill out your educational background, known skills, and career interests to generate ML predictions.
                </p>
            </div>
            """
        )
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            if st.button("✨ Load Sample Candidate (Alex Morgan)", type="primary", use_container_width=True):
                st.session_state["p_name"] = "Alex Morgan"
                st.session_state["p_edu"] = "Final-Year B.Tech IT Student"
                st.session_state["p_exp"] = "Beginner"
                st.session_state["p_skills"] = ["Python", "SQL", "HTML", "CSS"]
                st.session_state["p_interests"] = "AI, Data Science, Machine Learning, Statistical Analysis"
                st.session_state["p_goal"] = "Data Scientist"
                st.session_state["p_domain"] = "Data Science"
                st.session_state["p_hours"] = 3.0
                st.session_state["p_timeline"] = 6
                st.session_state["p_prompt"] = "I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months."
                payload = {
                    "name": "Alex Morgan",
                    "education": "Final-Year B.Tech IT Student",
                    "experience_level": "Beginner",
                    "career_goal": "Data Scientist",
                    "preferred_domain": "Data Science",
                    "study_hours": 3.0,
                    "timeline_months": 6,
                    "interests": "AI, Data Science, Machine Learning, Statistical Analysis",
                    "skills": ["Python", "SQL", "HTML", "CSS"],
                    "free_text": "I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months."
                }
                saved = client.save_profile(payload)
                st.session_state["profile"] = saved
                st.session_state["selected_domain"] = "Data Science"
                st.rerun()

        with col_e2:
            if st.button("📝 Complete Candidate Profile", use_container_width=True):
                st.session_state["nav"] = "👤 Candidate Profile & Skills"
                st.rerun()
        return

    skills = profile.get("normalized_skills") or profile.get("skills", [])
    interests = profile.get("interests", "")
    education = profile.get("education", "")
    free_text = profile.get("free_text", "")
    target = profile.get("career_goal") or profile.get("preferred_domain") or "Data Science"

    # Run ML prediction & Skill Gap
    with st.spinner("Executing ML multi-class inference and NLP taxonomy gap mapping..."):
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
    known_cnt = gap_res.get("known_count", 0)
    total_req = gap_res.get("total_required_count", 0)
    missing_cnt = len(gap_res.get("missing_skills", []))

    # Top Metric Banner
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("ML Prediction", rec_career, f"Target: {target}", icon="🎯", accent="cyan")
    with col2:
        render_metric_card("Model Confidence", f"{int(confidence * 100)}%", pred_res.get("model_used", "XGBoost / LR"), icon="🤖", accent="emerald")
    with col3:
        render_metric_card("Domain Match", f"{match_pct}%", f"{known_cnt} of {total_req} requirements", icon="⚡", accent="purple")
    with col4:
        render_metric_card("Skills to Acquire", str(missing_cnt), f"{known_cnt} already mastered", icon="📚", accent="amber")

    render_html("<div style='height: 10px;'></div>")

    # Visual Charts Grid
    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        render_domain_prediction_chart(pred_res.get("rankings", []))
    with col_chart2:
        render_skill_match_gauge(match_pct)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # In-Depth Skill Gap Breakdown
    st.markdown("### 🔍 Precision Skill-Gap Inventory")
    st.markdown(f"Comparing current technical proficiencies against standard industry taxonomy for **{target}**:")

    render_skill_badges(
        known_skills=gap_res.get("already_known", []),
        missing_skills=gap_res.get("missing_skills", [])
    )

    render_html("<div style='height: 12px;'></div>")

    # Interactive Domain Comparison Sandbox
    with st.expander("🔄 Dynamic Domain Comparison (Compare Against Other Verticals)", expanded=False):
        st.caption("Curious how your current skills rank against another role? Select any domain below:")
        other_domain = st.selectbox(
            "Select alternative domain to compare:",
            [d for d in CAREER_DOMAINS if d != target],
            index=0,
            key="compare_domain_select"
        )
        if other_domain:
            other_gap = client.analyze_skill_gap(user_skills=skills, target_career=other_domain)
            comp_html = f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 10px; padding: 14px; margin-top: 10px;">
                <div style="font-weight: 700; color: #38bdf8; margin-bottom: 6px;">
                    Comparison Result: {other_domain}
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1;">
                    Readiness: <strong>{other_gap.get('match_percentage')}%</strong> ({other_gap.get('known_count')} of {other_gap.get('total_required_count')} skills met)
                </div>
            </div>
            """
            render_html(comp_html)
            render_skill_badges(
                known_skills=other_gap.get("already_known", []),
                missing_skills=other_gap.get("missing_skills", [])
            )

    render_html("<div style='height: 12px;'></div>")

    # Actionable AI Next Step Callout
    next_step = gap_res.get("next_step", "Begin studying foundational domain principles.")
    action_html = f"""
    <div style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 18px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 1.2rem;">💡</span>
            <span style="font-weight: 700; color: #38bdf8; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.05em;">AI Strategic Milestone Recommendation</span>
        </div>
        <div style="color: #f8fafc; font-size: 0.95rem; line-height: 1.5;">
            {next_step}
        </div>
    </div>
    """
    render_html(action_html)

    render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 24px 0;'>")

    # Roadmap Synthesis Action
    col_act1, col_act2 = st.columns([2, 3])
    with col_act1:
        if st.button("🗺️ Synthesize Full AI Learning Roadmap", type="primary", use_container_width=True):
            with st.spinner(f"Synthesizing {profile.get('timeline_months', 6)}-month adaptive curriculum, daily tasks, and tiered projects..."):
                roadmap = client.generate_roadmap(profile, target)
                st.session_state["roadmap"] = roadmap
                st.session_state["nav"] = "🗺️ Personalized Roadmap"
                st.success("🎉 Complete Career Roadmap successfully synthesized!")
                st.rerun()

    with col_act2:
        st.caption("Synthesizes month-by-month modules, 24 weekly milestones, time-budgeted daily study tasks (Theory, Coding, Practice), and 3-tiered portfolio projects.")
