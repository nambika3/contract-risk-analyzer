import os
import requests
import docx
import PyPDF2
import re
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv

# ----------------------------
#       Load API key
# ----------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
#         Headers
# ----------------------------
headers = {
    "Authorization" : f"Bearer {api_key}",
    "HTTP-Referer" : "http://localhost",
    "X-Title": "Contract Risk Analyzer"
}

url = "https://openrouter.ai/api/v1/chat/completions"

# ----------------------------
#         PDF Reader
# ----------------------------
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file :
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# ----------------------------
#        DOCX Reader
# ----------------------------
def read_docx(file_path):
    doc = docx.Document(file_path)
    text = "" 
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# ---------------------------------
# Split long contracts into chunks
# ---------------------------------
def split_text(text, max_chars=3000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks

# ----------------------------
# Function to redact basic PII
# ----------------------------
def anonymize_contract_text(text):
    """Basic PII redaction with regex"""
    text = re.sub(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b', '[REDACTED NAME]', text)  # Names
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[REDACTED EMAIL]', text)          # Emails
    text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}\d', '[REDACTED PHONE]', text)             # Phones
    text = re.sub(r'https?://[^\s]+', '[REDACTED URL]', text)                      # URLs
    text = re.sub(r'\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln)\b', '[REDACTED ADDRESS]', text)  # Addresses
    return text

# ----------------------------
#      Prompt Template
# ----------------------------
def build_prompt(text_chunk):
    return f"""
You are a legal risk analysis assistant.

Analyze the following contract section and provide structured insights under the following categories:

1. **Legal Risk** - clauses that may cause ambiguity, loopholes, or legal exposure.
2. **Security Risk** - anything that may expose systems, infrastructure, or digital assets.
3. **Privacy/Data Risk** - personal data handling, consent, sharing, or potential leaks.
4. **Safety Risk** - anything that could cause physical or organizational harm.
5. **Liability Risk** - limitations of liability, indemnity clauses, and their implications.
6. **Unfair Terms** - unusually one-sided clauses that favor one party disproportionately.
7. **Missing Protections** - lack of dispute resolution, termination conditions, or safeguards.

Be concise but thorough. Bullet points are preferred. Analyze the following:

{text_chunk}
"""

# ----------------------------
#        Streamlit UI
# ----------------------------
st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")
st.title("Contract Risk Analyzer")
st.markdown("---")
st.caption("Upload a PDF or Word document to identify Legal, Privacy, Security, and other risks.")

# ----------------------------
#       Privacy notice
# ----------------------------
with st.expander("Privacy Notice"):
    st.markdown("""
By uploading a document, you agree that its contents may be analyzed using **external AI APIs (OpenRouter + Anthropic Claude)**.  
No documents are saved to disk, and only the extracted text is sent for processing.

Please **do not upload contracts containing sensitive personal data, passwords, or trade secrets**.

You must **explicitly give consent** before analysis will proceed.
""")
    
user_consent = st.checkbox("I consent to sending this document to a third-party AI service (OpenRouter.ai + Claude)", value=False)
uploaded_file = st.file_uploader("Upload a contract file (.pdf or .docx)", type=["pdf", "docx"])

# ----------------------------
#       Upload File
# ----------------------------
if uploaded_file:
    if not user_consent:
        st.warning("You must provide consent before processing can begin.")
        st.stop()

    st.success(f"File `{uploaded_file.name}` uploaded successfully!")

    # ----------------------------
    #      Read content
    # ----------------------------
    if uploaded_file.name.endswith(".pdf"):
        contract_text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        contract_text = read_docx(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    
    # -------------------------------
    # Clear uploaded file from memory
    # -------------------------------
    del uploaded_file

    chunks = split_text(contract_text)
    st.info(f"Contract split into {len(chunks)} section(s) for analysis.")

    for i, chunk in enumerate(chunks):
        st.markdown(f"---\n### Section {i+1}")
        with st.spinner("Analyzing..."):
            prompt = build_prompt(chunk)

            payload = {
                "model": "anthropic/claude-3-haiku",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.markdown(result)
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error during request: {e}")