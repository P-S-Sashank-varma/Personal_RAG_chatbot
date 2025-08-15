import streamlit as st
from langchain_helper import execute_user_query

# Page configuration
st.set_page_config(
    page_title="About Sashank Varma",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background-color: #f5f5f5;
        padding-top: 20px;
    }
    
    /* Chat message bubbles */
    .user-message {
        background-color: #D1E8FF;
        padding: 12px;
        border-radius: 12px;
        margin-left: auto;
        margin-bottom: 10px;
        max-width: 70%;
    }
    .assistant-message {
        background-color: #E8FFE3;
        padding: 12px;
        border-radius: 12px;
        margin-right: auto;
        margin-bottom: 10px;
        max-width: 70%;
    }

    /* Title styling */
    .title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #4B0082;
        margin-bottom: 20px;
    }

    /* Chat input styling */
    .stTextInput>div>input {
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">About Sashank Varma ✨</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# React to user input
if query_text := st.chat_input("Ask away!"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(query_text)
        
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query_text})

    # Get assistant response
    response = execute_user_query(query_text)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
