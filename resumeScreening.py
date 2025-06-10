from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import fitz 
import io

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def convert_pdfs_to_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    image_list = []
    mat = fitz.Matrix(2.0, 2.0)

    for page_num, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")  
        image = Image.open(io.BytesIO(img_bytes))  
        image_list.append(image)
    # print(f"Loaded: {pdf_bytes} -> {len(doc)} pages")

    return image_list



def get_gemini_response(input_text, image_list):
    gemini_images = [image for image in image_list]

    if input_text:
        response = model.generate_content([input_text] + gemini_images)
    else:
        response = model.generate_content(gemini_images)

    return response.text


def process_resume_screening(name, job_title, file):
    input_text = f'''
    You are a resume screening expert, which provides feedback on its quality and suitability for a job or Applicant Tracking System. You need to screen the resume and return the result.
    Name of the candidate is {name}. Job title is {job_title}.
    Analyse the resume based on the below characteristics and give me the total score, and also provide me the individual score for each of the characteristics, along with the reason and the improvements needed to get the best job of it.


    -tailoring
    1)Hard Skills
    2)Soft Skills

    -content
    1)ATS Parse Rate
    2)Quantifying Impact
    3)Repetition
    4)Spelling & Grammar

    -format
    1)File Format & Size
    2)Resume Length
    3)Long Bullet Points

    -sections
    1)Contact Information
    2)Essential Sections
    3)Personality

    -style
    1)Design
    2)Email Address
    3)Active voice
    4)Buzzwords & Cliches

    Give total out of 100 for the resume.
    Extract the name of the candidate from the resume and answer in such a way that you are directly talking to the candidate.
    Additionally you can also give your feedback, for what to update and what to add or remove, and how to land a job
    '''

    image_list = convert_pdfs_to_images(file)

    response = get_gemini_response(input_text, image_list)
    return {"status": "received", "data": {"response": response}}







