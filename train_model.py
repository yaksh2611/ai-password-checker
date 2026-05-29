import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("passwords.csv")
X = df["password"]
y = df["strength"]

model = Pipeline([
    ("vectorizer", CountVectorizer(analyzer="char", ngram_range=(1, 3))),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

model.fit(X, y)
joblib.dump(model, "password_model.pkl")
print("Model saved!")
