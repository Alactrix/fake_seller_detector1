# ml_model/predict_model.py
import joblib
import os

# Get the directory where THIS file (predict_model.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load model and vectorizer with absolute paths
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Model file not found! Expected at: {MODEL_PATH}") from e

def predict_fake_review(text: str):
    if not text.strip():
        return "Neutral", 0.0
    
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0].max()
    
    label_map = {0: "Genuine Review", 1: "Fake Review"}
    return label_map[prediction], round(probability * 100, 2)