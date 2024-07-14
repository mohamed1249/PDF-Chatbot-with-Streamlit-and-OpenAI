# PDF Chatbot with Streamlit and OpenAI

This project demonstrates building a Streamlit application that interacts with a custom PDF using OpenAI's embedding and Pinecone for vector indexing. The app allows users to chat with the content of a PDF, providing a unique and interactive way to query and understand documents.

## Key Features

- **PDF Extraction**: Extracts text content from each page of the PDF.
- **Vector Index Construction**: Uses OpenAI's embeddings to construct a vector index for efficient querying.
- **Streamlit Interface**: Provides an interactive chat interface to ask questions and receive responses based on the PDF content.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mohamed1249/PDF-Chatbot-with-Streamlit-and-OpenAI/
    cd pdf-chatbot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up OpenAI API key**:
    - Obtain your API key from OpenAI.
    - Set the `OPENAI_API_KEY` environment variable:
        ```bash
        export OPENAI_API_KEY='your-openai-api-key'
        ```

## Usage

1. **Extract PDF Pages**:
    ```python
    import os
    from PyPDF2 import PdfReader
    import json

    def extract_pdf_pages(pdf_file_path):
        pdf_pages = {}
        with open(pdf_file_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page_number in range(len(reader.pages)):
                pdf_pages[page_number] = {
                    "page_number": page_number + 1,
                    'page_information': reader.pages[page_number].extract_text(),
                    'book_name': os.path.basename(pdf_file_path)
                }
        return pdf_pages

    text = extract_pdf_pages('Introduction_to_algorithms-3rd Edition.pdf')

    with open("data/Introduction_to_algorithms.json", "w") as f:
        json.dump(text, f)
    ```

2. **Construct Vector Index**:
    ```python
    import os
    from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
    from langchain.chat_models import ChatOpenAI

    def construct_index(directory_path='data/'):
        max_input_size = 4096
        num_outputs = 1028
        max_chunk_overlap = 20
        chunk_size_limit = 1000

        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo-0613", max_tokens=num_outputs))
        documents = SimpleDirectoryReader(directory_path).load_data()
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index.save_to_disk('LLM.json')

    construct_index()
    ```

3. **Run Streamlit App**:
    ```python
    import streamlit as st
    from gpt_index import GPTSimpleVectorIndex
    import os

    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        message_placeholder = st.chat_message('User')
        response_placeholder = st.chat_message('Assistant')
        message_placeholder.markdown(message['User'])
        response_placeholder.markdown(message['Assistant'])

    user_input = st.chat_input(placeholder="Type a message...")

    if user_input:
        message_placeholder = st.chat_message('User')
        message_placeholder.markdown(user_input)

        if len(user_input) > 2048:
            user_input = user_input[:2048]

        if len(st.session_state.chat_history) > 0 and len(st.session_state.chat_history) < 3:
            prompt = f"""Based on this chat history between you and the user:
                        {st.session_state.chat_history}
                        As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""
        elif len(st.session_state.chat_history) == 0:
            prompt = f"""As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""
        elif len(st.session_state.chat_history) >= 3:
            prompt = f"""Based on this chat history between you and the user:
                        {st.session_state.chat_history[-3]}
                        As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""

        response_placeholder = st.chat_message('Assistant')
        response_placeholder.markdown("Hello, How can I help you today!")
    ```

## Benefits

- **Interactive Document Exploration**: Chat with the content of any PDF to quickly find the information you need.
- **Efficient Querying**: Leveraging vector embeddings and Pinecone for fast and accurate responses.
- **User-Friendly Interface**: Streamlit provides a simple and intuitive chat interface for users.

## Future Work

- **Enhanced Prompting**: Improve the prompts for more precise and relevant responses.
- **Additional Functionalities**: Explore adding features like sentiment analysis and information extraction.
- **Real-World Integration**: Integrate the application into larger systems for practical document processing needs.

## Target Audience

- **Data Scientists**: Interested in utilizing OpenAI and Streamlit for document analysis.
- **Developers**: Looking to implement interactive AI-driven applications.
- **AI Enthusiasts**: Anyone keen on exploring the potential of AI for document understanding.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to discuss any changes or improvements.
