import streamlit as st
from gpt_index import GPTSimpleVectorIndex
import os
import time

# Initialize the OpenAI API client
os.environ["OPENAI_API_KEY"] = ""

# Initialize the chat history in the session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a placeholder to display the response as it is being generated


# Display the chat messages from the history
for message in st.session_state.chat_history:
    message_placeholder = st.chat_message('User')
    response_placeholder = st.chat_message('Assistant')
    message_placeholder.markdown(message['User'])
    response_placeholder.markdown(message['Assistant'])
    

# Accept user input
user_input = st.chat_input(placeholder="Type a message...")

# If the user entered a prompt, add it to the chat history and display it immediately
if user_input:
    
    message_placeholder = st.chat_message('User')
    message_placeholder.markdown(user_input)

    # Shorten the user input if it is too long
    if len(user_input) > 2048:
        user_input = user_input[:2048]

    # Create a prompt that is clear and concise
    if len(st.session_state.chat_history) > 0 and len(st.session_state.chat_history) <3:
        prompt = f"""Based on this chat history between you and the user:
                    {st.session_state.chat_history}
                    As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""
    elif len(st.session_state.chat_history) == 0 :
        prompt = f"""As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""
    elif len(st.session_state.chat_history) >=3 :
        prompt = f"""Based on this chat history between you and the user:
                    {st.session_state.chat_history[-3]}
                    As an LLM that is fine-tuned on information about algorithms, assist: {user_input}"""

    response_placeholder = st.chat_message('Assistant')


    response_placeholder.markdown("Hello, How can I help you today!")
