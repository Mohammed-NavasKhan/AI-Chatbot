import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import HuggingFaceHub
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HUGGINGFACE_API_TOKEN = "hf_SkQojHETEBQqnseFmIXIwhEPvMlRICxo"

st.header("My first Chatbot")
with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader(
        "Upload a PDF file and start asking questions", type="pdf")

if file is not None:
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            st.warning("No text found in the uploaded PDF.")
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                separators="\n",
                chunk_size=1000,
                chunk_overlap=150,
                length_function=len
            )
            chunks = text_splitter.split_text(text)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            vector_store = FAISS.from_texts(chunks, embeddings)

            user_question = st.text_input("Type your question here")

            if user_question:
                if len(user_question.strip()) == 0:
                    st.warning("Please enter a question.")
                else:
                    match = vector_store.similarity_search(user_question)

                    if not match:
                        st.warning("No relevant information found.")
                    else:
                        llm = HuggingFaceHub(
                            repo_id="google/flan-t5-small",
                            model_kwargs={"temperature": 0.5,
                                          "max_length": 1000},
                            huggingfacehub_api_token=HUGGINGFACE_API_TOKEN
                        )
                        chain = load_qa_chain(llm, chain_type="stuff")
                        response = chain.run(
                            input_documents=match, question=user_question)
                        st.write(response)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        st.error(e)
