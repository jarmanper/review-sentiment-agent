# Trains the AI

# train_model.py
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline



# Dummy training data
training_texts = [
    "I love this product", 
    "This is the worst experience ever",
    "Absolute garbage",
    "Fantastic and helpful",
    "This product exceeded my expectations",
    "I would not reccommend this to anyone",
    "Worst Product Ever.",
    "Best Product Ever!",
    "I am pleased with my purchase!!!",
    "This product was defective."

]

# Labels for above data
# 1 = Positive, 0 = Negative.
training_labels = [
    1, 
    0,
    0,
    1,
    1,
    0,
    0,
    1,
    1,
    0
]

# This creates a machine learning pipeline (Vectorize text -> Classify)
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Training the model
print("Currently Training the model, hold tight!")
model.fit(training_texts, training_labels)

# Saves the model to a file named 'sentiment_model.pkl'
# Uses pickle.dump to write binary to the file. Pickle takes the python objecy and converts its internal
# structure to a sequence of bytes - serialization.
with open ('sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as sentiment_model.pkl")