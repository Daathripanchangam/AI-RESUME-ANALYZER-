import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- FUNCTIONS ---------- #

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def analyze_resume(job_desc, resume_text):
    prompt = f"""
    You are an ATS (Applicant Tracking System).

    Compare the resume with the job description.

    Job Description:
    {job_desc}

    Resume:
    {resume_text}

    Give output in this format:

    ATS Score: (out of 100)

    Matching Skills:
    - ...

    Missing Keywords:
    - ...

    Suggestions to Improve:
    - ...

    Selection Chance:
    (percentage)

    Keep it clear and structured.
    """

    response = model.generate_content(prompt)
    return response.text

# ---------- UI ---------- #

st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume using AI and improve your chances of selection.")

# Job Description Input
job_desc = st.text_area("📌 Enter Job Description")

# File Upload
uploaded_file = st.file_uploader("📤 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Analyze Button
if st.button("Analyze Resume"):
    if job_desc and uploaded_file:

        # Extract text
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        with st.spinner("Analyzing..."):
            result = analyze_resume(job_desc, resume_text)

        st.success("Analysis Complete!")
        st.write(result)

    else:
        st.warning("Please provide both Job Description and Resume.")