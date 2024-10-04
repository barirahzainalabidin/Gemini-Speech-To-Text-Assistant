import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import tempfile

# Streamlit app title
st.title("Gemini Text-to-Speech Assistant")

# Configure the API key
api_key = st.text_input("Enter your Gemini API Key:", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

# Text input from the user
user_input = st.text_input("Type your query here:")

# Generate response from Gemini API and convert it to speech
if user_input:
    try:
        response = model.generate_content(user_input)
        response_text = response.text
        st.subheader("Gemini Responded:")
        st.write(response_text)

        # Step 4: Convert response to speech using gTTS
        tts = gTTS(response_text, lang='en')
        
        # Save the generated speech to a temporary file
        temp_audio = tempfile.NamedTemporaryFile(delete=False)
        tts.save(temp_audio.name)

        # Play the audio file
        st.audio(temp_audio.name, format="audio/mp3")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
