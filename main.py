import streamlit as st
from utils import transcribe_audio, cleanup_transcript
import theme

# Streamlit app
st.set_page_config(**theme.transcription_config)

title = """
    <h1 style="color:#32CD32; font-family:sans-serif;">LexMed: Leveraging AI to Elevate Disability Advocacy to New Heights</h1>
"""
st.markdown(title, unsafe_allow_html=True)

intro = """
    <h3 style="color:#32CD32;">Introducing Hearing Echo – A Game-Changer in Hearing Transcription</h3>
    <p>At LexMed, we are excited to unveil our flagship feature - Hearing Echo! Specially designed for Social Security Disability representatives, Hearing Echo revolutionizes the way you handle hearing transcripts. Say goodbye to the laborious task of manually sifting through hours of audio for key insights. Welcome to an era where high-quality, organized transcripts, akin to those used in Federal Court, are just a few clicks away.</p>
"""
st.markdown(intro, unsafe_allow_html=True)

features = """
    <h3 style="color:#32CD32;">Key Features of Hearing Echo</h3>
    <ul>
        <li><strong>Speaker Labeling:</strong> Clear identification and labeling of speakers in the transcript for effortless tracking of who said what.</li>
        <li><strong>Time Stamps:</strong> Every transcript comes with precise time stamps, making it easy to locate specific moments in the hearing.</li>
        <li><strong>High Accuracy:</strong> We promise highly accurate transcriptions, capturing each word spoken with meticulous precision.</li>
        <li><strong>Summary and Calls to Action:</strong> Get not just transcripts, but summaries highlighting the main points and actionable insights for your legal strategy.</li>
    </ul>
"""
st.markdown(features, unsafe_allow_html=True)

upcoming = """
    <h3 style="color:#32CD32;">Upcoming Features</h3>
    <ul>
        <li><strong>Expert Auditing:</strong> A robust review system to ensure the accuracy of vocational and medical expert testimonies.</li>
        <li><strong>Procedural Auditing:</strong> Insightful analysis of potential procedural errors by the Administrative Law Judge (ALJ).</li>
    </ul>
"""
st.markdown(upcoming, unsafe_allow_html=True)

process = """
    <h3 style="color:#32CD32;">Our Streamlined Process</h3>
    <ol>
        <li><strong>Upload</strong> your .ogg hearing audio file.</li>
        <li><strong>Submit</strong> the audio for transcription.</li>
        <li><strong>Relax</strong> and grab a coffee.</li>
        <li><strong>Download</strong> your transcript in PDF or TXT format, ready for use.</li>
    </ol>
"""
st.markdown(process, unsafe_allow_html=True)

deepgram_api_key = st.text_input("Enter your Deepgram API key:", type="password")
openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")

uploaded_audio = st.file_uploader("Upload an audio file", type=['ogg'])

custom_prompt = None

custom_prompt = st.text_input("Enter a custom prompt:", value="Clean up and format the following audio transcription:")

if st.button("Clean up Transcript"):
    if uploaded_audio:
        if deepgram_api_key and openai_api_key:
            st.markdown("Transcribing the audio...")
            transcript = transcribe_audio(deepgram_api_key, uploaded_audio)
            st.markdown(f"### Transcription:\n\n<details><summary>Click to view</summary><p><pre><code>{transcript}</code></pre></p></details>", unsafe_allow_html=True)

            st.markdown("Cleaning up the transcription...")
            if custom_prompt:
                cleaned_transcript = cleanup_transcript(openai_api_key, transcript, "gpt-4", custom_prompt)
            else:
                cleaned_transcript = cleanup_transcript(openai_api_key, transcript, "gpt-4")

            st.markdown(f"### Cleaned Transcript:")
            st.write(cleaned_transcript)
        else:
            st.error("Please enter valid Deepgram and OpenAI API keys.")

st.markdown(
    """
    ---
    ### Source code and contact information
    - The source code for this app can be found on GitHub: [LexMed](https://github.com/StanGirard/lexmed)
    - If you have any questions or comments, feel free to reach out to Nick Coleman at [LexMed.AI](https://lexmed.ai)
    """
)
