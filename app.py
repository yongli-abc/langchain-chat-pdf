import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

def main():
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 📚")

    openai_api_key = st.text_input("Enter your OpenAI API Key:")
    cost_placeholder = st.empty()  # Create a placeholder for the cost display.

    if 'total_cost' not in st.session_state:
        st.session_state.total_cost = 0

    cost_placeholder.text(f"Total Cost for this session (USD): {st.session_state.total_cost:.2f}")

    if openai_api_key:
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
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            knowledge_base = FAISS.from_texts(chunks, embeddings)

            # show user inpout
            user_question = st.text_input("Ask your question about your PDF:")
            if user_question:
                docs = knowledge_base.similarity_search(user_question)
                llm = OpenAI(openai_api_key=openai_api_key)
                chain = load_qa_chain(llm, chain_type="stuff")

                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=user_question)
                    st.session_state.total_cost += cb.total_cost

                st.write(response)

    # Update the cost display.
    cost_placeholder.text(f"Total Cost for this session (USD): {st.session_state.total_cost:.2f}")

if __name__ == '__main__':
    main()