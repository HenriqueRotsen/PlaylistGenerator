# Base image
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rule generator code
COPY rules_generator.py .

# Define the default command to generate the model
CMD ["python", "rules_generator.py"]