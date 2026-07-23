import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

df = pd.read_csv("dataset.csv").dropna()
df["label"] = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

pipeline = Pipeline([
    # ngram_range (1,2) lets the model see word pairs, so phrases like
    # "do not share" and "share your details" are distinguishable.
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000)),
])

pipeline.fit(X_train, y_train)

accuracy = accuracy_score(y_test, pipeline.predict(X_test))
print(f"Validation accuracy: {accuracy:.2%}")

os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/model.joblib")
print("Saved model/model.joblib")
