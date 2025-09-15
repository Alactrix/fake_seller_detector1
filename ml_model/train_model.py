import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Load dataset
df = pd.read_csv("fake reviews dataset.csv")

# 2. Preprocess labels
df = df[df["label"].isin(["CG", "OR"])]  # filter valid classes
df["label"] = df["label"].map({"CG": 0, "OR": 1})  # 0 = real, 1 = fake

# 3. Extract features and target
X = df["text_"]
y = df["label"]

# 4. TF-IDF Vectorizer (turn text into numbers)
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# 6. Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 8. Save the model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model and vectorizer saved to ml_model/")
