import streamlit as st

from resume_parser import extract_text_from_pdf
from skill_matcher import find_skill_gaps
from ai_helper import improve_resume
from docx_helper import generate_docx
from pdf_helper import generate_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Clinical Resume Analyzer",
    layout="centered"
)

st.title("🧬 Clinical Resume Analyzer")
st.write("Upload your resume, analyze skill gaps, and improve it using AI.")

# ---------------- SESSION STATE ----------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "improved_text" not in st.session_state:
    st.session_state.improved_text = None

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📄 Upload your resume (PDF only)",
    type=["pdf"]
)

if uploaded_file:
    st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
    st.success("Resume uploaded and parsed successfully.")

# ---------------- ROLE SELECTION ----------------
role_map = {
    "Clinical Data Associate (CDA)": "cda",
    "Clinical Research Associate (CRA)": "cra",
    "SAS Programmer": "sas_programmer"
}

role_label = st.selectbox(
    "🎯 Select target role",
    options=list(role_map.keys())
)

# ---------------- SKILL ANALYSIS ----------------
if st.session_state.resume_text:
    role_key = role_map[role_label]

    score, present, missing = find_skill_gaps(
        st.session_state.resume_text,
        role_key
    )

    st.subheader("📊 Skill Match Score")
    st.progress(score / 100)
    st.write(f"**Match Score:** {score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Skills Found")
        if present:
            for skill in present:
                st.write("•", skill)
        else:
            st.write("No matching skills found.")

    with col2:
        st.markdown("### ❌ Skills Missing")
        if missing:
            for skill in missing:
                st.write("•", skill)
        else:
            st.success("No missing skills detected!")

    # ---------------- AI IMPROVEMENT ----------------
    st.markdown("---")
    st.subheader("🤖 AI Resume Improvement")

    if st.button("✨ Generate Improved Resume"):
        with st.spinner("Improving resume using AI..."):
            st.session_state.improved_text = improve_resume(
                resume_text=st.session_state.resume_text,
                missing_skills=missing,
                role=role_label
            )
        st.success("AI-generated resume ready!")

# ---------------- OUTPUT SECTION ----------------
if st.session_state.improved_text:
    st.markdown("---")
    st.subheader("📝 Improved Resume Preview")

    st.text_area(
        label="",
        value=st.session_state.improved_text,
        height=300
    )

    # ---------------- DOWNLOADS ----------------
    st.markdown("### ⬇️ Download Options")

    docx_file = generate_docx(st.session_state.improved_text)
    pdf_file = generate_pdf(st.session_state.improved_text)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download as DOCX",
            data=docx_file,
            file_name="improved_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_file,
            file_name="improved_resume.pdf",
            mime="application/pdf"
        )
