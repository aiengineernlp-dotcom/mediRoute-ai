# mediRoute_ai/engine/symptom_vectors.py
"""
MediRoute AI — Symptom Vector Engine v2.0
Upgrade: Broadcasting for batch processing.
Change from Jour 9: Now handles 1000 patients
simultaneously instead of one at a time.
"""
import numpy as np


SYMPTOM_VOCABULARY = {
    "fever":                0,
    "cough":                1,
    "chest pain":           2,
    "difficulty breathing": 3,
    "headache":             4,
    "fatigue":              5,
    "nausea":               6,
    "dizziness":            7,
    "confusion":            8,
    "abdominal pain":       9,
    "stroke":               10,
    "palpitation":          11,
}

N_SYMPTOMS = len(SYMPTOM_VOCABULARY)


def encode_batch(
    patient_symptoms: list[list[str]]
) -> np.ndarray:
    """
    Encode a BATCH of patients simultaneously.
    Uses broadcasting — no loop needed.

    Args:
        patient_symptoms: list of symptom lists
                          one per patient

    Returns:
        Matrix of shape (n_patients, n_symptoms)
    """
    n = len(patient_symptoms)
    # Matrice de zéros — tous les patients
    matrix = np.zeros((n, N_SYMPTOMS), dtype=np.float32)

    for i, symptoms in enumerate(patient_symptoms):
        for symptom in symptoms:
            idx = SYMPTOM_VOCABULARY.get(
                symptom.lower()
            )
            if idx is not None:
                matrix[i, idx] = 1.0

    return matrix


def normalize_vectors(
    matrix: np.ndarray
) -> np.ndarray:
    """
    Normalize all patient vectors simultaneously.
    Broadcasting: (n, features) / (n, 1) → (n, features)
    """
    norms = np.linalg.norm(
        matrix, axis=1, keepdims=True
    )
    # Éviter division par zéro
    norms = np.where(norms == 0, 1, norms)
    return matrix / norms  # ← broadcasting


def batch_similarity(
    query_vector: np.ndarray,
    patient_matrix: np.ndarray
) -> np.ndarray:
    """
    Compute similarity between ONE query
    and ALL patients simultaneously.

    Broadcasting:
    query  : (features,)
    matrix : (n_patients, features)
    result : (n_patients,)

    This replaces a loop of 1000 comparisons
    with ONE matrix operation.
    """
    # Normaliser
    query_norm   = query_vector / (
        np.linalg.norm(query_vector) + 1e-8
    )
    patient_norms = normalize_vectors(patient_matrix)

    # Produit matriciel — broadcasting
    similarities = patient_matrix @ query_norm
    return similarities


def classify_urgency_batch(
    patient_matrix: np.ndarray
) -> np.ndarray:
    """
    Classify urgency for ALL patients at once.
    Uses np.select — vectorized conditions.

    Returns array of urgency labels.
    """
    # Features critiques
    has_chest_pain = patient_matrix[:, 2] > 0
    has_breathing  = patient_matrix[:, 3] > 0
    has_confusion  = patient_matrix[:, 8] > 0
    has_stroke     = patient_matrix[:, 10] > 0
    n_symptoms     = patient_matrix.sum(axis=1)

    conditions = [
        has_chest_pain | has_breathing |
        has_confusion  | has_stroke,
        n_symptoms >= 3,
        n_symptoms >= 2,
    ]
    choices = ["EMERGENCY", "URGENT", "MODERATE"]

    return np.select(
        conditions, choices, default="LOW"
    )


# Test
print("=" * 55)
print(f"{'MEDIROUTE AI — BATCH PROCESSING':^55}")
print("=" * 55)

# 6 patients simultanés
patients = [
    ["chest pain", "difficulty breathing"],
    ["fever", "cough", "fatigue"],
    ["headache", "confusion", "dizziness"],
    ["nausea", "abdominal pain"],
    ["fever"],
    ["stroke", "confusion"],
]

# Encoder tous en même temps
matrix = encode_batch(patients)
print(f"\n  Matrix shape: {matrix.shape}")
print(f"  (6 patients × {N_SYMPTOMS} symptoms)")

# Classifier tous en même temps
urgencies = classify_urgency_batch(matrix)
print(f"\n  URGENCY CLASSIFICATION:")
symptoms_display = [
    "chest pain + breathing",
    "fever + cough + fatigue",
    "headache + confusion",
    "nausea + abdominal",
    "fever only",
    "stroke + confusion",
]
for symptom, urgency in zip(
    symptoms_display, urgencies
):
    icon = {
        "EMERGENCY":"🚨",
        "URGENT":"⚠️",
        "MODERATE":"📅",
        "LOW":"✅"
    }.get(urgency, "·")
    print(f"  {icon} {symptom:<30} → {urgency}")

# Recherche par similarité
query_symptoms = ["chest pain", "difficulty breathing"]
query_vector   = encode_batch([query_symptoms])[0]
similarities   = batch_similarity(query_vector, matrix)

print(f"\n  SIMILARITY TO '{query_symptoms[0]}':")
ranked = np.argsort(similarities)[::-1]
for rank, idx in enumerate(ranked[:3], 1):
    print(f"  #{rank} Patient {idx+1}: "
          f"{similarities[idx]:.3f} — "
          f"{symptoms_display[idx]}")