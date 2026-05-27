import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report

from xgboost import XGBClassifier

# Load dataset
data = pd.read_csv("big_phishing_dataset.csv")

# Remove duplicates
data.drop_duplicates(inplace=True)

# Convert labels
data["type"] = data["type"].map({
    "legitimate": 0,
    "phishing": 1
})

# Input and output
X = data["url"]
y = data["type"]

# Convert URLs into vectors
vectorizer = TfidfVectorizer(
    ngram_range=(1,2)
)

X_vectorized = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Create XGBoost model
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    eval_metric='logloss'
)

# Train model
model.fit(X_train, y_train)

# Save model and vectorizer
import joblib

joblib.dump(model, "model.pkl")

joblib.dump(vectorizer, "vectorizer.pkl")

# Predict test data
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", accuracy * 100)

print("\nClassification Report:\n")

print(classification_report(y_test, predictions))

# Real-time URL checking
while True:

    url = input("\nEnter URL to check: ")

    # Exit condition
    if url == "exit":
        break

    # Convert URL into vector
    url_vector = vectorizer.transform([url])

    # Predict result
    result = model.predict(url_vector)

    # Confidence score
    probability = model.predict_proba(url_vector)

    confidence = max(probability[0]) * 100

    print(f"Confidence: {confidence:.2f}%")

    # Final output
    if result[0] == 1:

        print("⚠️ Phishing URL Detected")

    else:

        print("✅ Legitimate URL")