import streamlit as st
import pymongo

# MongoDB connection setup
MONGO_URI = "mongodb+srv://amankp0811:Aman12345@atssystem.vsowaiq.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["UserDB"]
users_collection = db["User"]

# Helper functions for MongoDB operations
def add_user(user_data):
    if users_collection.find_one({"email": user_data["email"]}):
        return False, "Email already registered."
    users_collection.insert_one(user_data)
    return True, "User registered successfully."

def check_login(email, password):
    user = users_collection.find_one({"email": email, "password": password})
    return user

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

def update_user_data(email, new_data, pdf_file=None):
    update_fields = {
        "name": new_data.get("name", ""),
        "job_title": new_data.get("job_title", ""),
        "keywords": new_data.get("keywords", "")
    }
    if pdf_file is not None:
        update_fields["resume_pdf"] = pdf_file
    users_collection.update_one(
        {"email": email},
        {"$set": update_fields}
    )

def update_user_pdf(email, pdf_file):
    users_collection.update_one(
        {"email": email},
        {"$set": {"resume_pdf": pdf_file}}
    )

def register_user():
    col_center = st.columns([2, 4, 2])[1]
    if 'show_login' not in st.session_state:
        st.session_state.show_login = False
    if st.session_state.show_login:
        login_user()
        return
    with col_center:
        with st.form(key="register", clear_on_submit=True):
            st.subheader("Register New User")
            name = st.text_input("Name", placeholder="Enter your name")
            job_title = st.text_input("Job Title", placeholder="Enter your job title")
            keywords = st.text_area("Job related Key Words (comma separated)", placeholder="Enter your keywords")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
            submit_button = st.form_submit_button("Register")
            user_data = {
                "name": name,
                "job_title": job_title,
                "keywords": keywords,
                "email": email,
                "password": password
            }
            if submit_button:
                if password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = add_user(user_data)
                    if success:
                        st.success(msg)
                        st.session_state.show_login = True
                        st.rerun()
                    else:
                        st.error(msg)
            
        st.write("Already have an account? Login here")
        # st.button('Login', on_click=login_user)
        if st.button('Login'):
            st.session_state.show_login = True
            st.rerun()

def login_user():
    col_center = st.columns([2, 4, 2])[1]  # Center column, width ratio 2/8
    with col_center:
        with st.form(key="login", clear_on_submit=True):
            st.subheader("Login")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                user = check_login(email, password)
                if user:
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "name": user.get("name", ""),
                        "job_title": user.get("job_title", ""),
                        "keywords": user.get("keywords", ""),
                        "email": user.get("email", "")
                    }
                    st.session_state.show_login = False
                    st.session_state.selected_option = "Resume Screening"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
    if st.button('Back to Register'):
        st.session_state.show_login = False
        st.rerun()