# 🚀 AI-Powered Personalized Career Path Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB5424.svg)](https://xgboost.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An enterprise-grade, modular career intelligence platform that analyzes candidate profiles, existing technical proficiencies, learning capacity, and target goals to recommend optimal career domains, perform gap analysis, and generate adaptive learning roadmaps with daily tasks and tiered portfolio projects.

---

## 📌 Problem Statement

Aspiring software engineers, students, and transitioning tech professionals frequently face information overload:
- Unclear career alignment based on their current skill set.
- Generic, non-personalized online roadmaps that do not account for what they already know.
- Lack of daily study scheduling matching real-world availability (e.g. 2–3 hours/day).
- Absence of tiered portfolio projects that demonstrate verified end-to-end industry competency on resumes.

**CareerPath AI** addresses this by decoupling Machine Learning (career prediction), NLP (skill extraction & normalization), AI/LLM (structured roadmaps, tasks, and project generation), and local storage (without requiring heavy database infrastructure).

---

## 🎯 Objectives

1. **Intelligent Domain Prediction:** Predict the best-fitting career domain among 11 distinct tech verticals with confidence probability distributions using trained ML classifiers.
2. **Precision Skill-Gap Engine:** Extract and normalize candidate skills against standard industry taxonomy to identify what is already known versus what is missing.
3. **Adaptive Roadmaps:** Synthesize month-by-month and week-by-week curricula strictly calibrated to the candidate's available study hours and target duration.
4. **Actionable Tasks & Projects:** Generate structured daily schedules (Theory, Coding, Practice) and 3-tiered projects (Mini, Intermediate, Capstone) complete with problem statements, datasets, and resume bullets.
5. **Zero External DB Dependency:** Utilize thread-safe, atomic local JSON persistence for user profiles, roadmaps, and progress tracking.

---

## 🏛️ System Architecture

