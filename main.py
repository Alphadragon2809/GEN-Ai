import os
import PyPDF2
from streamlit_option_menu import option_menu
import streamlit as st
from PIL import Image
from gemini_utility import (load_gemini_pro_model,gemini_pro_vision_response,embedding_model_response,gemini_pro_response)
working_directory=os.path.dirname(os.path.abspath(__file__))

# setting up the page config
st.set_page_config(
    page_title = "Gemini AI",
    page_icon = "🧠",
    layout = "centered"
)

with st.sidebar:
    selected = option_menu('Gemini AI',
                           ['ChatBot',
                            'Image Captioning',
                            'Embed text',
                            'Ask me anything'],
                           menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0
                           )

def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role


if selected == "ChatBot":

    model = load_gemini_pro_model()

    #initialse chat session in streamlit not already present
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])


    # streamlit page title
    st.title('🤖 ChatBot')

    #display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)


    # input field for users msg
    user_prompt=st.chat_input("Ask Gemini-Pro...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response=st.session_state.chat_session.send_message(user_prompt)

        #display gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# image captioning page
if selected == "Image Captioning":
    st.title('📸 Image Captioning')

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

    # 👉 Add text input for custom prompt
    custom_prompt = st.text_input("Ask gemini about that image...")

    if uploaded_image is not None and st.button("Get response!"):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        # Use the user’s custom prompt
        caption = gemini_pro_vision_response(custom_prompt, image)

        with col2:
            st.info(caption)




if selected == "Embed text":
    st.title('🔠 Embed Text')

    input_text = st.text_area(label='Enter text', placeholder='Type or paste your text here...')

    uploaded_file = st.file_uploader("Or upload a .txt or .pdf file", type=["txt", "pdf"])

    text_from_file = ""

    if uploaded_file:
        if uploaded_file.type == "text/plain":
            text_from_file = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text_from_file += page.extract_text()

        st.success("Text extracted from uploaded file:")
        st.write(text_from_file)

    final_text = input_text if input_text else text_from_file

    if final_text and st.button("Get Embeddings"):
        response = embedding_model_response(final_text)
        st.markdown(f"**Embedding Vector (first 10 dims):** `{response[:10]}`")



if selected == "Ask me anything":
    st.title('❓Ask me anything')
    user_prompt=st.text_area(label='',placeholder='Ask Gemini-Pro...')
    if st.button("Get an answer"):
        response=gemini_pro_response(user_prompt)
        st.markdown(response)