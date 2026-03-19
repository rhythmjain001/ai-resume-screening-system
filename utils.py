import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download stopwords (only runs first time)
nltk.download('stopwords')

# 📥 Extract text from PDF
def extract_text(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
            
    return text


# 🧹 Preprocess text (cleaning)
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)  # remove symbols/numbers
    
    words = text.split()
    stop_words = set(stopwords.words('english'))
    
    words = [word for word in words if word not in stop_words]
    
    return " ".join(words)


# 📊 Rank resumes based on similarity
def rank_resumes(resumes, job_desc):
    
    # Clean resumes and job description
    processed_resumes = [preprocess(resume) for resume in resumes]
    processed_job_desc = preprocess(job_desc)

    # Combine all text
    documents = processed_resumes + [processed_job_desc]

    # Convert text → vectors (TF-IDF)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    # Calculate similarity
    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1])

    return similarity_scores[0]
