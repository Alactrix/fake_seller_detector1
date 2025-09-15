# ml_model/predict_model.py

import joblib

# Load saved model and vectorizer
model = joblib.load("ml_model/model.pkl")
vectorizer = joblib.load("ml_model/vectorizer.pkl")

def predict_fake_review(text):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][prediction]

    label = "Fake Review" if prediction == 1 else "Genuine Review"
    return label, round(prob * 100, 2)
