from PyPDF2 import PdfReader
from dotenv import load_dotenv
import pickle
import os
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

# Set Streamlit page title and icon
st.set_page_config(page_title="ChatPDF LangChain HR App", page_icon="📋")

# Define a Streamlit sidebar
with st.sidebar:
    st.title('ChatPDF LangChain HR App')
    st.markdown(
        '''
        This app is an **LLM-powered chatbot** designed for HR professionals to evaluate candidate resumes. It uses:
        - [Streamlit](https://docs.streamlit.io/)
        - [LangChain](https://python.langchain.com/docs/get_started/introduction)
        - [OpenAI API](https://openai.com/blog/openai-api)
        '''
    )
    add_vertical_space(2)
    st.write('Created by [Pedro Alves](https://www.linkedin.com/in/pedro-a-d-s/)')

load_dotenv()

def main():
    st.title('HR Resume Evaluation')

    pdf = st.file_uploader('Upload a candidate\'s resume in PDF format', type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        store_name = pdf.name[:-4]

        if os.path.exists(f'../vector_store/{store_name}.pkl'):
            with open(f'../vector_store/{store_name}.pkl', 'rb') as f:
                VectorStore = pickle.load(f)
        else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f'{store_name}.pkl', 'wb') as f:
                pickle.dump(VectorStore, f)

        # Accept user query
        query = st.text_input('Ask questions about the candidate\'s qualifications (in English): ')

        if query:
            docs = VectorStore.similarity_search(query=query, k=3)
            
            llm = OpenAI(model_name='gpt-3.5-turbo')
            chain = load_qa_chain(llm=llm, chain_type='stuff')
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
            st.write('HR Evaluation:')
            st.write(response)

if __name__ == '__main__':
    main()