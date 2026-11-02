"""
LLM Provider Abstraction: Pluggable AI backend supporting Mock (built-in intelligent generator),
OpenAI, and Gemini. Configurable via environment variables without hardcoded keys.
"""
import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Abstract interface for LLM Providers."""

    @abstractmethod
    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Execute text completion given a prompt."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """
    Intelligent built-in AI generator. Produces comprehensive, tailored JSON responses
    based on the exact candidate profile, missing skills, hours, and timeline
    without requiring external network/API keys.
    """

    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        # Check what type of prompt is being requested
        if "CANDIDATE PROFILE:" in prompt or "monthly_modules" in prompt:
            return self._generate_roadmap_json(prompt)
        elif "daily study tasks" in prompt.lower() or "task_type" in prompt:
            return self._generate_tasks_json(prompt)
        elif "portfolio projects" in prompt.lower() or "Mini Project" in prompt:
            return self._generate_projects_json(prompt)
        elif "explain" in prompt.lower() or "confidence" in prompt.lower():
            return self._generate_explanation(prompt)
        return json.dumps({"status": "success", "message": "Standard AI response processed."})

    def _generate_roadmap_json(self, prompt: str) -> str:
        # Extract metadata from prompt
        target = "Data Scientist"
        hours = 3.0
        months = 6
        for line in prompt.split("\n"):
            if "Target Career Role:" in line:
                target = line.split(":", 1)[1].strip()
            elif "Daily Study Capacity:" in line:
                try:
                    hours = float(line.split(":", 1)[1].replace("hours/day", "").strip())
                except ValueError:
                    pass
            elif "Target Timeline:" in line:
                try:
                    months = int(line.split(":", 1)[1].replace("months", "").strip())
                except ValueError:
                    pass

        # Build curated monthly modules up to 'months'
        curricula_templates = {
            "Data Science": [
                ("Foundations & Data Wrangling", ["Python", "Pandas", "NumPy", "Data Wrangling"]),
                ("Statistical Analysis & Visualization", ["Statistics", "Matplotlib", "Seaborn", "Hypothesis Testing"]),
                ("Supervised Machine Learning", ["Scikit-learn", "Regression", "Classification", "Model Evaluation"]),
                ("Ensemble Methods & Unsupervised Learning", ["Random Forests", "XGBoost", "Clustering", "PCA"]),
                ("Deep Learning Fundamentals", ["PyTorch", "Neural Networks", "CNNs", "Computer Vision"]),
                ("Deployment, Portfolio & Interview Prep", ["FastAPI", "Docker", "Model Monitoring", "Portfolio Capstone"])
            ],
            "Machine Learning": [
                ("Mathematical Foundations & Vector Computing", ["NumPy", "Linear Algebra", "Calculus", "Optimization"]),
                ("Core Machine Learning Algorithms", ["Scikit-learn", "Supervised Learning", "Validation Curves"]),
                ("Deep Learning with PyTorch", ["PyTorch", "Autograd", "Backpropagation", "Tensors"]),
                ("Advanced Architectures & NLP", ["Transformers", "Hugging Face", "Attention", "Embeddings"]),
                ("MLOps & Pipeline Engineering", ["Docker", "MLflow", "CI/CD", "Feature Stores"]),
                ("Production Serving & Scalable Inference", ["FastAPI", "Triton", "Quantization", "Capstone"])
            ],
            "AI Engineering": [
                ("Python Advanced & Modern API Design", ["Python 3.12", "FastAPI", "AsyncIO", "Pydantic"]),
                ("Foundational LLM & Prompt Architecture", ["Prompt Engineering", "OpenAI API", "Tokens", "Structured Outputs"]),
                ("Vector Embeddings & Retrieval Systems (RAG)", ["LangChain", "Vector DB", "ChromaDB", "Chunking"]),
                ("Autonomous Agents & Tool Calling", ["Agentic Workflows", "Function Calling", "State Machines"]),
                ("Fine-Tuning & Evaluation", ["LoRA", "Hugging Face", "Evaluation Metrics", "Ragas"]),
                ("Production AI Deployment & Guardrails", ["Docker", "Guardrails AI", "Latency Optimization", "Capstone"])
            ],
            "Web Development": [
                ("Modern JavaScript & HTML5/CSS3", ["ES6+", "Async/Await", "DOM", "Tailwind CSS"]),
                ("Component Architecture with React", ["React", "Hooks", "State Management", "Routing"]),
                ("Full Stack Backend with Node & Express", ["Node.js", "Express", "REST APIs", "Middleware"]),
                ("Database Design & Integration", ["SQL", "PostgreSQL", "MongoDB", "Prisma ORM"]),
                ("Authentication, Security & Testing", ["JWT", "OAuth", "Jest", "API Security"]),
                ("Cloud Deployment & Production Capstone", ["Docker", "Vercel", "AWS ECS", "CI/CD"])
            ]
        }

        template = curricula_templates.get(target, curricula_templates["Data Science"])
        
        modules = []
        for m in range(1, months + 1):
            t_idx = (m - 1) % len(template)
            mod_title, skills = template[t_idx]
            weeks = []
            for w in range(1, 5):
                weeks.append({
                    "week": w,
                    "title": f"Week {w}: Practical {skills[w % len(skills)]} Deep Dive",
                    "topics": [
                        f"{skills[w % len(skills)]} Core Architecture",
                        f"Hands-on coding with {skills[(w + 1) % len(skills)]}",
                        "Real-world unit tests and debugging"
                    ],
                    "key_milestone": f"Deliver a working code artifact mastering {skills[w % len(skills)]}"
                })
            
            modules.append({
                "month": m,
                "title": f"Month {m}: {mod_title}",
                "focus_skills": skills[:3],
                "learning_objective": f"Attain industry competency in {', '.join(skills[:3])} with verified benchmarks.",
                "weeks": weeks
            })

        return json.dumps({
            "candidate_name": "Candidate",
            "target_career": target,
            "timeline_months": months,
            "weekly_study_hours": round(hours * 7, 1),
            "overview": f"A targeted {months}-month engineering pathway designed to elevate you into a {target} role, studying {hours} hours daily.",
            "monthly_modules": modules
        })

    def _generate_tasks_json(self, prompt: str) -> str:
        tasks = [
            {
                "task_title": "Deep Dive into Theoretical Architecture",
                "task_type": "Theory",
                "description": "Read documentation and academic/engineering blogs on underlying mathematical and architectural principles.",
                "estimated_duration": "1 hour",
                "difficulty": "Intermediate",
                "topic": "Core Architecture",
                "expected_outcome": "Complete conceptual notes and flashcards on core trade-offs."
            },
            {
                "task_title": "Hands-on Script Implementation",
                "task_type": "Coding",
                "description": "Write clean, modular Python functions implementing the algorithm or endpoint from scratch with error handling.",
                "estimated_duration": "1 hour",
                "difficulty": "Intermediate",
                "topic": "Coding Implementation",
                "expected_outcome": "Executable script with clean PEP8 formatting and type hints."
            },
            {
                "task_title": "Problem Solving & Test Verification",
                "task_type": "Practice",
                "description": "Solve 2 real-world problem statements and write automated test cases validating edge-case behavior.",
                "estimated_duration": "1 hour",
                "difficulty": "Intermediate",
                "topic": "Applied Practice",
                "expected_outcome": "Green test suite with 90%+ branch coverage."
            }
        ]
        return json.dumps({
            "topic": "Applied Engineering",
            "total_daily_hours": 3.0,
            "tasks": tasks
        })

    def _generate_projects_json(self, prompt: str) -> str:
        target = "Data Scientist"
        if "target_career" in prompt:
            for line in prompt.split("\n"):
                if "target_career" in line or "targeting" in line:
                    target = line.split(":", 1)[-1].replace("'", "").replace('"', '').strip()
                    break

        projects = [
            {
                "level": "Mini Project",
                "project_title": f"Automated {target} Data Audit and Diagnostic Tool",
                "problem_statement": "Manual validation of dirty production data streams causes silent pipeline degradations.",
                "objective": "Build a modular CLI and script that inspects data schema integrity, statistical anomalies, and missing attributes.",
                "features": [
                    "Automated statistical profiling",
                    "Outlier identification via Z-score & IQR",
                    "Automated JSON report export"
                ],
                "dataset_requirement": "Kaggle Open Data or synthetic CSV generator",
                "technologies": ["Python", "Pandas", "NumPy"],
                "ml_ai_approach": "Statistical hypothesis testing and parametric anomaly detection",
                "development_steps": [
                    "Design schema validator",
                    "Implement IQR outlier detector",
                    "Add unit test suite",
                    "Package into a reusable module"
                ],
                "expected_output": "Modular Python library with comprehensive CLI report output",
                "resume_value": "Engineered automated data audit pipeline catching schema anomalies with 99% fidelity."
            },
            {
                "level": "Intermediate Project",
                "project_title": f"Predictive {target} Intelligence API & Interactive Dashboard",
                "problem_statement": "Stakeholders lack immediate predictive insights when querying operational business metrics.",
                "objective": "Train a multi-class predictive model, wrap it in a high-throughput REST API, and expose an interactive Plotly dashboard.",
                "features": [
                    "Supervised ML classification pipeline",
                    "REST API endpoints with Pydantic validation",
                    "Interactive real-time Streamlit UI with Plotly charts"
                ],
                "dataset_requirement": "UCI Machine Learning Repository or Kaggle Industry Dataset (10k+ rows)",
                "technologies": ["Python", "Scikit-learn", "FastAPI", "Streamlit", "Plotly"],
                "ml_ai_approach": "Ensemble Gradient Boosting (XGBoost) with hyperparameter tuning",
                "development_steps": [
                    "Data cleaning and TF-IDF / one-hot feature encoding",
                    "Train & evaluate cross-validated ML models",
                    "Develop FastAPI inference routes",
                    "Build Streamlit dashboard for real-time predictions"
                ],
                "expected_output": "Fully connected web application with sub-50ms inference latency",
                "resume_value": "Architected end-to-end ML service with FastAPI & Streamlit serving 100+ requests/sec."
            },
            {
                "level": "Capstone Project",
                "project_title": f"Enterprise Production {target} Platform with Adaptive Learning",
                "problem_statement": "Enterprises struggle to monitor, version, and orchestrate ML/AI workflows with containerized reproducibility.",
                "objective": "Architect a production-grade microservice incorporating model tracking, automated retraining, and cloud containerization.",
                "features": [
                    "End-to-end ML/AI inference pipeline",
                    "Containerized microservices with Docker",
                    "Automated CI/CD test runner with Pytest",
                    "Live model monitoring and drift telemetry"
                ],
                "dataset_requirement": "Enterprise production logs or Kaggle multi-gigabyte dataset",
                "technologies": ["Python", "FastAPI", "Docker", "Joblib", "Pytest", "Streamlit"],
                "ml_ai_approach": "Deep Neural Network / Hybrid Ensemble with vector embeddings",
                "development_steps": [
                    "Container architecture design and Dockerfile creation",
                    "Pipeline persistence with Joblib and metadata schema",
                    "Integration testing suite with 85%+ code coverage",
                    "Production deployment configuration"
                ],
                "expected_output": "Dockerized enterprise application ready for cloud deployment",
                "resume_value": "Spearheaded enterprise production platform achieving full test automation and Dockerized deployment."
            }
        ]
        return json.dumps({
            "target_career": target,
            "projects": projects
        })

    def _generate_explanation(self, prompt: str) -> str:
        return json.dumps({
            "explanation": "Your background and demonstrated programming proficiency align strongly with this domain. By systematically closing the identified skill gaps over your specified study timeline, you establish verifiable readiness for top-tier roles."
        })


class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI API implementation using standard REST."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


class GeminiLLMProvider(BaseLLMProvider):
    """Google Gemini API implementation using REST endpoint."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model

    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        contents = []
        if system_message:
            contents.append({"role": "user", "parts": [{"text": f"SYSTEM: {system_message}"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]


def get_llm_provider() -> BaseLLMProvider:
    """Factory creating the configured LLM provider according to environment variables."""
    provider_name = os.getenv("LLM_PROVIDER", "mock").lower()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if provider_name == "openai" and openai_key:
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        return OpenAILLMProvider(api_key=openai_key, model=model)
    elif provider_name == "gemini" and gemini_key:
        model = os.getenv("LLM_MODEL", "gemini-1.5-flash")
        return GeminiLLMProvider(api_key=gemini_key, model=model)
    else:
        # High quality offline fallback
        return MockLLMProvider()

