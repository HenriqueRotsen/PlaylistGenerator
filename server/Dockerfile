# Base image
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask server code
COPY ./server.py .

# Expose the Flask port
EXPOSE 5000

# Start the Flask server
CMD ["python", "server.py"]