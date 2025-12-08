# Unit tests for the sentiment analysis API
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sentiment Analysis API is running!"}

def test_predict_positive():
    response = client.post("/predict", json={"text": "I love this product"})
    assert response.status_code == 200
    assert response.json()['sentiment'] == "Positive"

def test_predict_negative():
    response = client.post("/predict", json={"text": "This is garbage"})
    assert response.status_code == 200
    assert response.json()['sentiment'] == "Negative"