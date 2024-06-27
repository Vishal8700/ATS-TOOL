import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text  # Correct attribute to access the generated text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)  # Use PdfReader from PyPDF2
    text = ""
    for page in reader.pages:  # Iterate over pages directly
        text += page.extract_text()
    return text

# Prompt for the AI model

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

Resume:
{text}
"""
input_prompt2 = """
You are a highly experienced ATS (Applicant Tracking System) with a deep understanding of various technical fields including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the given resume based on the provided job description. 

Consider that the job market is highly competitive, and provide the best guidance for improving the resume. Your evaluation should include:

1. **JD Match Percentage:** Provide the percentage match between the resume and the job description.
2. **Missing Keywords:** List any critical keywords missing from the resume that are relevant to the job description.
3. **Profile Summary:** Write a detailed summary of the resume's strengths and weaknesses, especially in relation to the job description.

Format the response as follows:

---
**JD Match Percentage:**
**<JD Match Percentage>**

---

**Missing Keywords:**
- <Keyword 1>
- <Keyword 2>
- ...

---

**Profile Summary:**
<Profile Summary>

---

resume: {text}
description: {jd}

Provide your response in the exact format specified above.
"""

# Streamlit UI setup
st.markdown("<h1 style='text-align: center; color: #9b53fb;'>Smart ATS 🤖</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #9b53fb;margin-bottom: 30px ;'>Improve Your Resume for ATS 📄</h3>", unsafe_allow_html=True)

st.markdown("### Job Description 📝")
jd = st.text_area("Paste the Job Description", height=200)

st.markdown("### Upload Your Resume 📁")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"], help="Please Upload Your Resume")

# submit = st.button("Submit")

# if submit:
#     if uploaded_file is not None:
#         text = input_pdf_text(uploaded_file)
#         response = get_gemini_response(input_prompt.format(text=text, jd=jd))
#         st.markdown("<h2>AI Response:</h2>", unsafe_allow_html=True)
#         st.markdown(response)
#     else:
#         st.error("Please upload your resume.")
col1,col2 = st.columns(2)

with col1:
    submit1 = st.button("Review Resume")

with col2:
    submit2 = st.button("Match Percentage")

if submit1:
    if uploaded_file is not None:
        try:
            pdf_text = input_pdf_text(uploaded_file)
            prompt_text = input_prompt1.format(text=pdf_text)  # Format the prompt with the resume text
            response = get_gemini_response(prompt_text)
            st.markdown("<h2>AI Response:</h2>", unsafe_allow_html=True)
            st.markdown(response)

        except FileNotFoundError:
            st.warning("Please upload the resume")
        except RuntimeError as e:
            st.error(str(e))

elif submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt2.format(text=text, jd=jd))
        st.markdown("<h2>AI Response:</h2>", unsafe_allow_html=True)
        st.markdown(response)
    else:
        st.error("Please upload your resume.")

# Custom CSS for styling
st.markdown("""
<style>
    .stButton button {
        background-color: #6005d9;
        color: white;
        margin-top: 30px:
        font-size: 16px;
        
        border: none;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #6005d9;
    }
    .stTextArea textarea {
        font-size: 14px;
        padding: 10px;
    }
    .stTextArea textarea:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 5px #4CAF50;
    }
    .stFileUploader div {
        font-size: 16px;
    }
    @media only screen and (max-width: 600px) {
        .stButton button {
            font-size: 14px; /* Adjust button font size */
        }
        .stTextArea textarea {
            font-size: 12px; /* Adjust text area font size */
        }
    }
    
</style>
""", unsafe_allow_html=True)

# Adding a footer
st.markdown("<h6 style='text-align: center; color: #f2fffc;margin-top: 40px'>Develope with 💖 By git.alien</h6>", unsafe_allow_html=True)
