import streamlit as st
from google.generativeai import upload_file
import os
from dotenv import load_dotenv
from pathlib import Path
import tempfile
import google.generativeai as genai
import time
from agent import MultimodalAgent

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

st.set_page_config(
    page_title="Music recommendation for Social Media Post",
    layout="wide"
)

st.title("Music recommendation for Social Media Post")
st.header("Powered by Google Gemini Flash")

# @st.cache_resource
# def initiate_agent():
#     return MultimodalAgent()

multimodal_agent = MultimodalAgent()

image_file = st.file_uploader(label="Upload photo", type=["jpg", "png", "jpeg"], 
                                   help="Upload a photo for AI analysis")

if image_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        temp_image.write(image_file.read())
        image_path = temp_image.name

    st.image(image_path)
    user_query = st.text_area(
        "Provide specific info of the image!", 
        placeholder="Provide inforation about the image like where(location) it is clicked, how are u feeling etc.",
        help="Provide specific info for insights."
    )

    language = st.multiselect("Select languages for music", 
                                   ["English", "Hindi", "Tamil", "Telugu"])

    if st.button("Analyze image", key="analyze_image_button"):
        if not user_query:
            st.warning("Please enter information to analyze the image")
        elif not language:
            st.warning("Please select languages for music")
        else:
            try:
                with st.spinner("Processing image and gathering insights"):
                    # Process the image
                    processed_image = upload_file(image_path)
                    time.sleep(1)

                    # Prompt for analysis
                    analysis_prompt = (
                        f""" Analyze the uploaded image for content and context.
                        Analyze it along with image information. 
                        {user_query}
                        music language: {language}
                        Provide top 5 music recommendation with lyrics using the image insights and web search.
                        """
                    )

                    # AI agent processing
                    response = multimodal_agent.run(analysis_prompt, images=[processed_image])
                    print(response)

                    # Display the result
                    st.subheader("Analysis Report")
                    st.markdown(response.content)
            except Exception as e:
                st.error(f"An error occurred during analysis {e}")
            finally:
                # Clean the temporary image file
                Path(image_path).unlink(missing_ok=True)
else: 
    st.info("Upload a image file to begin the analysis")