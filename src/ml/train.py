from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "telco_churn.csv"
MODEL_DIR = PROJECT_ROOT / "data" / "model"
MODEL_PATH = MODEL_DIR / "churn_model.joblib"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Standardize column naming (some sources use "customerID" / "CustomerID")
    if "customerID" in df.columns and "CustomerID" not in df.columns:
        df = df.rename(columns={"customerID": "CustomerID"})

    return df


def build_pipeline(X: pd.DataFrame) -> Pipeline:
    # Split columns by type
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    # Preprocess numeric: fill missing with median
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    # Preprocess categorical: fill missing + one-hot encode
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    # Simple, strong baseline model
    model = LogisticRegression(max_iter=1000)

    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )


def main():
    df = load_data()

    # Target: "Churn" should be Yes/No
    if "Churn" not in df.columns:
        raise ValueError("Expected a 'Churn' column in the dataset.")

    # Basic cleanup: TotalCharges sometimes comes as text -> convert
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Drop ID column from features
    drop_cols = [c for c in ["CustomerID", "customerID"] if c in df.columns]
    X = df.drop(columns=drop_cols + ["Churn"])
    y = (df["Churn"].astype(str).str.strip().str.lower() == "yes").astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = build_pipeline(X_train)
    pipe.fit(X_train, y_train)

    # Evaluate
    proba = pipe.predict_proba(X_test)[:, 1]
    preds = (proba >= 0.5).astype(int)

    print("ROC-AUC:", round(roc_auc_score(y_test, proba), 4))
    print(classification_report(y_test, preds))

    # Save model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
