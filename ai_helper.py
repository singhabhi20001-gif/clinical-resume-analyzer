from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # loads .env safely

def improve_resume(resume_text, missing_skills, role):
    client = OpenAI()

    skills_text = ", ".join(missing_skills) if missing_skills else "None"

    prompt = f"""
You are an expert clinical career advisor.

Target role: {role}

Missing skills to address:
{skills_text}

Original resume text:
{resume_text}

Rewrite the resume to:
- Better align with the target role
- Naturally include the missing skills where appropriate
- Keep it professional and ATS-friendly
- Do NOT invent fake experience
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content
