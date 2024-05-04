import streamlit as st
from utils import transcribe_audio, cleanup_transcript
import theme

# Streamlit app
st.set_page_config(**theme.transcription_config)

# Set brand colors
primary_color = "#3d3d6b"
secondary_color = "#17b0dd"
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
        ### Data Security at LexMed
        - Founded by licensed attorneys, LexMed prioritizes confidentiality, attorney-client privilege, and robust IT security. Rest assured, your data is protected against any security risks and unauthorized disclosure.
        """
    )

    st.markdown(
        """
        ### How We Keep Your Data Secure
        """
    )
    st.image("https://d1yei2z3i6k35z.cloudfront.net/4827292/64fa66775551a_Untitleddesign1.png")
    st.image("https://d1yei2z3i6k35z.cloudfront.net/4827292/64fa669297d2f_Untitleddesign41.png")
    st.image("https://d1yei2z3i6k35z.cloudfront.net/4827292/64fa669acb672_Untitleddesign51.png")

    st.markdown(
        """
        ### Flexible Pricing
        - Your first summary is on us, and then just $2/page. For high-volume cases, contact us for bulk discounts.
        """
    )

with sidebar_right:
    st.markdown(
        """
        ### Frequently Asked Questions
        #### Is it Accurate?
        While generally precise, LexMed's Hearing Echo may occasionally encounter challenges with vague or complex testimonies. We advise reviewing transcripts carefully before official use.

        #### What is LexMed's Data Usage and Retention Policy?
        LexMed respects your data privacy by retaining transcripts only until you choose to delete them from our web app. We use customer data solely to facilitate access and do not employ it for other purposes. LexMed is committed to non-disclosure of customer data to third parties, except as required for operations through OpenAI's API.

        #### Why Do I Need A Hearing Transcript?
        Hearing Echo transforms raw audio into a structured narrative, streamlining the review process and saving you time and resources. This tool allows for easy referencing and citing of key testimonies in post-hearing objections and appeals.

        #### Are Your Services Secure?
        We adhere to the rigorous security best practices defined by Amazon Web Services (AWS), ensuring the utmost security of your data. AWS's guidelines exceed general SOC 2 standards, providing an additional layer of data protection.
        """
    )

    st.markdown(
        """
        ### Why Choose LexMed for Your Practice?
        #### Unmatched Expertise
        As founders and seasoned Social Security Disability attorneys, we have a deep understanding of the sector's intricacies. Our team's direct experience in disability law equips us with unique insights into the specific needs and challenges of legal professionals in this area, setting us apart in the field.

        #### Elevating Case Preparation and Strategy
        - LexMed offers more than just accurate hearing transcripts; we provide powerful tools for effective analysis and utilization of this information. By transforming hearing data into insightful and organized content, we empower you to build stronger cases, grounded in robust evidence and coherent narratives.

        #### Transforming Traditional Hearing Analysis
        - Forget the days of tediously listening to long audio recordings. LexMed's cutting-edge technology efficiently converts spoken words into structured, actionable text, enabling legal teams to concentrate on more critical aspects of case preparation and strategy development.

        #### Time-Saving Technology
        - LexMed's Hearing Echo is designed to save you valuable hours. It expedites case preparation without sacrificing detail or accuracy, ensuring that you have more time for higher-value legal tasks.

        #### Enhanced Accuracy and Clarity
        - Our transcripts are comprehensive tools that offer a deeper understanding and more precise advocacy. They go beyond mere transcription to provide clarity and insight into each case.

        #### Streamlined Workflow Integration
        - Designed for seamless integration into your existing workflow, our system enhances efficiency without disrupting your established processes, fitting effortlessly into your practice.

        #### Commitment to Continuous Improvement
        - We are committed to continuous evolution, consistently integrating the latest technological advancements to offer superior services. Our goal is to continually enhance our offerings to better serve your practice.
        """
    )

    st.markdown(
        """
        ### Join the LexMed Community
        Become a part of the LexMed community and experience how our innovative solutions can transform your Social Security Disability practice. Reach out to us to learn more or to schedule a demo.
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
