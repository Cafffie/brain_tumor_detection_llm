import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key= os.environ["GOOGLE_API_KEY"])

def app_response(prompt, image):
    model= genai.GenerativeModel("gemini-pro-vision")
    response= model.generate_content([prompt, image[0]])
    return response.text

def input_image(image_file):
    if image_file is not None:
        bytes= image_file.getvalue()
        image_data=[{
            "mime_type": image_file.type,
            "data": bytes
        }]
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")


#Streamlit app (Front end)
st.set_page_config(page_title= "Brain Tumor Detection App")
st.title("Brain Tumor Detection App")


uploaded_image= st.file_uploader(
    "Upload an image...",
    type= ["jpg", "jpeg", "png"],
    help= "Please upload an image"
)

image=""
if uploaded_image is not None:
    image= Image.open(uploaded_image)
    st.image(image, caption="Upload an image", use_column_width=True)

submit= st.button("Detect tumor")

prompt="""
        You are a consultant medical doctor, specialized in radiology and a professional neurologist. 
        You are to scrutinize images and tell if it contains any form of brain tumor or not. 
        If it doesn't contain any tumor, state that the patient is healthy and contain no tumor in the format below.
        1. Tumor: "None"
        2. Status: "Healthy"
        
        If it contains tumor, state that it contains tumor. Give in details the name of brain tumor, type of tumor (benign or malignant), 
        location, health status(healthy, mild, critical) and how far it has spread, size, with percentage growth and possible treatments in the format below.
        1. Tumor: "Yes"
        2. Name of tumor: "",
        3. Type of tumor: "",
        4. Health Status: ""
        5. location: "",
        6. size: "",
        7. percentage growth: "%",
        8. possible treatment: ""

        Also examine the images for any form of normalties and abnormalties and Give in details what you saw.
        """

if submit:
    image_info= input_image(uploaded_image)
    response= app_response(prompt, image_info)
    st.header("Tumor Detector report:")
    st.write(response)

