FROM python:3.10

# Copy your application code
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable for Google credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/vision_key.json"

# Copy credentials file
COPY vision_key.json /app/vision_key.json

# Run the application
CMD ["python", "main.py"]
