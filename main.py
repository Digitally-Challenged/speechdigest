import streamlit as st
import asyncio
from utils import transcribe_audio, cleanup_transcript
import theme

# Streamlit app configuration
st.set_page_config(**theme.transcription_config)

# Define brand colors
primary_color = "#3d3d6b"
secondary_color = "#17b0dd"
background_color = "#fefefe"

# Define fonts
heading_font = "Audiowide"
body_font = "Arial"

# Custom CSS styles for a consistent and attractive look
st.markdown(
    f"""
    <style>
    h1, h3 {{
        font-family: {heading_font}, sans-serif;
    }}
    h1 {{
        color: {primary_color};
    }}
    h3, p, ul, ol, .stTextInput, .stFileUploader {{
        color: {secondary_color};
        font-family: {body_font}, sans-serif;
    }}
    .sidebar .sidebar-content {{
        background-color: {background_color};
    }}
    .stButton {{
        background-color: {primary_color};
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
    }}
    .stButton:hover {{
        background-color: {secondary_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Set up sidebar components
sidebar_left = st.sidebar.container()
sidebar_right = st.sidebar.container()

# Main content container
main_container = st.container()

# Sidebar right with information about the service
with sidebar_right:
    st.markdown(
        """
        ### Why Choose LexMed for Your Practice?
        #### Unmatched Expertise
        Our founders, seasoned Social Security Disability attorneys, provide deep insights into sector intricacies.

        #### Elevating Case Preparation and Strategy
        LexMed transforms hearing data into insightful, organized content beyond simple transcription.

        #### Transforming Traditional Hearing Analysis
        Our technology efficiently converts spoken words into structured, actionable text, saving you hours.

        #### Enhanced Accuracy and Clarity
        Our transcripts provide deep understanding and precise advocacy, improving clarity and insight into each case.
        """,
        unsafe_allow_html=True
    )

# Main content with application details
Incorporating emojis into your Streamlit application can add a friendly, engaging touch to the interface, making it more interactive and visually appealing. Here’s how you can incorporate emojis effectively in your application:

1. **Titles and Headings**: Use emojis to draw attention to specific sections or to add personality to headings. This can make the interface more relatable and less formal.

2. **Buttons and Calls to Action**: Adding emojis to buttons can make the calls to action more engaging. For instance, a coffee emoji next to "Relax and grab a coffee" enhances the casual, friendly tone.

3. **List Items**: Emojis can be used as bullet points or next to key features and upcoming features to visually represent the point being made.

4. **Success and Error Messages**: Use emojis in feedback messages to users, such as success notifications (✅) or errors (❌). This helps in conveying the tone along with the message.

5. **Sidebar Information**: Emphasize certain aspects of the sidebar content with relevant emojis to make the text less dense and more enjoyable to read.

6. **File Uploader and Text Inputs**: Place emojis next to input fields to visually explain what the input is for, making the user interface friendlier.

Here's an example of how to incorporate emojis into your existing Streamlit script:

```python
# Main content with application details
with main_container:
    st.markdown("<h1>🌟 LexMed: Leveraging AI to Elevate Disability Advocacy</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <h3>🎧 Introducing Hearing Echo – A Revolutionary Feature in Hearing Transcription</h3>
        <p>Discover the flagship feature of LexMed, Hearing Echo, designed for Social Security Disability representatives. This tool revolutionizes hearing transcript handling, offering Federal Court-level organized and high-quality transcripts.</p>
        """,
        unsafe_allow_html=True
    )

    # Key features
    st.markdown(
        """
        <h3>🔑 Key Features of Hearing Echo</h3>
        <ul>
            <li>👥 <strong>Speaker Labeling:</strong> Clear identification of speakers in the transcript.</li>
            <li>⏱️ <strong>Time Stamps:</strong> Includes precise time stamps for easy navigation.</li>
            <li>🎯 <strong>High Accuracy:</strong> Captures each word with meticulous precision.</li>
            <li>📝 <strong>Summary and Calls to Action:</strong> Provides summaries and actionable insights for your legal strategy.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # Upcoming features
    st.markdown(
        """
        <h3>🔜 Upcoming Features</h3>
        <ul>
            <li>🔍 <strong>Expert Auditing:</strong> A robust system to verify expert testimonies.</li>
            <li>📊 <strong>Procedural Auditing:</strong> Analysis of potential procedural errors by ALJs.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # Process description
    st.markdown(
        """
        <h3>🔄 Our Streamlined Process</h3>
        <ol>
            <li>📤 <strong>Upload</strong> your .ogg hearing audio file.</li>
            <li>📝 <strong>Submit</strong> the audio for transcription.</li>
            <li>☕ <strong>Relax</strong> and grab a coffee.</li>
            <li>📥 <strong>Download</strong> your transcript in PDF or TXT format, ready for use.</li>
        </ol>
        """,
        unsafe_allow_html=True
    )
    
    )

    # Process description
    st.markdown(
        """
        <h3>Our Streamlined Process</h3>
        <ol>
            <li><strong>Upload</strong> your .ogg hearing audio file.</li>
            <li><strong>Submit</strong> the audio for transcription.</li>
            <li><strong>Relax</strong> and grab a coffee.</li>
            <li><strong>Download</strong> your transcript in PDF or TXT format, ready for use.</li>
        </ol>
        """,
        unsafe_allow_html=True
    )

    # File uploader and custom prompt input
    uploaded_audio = st.file_uploader("Upload an audio file", type=['ogg'])
    custom_prompt = st.text_input("Enter a custom prompt:", value="Clean up and format the following audio transcription:")

    # Transcript cleanup process
    if st.button("Clean up Transcript"):
        if uploaded_audio:
            st.markdown("Transcribing the audio...")
            transcript = transcribe_audio(uploaded_audio)
            st.markdown(f"### Transcription:\n\n<details><summary>Click to view</summary><p><pre><code>{transcript}</code></pre></p></details>", unsafe_allow_html=True)
            st.markdown("Cleaning up the transcription...")
            cleaned_transcript = asyncio.run(cleanup_transcript_async(transcript, custom_prompt))
            st.markdown(f"### Cleaned Transcript:", unsafe_allow_html=True)
            st.write(cleaned_transcript)
        else:
            st.error("Please upload an audio file to clean up the transcript.")
