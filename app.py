from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Access the Google API key from Streamlit secrets
api_key = st.secrets["GOOGLE_API_KEY"]

# Configure genai with the API key
genai.configure(api_key=api_key)

model=genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(inp,image,prompt):
    response=model.generate_content([inp,image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")







st.set_page_config(page_title="Gemini Image OCR/QA Demo")

st.header("Gemini Application")
inp=st.text_input("Input Prompt: ", key="input")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","jpeg", "png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width =True)

submit=st.button("Process")


input_prompt = """
We will upload an image. Please analyze the image and extract all readable text from it. 
Consider capturing printed, handwritten, or stylized text accurately. 
Output the text in the original order as it appears in the image, 
preserving any formatting such as line breaks, bullet points, or headings. 
Avoid interpreting the text beyond capturing it exactly as it is shown.
"""

# input_prompt = """
# Please review the image provided and perform text extraction on any visible written content.
# Then, answer the following questions based on the content extracted and visual elements in the image:
# 1. What is the main subject or topic of the image?
# 2. Summarize any key points or headings found in the image.
# 3. List any numerical values, dates, or special terms visible in the image.
# 4. If the image is a form or structured document, identify and categorize its main sections or fields.

# Ensure that text is accurately captured, and answer questions clearly based on the visual content.
# """

# if submit is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,inp)
    st.subheader("The Response is")
    st.write(response)
