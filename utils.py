import openai
from io import BytesIO
import tempfile
import os
import streamlit as st
from deepgram import Deepgram
import requests

# Create a function to transcribe audio using Deepgram
def transcribe_audio(deepgram_api_key, audio_file):
    deepgram = Deepgram(deepgram_api_key)
    with BytesIO(audio_file.read()) as audio_bytes:
        # Get the extension of the uploaded file
        file_extension = os.path.splitext(audio_file.name)[-1]

        # Create a temporary file with the uploaded audio data and the correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
            temp_audio_file.write(audio_bytes.read())
            temp_audio_file.seek(0)  # Move the file pointer to the beginning of the file

            # Transcribe the temporary audio file using Deepgram
            with open(temp_audio_file.name, 'rb') as audio:
                source = {'buffer': audio, 'mimetype': 'audio/wav'}
                options = {'punctuate': True, 'language': 'en-US'}
                response = deepgram.transcription.prerecorded(source, options)
                transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

    return transcript

def call_gpt(api_key, prompt, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=400,
    )

    return response['choices'][0]['message']['content']

def call_gpt_streaming(api_key, prompt, model):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True
    )

    collected_events = []
    completion_text = ''
    placeholder = st.empty()

    for event in response:
        collected_events.append(event)
        # Check if content key exists
        if "content" in event['choices'][0]["delta"]:
            event_text = event['choices'][0]["delta"]["content"]
            completion_text += event_text
            placeholder.write(completion_text)  # Write the received text
    return completion_text

# Create a function to clean up the transcript using GPT-4
def cleanup_transcript(api_key, transcript, model, custom_prompt=None):
    openai.api_key = api_key
    prompt = f"Please clean up and format the following audio transcription: {transcript}"
    if custom_prompt:
        prompt = f"{custom_prompt}\n\n{transcript}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=150,
    )

    cleaned_transcript = response['choices'][0]['message']['content']
    return cleaned_transcript

# Streamlit app
def main():
    st.title("Audio Transcription and Cleanup")

    # Get the Deepgram API key from the user
    deepgram_api_key = st.text_input("Enter your Deepgram API key:")

    # Get the OpenAI API key from the user
    openai_api_key = st.text_input("Enter your OpenAI API key:")

    # Upload audio file
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

    if audio_file is not None:
        # Transcribe the audio using Deepgram
        transcript = transcribe_audio(deepgram_api_key, audio_file)
        st.subheader("Transcription")
        st.write(transcript)

        # Clean up the transcript using GPT-4
        if st.button("Clean up Transcript"):
            cleaned_transcript = cleanup_transcript(openai_api_key, transcript, "gpt-4")
            st.subheader("Cleaned Transcript")
            st.write(cleaned_transcript)

if __name__ == "__main__":
    main()
