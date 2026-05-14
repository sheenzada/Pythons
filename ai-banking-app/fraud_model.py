import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Training data
data = {
    "amount": [50, 100, 200, 500, 1000, 5000, 7000, 10000],
    "is_fraud": [0, 0, 0, 0, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["amount"]]
y = df["is_fraud"]

# Train model
model = RandomForestClassifier()

model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")