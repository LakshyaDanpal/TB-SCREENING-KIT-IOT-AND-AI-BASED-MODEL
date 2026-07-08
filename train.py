# =======================
# Train Random Forest
# =======================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import joblib

#  Load your prepared 10-column dataset
df = pd.read_csv("saliva_detection_proper_10cols.csv")

#  Split into features and target
X = df.drop(columns=["PCR_result"])
y = df["PCR_result"]

# Convert target labels to numeric (if needed)
y = y.map({"pos": 1, "neg": 0}).fillna(y).astype(int)

# Split dataset into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train, y_train)

#  Evaluate model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f" Accuracy: {acc:.3f}")
print("\n Classification Report:\n", classification_report(y_test, y_pred))

#  Show feature importances
importances = model.feature_importances_
plt.figure(figsize=(8, 4))
plt.barh(X.columns, importances)
plt.xlabel("Feature Importance")
plt.ylabel("Protein Peaks")
plt.title("Random Forest - Feature Importance")
plt.tight_layout()
plt.show()

#  Save trained model
joblib.dump(model, "saliva_rf_model.pkl")
print(" Model saved as saliva_rf_model.pkl")


