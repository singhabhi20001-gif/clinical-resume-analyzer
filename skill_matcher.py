import json
import os

def load_skills(role):
    """
    Load required skills for a given role from skills/*.json
    """
    base_dir = os.path.dirname(__file__)
    skills_path = os.path.join(base_dir, "skills", f"{role}.json")

    with open(skills_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["skills"]


def normalize(text):
    """
    Normalize text for comparison
    """
    return text.lower()


def find_skill_gaps(resume_text, role):
    """
    Compare resume text with required skills and calculate score
    """
    resume_text = normalize(resume_text)
    required_skills = load_skills(role)

    present = []
    missing = []

    for skill in required_skills:
        if normalize(skill) in resume_text:
            present.append(skill)
        else:
            missing.append(skill)

    if not required_skills:
        score = 0
    else:
        score = int((len(present) / len(required_skills)) * 100)

    return score, present, missing
