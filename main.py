import streamlit as st                            # For Web Interface (Front-End)
from pdfminer.high_level import extract_text      # To Extract Text from Resume PDF
from sentence_transformers import SentenceTransformer      # To generate Embeddings of text
from sklearn.metrics.pairwise import cosine_similarity     # To get Similarity Score of Resume and Job Description
from groq import Groq                             # API to use LLM's
import re                                         # To perform Regular Expression Functions
from dotenv import load_dotenv                    # Loading API Key from .env file
import os

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📝", layout="wide")

# Load environment variables from .env
load_dotenv()

# Fetch the key from the environment
api_key = os.getenv("GROQ_API_KEY")


#  Session States to store values 
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "resume" not in st.session_state:
    st.session_state.resume=""

if "job_desc" not in st.session_state:
    st.session_state.job_desc=""



# Title of the Project, change according to your style
st.title("AI Resume Analyzer 📝")
st.markdown("##### *Analyze your resume against any job description using AI*")
st.divider()



# <------- Defining Functions ------->

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        extracted_text = extract_text(uploaded_file)
        return extracted_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return "Could not extract text from the PDF file."


# Function to calculate similarity 
def calculate_similarity_bert(text1, text2):
    ats_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')      # Use BERT or SBERT or any model you want
    # Encode the texts directly to embeddings
    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])
    
    # Calculate cosine similarity without adding an extra list layer
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity


def get_report(resume,job_desc):
    client = Groq(api_key=api_key)

    # Change the prompt to get the results in your style
    prompt=f"""
    # Role:
    You are a professional Resume Analyst and Career Coach with expertise in HR, recruitment, and ATS systems.

    # Task:
    Analyze the candidate's resume against the provided job description and generate a professional, structured evaluation report.

    # Instructions:
    1. Identify all key requirements from the job description (skills, experience, qualifications, certifications, soft skills, etc.)
    2. For each requirement, evaluate how well the resume meets it.
    3. Assign a score out of 5 for each point.
    4. Use the following emoji indicators:
       - ✅ Resume clearly meets this requirement
       - ❌ Resume does not meet this requirement
       - ⚠️ Partially meets or unclear

    # Report Structure (follow this EXACTLY):

    ## 📋 Candidate Overview
    Provide a 2-3 line summary of the candidate's profile based on their resume.

    ## 🎯 Job Role Summary
    Provide a 2-3 line summary of what the job requires.

    ## 📊 Evaluation Table
    Present a markdown table with these exact columns:
    | # | Requirement | Score | Status | Remarks |
    |---|-------------|-------|--------|---------|
    Fill in each row with a specific job requirement, score (e.g. 4/5), emoji status, and a brief remark.

    ## 🔍 Detailed Analysis
    For each requirement from the table, write a detailed paragraph explaining the score and reasoning.
    Format: **Requirement Name (Score/5) [emoji]** — Explanation...

    ## 📈 Score Summary
    - List total score as: X / Y (where Y = number of requirements x 5)
    - Show percentage match
    - Give an overall fit rating: Excellent / Good / Average / Poor

    ## 💡 Suggestions to Improve Your Resume:
    Give 5-7 specific, actionable bullet points on what the candidate should add, change, or improve in their resume to better fit this role.

    # Inputs:
    Candidate Resume: {resume}
    ---
    Job Description: {job_desc}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional resume analyst. Respond only with the final report. Do not show your thinking or reasoning process."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def extract_scores(text):
    # Regular expression pattern to find scores in the format x/5, where x can be an integer or a float
    pattern = r'(\d+(?:\.\d+)?)/5'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    # Convert matches to floats
    scores = [float(match) for match in matches]
    return scores




# <--------- Starting the Work Flow ---------> 

# Displays Form only if the form is not submitted
if not st.session_state.form_submitted:
    with st.form("my_form"):

        # Taking input a Resume (PDF) file 
        resume_file = st.file_uploader(label="Upload your Resume/CV in PDF format", type="pdf")

        # Taking input Job Description
        st.session_state.job_desc = st.text_area("Enter the Job Description of the role you are applying for:",placeholder="Job Description...")

        # Form Submission Button
        submitted = st.form_submit_button("Analyze")
        if submitted:

            #  Allow only if Both Resume and Job Description are Submitted
            if st.session_state.job_desc and resume_file:
                st.info("Extracting Information")

                st.session_state.resume = extract_pdf_text(resume_file)      # Calling the function to extract text from Resume

                st.session_state.form_submitted = True
                st.rerun()                 # Refresh the page to close the form and give results

            # Donot allow if not uploaded
            else:
                st.warning("Please Upload both Resume and Job Description to analyze")


if st.session_state.form_submitted:
    score_place = st.info("Generating Scores...")

    # Call the function to get ATS Score
    ats_score = calculate_similarity_bert(st.session_state.resume,st.session_state.job_desc)

    col1,col2 = st.columns(2,border=True)
    with col1:
        st.write("Few ATS uses this score to shortlist candidates, Similarity Score:")
        st.subheader(str(ats_score))

    # Call the function to get the Analysis Report from LLM (Groq)
    report = get_report(st.session_state.resume,st.session_state.job_desc)

    # Calculate the Average Score from the LLM Report
    report_scores = extract_scores(report)                 # Example : [3/5, 4/5, 5/5,...]
    avg_score = sum(report_scores) / (5*len(report_scores))
    avg_percent = round(avg_score * 100, 2)  # Example: 2.4

    if avg_percent >= 80:
        fit = "🟢 Excellent Fit"
    elif avg_percent >= 60:
        fit = "🟡 Good Fit"
    elif avg_percent >= 40:
        fit = "🟠 Average Fit"
    else:
        fit = "🔴 Needs Improvement"

    with col2:
        st.write("Total Average score according to our AI report:")
        st.subheader(f"{avg_percent}%")
        st.write(fit)
    score_place.success("Scores generated successfully!")


    st.subheader("AI Generated Analysis Report:")

    # Displaying Report 
    st.markdown(f"""
            <div style='text-align: left; background-color: transparent; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                {report}
            </div>
            """, unsafe_allow_html=True)
    
    # Download Button
    st.download_button(
        label="Download Report",
        data=report,
        file_name="report.txt",
        icon=":material/download:",
        )
    

# <-------------- End of the Work Flow --------------->