import streamlit as st
from utils import extract_text, rank_resumes

# Page settings
st.set_page_config(page_title="AI Resume Screening System", layout="centered")

# Title
st.title("📄 AI Resume Screening System")
st.write("Upload resumes and match them with job description using AI")

# Job Description Input
job_desc = st.text_area("📝 Enter Job Description")

# File Upload
uploaded_files = st.file_uploader(
    "📂 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# Button
if st.button("🔍 Analyze Resumes"):
    
    # Validation
    if not job_desc.strip():
        st.warning("⚠️ Please enter a job description")
    
    elif not uploaded_files:
        st.warning("⚠️ Please upload at least one resume")
    
    else:
        resumes = []
        file_names = []

        # Extract text from each file
        for file in uploaded_files:
            text = extract_text(file)
            resumes.append(text)
            file_names.append(file.name)

        # Rank resumes
        scores = rank_resumes(resumes, job_desc)

        # Combine results
        results = list(zip(file_names, scores))

        # Sort by score (highest first)
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # Display Results
        st.subheader("📊 Ranking Results")

        for i, (name, score) in enumerate(results):
            st.write(f"**{i+1}. {name}** → Score: `{score:.2f}`")

        st.success("✅ Analysis Complete!")