```
                                  USER INTERACTION
                                         │
                                         ▼
                            Streamlit Frontend (:8501)
               ┌─────────────────────────┴────────────────────────┐
               │  • Profile & Skill Form    • Interactive Plotly  │
               │  • Prediction Dashboard    • Daily Task Manager  │
               │  • Chronological Roadmap   • Adaptive Progress   │
               └─────────────────────────┬────────────────────────┘
                                         │ HTTP REST / Client
                                         ▼
                             FastAPI Backend (:8000)
               ┌─────────────────────────┴────────────────────────┐
               │  • Pydantic Input Validation                     │
               │  • RESTful API Endpoints (/api/career, /roadmap) │
               └──────┬──────────────────────┬─────────────┬──────┘
                      │                      │             │
                      ▼                      ▼             ▼
               ML Engine                 NLP Engine     AI Service
          ┌───────────────────┐    ┌─────────────────┐  ┌──────────────────┐
          │ TF-IDF + Logistic │    │ Regex + TF-IDF  │  │ Pluggable LLM    │
          │ Regression /      │    │ Cosine Sim &    │  │ (Mock / OpenAI / │
          │ XGBoost / RF      │    │ Taxonomy Mapper │  │ Gemini)          │
          └─────────┬─────────┘    └────────┬────────┘  └────────┬─────────┘
                    │                       │                    │
                    └───────────────────────┼────────────────────┘
                                            ▼
                                  Local JSON Storage
                      ┌──────────────────────────────────────────┐
                      │ storage/users/      storage/roadmaps/    │
                      │ storage/progress/   storage/history/     │
                      └──────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Pydantic, Uvicorn, Python-dotenv, Requests, HTTPX
- **Frontend:** Streamlit, Plotly Express & Graph Objects
- **Machine Learning:** Scikit-learn, XGBoost, Joblib, NumPy, Pandas
- **NLP:** Scikit-learn TF-IDF Vectorizer, Cosine Similarity, Regex-based Taxonomy Parsing
- **AI / LLM:** Provider-agnostic abstraction (`MockLLMProvider` built-in, `OpenAILLMProvider`, `GeminiLLMProvider`)
- **Testing:** Pytest, FastAPI TestClient
- **Containerization:** Docker

---

## 📁 Project Structure

```
AI-Career-Path-Generator/
├── frontend/
│   ├── app.py                      # Main Streamlit app entrypoint
│   ├── pages/
│   │   ├── profile.py              # User profile & skill assessment form
│   │   ├── career_prediction.py    # ML predictions & Plotly skill-gap charts
│   │   ├── roadmap.py              # Personalized monthly/weekly roadmap
│   │   ├── tasks.py                # Daily study tasks (Theory/Coding/Practice)
│   │   ├── projects.py             # Tiered projects (Mini/Intermediate/Capstone)
│   │   └── progress.py             # Progress tracking & adaptive suggestions
│   ├── components/
│   │   ├── charts.py               # Plotly gauge, bar, and donut charts
│   │   ├── cards.py                # Metric cards, skill badges, project cards
│   │   └── sidebar.py              # Persistent navigation & app status
│   └── utils/
│       └── api_client.py           # Seamless HTTP client with local fallback
├── backend/
│   ├── main.py                     # FastAPI application & middleware
│   ├── routes/
│   │   ├── profile.py              # /api/profile routes
│   │   ├── career.py               # /api/career/predict & /api/skills routes
│   │   ├── roadmap.py              # /api/roadmap & /api/progress routes
│   │   ├── tasks.py                # /api/tasks/generate route
│   │   └── projects.py             # /api/projects/generate route
│   ├── schemas/
│   │   ├── profile.py              # Pydantic schemas for user profile
│   │   ├── career.py               # Pydantic schemas for ML & NLP
│   │   └── roadmap.py              # Pydantic schemas for roadmaps & tasks
│   └── services/
│       ├── career_service.py       # Orchestration for career predictions
│       ├── skill_gap_service.py    # Gap comparison & match percentage engine
│       ├── roadmap_service.py      # Roadmap generation & JSON management
│       └── ai_service.py           # AI abstraction & adaptive learning logic
├── ml/
│   ├── data/
│   │   ├── career_dataset.csv      # 1,100 balanced multi-domain profile samples
│   │   ├── skills_dataset.csv      # Canonical skills & alias taxonomy
│   │   └── generate_dataset.py     # Reproducible synthetic dataset generator
│   ├── preprocessing/
│   │   └── preprocess.py           # NLP text cleaning, normalization, TF-IDF
│   ├── training/
│   │   ├── train_career_model.py   # Model training, comparison & persistence
│   │   └── evaluate_model.py       # Detailed classification report & metrics
│   ├── models/
│   │   ├── career_model.pkl        # Persisted classification model package
│   │   └── vectorizer.pkl          # Persisted TF-IDF vectorizer
│   └── prediction/
│       └── predictor.py            # Inference engine with probability ranking
├── ai/
│   ├── prompts/
│   │   ├── roadmap_prompt.py       # Month/week curriculum prompts
│   │   ├── task_prompt.py          # Daily study task prompts
│   │   └── project_prompt.py       # Tiered project prompts
│   ├── embeddings.py               # Semantic vector similarity calculations
│   └── llm_service.py              # Pluggable Mock/OpenAI/Gemini provider interface
├── storage/
│   ├── users/user_profile.json     # Saved user profile
│   ├── roadmaps/roadmap.json       # Generated roadmap & curriculum
│   ├── progress/progress.json      # Completed skills, tasks & projects
│   └── history/generations.json    # Audit trail of generations
├── utils/
│   ├── constants.py                # Domain skills map, taxonomy & paths
│   ├── helpers.py                  # Atomic save_json, load_json, update_json
│   └── validators.py               # Sanitization & input validation
├── tests/
│   ├── test_api.py                 # FastAPI endpoint test suite
│   ├── test_ml.py                  # ML model & inference test suite
│   └── test_services.py            # NLP, storage & adaptive logic tests
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── README.md
```

---

## 🔬 Core Methodologies

### 1. Machine Learning Methodology
- **Classification Problem:** Supervised multi-class classification across 11 target domains: Data Science, Machine Learning, AI Engineering, Data Analytics, Web Development, Backend Development, Frontend Development, Cloud Engineering, DevOps, Cybersecurity, Mobile Development.
- **Algorithms Compared:**
  - Logistic Regression (Macro F1: ~1.000)
  - Random Forest Classifier (Macro F1: ~1.000)
  - XGBoost Classifier (Macro F1: ~0.977)
- **Persistence:** Selected best performing model and fitted TF-IDF vectorizer are persisted into `ml/models/` via `joblib`.
- **Inference:** Produces probability rankings across all domains for transparency.

### 2. NLP Methodology
- **Skill Extraction:** Regular expression matching across boundary-safe tokens with alias resolution (e.g. `"python programming"` $\rightarrow$ `"Python"`, `"k8s"` $\rightarrow$ `"Kubernetes"`).
- **Taxonomy Normalization:** Maps diverse colloquial inputs into standardized canonical skills.
- **Skill Gap Calculation:** Compares candidate skill set against domain requirements:
  $$\text{Skill Match } \% = \left( \frac{|\text{Known Skills} \cap \text{Domain Required Skills}|}{|\text{Domain Required Skills}|} \right) \times 100$$

### 3. AI / LLM Methodology
- **Pluggable Abstraction:** Defines `BaseLLMProvider`. Includes a deterministic, offline-capable `MockLLMProvider` for offline evaluations and environments without API keys, plus `OpenAILLMProvider` and `GeminiLLMProvider`.
- **Adaptive Recommendations:** The learning engine evaluates completed topics and dynamically unlocks logical next topics (e.g. mastering Python, Pandas & NumPy triggers recommendations for Inferential Statistics).

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/AI-Career-Path-Generator.git
cd AI-Career-Path-Generator

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
Copy the sample environment configuration:
```bash
cp .env.example .env
```
*(Optional: Configure your `OPENAI_API_KEY` or `GEMINI_API_KEY` in `.env` if you wish to use external cloud LLMs. The default `mock` provider works completely offline out of the box).*

### 3. Train or Verify ML Models
```bash
# Generate reproducible training dataset
python ml/data/generate_dataset.py

