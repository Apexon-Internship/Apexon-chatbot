import streamlit as st
import pandas as pd
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from uuid import uuid4
import openai
import os

# Set API key
os.environ['OPENAI_API_KEY'] = ''  # Replace with your actual API key

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
    """Check if the user's request is relevant to Apexon's services."""
    guardrail_prompt = """
    You are an intelligent filter trained to identify if questions are relevant to Apexon's services and solutions in areas like healthcare, finance, and technology implementation. 
    For each example below, identify if the query is allowed or not:
    
    Query: "Tell me about Apexon's work in cloud solutions."
    Response: allowed
    
    Query: "What is the best dog breed for apartment living?"
    Response: not_allowed
    
    Based on the pattern above, determine if the following query is allowed or not:
    Query: "{}"
    """.format(user_request)
    messages = [
        {"role": "system", "content": guardrail_prompt},
        {"role": "user", "content": user_request},
    ]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip().lower() == 'allowed'


def get_chat_response(user_request):
    """ Generate a response for an allowed topic """
    system_prompt = """You are a knowledgeable, articulate, and user-friendly assistant representing Apexon. Your primary goal is to generate crisp, accurate, and contextually relevant answers based on the user’s input, specifically related to our services, solutions, and expertise at Apexon. Be concise yet informative, provide step-by-step guidance when needed, and offer clarifications to avoid misunderstandings. Maintain a professional and approachable tone that reflects our brand identity. When using data from retrieved content, generate an organized and coherent response with clear sections, linking your answers to our capabilities, case studies, and service offerings whereever needed."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request},
    ]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.5
    )
    return response.choices[0].message.content
def app():
    st.title('Apexon Query Answer Interface with Guardrails')
    user_query = st.text_area("Enter your query related to Apexon's services:", height=150)
    if st.button("Generate Answer"):
        if check_topic_allowed(user_query):
            response = get_chat_response(user_query)
            st.text_area("Response:", response, height=300)
        else:
            st.error("Please ensure your query is relevant to Apexon's services and solutions.")

if __name__ == "__main__":
    app()
