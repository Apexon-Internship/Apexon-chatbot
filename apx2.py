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

# Setup embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Setup ChromaDB vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"  # Local directory to save data, remove if not needed
)

# Streamlit App
def app():
    st.title('Apexon Query Answer Interface')
    
    # File uploader
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    if uploaded_file is not None:
        # Process the CSV file
        data = pd.read_csv(uploaded_file)
        
        # Create documents from CSV data
        documents = [
            Document(
                page_content=row['Chunk_Content'],
                metadata={'URL': row['URL'], 'Chunk_Index': row['Chunk_Index']},
                id=str(uuid4())
            ) for index, row in data.iterrows()
        ]
        
        # Add documents to the vector store
        vector_store.add_documents(documents=documents, ids=[doc.id for doc in documents])
        
        st.success("Documents added successfully!")

    user_query = st.text_area("Enter your query:", height=150)
    if st.button("Generate Answer"):
        if user_query:
            response = generate_response(user_query)
            st.text_area("Response:", response, height=300)

def generate_response(query):
    results = vector_store.similarity_search(query, k=5)  # Adjust 'k' as needed
    context = "\n\n".join([f"Content from {res.metadata['URL']}:\n{res.page_content}" for res in results])
    
    # Set up query for GPT endpoint
    messages = [
        {"role": "system", "content": """You are a knowledgeable, articulate, and user-friendly assistant representing Apexon. Your primary goal is to generate crisp, accurate, and contextually relevant answers based on the user’s input, specifically related to our services, solutions, and expertise at Apexon. Be concise yet informative, provide step-by-step guidance when needed, and offer clarifications to avoid misunderstandings. Maintain a professional and approachable tone that reflects our brand identity. When using data from retrieved content, generate an organized and coherent response with clear sections, linking your answers to our capabilities, case studies, and service offerings whereever needed."""},
        {"role": "user", "content": query},
        {"role": "assistant", "content": context}
    ]
    
    # Call the GPT endpoint
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0]. message.content

if __name__ == "__main__":
    app()

