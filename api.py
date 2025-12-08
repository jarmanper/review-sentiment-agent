# The web server/REST API for the AI model

import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import datetime
import os

# Initialize the app
app = FastAPI()

# Configure CORS to allow requests from your React portfolio
# For production, set FRONTEND_URL environment variable with your Vercel URL
allowed_origins = [
    "http://localhost:3000",  # Local development (Create React App)
    "http://localhost:5173",  # Vite default port
    "http://localhost:5174",  # Vite alternative port
]

# Get production URL from environment variable if set
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# In development, allow all origins for easier testing
# In production, use specific origins for security
is_production = os.getenv("ENVIRONMENT") == "production"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if is_production else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Defines the data structure we expect from users
class TextInput(BaseModel):
    text: str

# Helper function to log predictions to a CSV file
def log_prediction(text, prediction):
    with open("model_logs.csv", "a", newline="") as file:
        writer = csv.writer(file)
        # Log the Current Time, The Input Text, and The Result
        writer.writerow([datetime.datetime.now(), text, prediction])

# Load the model from Phase 1.
with open ('sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running!"}

@app.post("/predict")
def predict_sentiment(input_data: TextInput):
    # Gets the text from input_data and predicts.
    user_text = [input_data.text]
    
    # Uses the model to predict (returns a list, like [1] or [0])
    prediction = model.predict(user_text)[0]
    
    # Converts the 1 or 0 into "Positive" or "Negative" text
    if prediction == 1:
        sentiment_label = "Positive"
    elif prediction == 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Unknown" 

    # Log the prediction
    log_prediction(input_data.text, sentiment_label)
    
    # Return the JSON response
    return {
        "text": input_data.text, 
        "sentiment": sentiment_label,
        "model_version": "v1.0" 
    }