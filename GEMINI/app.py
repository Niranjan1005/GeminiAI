import streamlit as st
import google.generativeai as genai
import logging

import json

from loghandler import MaxLinesRotatingFileHandler

with open('api.json', 'r') as f:
  data = json.load(f)

# Configure the GenerativeAI API key
genai.configure(api_key=data['api'])

# Create a GenerativeModel instance
model = genai.GenerativeModel('gemini-pro')

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Set up logging
# Configure the logger with the custom handler
log_filename = 'logs/chat_log.txt'
max_lines = 1000
logging.basicConfig(handlers=[MaxLinesRotatingFileHandler(log_filename, max_lines=max_lines)],
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Streamlit app
def main():
    st.set_page_config(
        page_title="GEMINI",
        page_icon="🤖",
        layout="centered"
    )

    st.markdown("<h1 style='text-align: center;'>GEMINI AI</h1>", unsafe_allow_html=True)

    # Display all messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # Log messages to the file
            logging.info(f'{message["role"]}: {message["content"]}')

    try:
        user_prompt = st.chat_input()

        if user_prompt is not None:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)
                # Log user input to the file
                logging.info(f'user: {user_prompt}')

            # Generate content using the GenerativeModel
            response = model.generate_content(user_prompt)

            if response and hasattr(response, 'text'):
                # Display the generated content above the input bar
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.write(response.text)
                    # Log assistant response to the file
                    logging.info(f'assistant: {response.text}')
            else:
                st.warning("Failed to generate content. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Log errors to the file
        logging.error(f'Error: {str(e)}')

if __name__ == "__main__":
    main()
