"""
Sidebar navigation, candidate status, and global controls.
Provides persistent state monitoring, backend status ping, and 1-click quick presets.
"""
import streamlit as st
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html

client = APIClient()


def render_sidebar():
    """Renders the persistent left sidebar with rich navigation, user state, and diagnostics."""
    with st.sidebar:
        # Brand Header
        brand_html = """
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 38px; height: 38px; border-radius: 10px;
                    background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.25rem; box-shadow: 0 0 15px rgba(2, 132, 199, 0.4);
                ">🚀</div>
                <div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">CareerPath AI</div>
                    <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Intelligence Suite</div>
                </div>
            </div>
        </div>
        """
        render_html(brand_html)

        # Main Navigation
        pages = [
            "🏠 Overview & Architecture",
            "👤 Candidate Profile & Skills",
            "🤖 ML Career Prediction",
            "🗺️ Personalized Roadmap",
            "✅ Daily Tasks & Practice",
            "🚀 Portfolio Projects",
            "📈 Progress Dashboard"
        ]

        current_nav = st.session_state.get("nav", pages[0])
        default_idx = 0
        for i, p in enumerate(pages):
            if current_nav in p or p in current_nav:
                default_idx = i
                break

        page_selection = st.radio(
            "Navigation Menu",
            pages,
            index=default_idx,
            label_visibility="collapsed"
        )

        render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 18px 0;'>")

        # Active Candidate Profile Card
        profile = st.session_state.get("profile")
        if profile and profile.get("name"):
            name = profile.get("name", "Alex Morgan")
            target = profile.get("career_goal") or profile.get("preferred_domain") or "Data Scientist"
            hours = profile.get("study_hours", 3.0)
            timeline = profile.get("timeline_months", 6)
            skills_count = len(profile.get("skills", []))

            # Fetch completion from storage
            progress = client.get_progress()
            comp_pct = progress.get("overall_completion_percentage", 0.0)

            profile_html = f"""
            <div style="
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 12px;
                padding: 14px;
                margin-bottom: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            ">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <div style="
                        width: 32px; height: 32px; border-radius: 50%;
                        background: #0284c7; color: white; display: flex;
                        align-items: center; justify-content: center; font-weight: bold; font-size: 0.85rem;
                    ">{name[0].upper()}</div>
                    <div style="overflow: hidden;">
                        <div style="font-weight: 700; color: #f8fafc; font-size: 0.92rem; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{name}</div>
                        <div style="font-size: 0.75rem; color: #38bdf8;">🎯 {target}</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
                    <span>⏱️ {hours}h / day</span>
                    <span>📅 {timeline} Months</span>
                    <span>🛠️ {skills_count} Skills</span>
                </div>
                <div style="margin-top: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #cbd5e1; margin-bottom: 2px;">
                        <span>Overall Progress</span>
                        <span style="font-weight: 700; color: #38bdf8;">{comp_pct:.1f}%</span>
                    </div>
                    <div style="width: 100%; height: 5px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
                        <div style="width: {min(comp_pct, 100.0)}%; height: 100%; background: linear-gradient(90deg, #38bdf8, #10b981); border-radius: 3px;"></div>
                    </div>
                </div>
            </div>
            """
            render_html(profile_html)
        else:
            empty_html = """
            <div style="
                background: rgba(15, 23, 42, 0.6);
                border: 1px dashed rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 12px;
                text-align: center;
                margin-bottom: 12px;
            ">
                <div style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 6px;">No candidate profile active.</div>
                <div style="font-size: 0.74rem; color: #64748b;">Complete the profile assessment to unlock personalized recommendations.</div>
            </div>
            """
            render_html(empty_html)

        # Quick Demo Preset Loader
        if st.button("✨ Load Sample Candidate", help="Instantly preloads Alex Morgan (Data Science Track)", use_container_width=True):
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

            payload = {
                "name": st.session_state["p_name"],
                "education": st.session_state["p_edu"],
                "experience_level": st.session_state["p_exp"],
                "career_goal": st.session_state["p_goal"],
                "preferred_domain": st.session_state["p_domain"],
                "study_hours": st.session_state["p_hours"],
                "timeline_months": st.session_state["p_timeline"],
                "interests": st.session_state["p_interests"],
                "current_projects": st.session_state["p_projects"],
                "skills": st.session_state["p_skills"],
                "free_text": st.session_state["p_prompt"]
            }
            saved = client.save_profile(payload)
            st.session_state["profile"] = saved
            st.session_state["nav"] = "🤖 ML Career Prediction"
            st.success("Sample Profile Loaded!")
            st.rerun()

        render_html("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 16px 0;'>")

        # System Architecture & Status Diagnostics
        is_healthy = client.check_health()
        status_text = "FastAPI Connected" if is_healthy else "Direct Local Engine"
        status_dot = "🟢" if is_healthy else "⚡"
        status_desc = "Port 8000 REST" if is_healthy else "Zero-latency in-memory"

        diag_html = f"""
        <div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-weight: 600; color: #cbd5e1;">Engine Architecture:</span>
                <span style="font-weight: 600; color: {'#34d399' if is_healthy else '#38bdf8'}; font-size: 0.72rem;">{status_dot} {status_text}</span>
            </div>
            <div style="font-size: 0.68rem; color: #64748b;">Mode: {status_desc}</div>
        </div>
        <div style="font-size: 0.72rem; color: #64748b; line-height: 1.5; background: rgba(15,23,42,0.4); padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.04);">
            • <strong>ML:</strong> TF-IDF + Logistic / XGBoost<br>
            • <strong>NLP:</strong> Regex & Taxonomy Normalizer<br>
            • <strong>AI/LLM:</strong> Pluggable Intelligence<br>
            • <strong>Storage:</strong> Thread-safe Atomic JSON
        </div>
        """
        render_html(diag_html)

        render_html("<div style='height: 10px;'></div>")

        # Clear session state button
        if st.button("🧹 Reset App State", help="Clears loaded cache in current browser session", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    return page_selection
