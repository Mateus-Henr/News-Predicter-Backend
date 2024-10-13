# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY src/ /app/src

# Expose the port Flask will run on (Cloud Run will provide the actual port via the environment variable)
EXPOSE 5001

# Command to run the Flask app
CMD ["python", "src/run.py"]