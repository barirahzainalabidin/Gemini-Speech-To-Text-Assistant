import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import speech_recognition as sr
import os
from io import BytesIO
import tempfile

# Streamlit app title
st.title("Gemini Speech Assistant")

# Step 1: Configure the API key
api_key = st.text_input("Enter your Gemini API Key:", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

# Step 2: Allow user to choose between text input or speech
mode = st.radio("Select input mode:", ("Text", "Speech"))

# Step 3: Input handling based on the selected mode
user_input = ""
if mode == "Text":
    user_input = st.text_input("Type your query here:")
elif mode == "Speech":
    st.info("Click the button below and speak to your microphone.")
    if st.button("Record"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            try:
                audio_data = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio_data)
                st.write("You said: ", user_input)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Step 4: Generate response from Gemini API
if user_input:
    try:
        response = model.generate_content(user_input)
        response_text = response.text
        st.subheader("Gemini Responded:")
        st.write(response_text)

        # Step 5: Convert response to speech using gTTS
        tts = gTTS(response_text, lang='en')
        
        # Save the generated speech to a temporary file
        temp_audio = tempfile.NamedTemporaryFile(delete=False)
        tts.save(temp_audio.name)

        # Play the audio file
        st.audio(temp_audio.name, format="audio/mp3")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
