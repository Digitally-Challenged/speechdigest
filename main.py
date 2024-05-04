Great! Let's update the `main.py` file to incorporate the brand colors and fonts you specified. Here's the revised version:

```python
import streamlit as st
from utils import transcribe_audio, cleanup_transcript
import theme

# Streamlit app
st.set_page_config(**theme.transcription_config)

# Set brand colors
primary_color = "#17b0dd"
secondary_color = "#3d3d6b"
background_color = "#fefefe"

# Set fonts
heading_font = "Audiowide"
body_font = "Arial"

# Custom CSS styles
st.markdown(
    f"""
    <style>
    h1 {{
        color: {primary_color};
        font-family: {heading_font}, sans-serif;
    }}
    h3 {{
        color: {secondary_color};
        font-family: {heading_font}, sans-serif;
    }}
    p, ul, ol {{
        color: {secondary_color};
        font-family: {body_font}, sans-serif;
    }}
    .sidebar .sidebar-content {{
        background-color: {background_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create sidebars
sidebar_left = st.sidebar.container()
sidebar_right = st.sidebar.container()

# Main content
main_container = st.container()

with sidebar_left:
    st.markdown(
        """
        ### About LexMed
        LexMed is a cutting-edge AI-powered platform designed to revolutionize the way Social Security Disability representatives handle hearing transcripts. Our mission is to streamline the process and provide high-quality, organized transcripts that save time and effort.
        """
    )

    st.markdown(
        """
        ### Contact Us
        If you have any questions or comments, feel free to reach out to Nick Coleman at [LexMed.AI](https://lexmed.ai).
        """
    )

with sidebar_right:
    st.markdown(
        """
        ### Testimonials
        "Hearing Echo has been a game-changer for our practice. The accurate transcriptions and summaries have saved us countless hours of manual work." - John Doe, Disability Attorney
        """
    )

    st.markdown(
        """
        ### FAQ
        - **Q:** How long does the transcription process take?
          **A:** The transcription process typically takes a few minutes, depending on the length of the audio file.

        - **Q:** What audio formats are supported?
          **A:** Currently, we support .ogg audio files. Support for additional formats will be added in the future.
        """
    )

with main_container:
    title = f"<h1>LexMed: Leveraging AI to Elevate Disability Advocacy to New Heights</h1>"
    st.markdown(title, unsafe_allow_html=True)

    intro = f"<h3>Introducing Hearing Echo – A Game-Changer in Hearing Transcription</h3><p>At LexMed, we are excited to unveil our flagship feature - Hearing Echo! Specially designed for Social Security Disability representatives, Hearing Echo revolutionizes the way you handle hearing transcripts. Say goodbye to the laborious task of manually sifting through hours of audio for key insights. Welcome to an era where high-quality, organized transcripts, akin to those used in Federal Court, are just a few clicks away.</p>"
    st.markdown(intro, unsafe_allow_html=True)

    features = """
        <h3>Key Features of Hearing Echo</h3>
        <ul>
            <li><strong>Speaker Labeling:</strong> Clear identification and labeling of speakers in the transcript for effortless tracking of who said what.</li>
            <li><strong>Time Stamps:</strong> Every transcript comes with precise time stamps, making it easy to locate specific moments in the hearing.</li>
            <li><strong>High Accuracy:</strong> We promise highly accurate transcriptions, capturing each word spoken with meticulous precision.</li>
            <li><strong>Summary and Calls to Action:</strong> Get not just transcripts, but summaries highlighting the main points and actionable insights for your legal strategy.</li>
        </ul>
    """
    st.markdown(features, unsafe_allow_html=True)

    upcoming = """
        <h3>Upcoming Features</h3>
        <ul>
            <li><strong>Expert Auditing:</strong> A robust review system to ensure the accuracy of vocational and medical expert testimonies.</li>
            <li><strong>Procedural Auditing:</strong> Insightful analysis of potential procedural errors by the Administrative Law Judge (ALJ).</li>
        </ul>
    """
    st.markdown(upcoming, unsafe_allow_html=True)

    process = """
        <h3>Our Streamlined Process</h3>
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
