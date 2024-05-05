import os
import json
import logging
import openai
import asyncio
import aiohttp
from io import BytesIO
import tempfile
from deepgram import Deepgram
from system_prompt import SYSTEM_PROMPT

# Retrieve the API keys from environment variables
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def count_tokens(text):
    """ Count English words in a given text efficiently. """
    return len(text.split())

def chunk_transcript(transcript_data, max_tokens=700, overlap_tokens=200):
    """ Improved function with batch file writing and optimized processing. """
    chunks = []
    current_chunk = []
    current_token_count = 0

    for entry in transcript_data:
        entry_text = entry['text']
        entry_token_count = count_tokens(entry_text)

        if current_token_count + entry_token_count > max_tokens:
            chunks.append(current_chunk)
            current_chunk = current_chunk[-1:]  # Keep the last entry for overlap
            current_token_count = count_tokens(current_chunk[-1]['text'])

        current_chunk.append(entry)
        current_token_count += entry_token_count

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

async def send_to_gpt4(system_prompt, chunk_data, model="gpt-4"):
    """Send structured system description to GPT-4 and return the response."""
    try:
        response = await asyncio.to_thread(openai.ChatCompletion.create,
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an excellent optimizer of raw ARS transcripts. Your output is limited to JSON."
                },
                {
                    "role": "user",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(chunk_data)
                }
            ]
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            logging.info("No content returned in the response.")
            return None
    except Exception as e:
        logging.error(f"Error sending data to GPT-4: {e}")
        return None

async def fetch_response(session, chunk_data):
    try:
        response = await send_to_gpt4(SYSTEM_PROMPT, chunk_data)
        return response
    except Exception as e:
        logging.error(f"Error processing chunk data: {e}")
        return None

async def process_chunks_and_aggregate(chunked_data):
    responses = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for chunk_data in chunked_data:
            task = asyncio.ensure_future(fetch_response(session, chunk_data))
            tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    aggregated_json = []
    for response in responses:
        if response:
            try:
                chunk_data = json.loads(response)
                aggregated_json.extend(chunk_data)
            except Exception as e:
                logging.error(f"Error parsing response: {e}")

    # Sort the aggregated JSON based on the 'id' field
    aggregated_json = sorted(aggregated_json, key=lambda x: x['id'])

    return aggregated_json

# Create a function to transcribe audio using Deepgram
def transcribe_audio(audio_file):
    deepgram = Deepgram(DEEPGRAM_API_KEY)
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

# Create a function to clean up the transcript using GPT-4
async def cleanup_transcript(transcript, model, custom_prompt=None):
    openai.api_key = OPENAI_API_KEY

    # Parse the transcript into JSON format
    transcript_data = [{"id": i, "text": text} for i, text in enumerate(transcript.split('\n'), start=1)]

    # Chunk the transcript data
    chunked_data = chunk_transcript(transcript_data)

    # Process the chunks and aggregate the results
    aggregated_json = await process_chunks_and_aggregate(chunked_data)

    # Convert the aggregated JSON back to text format
    cleaned_transcript = '\n'.join([entry['text'] for entry in aggregated_json])

    return cleaned_transcript
