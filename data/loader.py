# patient file manager

"""
Patient data File manager
"""

import csv
import json
import os
from datetime import datetime


class PatientFileManager:
    """
    Gere la persistance du patient (donc le programme reconnait le patient dans le temps) encore appelle data persistence.
    Gere les fichiers CSV input et les JSON output
    """

    def __init__(self, data_dir: str = 'mediRoute_data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_patients_csv(self, patients: list[dict], filename: str = 'patients.csv') -> str:
        """Save patient records to CSV"""

        filepath = os.path.join(self.data_dir, filename)  # on localise le chemin du fichier patient dans le os

        if not patients:
            raise ValueError("No patients to save")  # si le fichier trouver est vide

        # par cointre s'il n'est pas vide alors ....
        with open(filepath, 'w', newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=patients[0].keys())
            writer.writeheader()
            writer.writerows(patients)

        print(f"  ✅ Saved {len(patients)} patients -> {filepath}")

        return filepath

    def load_patients_csv(self, filename: str) -> list[dict]:

        """Load patients records from CSV"""

        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                records = list(csv.DictReader(f))
                print(f"   ✅ Loaded {len(records)} records")
                return records
        except FileNotFoundError:
            raise FileNotFoundError(
                f" File not found : {filepath}"
            )

    def save_assessement_json(self, assessment: dict, patient_id: str) -> str:
        """ Save assessment result as JSON. """
        filename = f"assessment_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(assessment, f,
                      indent=2)  # 🚩🚩cette ligne🚩🚩d'ou vient-il? il fait quoi? pourquoi? il va ou? et cause/entraine quoi?#Classe  de base - interface commune
        print(f" ✅  assessement saved -> {filepath}")
        return filepath

    def load_all_assessements(self) -> list[dict]:
        """Load all assessment JSON files"""
        assessments = []

        for filename in os.listdir(self.data_dir):
            if filename.starswith("assessment_") and filename.endswith(".json"):
                filepath = os.path.join(self.data_dir, filename)
                with open(filename, 'r') as f:
                    assessments.append(json.load(f))
        return assessments


# Test
manager = PatientFileManager()

# donnees patients simulees

patients = [
    {"id": "P001", "name": "John", "age": 34, "symptoms": "fever,cough", "priority": "low"},
    {"id": "P002", "name": "Sara", "age": 28, "symptoms": "chest pain", "priority": "high"},
    {"id": "P003", "name": "Bob", "age": 45, "symptoms": "headache,fatigue", "priority": "medium"},
    {"id": "P004", "name": "Alice", "age": 52, "symptoms": "difficulty breathing", "priority": "high"},
]

# sauvegarder
manager.save_patients_csv(patients)

# Recharger
loaded = manager.load_patients_csv("patients.csv")
print(f"\n Loaded records: ")
for p in loaded:
    print(f"{p['id']} | {p['name']} | {p['age']}| {p['symptoms']}")

# Sauvegarder un assessment

assessment = {
    "patient_id": "P002",
    "urgency": "EMERGENCY",
    "specialist": "Cardiologist",
    "action": "GO to ER immediately",
    "timestamp": datetime.now().isoformat()

}
manager.save_assessement_json(assessment, "POO2")


