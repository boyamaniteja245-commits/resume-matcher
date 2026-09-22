# AI Resume Matcher 🚀

An AI-powered Resume Matcher that analyzes a candidate's resume against a job description and provides an intelligent assessment of skill alignment, missing skills, and improvement suggestions.

🔗 **Live Demo:** https://resume-matc.streamlit.app/

---

## 📌 Overview

AI Resume Matcher is a web application built with **Python, Streamlit, and Google's Gemini API**.

The application allows users to upload their resume in PDF format and provide a job description. The AI analyzes both inputs and generates useful insights to help candidates understand how well their resume matches the requirements of a particular job.

The project is designed to make resume analysis faster, easier, and more accessible for students, freshers, and job seekers.

---

## ✨ Features

- 📄 Upload resume in PDF format
- 📝 Enter or paste a job description
- 🤖 AI-powered resume analysis using Google Gemini
- 🎯 Analyze alignment between resume and job requirements
- 🛠️ Identify relevant skills
- ⚠️ Highlight missing or insufficient skills
- 💡 Provide suggestions for improving the resume
- 🌐 Simple and interactive Streamlit interface
- 🔐 Secure API key management using Streamlit Secrets
- ⚡ Fast AI-powered analysis
- 📱 Accessible through a public web application

---

## 🧠 How It Works

The application follows a simple workflow:

```text
User
  │
  ▼
Upload Resume PDF
  │
  ▼
Enter Job Description
  │
  ▼
Extract Resume Text
  │
  ▼
Send Resume + Job Description
  │
  ▼
Google Gemini API
  │
  ▼
AI Analysis
  │
  ▼
Skills / Match Analysis / Suggestions
