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
        text += page.extract_text()
    return text

# Initialize the Hugging Face QA pipeline with a small model
#qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Load your PDF and extract text
print("Extracting text from exPDF...")
pdf_text = extract_pdf_text("annual.pdf")
print("Text extraction completed.")
print("Extracted Text:\n", pdf_text[:1000])  # Print the first 1000 characters

# Process the text with spaCy (for any pre-processing if needed)
print("Processing text with spaCy...")
doc = nlp(pdf_text)
print("Text processing completed.")

# Function to ask a question
def ask_question(question):
    result = qa_pipeline(question=question, context=pdf_text)
    return result['answer']

# Interactive loop to keep asking questions
print("Ask a question about the document (type 'exit' to quit):")
while True:
    question = input("Question: ")
    if question.lower() == 'exit':
        break
    answer = ask_question(question)
    print(f"Answer: {answer}")
