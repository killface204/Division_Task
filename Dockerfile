# Use official Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy your application code
COPY . .

RUN pip install -r requirements.txt

# Default command (modify as needed)
CMD ["python", "main.py"]
