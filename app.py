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

# ---------------- HEADER ----------------
st.title("🧬 Clinical Resume Analyzer")
st.write(
    "Analyze your clinical resume, identify skill gaps, "
    "and generate an AI-enhanced version."
)

# ---------------- SESSION STATE ----------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "improved_text" not in st.session_state:
    st.session_state.improved_text = None

if "demo_unlocked" not in st.session_state:
    st.session_state.demo_unlocked = False

# ---------------- STEP 1: FILE UPLOAD ----------------
st.markdown("### Step 1️⃣: Upload Your Resume")
st.caption("PDF format only. Your file is not stored.")

uploaded_file = st.file_uploader(
    "📄 Upload resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
    st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
    st.success("Resume uploaded and parsed successfully.")

# ---------------- STEP 2: ROLE SELECTION ----------------
st.markdown("### Step 2️⃣: Choose Target Role")

role_map = {
    "Clinical Data Associate (CDA)": "cda",
    "Clinical Research Associate (CRA)": "cra",
    "SAS Programmer": "sas_programmer"
}

role_label = st.selectbox(
    "🎯 Select the role you are applying for",
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

    # ---------------- STEP 3: AI IMPROVEMENT (FAKE PAYWALL) ----------------
    st.markdown("---")
    st.markdown("### Step 3️⃣: AI Resume Improvement")

    if not st.session_state.demo_unlocked:
        _ = st.info(
            "💳 **AI Resume Improvement (Premium Feature)**\n\n"
            "Our AI enhances your resume for the selected clinical role by:\n"
            "• Highlighting relevant clinical skills\n"
            "• Improving clarity and structure\n"
            "• Making the resume more ATS-friendly\n"
            "• Naturally incorporating missing skills (without inventing experience)\n\n"
            "🚀 The paid version is launching soon.\n"
            "Join the waitlist to get early access and special launch pricing."
        )

        # 🔴 REPLACE THIS WITH YOUR REAL GOOGLE FORM LINK
        st.markdown(
            "[👉 Join the waitlist](https://docs.google.com/forms/d/e/1FAIpQLSeQCAtMVQo_nzBqFQRTIl_ev_7jlZ9ENrWuXL2Tm3tYAZL2Wg/viewform?usp=dialog)"
        )

        st.caption("🎁 Free demo available: Try AI improvement once.")

        if st.button("🎁 Try Free Demo"):
            st.session_state.demo_unlocked = True
            st.rerun()

    else:
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
        height=320
    )

    # ---------------- DOWNLOAD OPTIONS ----------------
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

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Built by Abhishek Singh • Streamlit • OpenAI • Clinical AI Project"
)
