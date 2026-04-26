import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# 1. GENERATE DATA (larger + realistic)
# -------------------------------
np.random.seed(42)

normal = pd.DataFrame({
    "duration": np.random.randint(1, 60, 100),
    "src_bytes": np.random.randint(50, 1500, 100),
    "dst_bytes": np.random.randint(20, 800, 100),
    "failed_logins": np.zeros(100),
    "connections": np.random.randint(1, 20, 100),
    "label": 0
})

attack = pd.DataFrame({
    "duration": np.random.randint(100, 800, 80),
    "src_bytes": np.random.randint(5000, 20000, 80),
    "dst_bytes": np.random.randint(2000, 10000, 80),
    "failed_logins": np.random.randint(1, 10, 80),
    "connections": np.random.randint(50, 300, 80),
    "label": 1
})

df = pd.concat([normal, attack]).sample(frac=1)

# Feature Engineering
df["bytes_ratio"] = df["src_bytes"] / (df["dst_bytes"] + 1)

X = df.drop("label", axis=1)
y = df["label"]

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "ids_model.joblib")

print("Model trained and saved successfully!")