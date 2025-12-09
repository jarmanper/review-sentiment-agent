# Sentiment Analysis API
# This is the main backend that serves our machine learning model
# It receives text from the frontend and returns whether it's positive or negative

import pickle
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Fire up the FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="Analyzes text to determine if it's positive or negative",
    version="1.0.0"
)

# Set up CORS so our frontend can talk to this API
# We need to allow requests from wherever our frontend is hosted
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you might want to restrict this
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# This defines what data we expect when someone sends us text to analyze
class TextInput(BaseModel):
    text: str

# Load the trained model when the server starts
# This model was created by running train_model.py
with open("sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def home():
    """Health check endpoint - just returns a message to confirm the API is running"""
    return {"message": "Sentiment Analysis API is running!"}

@app.post("/predict")
def predict_sentiment(input_data: TextInput):
    """
    Takes in text and returns whether it's positive or negative
    The model returns 1 for positive and 0 for negative
    """
    # Put the text in a list since that's what the model expects
    user_text = [input_data.text]
    
    # Ask the model what it thinks
    prediction = model.predict(user_text)[0]
    
    # Convert the number to something more readable
    if prediction == 1:
        sentiment_label = "Positive"
    else:
        sentiment_label = "Negative"
    
    # Send back the results
    return {
        "text": input_data.text,
        "sentiment": sentiment_label,
        "model_version": "1.0"
    }
