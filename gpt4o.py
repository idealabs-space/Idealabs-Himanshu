import streamlit as st
import requests
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

def query_azure_openai(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        url = f"{AZURE_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No response')
    except Exception as e:
        st.error(f"Error: {str(e)}\nURL: {url}")
        return None

st.title("Azure OpenAI Chat")
user_input = st.text_area("Enter your query:")

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: red;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 4px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: white;
        color: red;
        border: 2px solid red;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if st.button("Submit"):
    if user_input:
        response = query_azure_openai(user_input)
        if response:
            st.write("Response:", response)