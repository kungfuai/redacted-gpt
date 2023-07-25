import os
import openai
import streamlit as st
from dotenv import load_dotenv
from masked_ai.masker import Masker

load_dotenv()
st.title("Redacted ChatGPT")
# checkbox
show_redaction = st.checkbox("Show redaction process", value=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

redacted_messages = []

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # chat completion
    masker = Masker(prompt)
    # print(masker)
    # raise Exception("stop")
    redacted_messages.append({"role": "user", "content": masker.masked_data})
    if show_redaction:
        with st.chat_message("redacted"):
            st.markdown(masker.masked_data)
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=redacted_messages, # st.session_state["messages"],
        # temperature=0.9,
        # max_tokens=100,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0.6,
        # stop=["\n", " User:", " Assistant:"],
    )
    generated_text = openai_response.choices[0]["message"]["content"]
    if show_redaction:
        with st.chat_message("redacted"):
            st.markdown(generated_text)
    # response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    
    # Add assistant response to chat history
    redacted_messages.append({"role": "assistant", "content": generated_text})
    unmasked = masker.unmask_data(generated_text)
    # print("unmasked:", unmasked)
    with st.chat_message("assistant"):
        st.markdown(unmasked)
    st.session_state["messages"].append({"role": "assistant", "content": unmasked})