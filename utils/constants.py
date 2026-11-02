"""
Constants and domain mappings for AI-Powered Personalized Career Path Generator.
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
USERS_DIR = STORAGE_DIR / "users"
ROADMAPS_DIR = STORAGE_DIR / "roadmaps"
PROGRESS_DIR = STORAGE_DIR / "progress"
HISTORY_DIR = STORAGE_DIR / "history"

ML_DIR = BASE_DIR / "ml"
ML_DATA_DIR = ML_DIR / "data"
ML_MODELS_DIR = ML_DIR / "models"

# Storage Files
DEFAULT_USER_PROFILE = USERS_DIR / "user_profile.json"
DEFAULT_ROADMAP = ROADMAPS_DIR / "roadmap.json"
DEFAULT_PROGRESS = PROGRESS_DIR / "progress.json"
DEFAULT_HISTORY = HISTORY_DIR / "generations.json"

# Supported Career Domains
CAREER_DOMAINS = [
    "Data Science",
    "Machine Learning",
    "AI Engineering",
    "Data Analytics",
    "Web Development",
    "Backend Development",
    "Frontend Development",
    "Cloud Engineering",
    "DevOps",
    "Cybersecurity",
    "Mobile Development"
]

# Canonical Skills Taxonomy (Standardized names)
CANONICAL_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin",
    "HTML", "CSS", "React", "Vue", "Angular", "Next.js", "Node.js", "Express", "Django", "FastAPI", "Flask", "Spring Boot",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "NumPy", "Pandas", "Matplotlib", "Seaborn", "Statistics", "Machine Learning", "Scikit-learn",
    "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "LLM", "Hugging Face", "LangChain", "Vector DB",
    "Power BI", "Tableau", "Excel", "Data Wrangling", "ETL",
    "Docker", "Kubernetes", "Linux", "Git", "GitHub", "CI/CD", "AWS", "Azure", "GCP", "Terraform",
    "Network Security", "Cryptography", "Penetration Testing", "Ethical Hacking", "SIEM", "SOC",
    "Flutter", "React Native", "Android", "iOS", "REST API", "GraphQL", "Microservices", "System Design"
]

# Skill Normalization Alias Mapping (lowercased alias -> Canonical Skill)
SKILL_ALIASES = {
    "python": "Python",
    "python programming": "Python",
    "python language": "Python",
    "py": "Python",
    "python3": "Python",
    
    "javascript": "JavaScript",
    "js": "JavaScript",
    "js programming": "JavaScript",
    
    "typescript": "TypeScript",
    "ts": "TypeScript",
    
    "java": "Java",
    "core java": "Java",
    "java programming": "Java",
    
    "c++": "C++",
    "cpp": "C++",
    
    "c#": "C#",
    "csharp": "C#",
    
    "golang": "Go",
    "go": "Go",
    
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "tailwind": "CSS",
    "bootstrap": "CSS",
    
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "vue": "Vue",
    "vuejs": "Vue",
    "angular": "Angular",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express",
    "expressjs": "Express",
    "django": "Django",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "flask": "Flask",
    "spring": "Spring Boot",
    "spring boot": "Spring Boot",
    
    "sql": "SQL",
    "structured query language": "SQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "redis": "Redis",
    
    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "statistics": "Statistics",
    "stats": "Statistics",
    "probability": "Statistics",
    
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "neural networks": "Deep Learning",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    
    "nlp": "NLP",
    "natural language processing": "NLP",
    "text processing": "NLP",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "opencv": "Computer Vision",
    
    "llm": "LLM",
    "large language models": "LLM",
    "huggingface": "Hugging Face",
    "hugging face": "Hugging Face",
    "langchain": "LangChain",
    "vector database": "Vector DB",
    "vector db": "Vector DB",
    
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "tableau": "Tableau",
    "excel": "Excel",
    "ms excel": "Excel",
    "data wrangling": "Data Wrangling",
    "etl": "ETL",
    
    "docker": "Docker",
    "containerization": "Docker",
    "containers": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "linux": "Linux",
    "unix": "Linux",
    "bash": "Linux",
    "shell scripting": "Linux",
    "git": "Git",
    "github": "GitHub",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "terraform": "Terraform",
    
    "cybersecurity": "Network Security",
    "cyber security": "Network Security",
    "network security": "Network Security",
    "cryptography": "Cryptography",
    "penetration testing": "Penetration Testing",
    "pentesting": "Penetration Testing",
    "ethical hacking": "Ethical Hacking",
    "siem": "SIEM",
    "soc": "SOC",
    
    "flutter": "Flutter",
    "react native": "React Native",
    "android": "Android",
    "android development": "Android",
    "ios": "iOS",
    "swift": "Swift",
    "kotlin": "Kotlin",
    
    "rest api": "REST API",
    "restful api": "REST API",
    "apis": "REST API",
    "api": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    "system design": "System Design"
}

# Domain Standard Requirements
DOMAIN_SKILLS_MAP = {
    "Data Science": [
        "Python", "SQL", "NumPy", "Pandas", "Matplotlib", "Statistics",
        "Machine Learning", "Scikit-learn", "Deep Learning", "Power BI"
    ],
    "Machine Learning": [
        "Python", "NumPy", "Pandas", "Statistics", "Machine Learning",
        "Scikit-learn", "Deep Learning", "PyTorch", "TensorFlow", "Docker", "Git"
    ],
    "AI Engineering": [
        "Python", "Deep Learning", "PyTorch", "NLP", "LLM",
        "LangChain", "Vector DB", "FastAPI", "Docker", "Git"
    ],
    "Data Analytics": [
        "SQL", "Excel", "Power BI", "Tableau", "Python",
        "Pandas", "Statistics", "Data Wrangling", "Git"
    ],
    "Web Development": [
        "HTML", "CSS", "JavaScript", "React", "Node.js",
        "Express", "SQL", "MongoDB", "Git", "REST API"
    ],
    "Backend Development": [
        "Python", "FastAPI", "Django", "SQL", "PostgreSQL",
        "Redis", "Docker", "REST API", "Git", "Microservices", "System Design"
    ],
    "Frontend Development": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React",
        "Next.js", "Git", "REST API"
    ],
    "Cloud Engineering": [
        "Linux", "AWS", "Azure", "Docker", "Kubernetes",
        "Terraform", "CI/CD", "Git", "Python", "Network Security"
    ],
    "DevOps": [
        "Linux", "Docker", "Kubernetes", "CI/CD", "Git",
        "Terraform", "AWS", "Python", "Prometheus", "Bash"
    ],
    "Cybersecurity": [
        "Linux", "Network Security", "Cryptography", "Penetration Testing",
        "Ethical Hacking", "Python", "SIEM", "SOC", "Git"
    ],
    "Mobile Development": [
        "Flutter", "React Native", "Android", "iOS", "Kotlin",
        "Swift", "Git", "REST API"
    ]
}

