"""
Evaluation script to load trained model artifacts, generate classification reports,
and test inference with various candidate profiles.
"""
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from utils.constants import ML_DATA_DIR, ML_MODELS_DIR


def evaluate_saved_model():
    model_path = ML_MODELS_DIR / "career_model.pkl"
    vectorizer_path = ML_MODELS_DIR / "vectorizer.pkl"
    dataset_path = ML_DATA_DIR / "career_dataset.csv"

    if not model_path.exists() or not vectorizer_path.exists():
        raise FileNotFoundError("Model or vectorizer artifact missing. Please train first.")

    model_package = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    model = model_package["model"]
    label_encoder = model_package["label_encoder"]
    model_name = model_package["model_name"]

    print(f"Loaded {model_name} from {model_path}")
    print(f"Benchmark Metrics recorded during training:")
    for m_name, metrics in model_package.get("metrics", {}).items():
        print(f"  {m_name}: Accuracy={metrics['accuracy']:.4f}, Macro-F1={metrics['f1_score']:.4f}")

    df = pd.read_csv(dataset_path)
    X_raw = df["skills"] + " " + df["interests"].fillna("")
    y_raw = df["domain"]
    y = label_encoder.transform(y_raw)

    _, X_test_raw, _, y_test = train_test_split(
        X_raw, y, test_size=0.2, random_state=42, stratify=y
    )

    X_test = vectorizer.transform(X_test_raw)
    y_pred = model.predict(X_test)

    print("\n--- DETAILED CLASSIFICATION REPORT ---")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))


if __name__ == "__main__":
    evaluate_saved_model()
