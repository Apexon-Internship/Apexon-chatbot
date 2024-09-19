import streamlit as st
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

def app():
    st.title('Content Chunking Tool')

    # File uploader for user to upload their CSV
    uploaded_file = st.file_uploader("Upload your CSV containing URLs and Cleaned Text", type=['csv'])
    if uploaded_file is not None:
        # Step 1: Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Step 2: Extract URL and Content columns
        urls = df['URL']
        contents = df['Cleaned Text']

        # Step 3: Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        # Prepare data structure for chunks
        chunked_data = []

        # Step 4: Loop over each content, chunk it, and store the result
        for i, content in enumerate(contents):
            # Split the content into chunks
            chunks = text_splitter.create_documents([content])
            
            # Add each chunk and its corresponding URL to the chunked_data list
            for j, chunk in enumerate(chunks):
                chunked_data.append({
                    'URL': urls[i],
                    'Chunk_Index': j + 1,
                    'Chunk_Content': chunk.page_content
                })

        # Step 5: Create a DataFrame from the chunked_data list
        chunked_df = pd.DataFrame(chunked_data)

        # Step 6: Save the DataFrame to a CSV file
        output_file_path = 'urls_and_chunks.csv'  # specify where you want to save the output file
        chunked_df.to_csv(output_file_path, index=False)

        # Display success message
        st.success(f"Chunks created and stored in '{output_file_path}' successfully!")

if __name__ == "__main__":
    app()
