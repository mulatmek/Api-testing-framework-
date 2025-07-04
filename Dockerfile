# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Default command
ENTRYPOINT ["./entrypoint.sh"]
