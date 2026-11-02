"""
Profile Page: Candidate information assessment form, skill selector,
interactive NLP skill extraction sandbox, and profile persistence.
"""
import streamlit as st
from utils.constants import CANONICAL_SKILLS, CAREER_DOMAINS
from frontend.utils.api_client import APIClient
from frontend.utils.ui_helpers import render_html

client = APIClient()

SKILL_CATEGORIES = {
    "All": CANONICAL_SKILLS,
    "AI & Data": [
        "Python", "SQL", "NumPy", "Pandas", "Matplotlib", "Seaborn", "Statistics",
        "Machine Learning", "Scikit-learn", "Deep Learning", "TensorFlow", "PyTorch",
        "NLP", "Computer Vision", "LLM", "Hugging Face", "LangChain", "Vector DB",
        "Power BI", "Tableau", "Excel", "Data Wrangling", "ETL"
    ],
    "Web & Fullstack": [
        "JavaScript", "TypeScript", "HTML", "CSS", "React", "Vue", "Angular",
        "Next.js", "Node.js", "Express", "Django", "FastAPI", "Flask",
        "Spring Boot", "REST API", "GraphQL", "PostgreSQL", "MySQL", "MongoDB", "Redis"
    ],
    "Cloud & DevOps": [
        "Docker", "Kubernetes", "Linux", "Git", "GitHub", "CI/CD",
        "AWS", "Azure", "GCP", "Terraform", "Microservices", "System Design"
    ],
    "Cybersecurity": [
        "Network Security", "Cryptography", "Penetration Testing",
        "Ethical Hacking", "SIEM", "SOC", "Linux"
    ],
    "Mobile & Languages": [
        "Flutter", "React Native", "Android", "iOS",
        "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin"
    ]
}


