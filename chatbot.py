import streamlit as st
import random
import time
import requests
import json


def response_stream_emulator(r):
    response = r
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


token_access = "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"
headers = {"Authorization": f"Bearer {token_access}"}

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def query(payload):
    data = json.dumps(payload)

    time.sleep(1)

    while True:

      try:
        
        response = requests.request("POST", API_URL, headers=headers, data=data)
        break
      
      except Exception:

          continue
          
    return json.loads(response.content.decode("utf-8"))

st.title("summary chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("enter prompt"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        data = query(
            {
                "inputs": prompt,
                "parameters": {"do_sample": False},
            }
        )

        print(data)

        summary = ""
        
        if data and isinstance(data, list) and "summary_text" in data[0]:
            summary = data[0]["summary_text"]
            st.write_stream(response_stream_emulator(summary))
        else:
            st.write("No summary available.")
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": summary})
