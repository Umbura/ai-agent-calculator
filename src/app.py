"""
Streamlit Web Interface

This module provides a modern, chat-based web interface for the AI Agent.
It utilizes 'StreamlitCallbackHandler' to visualize the agent's reasoning process
(Thought/Action/Observation) in a collapsible UI element, similar to Gemini/ChatGPT.
"""

import sys
import os
import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler

# --- PATH FIX ---
# Add the project root directory to the Python path.
# This allows 'from src.agent import ...' to work even when running this script directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import initialize_agent

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Agent",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (GEMINI/CHATGPT STYLE) ---
st.markdown("""
<style>
    /* Remove excessive top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 10rem;
    }
    
    /* Hide default Streamlit menu, header, and footer for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat message styling */
    .stChatMessage {
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* --- INPUT BAR FINE-TUNING --- */
    
    /* Input Area (Textarea) */
    div[data-testid="stChatInput"] textarea {
        background-color: #2b2c2e !important;
        color: #ffffff !important;
        
        /* Borders and Rounding */
        border: 1px solid #444 !important;
        border-radius: 30px !important;
        
        /* Internal Spacing */
        padding-top: 13px !important; 
        padding-bottom: 13px !important;
        padding-left: 20px !important; 
        padding-right: 20px !important;
        
        /* Dimensions */
        min-height: 55px !important;
        max-height: 200px !important; /* Limit max growth */
        line-height: 1.5 !important;
        
        /* Enable Scroll */
        overflow-y: auto !important;
    }
    
    /* --- SCROLLBAR CUSTOMIZATION --- */
    /* Thin, dark scrollbar to match the theme */
    div[data-testid="stChatInput"] textarea::-webkit-scrollbar {
        width: 8px;
    }
    div[data-testid="stChatInput"] textarea::-webkit-scrollbar-track {
        background: transparent;
    }
    div[data-testid="stChatInput"] textarea::-webkit-scrollbar-thumb {
        background-color: #555;
        border-radius: 20px;
    }
    
    /* Remove default blue border on focus */
    div[data-testid="stChatInput"] textarea:focus {
        border-color: #666 !important;
        box-shadow: none !important;
    }
    
    /* Send Button Icon */
    div[data-testid="stChatInput"] button {
        color: #cccccc !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>✨ AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; margin-bottom: 2rem;'>Powered by Llama 3.3 & Tavily Search</p>", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AGENT INITIALIZATION ---
@st.cache_resource
def get_agent():
    return initialize_agent()

try:
    agent = get_agent()
except Exception as e:
    st.error(f"Failed to initialize agent. Check your .env file. Error: {e}")
    st.stop()

# --- RENDER CHAT HISTORY ---
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Type your message..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Generate Assistant Response
    with st.chat_message("assistant", avatar="✨"):
        # Create a status container to hide the "thinking" process
        with st.status("🧠 Thinking...", expanded=False) as status:
            
            # Initialize the LangChain Streamlit Callback
            st_callback = StreamlitCallbackHandler(
                st.container(),
                expand_new_thoughts=False,
                collapse_completed_thoughts=True
            )
            
            try:
                # Invoke the Agent
                response = agent.invoke(
                    {"input": prompt},
                    config={"callbacks": [st_callback]}
                )
                
                # Update status on success
                status.update(label="Complete!", state="complete", expanded=False)
                output_text = response["output"]
                
            except Exception as e:
                # Update status on error
                status.update(label="Error!", state="error", expanded=True)
                output_text = f"An error occurred: {str(e)}"

        # 3. Display Final Answer
        st.markdown(output_text)
        
        # Save to History
        st.session_state.messages.append({"role": "assistant", "content": output_text})