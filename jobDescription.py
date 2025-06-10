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

def get_gemini_response(input_text, image_list):
    gemini_images = [image for image in image_list]

    if input_text:
        response = model.generate_content([input_text] + gemini_images)
    else:
        response = model.generate_content(gemini_images)

    return response.text

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


def process_job_description(job_title, job_description, file):
    input_text = f'''
    You have to provides feedback on its quality and suitability of resume for a job or Applicant Tracking System. You need to screen the job description and return the result.
    Job title is {job_title}. Job description is {job_description}.
    Scan the resume and job description and tell me the changes needed to make the resume more suitable for the job.
    Our focus is to make the resume more suitable for the provided job description.
    Extract the name of the candidate from the resume and answer in such a way that you are directly talking to the candidate.
    Also mainly focus on skills and keywords that are needed for the job.
    '''
    image_list = convert_pdfs_to_images(file)
    response = get_gemini_response(input_text, image_list)
    return {"status": "received", "data": {"response": response}}












# from dotenv import load_dotenv

# load_dotenv()
# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image 
# import pdf2image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,pdf_cotent,prompt):
#     model=genai.GenerativeModel('gemini-pro-vision')
#     response=model.generate_content([input,pdf_content[0],prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ## Convert the PDF to image
#         images=pdf2image.convert_from_bytes(uploaded_file.read())

#         first_page=images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume EXpert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

# #submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt1,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")
        











# from load_dotenv import load_dotenv
# import pdf2image
# import google.generativeai as genai
# import os
# import base64
# import io

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input, pdf_content, prompt):
#     model = genai.GenerativeModel("gemini-pro-vision-001")
#     response = model.generate_content(input, pdf_content[0], prompt)
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None  :
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         first_page = images[0]
        
#         # convert into bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format="JPEG")
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_part = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode("utf-8")
#             }
#         ]
#         return pdf_part
#     else:
#         raise FileNotFoundError("No file uploaded")

# uploaded_file = "OLD Aman Patel Resume.pdf"
# pdf_content = input_pdf_setup(uploaded_file)
# # response = get_gemini_response(prompt, pdf_content, input_job_description)
# print(pdf_content)


# def process_job_description(job_title, job_description, pdf_bytes):
#     return {"status": "received", "data": {"job_title": job_title, "job_description": job_description}}