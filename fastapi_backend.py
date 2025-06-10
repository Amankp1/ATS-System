from fastapi import FastAPI, HTTPException, File, Form
from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile
from resumeScreening import process_resume_screening
from PIL import Image
from jobDescription import process_job_description

app = FastAPI()

class ResumeScreeningRequest(BaseModel):
    name: str
    job_title: str  # job title of the candidate
    # keywords: str

class JobDescriptionRequest(BaseModel):
    job_title: str
    job_description: str
    

@app.post("/resume-screening")
async def resume_screening(
    name: str = Form(...),
    job_title: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()
    # Here you would process the data and PDF
    print("Getting response")
    result = process_resume_screening(name, job_title, contents)
    return {"status": "received", "data": result}

@app.post("/job-description")
async def job_description(
    job_title: str = Form(...),
    job_description: str = Form(...),
    file: UploadFile = File(...)
):   
    contents = await file.read()
    print("Getting response") 
    result = process_job_description(job_title, job_description, contents)
    return {"status": "received", "data": result} 