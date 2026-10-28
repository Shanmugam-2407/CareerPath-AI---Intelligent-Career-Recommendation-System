"""
ML Training Pipeline: Trains and compares Logistic Regression, Random Forest, and XGBoost.
Selects the best performing model and persists it to ml/models/ using Joblib.
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder

from utils.constants import ML_DATA_DIR, ML_MODELS_DIR


def train_models():
    dataset_path = ML_DATA_DIR / "career_dataset.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    # Feature engineering: combine skills and interests for rich semantic signal
    X_raw = df["skills"] + " " + df["interests"].fillna("")
    y_raw = df["domain"]

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    classes = label_encoder.classes_

    # Split train/test
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.2, random_state=42, stratify=y
    )

    # TF-IDF Vectorization
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w\+\#\.\-]+\b",
        max_features=500,
        sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, C=2.0),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=15, random_state=42),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric="mlogloss"
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model = None

    print("\n--- MODEL COMPARISON & BENCHMARKING ---")
    for name, clf in models.items():
        print(f"\nTraining {name}...")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="macro", zero_division=0)

        results[name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1)
        }

        print(f"{name} Results:")
        print(f"  Accuracy : {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall   : {rec:.4f}")
        print(f"  F1-Score : {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = clf

    print(f"\nBest Model Selected: {best_model_name} with Macro F1-Score of {best_f1:.4f}")

    # Ensure model directory exists
    ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Save vectorizer
    vectorizer_path = ML_MODELS_DIR / "vectorizer.pkl"
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Saved vectorizer to {vectorizer_path}")

    # Save model package with metadata and label encoder
    model_package = {
        "model": best_model,
        "model_name": best_model_name,
        "label_encoder": label_encoder,
        "classes": list(classes),
        "metrics": results,
        "best_metrics": results[best_model_name]
    }
    model_path = ML_MODELS_DIR / "career_model.pkl"
    joblib.dump(model_package, model_path)
    print(f"Saved best model package to {model_path}")

    return model_package


if __name__ == "__main__":
    train_models()
