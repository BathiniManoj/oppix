import PyPDF2
import spacy
from spacy.matcher import PhraseMatcher
import re

# Load NLP model once
nlp = spacy.load("en_core_web_sm")


# ---------- SKILL DATABASE ----------
SKILL_DATABASE = [
    # Programming
    "python", "java", "c++", "javascript", "typescript",
    
    # Frameworks
    "django", "flask", "react", "angular", "node.js",
    
    # Data
    "machine learning", "deep learning", "data science",
    "artificial intelligence", "nlp", "computer vision",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb",
    
    # Tools
    "git", "docker", "kubernetes", "aws", "azure",
    
    # Others
    "pandas", "numpy", "tensorflow", "pytorch"
]


# ---------- PDF TEXT EXTRACTION ----------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "

    return text.lower()


# ---------- ADVANCED SKILL EXTRACTION ----------
def extract_skills(text):

    doc = nlp(text)

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    patterns = [nlp(skill) for skill in SKILL_DATABASE]
    matcher.add("SKILLS", patterns)

    matches = matcher(doc)

    extracted_skills = set()

    for match_id, start, end in matches:
        skill = doc[start:end].text.lower().strip()
        extracted_skills.add(skill)

    return list(extracted_skills)

# 
ROLE_KEYWORDS = {
    "software": [
        "python", "django", "rest api", "sql",
        "git", "backend", "oop", "unit testing"
    ],
    "frontend": [
        "html", "css", "javascript", "react",
        "responsive", "ui", "frontend"
    ],
    "data": [
        "sql", "excel", "python", "data analysis",
        "power bi", "tableau"
    ]
}

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def ats_score(resume_text, role):
    keywords = ROLE_KEYWORDS.get(role, [])
    text = normalize(resume_text)

    matched = [k for k in keywords if k in text]
    score = int((len(matched) / len(keywords)) * 100) if keywords else 0

    return score, matched, keywords