# mediRoute-ai/data/loader.py
"""
MediRoute AI — Data Loader v2.0
Upgrade: Pandas replaces raw CSV reader.
Now supports CSV, JSON, and validation
in one unified pipeline.
"""
import pandas as pd
import json
from pathlib import Path


# Types attendus par colonne
PATIENT_SCHEMA = {
    "id":        str,
    "name":      str,
    "age":       int,
    "gender":    str,
    "symptoms":  str,
    "source":    str,
}

REQUIRED_COLUMNS = ["id", "name", "age", "symptoms"]


def load_patients_csv(filepath: str) -> pd.DataFrame:
    """
    Load patient data from CSV into DataFrame.
    Applies type casting and basic validation.

    Args:
        filepath: Path to CSV file

    Returns:
        Clean DataFrame ready for processing
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"Patient file not found: {filepath}"
        )

    df = pd.read_csv(filepath)

    # Vérifier les colonnes requises
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}"
        )

    # Nettoyage de base
    df.columns = df.columns.str.strip().str.lower()
    df["name"] = df["name"].str.strip().str.title()
    df["symptoms"] = df["symptoms"].str.strip().str.lower()

    # Cast des types
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    return df


def load_patients_json(filepath: str) -> pd.DataFrame:
    """Load patient data from JSON into DataFrame."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict) and "patients" in data:
        return pd.DataFrame(data["patients"])
    else:
        raise ValueError("Unexpected JSON structure")


def get_summary(df: pd.DataFrame) -> dict:
    """
    Generate a summary report of the loaded dataset.
    Used for admin dashboard stats.
    """
    return {
        "total_patients":   len(df),
        "missing_values":   df.isnull().sum().to_dict(),
        "age_stats": {
            "mean":         round(df["age"].mean(), 1),
            "min":          int(df["age"].min()),
            "max":          int(df["age"].max()),
        },
        "columns":          list(df.columns),
        "dtypes":           df.dtypes.astype(str).to_dict(),
    }


def save_processed(
    df: pd.DataFrame,
    filepath: str,
    format: str = "csv"
) -> str:
    """Save processed DataFrame to file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == "csv":
        df.to_csv(filepath, index=False)
    elif format == "json":
        df.to_json(filepath, orient="records", indent=2)
    else:
        raise ValueError(f"Unknown format: {format}")

    return filepath


# Test
if __name__ == "__main__":
    import os

    # Créer un CSV de test
    test_data = """id,name,age,gender,symptoms,source
P001,ahmed ali,34,M,chest pain,web
P002,SARA SMITH,28,F,fever,mobile
P003,Bob Chen,45,M,headache,web
P004,,67,F,confusion,mobile
P005,Ravi Kumar,23,M,cough,web"""

    with open("test_patients.csv", "w") as f:
        f.write(test_data)

    df = load_patients_csv("test_patients.csv")
    summary = get_summary(df)

    print("=" * 50)
    print(f"{'MEDIROUTE AI — DATA LOADER v2.0':^50}")
    print("=" * 50)
    print(f"\n  Loaded: {summary['total_patients']} patients")
    print(f"\n  Missing values:")
    for col, count in summary["missing_values"].items():
        if count > 0:
            print(f"    {col}: {count}")
    print(f"\n  Age stats: {summary['age_stats']}")
    print(f"\n  Preview:")
    print(df.to_string(index=False))

    os.remove("test_patients.csv")