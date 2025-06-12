# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app with uvicorn
# CMD ["python", "-m", "uvicorn", "fastapi_backend:app", "--host", "0.0.0.0", "--port", "8000"] 
CMD ["streamlit", "run", "App.py"]
