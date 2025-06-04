FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy app code
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt


# Expose FastAPI port
EXPOSE 8080

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
