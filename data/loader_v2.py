"""
MediRoute AI - Data loader v2.0
upgrade: Pandas replace Raw csv reader
now supports CSV, JSON, and valdation in one unified Pipeline.
"""


import pandas as pd
import json
from pathlib import Path

# Types attendus par colonne

PATIENT_SCHEMA = {
    "id" : str,
    "name" : str,
    "age": int,
    "gender" : str,
    "symptoms":str,
    "sources": str,
}

REQUIRED_COLUMNS = ["id","name","age","gender","symptoms","sources"]


def load_patient_csv(filepath:str) -> pd.DataFrame:
    """
    Load patient data from csv into DataFrame.
    Applies type Casting and basic validation.

    Args:
        - filepath: PATH to csv file
    Returns:
        - Clean DataFrame ready for processing

    """

    # charger le fichier si il existe
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Patient File not Found:{filepath}")
    else:
        # on lit le df
        df = pd.read_csv(filepath)


    # Verifier les colonnes requises

    missing_cols = set(REQUIRED_COLUMNS) - set (df.columns)

    if missing_cols:
        raise ValueError (f"Missing required columns {missing_cols}")
    else:

        # on fait ne Nettoyage de base

        # df.columns = df.columns.lower().strip()  pourquoi pas cette ligne
        df.columns = df.columns.str.lower().str.strip()

        df["name"] = df ["name"].str.lower().str.strip().str.title() #
        df["symptoms"] = df ["symptoms"].str.lower().str.strip().str.title() #

        # cast des types

        df["age"] = pd.to_numerique(df["age"],errors="coerce")

        return df



def load_patients_json(filepath:str)->pd.DataFrame:
    """Load patient Data from Json into DataFrame."""

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not Found: {filepath}")
    else:
        with open(filepath, 'r',encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

    if isinstance (data, list):
        return pd.Dataframe (data)
    elif isinstance (data, list) and "patients" in data:
        return pd.DataFrame(data["patients"])
    else:
        raise ValueError("Unexpected Json Structure")



def get_summary(df: pd.DataFrame)-> dict:
    """
    Generate a summary report from the loaded dataset.
    Used for admin DASHboard stats.
    """
    return{
        "total_patients" : len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "age_stats":{
            "mean" : round(df["age"].mean(),1),
            "min": int(df["age"].min()),
            "max" :int(df["max"].max()),
        },
        "columns" : list(df.columns),
        "dtype": df.dtypes.astype(str).to_dicts(),
    }



def save_processed(df:pd.DataFrame, filepath:str,format:str = 'csv')-> str:
    """Save processed dataframe to File"""

    path = Path(filepath)
    path.parent.mkdir(parents=True,exist_ok=True)

    if format=="csv":
        df.to_csv(filepath,index=False)
    elif format =='json':
        df.to_json(filepath,orient="records",indent=2)
    else:
        raise ValueError(f"Unknow format: {format}")

    return filepath

#Test



