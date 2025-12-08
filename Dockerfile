# Lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the code into the container
COPY . /app

# Install dependencies
RUN pip install fastapi uvicorn scikit-learn==1.7.1


# Expose the port the app runs on
EXPOSE 8000

# Run the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]