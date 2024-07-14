import os
from PyPDF2 import PdfReader
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
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
# Open a file object in write mode
with open("data/Introduction_to_algorithms.json", "w") as f:
    # Save the dictionary variable to the file
    json.dump(text, f)

# Initialize the OpenAI API client
os.environ["OPENAI_API_KEY"] = ""

def construct_index(directory_path='data/'):
    max_input_size = 4096
    num_outputs = 1028
    max_chunk_overlap = 20
    chunk_size_limit = 1000

    prompt_helper = PromptHelper(max_input_size,num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo-0613", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('LLM.json')

construct_index()


