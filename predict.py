import pickle
import numpy as np
from flask import Flask, request, jsonify
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

model_path = "model.bin"
vectorizer_path = "vectorizer.pkl"

# Load files
def load_file(file):
    with open(file, 'rb') as f_in:
        return pickle.load(f_in)

model = load_file(model_path)
vectorizer = load_file(vectorizer_path)

# Initialize Flask app
app = Flask("yt-comment")

@app.route("/predict", methods=['POST'])
def predict():
    """
    Make predictions on new text and return sentiment labels
    """
    # Label mapping
    label_map = {
        0: 'negative',  # adjust these if your mapping is different
        1: 'neutral',
        2: 'positive'
    }

    # Get JSON data from request
    data = request.get_json()

    # Extract text data
    text = data.get('text')
    
    # If input is a single string, convert to list
    if isinstance(text, str):
        text = [text]
    
    # Transform text data to numerical features using the loaded vectorizer
    text_tfidf = vectorizer.transform(text)
    
    # Make prediction
    numeric_pred = model.predict(text_tfidf)
    
    # Convert to text labels
    text_predictions = [label_map[pred] for pred in numeric_pred]
    result = {
        "predicted_sentiment": text_predictions
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
