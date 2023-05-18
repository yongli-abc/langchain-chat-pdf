from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIGPTEmbeddings
from langchain.vectorstores import FAISS

def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 📚")

    pdf = st.file_uploader("Upload your PDF", type=["pdf"])

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIGPTEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

if __name__ == '__main__':
    main()