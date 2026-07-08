import pandas as pd
import joblib

# Load the trained model
model = joblib.load("saliva_rf_model.pkl")
print("Model loaded successfully!\n")

# List of feature names from your dataset
feature_names = [
    "protein_peak_1", "protein_peak_2", "protein_peak_3", "protein_peak_4", "protein_peak_5",
    "protein_peak_6", "protein_peak_7", "protein_peak_8", "protein_peak_9"
]

# Collect input from user
user_input = {}
print("Enter values for the 9 protein peaks:")
for feature in feature_names:
    while True:
        try:
            value = float(input(f"{feature}: "))
            user_input[feature] = [value]
            break
        except ValueError:
            print("Please enter a valid number.")

# Convert to DataFrame
X_new = pd.DataFrame(user_input)

# Make prediction
pred = model.predict(X_new)
pred_label = "Postive" if pred[0] == 1 else "Negative"

print(f"\nPredicted PCR result: {pred_label}")
