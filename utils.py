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

def generate_image_prompt(api_key, user_input):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Create a text that explains in a lot of details how the meme about this topic would look like: {user_input}"}],
        temperature=0.7,
        max_tokens=50,
    )

    return response['choices'][0]['message']['content']

def generate_image(api_key, prompt):
    openai.api_key = api_key

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )

    return response['data'][0]['url']

def generate_images(api_key, prompt, n=4):
    openai.api_key = api_key

    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size="256x256",
        response_format="url",
    )

    return response['data']
