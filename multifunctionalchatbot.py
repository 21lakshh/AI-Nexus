import streamlit as st
import numpy as np
import os 
from PIL import Image
from streamlit_option_menu import option_menu
from gemeni_utility import load_gemeni_pro_model
from gemeni_utility import load_gemeni_pro_vision_model
from gemeni_utility import gemini_pro_response

# Page configuration
st.set_page_config(
    page_title="🤖 AI Nexus - Multi-functional Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

working_dir = os.path.dirname(os.path.abspath(__file__))

with st.sidebar:
    selected = option_menu("AI Nexus", 
                         ["💬 Smart Chat", 
                          "🖼️ Image Insight", 
                          "❓ Knowledge Query",
                          "💻 Code Helper"],
                         menu_icon="robot",
                         icons=None,
                         default_index=0,
                         styles={
                             "container": {"padding": "5px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px"},
                             "nav-link-selected": {"background-color": "#4f8bf9"},
                         })


# Some chatbot frameworks (like OpenAI's API) use "model" to refer to the AI assistant.
# Streamlit (or another framework being used) might expect the role to be labeled as "assistant" instead
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Chatbot function
def chatbot_section():
    model = load_gemeni_pro_model()
    
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    st.title("💬 Smart Chat Assistant")
    st.subheader("Let's have a conversation!", divider="rainbow")
    
    # Clear chat button
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    
    # Chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)  

    # message.parts[0].text extracts the text content of the message.
    # st.markdown(...) displays the text message with Markdown formatting (allowing bold, italics, links, etc.).

    # if message.role == "model" it converts it to "assistant" and displays assistant's message.
    # if message.role == "user" it converts it to "user" and displays user's message.

    # user input
    user_input = st.chat_input("Type a message...") # input box for user to type a message
    if user_input:
        st.chat_message("user").markdown(user_input)
     # Opens a chat message block with the role "user", meaning the message appears in the chat UI as a user message.

        
        with st.spinner("🤖 Thinking..."):
            # model response
            gemeni_response = st.session_state.chat_session.send_message(user_input)
            # display model response
            with st.chat_message("assistant"):
                st.markdown(gemeni_response.parts[0].text)


# Image Captioning function
def image_captioning_section():
    st.title("🖼️ Image Insight Analyzer")
    st.subheader("Upload an image and get insights!", divider="rainbow")
    
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    custom_prompt = st.text_area("Custom Prompt (optional):", 
                               value="Describe this image in short",
                               height=100)
    
    if uploaded_image and st.button("🔍 Analyze Image"):
        with st.spinner("🔎 Analyzing image..."):
            image = Image.open(uploaded_image)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(image)
            
            with col2:
                response = load_gemeni_pro_vision_model(custom_prompt, image)
                st.success("📝 Analysis Results:")
                st.info(response)

# Q&A function
def qa_section():
    st.title("❓ Knowledge Query Engine")
    st.subheader("Ask me anything!", divider="rainbow")
    
    question = st.text_area("Enter your question:", 
                          placeholder="What's the meaning of life?",
                          height=150)
    
    if st.button("🚀 Get Answer"):
        with st.spinner("🧠 Processing your question..."):
            response = gemini_pro_response(question)
            st.success("📚 Answer:")
            st.markdown(response)

# New Code Helper function
def code_helper_section():
    st.title("💻 Code Assistant")
    st.subheader("Get help with programming", divider="rainbow")
    
    code = st.text_area("Paste your code here:", height=200)
    question = st.text_input("What do you need help with?")
    
    if code and question:
        with st.spinner("👩💻 Analyzing code..."):
            prompt = f"Code:\n{code}\n\nQuestion: {question}"
            response = gemini_pro_response(prompt)
            
            st.success("🔧 Solution:")
            st.markdown(response)

# Main app logic
if selected == "💬 Smart Chat":
    chatbot_section()

elif selected == "🖼️ Image Insight":
    image_captioning_section()

elif selected == "❓ Knowledge Query":
    qa_section()

elif selected == "💻 Code Helper":
    code_helper_section()