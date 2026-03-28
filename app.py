import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="SyncBot", page_icon="📡")
st.title("SyncBot: Digital Communication Expert")

# 1. Setup the AI Client using the new SDK
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Note: The new SDK prefers the term "model" instead of "assistant"
    st.session_state.messages.append({"role": "model", "content": "Hello! I am SyncBot. Ask me anything about synchronization in digital communication."})

# 2. Display all past messages
for message in st.session_state.messages:
    # Streamlit UI uses "assistant", so we map "model" back to "assistant" just for the visuals
    ui_role = "assistant" if message["role"] == "model" else message["role"]
    with st.chat_message(ui_role):
        st.markdown(message["content"])

# 3. Handle user input
if prompt := st.chat_input("Ask me about phase-locked loops, frame sync, etc..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 4. Let the AI generate a real response
    with st.chat_message("assistant"):
        history_text = "\n".join([f'{m["role"].upper()}: {m["content"]}' for m in st.session_state.messages])

        # Define the strict rules for the bot
        syncbot_persona = """You are SyncBot, an expert professor and assistant specializing strictly in Synchronization in Digital Communication. 
        Your primary goals are to teach, explain, and quiz users on topics like Phase-Locked Loops (PLL), Frame Synchronization, Carrier Synchronization, Symbol Timing Recovery, etc.
        Keep your answers clear, accurate, and structured.
        CRITICAL RULE: If a user asks a question completely unrelated to electronics, telecommunications, or synchronization, you MUST politely decline to answer and steer the conversation back to your area of expertise."""

        # Call the API with the system instructions attached
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history_text,
            config=types.GenerateContentConfig(
                system_instruction=syncbot_persona,
            )
        )
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "model", "content": response.text})