import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Function to extract text from PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = " ".join([page.get_text() for page in doc])
    if not text.strip():
        text = "No valid text extracted."
    return text


# Text cleaning to improve similarity match
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)   # Remove special characters
    text = re.sub(r'\s+', ' ', text)           # Normalize whitespace
    return text.strip()


# Main function to rank resume
def rank_resume(resume_path):
    resume_text = extract_text_from_pdf(resume_path)
    with open('job_description.txt', 'r', encoding='utf-8') as f:
        jd_text = f.read()

    # Clean both texts before comparison
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    # Debug prints for verification
    print("Resume Text:\n", resume_text[:500])
    print("\nJD Text:\n", jd_text[:500])

    if not resume_text or not jd_text:
        return 0.0  # Avoid crashing if text is empty

    docs = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(docs)
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)
