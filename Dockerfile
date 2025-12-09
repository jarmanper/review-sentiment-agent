# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set up the working directory inside the container
WORKDIR /app

# Copy all the project files into the container
COPY . /app

# Install the Python packages we need
RUN pip install --no-cache-dir -r requirements.txt

# The API runs on port 8000
EXPOSE 8000

# Start the API server when the container launches
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
