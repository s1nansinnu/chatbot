import streamlit as st
import requests

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")
API_URL = "http://127.0.0.1:8000"

st.title("Chatbot")
st.caption("A chatbot using gemini 2.5 flash Model")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Chat Controls")
    
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.tokens_used = 0
        st.rerun()
    
    st.divider()    
    if st.session_state.session_id:
        st.text_input("Session ID", value=st.session_state.session_id, disabled=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"Message": prompt}
                if st.session_state.session_id:
                    payload["SessionId"] = st.session_state.session_id
                
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data["Response"]
                    st.session_state.session_id = data["SessionId"]
                else:
                    bot_response = f"Error: {response.status_code} - {response.text}"
                    
            except requests.exceptions.ConnectionError:
                bot_response = "Could not connect to the backend. Make sure the FastAPI server is running on port 8000."
            except Exception as e:
                bot_response = f"An error occurred: {str(e)}"
        
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()