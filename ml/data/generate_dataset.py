"""
Script to generate a rich, realistic career domain classification dataset.
Generates 1,100 samples across 11 target career domains with realistic skill combinations.
"""
import random
import pandas as pd
from pathlib import Path

# Fix random seed for reproducibility
random.seed(42)

CAREER_PROFILES = {
    "Data Science": {
        "core": ["Python", "SQL", "Pandas", "NumPy", "Statistics"],
        "common": ["Matplotlib", "Seaborn", "Machine Learning", "Scikit-learn", "Data Wrangling"],
        "optional": ["Deep Learning", "Power BI", "Tableau", "Git", "Excel", "R", "Big Data", "NLP"],
        "interests": ["data analysis", "predictive modeling", "statistical thinking", "insights discovery", "business forecasting"]
    },
    "Machine Learning": {
        "core": ["Python", "Machine Learning", "Scikit-learn", "NumPy", "Pandas"],
        "common": ["Deep Learning", "PyTorch", "TensorFlow", "Statistics", "Git"],
        "optional": ["Docker", "Linux", "MLOps", "Computer Vision", "NLP", "Feature Engineering"],
        "interests": ["model architecture", "algorithm optimization", "neural networks", "autonomous systems", "pattern recognition"]
    },
    "AI Engineering": {
        "core": ["Python", "Deep Learning", "PyTorch", "NLP", "LLM"],
        "common": ["LangChain", "Vector DB", "Hugging Face", "FastAPI", "Docker"],
        "optional": ["Computer Vision", "Git", "REST API", "Kubernetes", "Fine-Tuning", "RAG"],
        "interests": ["generative ai", "prompt engineering", "agentic workflows", "transformer models", "ai integration"]
    },
    "Data Analytics": {
        "core": ["SQL", "Excel", "Power BI", "Data Wrangling", "Statistics"],
        "common": ["Tableau", "Python", "Pandas", "Matplotlib", "ETL"],
        "optional": ["Seaborn", "Git", "Dashboarding", "Business Analytics", "Reporting"],
        "interests": ["business intelligence", "metrics visualization", "dashboard creation", "trend analysis", "reporting"]
    },
    "Web Development": {
        "core": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        "common": ["Express", "SQL", "Git", "REST API", "MongoDB"],
        "optional": ["TypeScript", "Next.js", "Tailwind", "Docker", "Redux", "Bootstrap"],
        "interests": ["full stack web", "interactive user interfaces", "responsive design", "web apps", "client server architecture"]
    },
    "Backend Development": {
        "core": ["Python", "FastAPI", "SQL", "PostgreSQL", "REST API"],
        "common": ["Docker", "Redis", "Git", "Microservices", "System Design"],
        "optional": ["Django", "Linux", "Node.js", "Java", "Spring Boot", "Go", "CI/CD", "Kafka"],
        "interests": ["high-throughput systems", "api design", "database indexing", "scalable architecture", "server-side logic"]
    },
    "Frontend Development": {
        "core": ["HTML", "CSS", "JavaScript", "TypeScript", "React"],
        "common": ["Next.js", "Git", "REST API", "Tailwind", "Responsive Design"],
        "optional": ["Vue", "Angular", "Redux", "UI/UX", "Jest", "Figma", "Webpack"],
        "interests": ["ui design", "component libraries", "frontend performance", "user experience", "browser rendering"]
    },
    "Cloud Engineering": {
        "core": ["Linux", "AWS", "Docker", "Kubernetes", "Terraform"],
        "common": ["Azure", "GCP", "CI/CD", "Git", "Python"],
        "optional": ["Network Security", "Bash", "Ansible", "CloudFormation", "IAM"],
        "interests": ["cloud architecture", "serverless", "infrastructure provisioning", "high availability", "cloud migration"]
    },
    "DevOps": {
        "core": ["Linux", "Docker", "Kubernetes", "CI/CD", "Git"],
        "common": ["Terraform", "AWS", "Python", "Prometheus", "Bash"],
        "optional": ["Ansible", "Jenkins", "Grafana", "Helm", "GCP", "Azure"],
        "interests": ["pipeline automation", "continuous deployment", "observability", "infrastructure as code", "system reliability"]
    },
    "Cybersecurity": {
        "core": ["Linux", "Network Security", "Cryptography", "Penetration Testing", "Ethical Hacking"],
        "common": ["SIEM", "SOC", "Python", "Git", "Wireshark"],
        "optional": ["Burp Suite", "Metasploit", "Bash", "Incident Response", "Vulnerability Management"],
        "interests": ["threat modeling", "defensive security", "network analysis", "vulnerability patching", "security auditing"]
    },
    "Mobile Development": {
        "core": ["Flutter", "React Native", "Android", "iOS", "Git"],
        "common": ["Kotlin", "Swift", "REST API", "Mobile UI", "Firebase"],
        "optional": ["Dart", "SQLite", "App Store Deployment", "GraphQL", "Redux"],
        "interests": ["mobile app design", "cross platform apps", "native performance", "app store publishing", "touch UX"]
    }
}

def generate_samples(samples_per_domain: int = 100) -> pd.DataFrame:
    rows = []
    
    for domain, profile in CAREER_PROFILES.items():
        for i in range(samples_per_domain):
            # Select skills based on probability
            # 3 to 5 core skills
            k_core = random.randint(3, len(profile["core"]))
            selected_core = random.sample(profile["core"], k_core)
            
            # 2 to 4 common skills
            k_common = random.randint(1, min(len(profile["common"]), 4))
            selected_common = random.sample(profile["common"], k_common)
            
            # 0 to 2 optional skills
            k_opt = random.randint(0, min(len(profile["optional"]), 2))
            selected_opt = random.sample(profile["optional"], k_opt)
            
            # 5% chance of minor cross-domain noise skill
            noise = []
            if random.random() < 0.2:
                all_skills = [s for d, p in CAREER_PROFILES.items() if d != domain for s in p["core"]]
                noise = [random.choice(all_skills)]
            
            all_user_skills = list(set(selected_core + selected_common + selected_opt + noise))
            random.shuffle(all_user_skills)
            skills_str = ", ".join(all_user_skills)
            
            # Select interests
            k_int = random.randint(1, 3)
            interests = ", ".join(random.sample(profile["interests"], k_int))
            
            # Profile summary text
            profile_text = f"Skills: {skills_str}. Interested in {interests}. Aiming for {domain} roles."
            
            rows.append({
                "profile_id": f"{domain[:3].upper()}_{i:03d}",
                "domain": domain,
                "skills": skills_str,
                "interests": interests,
                "profile_text": profile_text,
                "skill_count": len(all_user_skills)
            })
            
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / "career_dataset.csv"
    df = generate_samples(samples_per_domain=100)
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples across {df['domain'].nunique()} domains. Saved to {out_path}")
