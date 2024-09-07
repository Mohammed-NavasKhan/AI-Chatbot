
import spacy
from transformers import pipeline
from pypdf import PdfReader

# Load spaCy's small model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Increase the maximum length
nlp.max_length = 1500000  # Increase as needed, depending on your text length

# Function to read text from a PDF file
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text().replace('\n', ' ').strip()  # Improve preprocessing
    return text

# Initialize the Hugging Face QA pipeline with a more efficient model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


# Load your PDF and extract text
print("Extracting text from PDF...")
pdf_text = extract_pdf_text("bitcoin.pdf")
print("Text extraction completed.")
print("Extracted Text:\n", pdf_text[:1000])  # Print the first 1000 characters

# Process the text with spaCy (for any pre-processing if needed)
print("Processing text with spaCy...")
doc = nlp(pdf_text)
print("Text processing completed.")

# Function to split text into smaller chunks
def split_text(text, max_length=512):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(nlp(sentence))
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Function to ask a question
def ask_question(question):
    chunks = split_text(pdf_text)
    best_answer = ""
    best_score = 0

    for chunk in chunks:
        result = qa_pipeline(question=question, context=chunk)
        if result['score'] > best_score:
            best_answer = result['answer']
            best_score = result['score']

    return best_answer

# Interactive loop to keep asking questions
print("Ask a question about the document (type 'exit' to quit):")
while True:
    question = input("Question: ")
    if question.lower() == 'exit':
        break
    answer = ask_question(question)
    print(f"Answer: {answer}")
