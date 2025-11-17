import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import json
import os

# Load dataset
df = pd.read_csv("dataset_fixed.csv")

# Drop URL column (not numeric)
X = df.drop(columns=["url", "label", "score"])
y = df["label"]

# Handle missing values (like -1 placeholders)
X = X.replace(-1, 0)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Get feature importance (weights)
feature_weights = dict(zip(X.columns, model.coef_[0]))

# Normalize to 100-point scale (like your config.json)
total = sum(abs(w) for w in feature_weights.values())
normalized_weights = {k: round(abs(v) / total * 100, 2) for k, v in feature_weights.items()}

# Load your old config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Update weights
for key in normalized_weights:
    if key in config:
        config[key] = normalized_weights[key]

# Save updated config
with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=4)

print("\n🎯 New optimized weights saved to config.json:")
print(json.dumps(normalized_weights, indent=4))
