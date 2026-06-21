# AI Resume Analyzer 📝

An intelligent web-based tool that helps job seekers evaluate and enhance their resumes by comparing them against a specific job description. Built entirely in a single Python file.

🔗 **Live Demo:** [Try it here](https://ai-resume-analyzer-cdmx5uygtmxg9oguzrg9g3.streamlit.app/) 

---

## 🔍 What Does It Do?

- Extracts text from your resume (PDF)
- Takes a job description as input
- Calculates an **ATS Similarity Score** using Sentence Transformers (`all-mpnet-base-v2`)
- Generates a **detailed AI evaluation report** using Groq's LLM (`llama-3.3-70b-versatile`) with scores, emojis, and a structured table
- Gives **actionable suggestions** to improve your resume for that specific role
- Lets you **download the full report** as a `.txt` file

---

## 🎯 Why Use This?

- Understand how your resume performs in ATS screenings
- Get professional-quality feedback instantly
- Tailor your resume to specific job roles with data-driven insights

---

## 🛠️ Built With

| Tool | Purpose |
|------|---------|
| Streamlit | Web Interface |
| pdfminer.six | PDF Text Extraction |
| Sentence Transformers | ATS Similarity Score |
| Groq API + LLaMA | AI Report Generation |
| Python dotenv | API Key Management |

---

## 💡 What Could Be Added

- Support for **DOCX resume uploads** in addition to PDF
- Option to **choose between multiple LLM models** from the UI itself
- A **resume scoring history** so users can track improvements over time
- **Side-by-side comparison** of multiple resumes against the same job description
- **Cover letter generator** based on the resume and job description
- **LinkedIn job description scraper** so users just paste a job URL instead of the full text
- A more **visual dashboard** with charts showing skill gaps and match percentages
- **Multi-language support** for resumes and job descriptions
