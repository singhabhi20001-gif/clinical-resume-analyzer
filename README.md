🧬 Clinical Resume Analyzer

An AI-powered web app that analyzes clinical resumes, identifies skill gaps for specific roles, and generates an improved, ATS-friendly resume.

🔗 Live Demo: (add your Streamlit app URL here)

🚀 Features

PDF resume upload

Role-based skill gap analysis (CDA, CRA, SAS Programmer)

Skill match score and missing skills

AI-powered resume improvement (demo unlock mode)

Download improved resume as PDF or DOCX

🛠 Tech Stack

Streamlit

Python

OpenAI API

PyPDF2

python-docx

reportlab

▶️ Run Locally
git clone https://github.com/singhabhi20001-gif/clinical-resume-analyzer.git
cd clinical-resume-analyzer
pip install -r requirements.txt
streamlit run app.py


Create a .env file for local testing:

OPENAI_API_KEY=your_api_key_here

🔐 Security

API keys are never hardcoded

.env is ignored via .gitignore

Production uses Streamlit Cloud Secrets

👨‍💻 Author

Abhishek Singh

⭐ Feel free to star the repo if you find it useful