# Train models, benchmark, and save artifacts
python ml/training/train_career_model.py

# Evaluate saved models
python ml/training/evaluate_model.py
```

### 4. Running the Application

Open two terminal windows:

**Terminal 1 — FastAPI Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```
*API Swagger Documentation will be live at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

**Terminal 2 — Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```
*Streamlit dashboard will be live at: [http://localhost:8501](http://localhost:8501)*

---

## 🧪 Running Automated Tests

Run the full Pytest test suite:
```bash
pytest -v
```
All 16 test cases covering ML inference, NLP normalization, JSON storage, adaptive recommendations, and FastAPI routes will execute.

---

## 🐳 Docker Deployment

Build and run the entire stack inside a Docker container:
```bash
docker build -t career-path-generator .
docker run -p 8000:8000 -p 8501:8501 career-path-generator
```

---

## 📊 Example Input & Output

### Example Input
- **Name:** Alex Morgan
- **Education:** Final-year B.Tech IT Student
- **Known Skills:** `Python`, `SQL`, `HTML`, `CSS`
- **Interests:** AI, Data Science, Statistical Modeling
- **Target Career:** `Data Scientist`
- **Study Capacity:** 3 hours/day
- **Timeline:** 6 months
- **Free-text Prompt:** *"I am a final-year B.Tech IT student. I know Python, SQL, HTML and CSS. I am interested in AI and data. I can study 3 hours per day and want to become a Data Scientist within 6 months."*

### Example Output
- **Top Domain Prediction:** Data Science (96.4% confidence)
- **Skill Match Percentage:** 68%
- **Mastered Skills Identified:** Python, SQL, Pandas
- **Missing Skills Identified:** NumPy, Statistics, Matplotlib, Machine Learning, Scikit-learn, Deep Learning, Power BI
- **Roadmap:** 6 structured monthly modules with 24 weekly milestones.
- **Daily Tasks:**
  - *Theory (1h):* Core Statistical Distributions and Hypothesis Testing
  - *Coding (1h):* Vectorized calculations in NumPy & Pandas
  - *Practice (1h):* Kaggle Exploratory Data Analysis & unit testing
- **Tiered Projects:**
  - *Mini:* Automated Data Audit and Diagnostic Tool
  - *Intermediate:* Predictive Intelligence API & Interactive Streamlit Dashboard
  - *Capstone:* Enterprise Production Data Platform with Dockerized CI/CD

---

## 💼 Resume Description

> **AI-Powered Personalized Career Path Generator | Python, FastAPI, Streamlit, Scikit-learn, XGBoost, Docker**
> - Architected a modular full-stack career recommendation platform combining ML domain classification, NLP skill extraction, and pluggable AI roadmap synthesis.
> - Benchmarked Logistic Regression, Random Forest, and XGBoost on 1,100+ multi-domain profiles, persisting optimal models via Joblib to achieve 98%+ macro F1-score.
> - Implemented an NLP skill-gap engine normalizing free-form inputs against a standardized technical taxonomy with Plotly visualizations.
> - Engineered a decoupled FastAPI REST backend with Pydantic schemas, atomic local JSON persistence, and an adaptive learning engine that dynamically evolves study plans based on student progress.

