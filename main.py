import streamlit as st
import asyncio
from utils import transcribe_audio, cleanup_transcript
import theme
import time
import plotly.express as px

# Streamlit app configuration
st.set_page_config(page_title="LexMed Transcription Service", layout="wide", **theme.transcription_config)

# Define custom styles and interactivity
primary_color = "#3d3d6b"
secondary_color = "#17b0dd"
background_color = "#fefefe"
heading_font = "Audiowide"
body_font = "Arial"

st.markdown(
    f"""
    <style>
    @keyframes fadeIn {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}

    body {{
        animation: fadeIn 1s ease-out;
    }}

    .stButton>button {{
        color: white;
        background-color: {secondary_color};
        border-radius: 8px;
        border: 2px solid {primary_color};
        transition: transform 0.3s ease-out;
    }}

    .stButton>button:hover {{
        transform: scale(1.1);
        background-color: {primary_color};
    }}

    h1, h3 {{
        color: {primary_color};
        font-family: {heading_font}, sans-serif;
    }}

    p, ul, ol {{
        color: {secondary_color};
        font-family: {body_font}, sans-serif;
    }}

    .sidebar .sidebar-content {{
        background-color: {background_color};
    }}

    @media (max-width: 768px) {{
        .stButton>button {{
            font-size: 18px; /* Larger text for mobile */
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content setup
sidebar_left = st.sidebar.container()
sidebar_right = st.sidebar.container()

with sidebar_left:
    st.image("https://d1yei2z3i6k35z.cloudfront.net/4827292/64fa66775551a_Untitleddesign1.png")
    st.markdown(
        """
        ### Data Security at LexMed
        Founded by licensed attorneys, LexMed prioritizes confidentiality, attorney-client privilege, and robust IT security. Rest assured, your data is protected against any security risks and unauthorized disclosure.
        """
    )

with sidebar_right:
    choose_service = st.selectbox("Choose Your Service:", ["Hearing Echo", "Case Preparation"])
    if choose_service == "Hearing Echo":
        st.markdown("Details about Hearing Echo...")
    else:
        st.markdown("Information on Case Preparation...")

# Main container setup
main_container = st.container()

with main_container:
    title = f"<h1>LexMed: Leveraging AI to Elevate Disability Advocacy to New Heights</h1>"
    st.markdown(title, unsafe_allow_html=True)

    intro = f"<h3>Introducing Hearing Echo – A Game-Changer in Hearing Transcription</h3>"
    st.markdown(intro, unsafe_allow_html=True)

    # Dynamic feature description based on service selection
    if choose_service == "Hearing Echo":
        st.markdown("""
            <p>At LexMed, we are excited to unveil our flagship feature - Hearing Echo! Specially designed for Social Security Disability representatives, Hearing Echo revolutionizes the way you handle hearing transcripts.</p>
            """, unsafe_allow_html=True)

        feature_chart_data = {"Features": ["Speaker Labeling", "Time Stamps", "Accuracy"], "Rating": [4.5, 4.7, 4.9]}
        feature_chart = px.bar(feature_chart_data, x='Features', y='Rating', color='Features', title="Feature Satisfaction Ratings")
        st.plotly_chart(feature_chart, use_container_width=True)
    else:
        st.markdown("""
            <p>LexMed offers more than just accurate hearing transcripts; we transform hearing data into insightful and organized content.</p>
            """, unsafe_allow_html=True)

    # Upload and process button
    uploaded_audio = st.file_uploader("Upload an audio file", type=['ogg'])
    custom_prompt = st.text_input("Enter a custom prompt:", value="Clean up and format the following audio transcription:")

    if st.button("Clean up Transcript"):
        if uploaded_audio:
            with st.spinner("Transcribing the audio... Please wait."):
                transcript = transcribe_audio(uploaded_audio)
                st.markdown(f"### Transcription:\n\n<details><summary>Click to view</summary><p><pre><code>{transcript}</code></pre></p></details>", unsafe_allow_html=True)
            
            with st.spinner("Cleaning up the transcription... Please wait."):
                cleaned_transcript = asyncio.run(cleanup_transcript(transcript, "gpt-4", custom_prompt))
            
            st.markdown(f"### Cleaned Transcript:")
            st.write(cleaned_transcript)

# Footer with additional user information
st.sidebar.info("For more information on how to use this tool, please visit our [User Guide](https://example.com).")
