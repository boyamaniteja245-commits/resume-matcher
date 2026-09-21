import json
import time
import streamlit as st
from pypdf import PdfReader
from google import genai
from google.genai import types

st.set_page_config(page_title="Smart Resume Matcher", page_icon="📄", layout="wide")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.6-flash"]

PROMPT = """You are an expert recruiter and career coach.
Compare the resume with the job description and respond ONLY with JSON in exactly this shape:
{
  "match_score": <integer 0-100>,
  "summary": "<2 sentence overall assessment>",
  "matching_skills": ["..."],
  "missing_skills": ["..."],
  "improvements": ["<specific, actionable suggestion>"],
  "rewrites": [
    {"original": "<a bullet from the resume>",
     "improved": "<rewritten to fit this job>"}
  ]
}
Give 3-5 improvements and 3 rewrites.
Never invent experience or skills the candidate does not have.
"""


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def analyze(resume, job):
    contents = PROMPT + "\n\nRESUME:\n" + resume + "\n\nJOB DESCRIPTION:\n" + job
    last_error = None
    # Try each model up to 3 times; the API sometimes returns 503 when busy.
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    ),
                )
                return json.loads(response.text)
            except Exception as e:
                last_error = e
                msg = str(e)
                busy = "503" in msg or "429" in msg or "UNAVAILABLE" in msg
                if not busy:
                    raise
                time.sleep(2 * (attempt + 1))
    raise last_error


st.title("📄 Smart Resume & Job Match")
st.caption("Upload your resume, paste a job description, and see how well you match.")

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Upload resume (PDF)", type="pdf")
    resume_text = st.text_area("...or paste your resume text", height=200)
with col2:
    job_text = st.text_area("Paste the job description", height=340)

if st.button("Analyze my match", type="primary"):
    resume = extract_text(uploaded) if uploaded else resume_text

    if not resume.strip() or not job_text.strip():
        st.error("Please provide both a resume and a job description.")
        st.stop()

    with st.spinner("Analyzing..."):
        try:
            result = analyze(resume, job_text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    score = int(result["match_score"])
    st.metric("Match score", f"{score}/100")
    st.progress(min(max(score, 0), 100) / 100)
    st.write(result["summary"])

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Matching skills")
        for s in result["matching_skills"]:
            st.write(f"- {s}")
    with right:
        st.subheader("⚠️ Missing skills")
        for s in result["missing_skills"]:
            st.write(f"- {s}")

    st.subheader("💡 Improvements")
    for tip in result["improvements"]:
        st.write(f"- {tip}")

    st.subheader("✍️ Before / After")
    for r in result["rewrites"]:
        b, a = st.columns(2)
        b.info("**Before**\n\n" + r["original"])
        a.success("**After**\n\n" + r["improved"])
