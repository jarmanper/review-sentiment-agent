# 3.9-slim is a lightweight Python base image
FROM python:3.10-slim

# TODO: 1. Set the working directory inside the container to /app
# Hint: The command is WORKDIR /app
WORKDIR /app

# Copy our code into the container
COPY . /app

# Install dependencies (We need fastapi, uvicorn, scikit-learn)
RUN pip install fastapi uvicorn scikit-learn==1.7.1


# Exposes the port the app runs on (FastAPI defaults to 8000, so we expose 8000)
EXPOSE 8000

# Command to run the app when the container starts
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]