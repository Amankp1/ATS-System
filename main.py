import streamlit as st
from signupLogin import register_user, login_user, update_user_data
import requests
import base64
 
st.set_page_config(page_title="ATS System", layout="wide")

options = ["Resume Screening", "Job Description", "Signup/Login"]



if "selected_option" not in st.session_state:
    st.session_state.selected_option = options[0]

# Custom header with clickable navigation
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("<div style='font-size: 2rem; font-weight: bold;'>ATS System</div>", unsafe_allow_html=True)
with col2:
    cols = st.columns(len(options))
    for i, opt in enumerate(options):
        if cols[i].button(opt, key=f"nav_{opt}"):
            st.session_state.selected_option = opt

st.markdown("<hr style='margin-top: 0;' />", unsafe_allow_html=True)

API_URL = "https://ats-system-hss9.onrender.com"  # Change if backend runs elsewhere

# Main content based on selected option
if st.session_state.selected_option == "Resume Screening":
    st.subheader("Resume Screening")
    user = st.session_state.get("user", {})
    logged_in = st.session_state.get("logged_in", False)
    with st.form("resume_screening_form"):
        name = st.text_input("Name", value=user.get("name", ""))
        job_title = st.text_input("Job Title", value=user.get("job_title", ""))
        # keywords = st.text_area("Job related Key Words (comma separated)", value=user.get("keywords", ""))
        file = st.file_uploader("Upload Resume(PDF)", type=["pdf"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Submitted!")
            user_data = {
                "name": name,
                "job_title": job_title
                # "keywords": keywords
            }
            if file is not None:
                st.write("File name:", file.name)
                files = {
                    "file": (file.name, file.getvalue(), "application/pdf")
                }
            if logged_in:
                pdf_bytes = file.read() if file is not None else None
                update_user_data(user.get("email", ""), user_data, pdf_bytes)
                st.session_state.user.update(user_data)

            # Send to FastAPI backend
            payload = user_data.copy()
            st.success(f"Payload")
            # if file is not None:
            #     payload["resume_pdf"] = base64.b64encode(file.getvalue()).decode()
            try:
                response = requests.post(f"{API_URL}/resume-screening", data=payload, files=files)
                if response.ok:
                    st.info(response.json()['data']['data']['response'])
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

elif st.session_state.selected_option == "Job Description":
    st.subheader("Based on Job Description")
    with st.form("job_desc_form"):
        job_title = st.text_input("Job Title")
        job_description = st.text_area("Job Description")
        file = st.file_uploader("Upload Resume(PDF)", type=["pdf"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Submitted!")
            payload = {
                "job_title": job_title,
                "job_description": job_description,
                # "file": file
            }
            if file is not None:
                st.write("File name:", file.name)
                files = {
                    "file": (file.name, file.getvalue(), "application/pdf")
                }
            try:
                response = requests.post(f"{API_URL}/job-description", data=payload, files=files)
                if response.ok:
                    st.info(response.json()['data']['data']['response'])
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

elif st.session_state.selected_option == "Signup/Login":
    register_user()

# amankp0811
# Aman12345
# mongodb+srv://amankp0811:Aman12345@atssystem.vsowaiq.mongodb.net/ 
# atssystem.vsowaiq.mongodb.net
