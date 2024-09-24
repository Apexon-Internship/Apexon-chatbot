import streamlit as st
import pandas as pd
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from uuid import uuid4
import openai

# Set the API key from Streamlit's secrets or directly for testing
openai.api_key = 'sk-None-dvpc3JgnrJeJTsYUkTs9T3BlbkFJaLbQpougGlLcVMLDtRrI'  # Replace with your actual API key when deploying securely

# Load CSV data
data = pd.read_csv('urls_and_chunks.csv')

# Setup embedding model and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"
)

# Create documents and add to the vector store
documents = [
    Document(
        page_content=row['Chunk_Content'],
        metadata={'URL': row['URL'], 'Chunk_Index': row['Chunk_Index']},
        id=str(uuid4())
    ) for index, row in data.iterrows()
]
vector_store.add_documents(documents=documents, ids=[doc.id for doc in documents])
def check_topic_allowed(user_request):
    
    guardrail_prompt = "Determine if the query is relevant to Apexon's services and solutions. Respond 'allowed' or 'not_allowed'."
    messages = [
        {"role": "system", "content": guardrail_prompt},
        {"role": "user", "content": user_request},
    ]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content == 'allowed'

def get_chat_response(user_request):
    """ Generate a response for an allowed topic """
    system_prompt = "You are a knowledgeable, articulate, and user-friendly assistant representing Apexon. Provide information on our services and solutions."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message.content
def app():
    st.title('Apexon Query Answer Interface')
    user_query = st.text_area("Enter your query related to Apexon's services:", height=150)
    if st.button("Generate Answer"):
        if check_topic_allowed(user_query):
            response = get_chat_response(user_query)
            st.text_area("Response:", response, height=300)
        else:
            st.error("Please ensure your query is relevant to Apexon's services and solutions.")

if __name__ == "__main__":
    app()