def render_profile_page():
    render_html(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">👤 Candidate Profile & <span class="gradient-text">Skill Assessment</span></h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
                Define your academic background, current technical proficiencies, daily study availability, and target goals.
            </p>
        </div>
        """
    )

    # 1-Click Quick Preset Chips
    render_html(
        """
        <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 18px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em;">
                    ⚡ Quick Fill Presets:
                </div>
                <div style="font-size: 0.78rem; color: #94a3b8;">Click any persona to auto-populate the assessment:</div>
            </div>
        </div>
        """
    )

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        if st.button("📊 Alex (Data Scientist)", use_container_width=True):
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

    with p_col2:
        if st.button("💻 Jordan (Full-Stack Dev)", use_container_width=True):
            st.session_state["p_name"] = "Jordan Lee"
            st.session_state["p_edu"] = "BCA Graduate"
            st.session_state["p_exp"] = "Intermediate"
            st.session_state["p_skills"] = ["JavaScript", "HTML", "CSS", "Git", "GitHub"]
            st.session_state["p_interests"] = "Modern Web Apps, Serverless, Microservices, UI Design"
            st.session_state["p_goal"] = "Full Stack Developer"
            st.session_state["p_domain"] = "Web Development"
            st.session_state["p_hours"] = 2.5
            st.session_state["p_timeline"] = 4
            st.session_state["p_projects"] = "Responsive ecommerce landing pages in HTML/CSS/JS."
            st.session_state["p_prompt"] = "I am a BCA graduate with good knowledge of JavaScript and frontend styling. I want to become a modern Full Stack Web Developer mastering React, Node.js, and databases within 4 months."
            st.rerun()

    with p_col3:
        if st.button("☁️ Samira (DevOps Engineer)", use_container_width=True):
            st.session_state["p_name"] = "Samira Patel"
            st.session_state["p_edu"] = "B.S. Information Systems"
            st.session_state["p_exp"] = "Experienced / Transitioning"
            st.session_state["p_skills"] = ["Linux", "Python", "Git", "GitHub", "REST API"]
            st.session_state["p_interests"] = "Infrastructure as Code, Kubernetes, CI/CD pipelines, Cloud Architecture"
            st.session_state["p_goal"] = "DevOps Engineer"
            st.session_state["p_domain"] = "DevOps"
            st.session_state["p_hours"] = 3.0
            st.session_state["p_timeline"] = 6
            st.session_state["p_projects"] = "Bash automation scripts and Linux server deployment."
            st.session_state["p_prompt"] = "I have worked in system administration and know Linux shell and Python scripting. I want to transition into a Cloud DevOps role mastering Docker, Kubernetes, CI/CD, and AWS."
            st.rerun()

    with p_col4:
        if st.button("🛡️ Marcus (Cybersecurity)", use_container_width=True):
            st.session_state["p_name"] = "Marcus Vance"
            st.session_state["p_edu"] = "B.Tech Computer Science (3rd Year)"
            st.session_state["p_exp"] = "Beginner"
            st.session_state["p_skills"] = ["Linux", "Python", "Git"]
            st.session_state["p_interests"] = "Penetration Testing, Ethical Hacking, Threat Hunting, SOC Operations"
            st.session_state["p_goal"] = "Cybersecurity Analyst"
            st.session_state["p_domain"] = "Cybersecurity"
            st.session_state["p_hours"] = 4.0
            st.session_state["p_timeline"] = 5
            st.session_state["p_projects"] = "Basic network packet capture and firewall config lab."
            st.session_state["p_prompt"] = "I am a Computer Science student with a strong interest in cyber defense. I know Linux and basic Python. I want to prepare for a SOC and Cybersecurity Analyst role."
            st.rerun()

    render_html("<div style='height: 12px;'></div>")

    # Form Container
    with st.form("candidate_profile_form"):
        # Section 1: Candidate Background
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                <span style="font-size: 1.1rem;">👤</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Personal & Academic Background</span>
            </div>
            """
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            name = st.text_input(
                "Full Name *",
                value=st.session_state.get("p_name", ""),
                placeholder="e.g. Alex Morgan"
            )
            education = st.text_input(
                "Current Degree / Educational Background *",
                value=st.session_state.get("p_edu", ""),
                placeholder="e.g. Final-Year B.Tech IT, B.Sc Computer Science, BCA"
            )

        with col_b2:
            exp_options = ["Beginner", "Intermediate", "Experienced / Transitioning"]
            default_exp = st.session_state.get("p_exp", "Beginner")
            exp_idx = exp_options.index(default_exp) if default_exp in exp_options else 0
            experience_level = st.selectbox(
                "Technical Experience Level",
                exp_options,
                index=exp_idx
            )
            interests = st.text_input(
                "Technical Passions & Subject Interests",
                value=st.session_state.get("p_interests", ""),
                placeholder="e.g. AI, Distributed Systems, Cloud Architecture, Analytics"
            )

        render_html("<div style='height: 12px;'></div>")

        # Section 2: Career Objectives & Schedule
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                <span style="font-size: 1.1rem;">🎯</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Career Targets & Availability Constraints</span>
            </div>
            """
        )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            career_goal = st.text_input(
                "Target Job Role / Title",
                value=st.session_state.get("p_goal", "Data Scientist"),
                placeholder="e.g. Data Scientist, AI Engineer, Full Stack Developer"
            )

            pref_domain_idx = 0
            if "p_domain" in st.session_state and st.session_state["p_domain"] in CAREER_DOMAINS:
                pref_domain_idx = CAREER_DOMAINS.index(st.session_state["p_domain"])

            preferred_domain = st.selectbox(
                "Preferred Tech Domain",
                CAREER_DOMAINS,
                index=pref_domain_idx
            )

        with col_c2:
            study_hours = st.slider(
                "Daily Study Capacity (Hours/Day) *",
                min_value=0.5,
                max_value=12.0,
                value=float(st.session_state.get("p_hours", 3.0)),
                step=0.5,
                help="The AI will calibrate your daily theory, coding, and practice tasks to fit this exact budget."
            )
            timeline_months = st.slider(
                "Target Timeline (Months) *",
                min_value=1,
                max_value=24,
                value=int(st.session_state.get("p_timeline", 6)),
                step=1,
                help="Total duration for the synthesized month-by-month and weekly learning roadmap."
            )

        current_projects = st.text_area(
            "Prior Projects or Portfolio Highlights (Optional)",
            value=st.session_state.get("p_projects", ""),
            placeholder="Briefly describe what you have built or worked on previously...",
            height=65
        )

        render_html("<div style='height: 12px;'></div>")

        # Section 3: Technical Skills Inventory
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                <span style="font-size: 1.1rem;">🛠️</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Technical Skills & Known Technologies</span>
            </div>
            """
        )

        current_skills = st.session_state.get("p_skills", ["Python", "SQL"])
        valid_default_skills = [s for s in current_skills if s in CANONICAL_SKILLS]

        selected_skills = st.multiselect(
            "Select skills you currently know or have practiced:",
            options=CANONICAL_SKILLS,
            default=valid_default_skills,
            help="Type to search through canonical industry skills."
        )

        render_html("<div style='height: 12px;'></div>")

        # Section 4: Free-text Career Description & NLP Prompt
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                <span style="font-size: 1.1rem;">💬</span>
                <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">Free-Text Career Description & Resume Snippet (NLP Analysis)</span>
            </div>
            """
        )

        free_text = st.text_area(
            "Describe your journey, skills, and goals in your own natural language:",
            value=st.session_state.get("p_prompt", ""),
            placeholder="e.g. I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months.",
            height=100
        )

        render_html("<div style='height: 15px;'></div>")

        submitted = st.form_submit_button(
            "🚀 Save Assessment & Run ML Career Analysis",
            type="primary",
            use_container_width=True
        )

    # Interactive NLP Extraction Sandbox
    with st.expander("🔬 Interactive NLP Skill Extractor Sandbox (Test Tokenizer)", expanded=False):
        st.caption("Test how the NLP taxonomy engine extracts and normalizes canonical skills from arbitrary free text in real time:")
        test_nlp_input = st.text_area(
            "Sample text to analyze:",
            value="I build fast backend APIs using FastAPI, Docker, and PostgreSQL. I also know basic React and Python.",
            height=70,
            key="test_nlp_sandbox"
        )
        if st.button("⚡ Extract Skills with NLP", key="btn_extract_nlp"):
            extracted = client.extract_skills_nlp(test_nlp_input)
            if extracted:
                st.success(f"Extracted {len(extracted)} canonical skills: {', '.join(extracted)}")
                badges = " ".join([f"<span class='pill-badge pill-emerald'>✓ {s}</span>" for s in extracted])
                render_html(f'<div style="line-height: 2;">{badges}</div>')
            else:
                st.warning("No canonical technical skills identified in this text snippet.")

    # Form Submission Handler
    if submitted:
        if not name.strip():
            st.error("⚠️ Please enter your Full Name.")
            return
        if not education.strip():
            st.error("⚠️ Please enter your Current Qualification.")
            return
        if not selected_skills and not free_text.strip():
            st.error("⚠️ Please select at least one technical skill or provide a text description.")
            return

        profile_payload = {
            "name": name.strip(),
            "education": education.strip(),
            "experience_level": experience_level,
            "career_goal": career_goal.strip() if career_goal else "Data Scientist",
            "preferred_domain": preferred_domain,
            "study_hours": float(study_hours),
            "timeline_months": int(timeline_months),
            "interests": interests.strip(),
            "current_projects": current_projects.strip(),
            "skills": selected_skills,
            "free_text": free_text.strip()
        }

        st.session_state["p_name"] = name
        st.session_state["p_edu"] = education
        st.session_state["p_exp"] = experience_level
        st.session_state["p_goal"] = career_goal
        st.session_state["p_domain"] = preferred_domain
        st.session_state["p_hours"] = study_hours
        st.session_state["p_timeline"] = timeline_months
        st.session_state["p_interests"] = interests
        st.session_state["p_projects"] = current_projects
        st.session_state["p_skills"] = selected_skills
        st.session_state["p_prompt"] = free_text

        with st.spinner("Processing NLP extraction and updating candidate profile..."):
            saved = client.save_profile(profile_payload)
            st.session_state["profile"] = saved
            st.session_state["selected_domain"] = career_goal or preferred_domain
            st.success("✅ Profile successfully validated, normalized, and persisted!")

            col_j1, col_j2 = st.columns([2, 3])
            with col_j1:
                if st.button("👉 Proceed to ML Career Prediction", type="primary", use_container_width=True):
                    st.session_state["nav"] = "🤖 ML Career Prediction"
                    st.rerun()
