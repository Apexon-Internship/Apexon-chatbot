**Project Overview**
This project involves the development of a Generative AI-powered chatbot capable of answering questions related to information found on Apexon.com. The chatbot is designed to provide users with accurate and contextually relevant responses by utilizing state-of-the-art generative AI models. This project will culminate in a demonstration to Apexon leadership on September 15, 2024.

**Objectives**
1. **Chatbot Development**: Create a conversational AI agent using generative AI technologies, specifically designed to handle inquiries based on information from Apexon.com.
2. **Operational Readiness**: Ensure the chatbot is fully functional, thoroughly tested, and ready for a live demo by the deadline.
3. **Presentation**: Develop a comprehensive demo to showcase the chatbot's capabilities and be prepared to discuss the development process, challenges, and potential future improvements.

**Key Deliverables**

1. **Functional Chatbot**: A fully operational generative AI chatbot that accurately and efficiently answers questions related to Apexon.com.
2. **Documentation**: Detailed project documentation including setup instructions, architecture overview, and a user manual.
3. **Source Code**: Complete and well-documented source code repository.
4. **Demo Presentation**: A presentation highlighting the chatbot's features, capabilities, and the development journey.

**Features**
- **Azure OpenAI Integration**: Utilizes Azure OpenAI models for generating responses based on the scraped content from Apexon.com.
- **Chroma DB**: Employs Chroma DB to store and query contextually relevant information from the website.
- **Guardrails**: Implements guardrails to ensure the chatbot does not provide irrelevant or inappropriate responses.
- **Fallback Mechanism**: Adds a fallback system to handle queries that the chatbot cannot answer.
- **Streamlit Interface**: Provides a user-friendly interface for interaction via Streamlit.

**Demo Presentation**
- The demo will be presented to Apexon leadership on September 15, 2024.
- A slide deck and live demonstration will showcase the chatbot's functionalities.
- Be prepared to discuss the development process, including challenges, solutions, and potential future enhancements.

**Future Improvements**
- **Expanded Data Sources**: Incorporate additional data sources to enhance the chatbot's knowledge base.
- **Advanced NLP Features**: Implement more sophisticated natural language understanding and generation techniques.
- **Continuous Learning**: Enable the chatbot to learn from user interactions and improve over time.

**Contributing**
Contributions are welcome from the team! Please fork the repository and submit a pull request.
Installation Instructions
Follow these steps to set up the project environment and install all necessary dependencies:

**1. Clone the Repository**

```bash
git clone <repository-url>
cd <repository-directory>
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
**2. Install Dependencies Create a requirements.txt file in your project directory with the following contents:**
Install the required libraries using pip:
```
```bash

pip install -r requirements.txt
```
**3. Running the Applications**
The project consists of three main Streamlit applications:

**apx_ingestion.py**

Handles data ingestion from Apexon.com.
Command to run:

```bash
streamlit run apx_ingestion.py
```

**apx_chunking.py**

Processes and chunks data stored in CSV format.
Command to run:
```bash
streamlit run apx_chunking.py
```
**apx2.py**

Implements the chatbot interface that interacts with users.
Command to run:
```bash
streamlit run apx2.py
```
