import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage

import os 
os.environ["OPENAI_API_KEY"] = "sk-proj-KWxehjbcUxJg_ocGYPnbDgMpYD5TrNhYkORGnRyrmKt3oxuHqTCMKPgcoaFeZT3BlbkFJao98mWC2fxENtv4J0vWG6yuUYSmVJWyn5BP0QE-n7FtQ1mWpCrOc_g4SMA"

from streamlit_chat import message

llm = ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:personal:sihprototype:A0uEp8wI")


# Streamlit App Title
st.title("LangChain Chatbot with History")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores chat history

# Memory setup (if needed)
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Chatbox UI
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask something:")  # Input box
    submitted = st.form_submit_button("Send")  # Submit button

# Handle user input
if submitted and user_input:
    # Append user input as a message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare history messages in LangChain format
    history_messages = [
        HumanMessage(content=msg["content"]) if msg["role"] == "user" 
        else AIMessage(content=msg["content"])
        for msg in st.session_state.messages
    ]

    # Add current user input as a new message
    history_messages.append(HumanMessage(content=user_input))
    
    # Generate assistant response
    response = llm(history_messages)
    response_content = response.content.strip()  # Get response text
    
    # Append assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True)  # User message
    else:
        message(msg["content"])  # Assistant message