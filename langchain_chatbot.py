import spacy
from transformers import pipeline
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub  # or use OpenAI depending on your model

# Load spaCy's small model
nlp = spacy.load("en_core_web_sm")

# Increase the maximum length
nlp.max_length = 1500000  # Increase as needed, depending on your text length

# Function to read text from a PDF file
def extract_pdf_text(pdf_path):
    print("Extracting text from PDF...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print("Text extraction completed.")
    return text

# Initialize the Hugging Face QA pipeline with a small model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")

# Load your PDF and extract text
pdf_text = extract_pdf_text("annual.pdf")

# Process the text with spaCy (for any pre-processing if needed)
print("Processing text with spaCy...")
doc = nlp(pdf_text)
print("Text processing completed.")

# Define a LangChain Prompt Template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="Given the following context: {context}. Answer the question: {question}"
)

# Initialize the LangChain LLMChain
llm_chain = LLMChain(
    llm=HuggingFaceHub(model_name="distilbert-base-uncased"),  # Replace with your model
    prompt=prompt_template
)

# Function to ask a question using LangChain
def ask_question(question):
    response = llm_chain.run({"context": pdf_text, "question": question})
    return response

# Example interaction
while True:
    user_input = input("Ask a question about the document (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    answer = ask_question(user_input)
    print(f"Answer: {answer}")
