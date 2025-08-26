# Use official Python 3.9 base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app source code
COPY app/ ./app/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
