# The "Agent" that talks to the API

import requests
import time

# The URL of the API (running locally or in Docker)
API_URL = "http://localhost:8000/predict"

# A list of "incoming" customer emails/reviews to process
incoming_queue = [
    "I am so happy with the service!",
    "The system is broken and I hate it.",
    "Data processing was fast and accurate.",
    "Why does this never work?"
]

print("Agent is starting up... monitoring queue.")


for review in incoming_queue:
    
    # Prepare the payload for the API
    payload = {"text": review} 
    
    # Send data to the API
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    sentiment = result['sentiment']
    
    print(f"Analyzing: '{review}' -> Verdict: {sentiment}")
    
    # Add 'Agentic Logic' 
    if sentiment == "Negative":
        print(">>> ALERT: Opening Support Ticket!")
    elif sentiment == "Positive":
        print(">>> INFO: Sending Thank You Email.")


    # Wait a second to simulate processing time
    time.sleep(1)

print("Queue empty. Agent going to sleep.")