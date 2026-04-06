# mediRoute_ai/engine/patient_scorer.py
"""
MediRoute AI — Vectorized Patient Scorer.
Scores and ranks patients by urgency using
pure NumPy broadcasting.
No loops. No if/else. Pure vectorization.
"""
import numpy as np


def compute_risk_scores(
    ages:        np.ndarray,
    n_symptoms:  np.ndarray,
    has_critical:np.ndarray,
    has_chronic: np.ndarray
) -> np.ndarray:
    """
    Compute risk score for ALL patients at once.

    Formula:
        score = age_factor
              + symptom_factor
              + critical_bonus
              + chronic_bonus

    All operations use broadcasting — no loops.
    """
    # Facteur âge — normalisé entre 0 et 1
    age_factor = np.clip(ages / 100, 0, 1) * 0.3

    # Facteur symptômes
    symptom_factor = np.clip(n_symptoms / 5, 0, 1) * 0.3

    # Bonus symptômes critiques
    critical_bonus = has_critical * 0.3

    # Bonus maladies chroniques
    chronic_bonus  = has_chronic * 0.1

    # Score total — broadcasting sur tous les patients
    scores = (age_factor
             + symptom_factor
             + critical_bonus
             + chronic_bonus)

    return np.clip(scores, 0, 1)


def prioritize_queue(
    patient_ids: np.ndarray,
    scores:      np.ndarray
) -> list[dict]:
    """
    Sort patients by risk score.
    Highest risk = seen first.
    """
    sorted_idx = np.argsort(scores)[::-1]

    urgency_labels = np.select(
        [scores > 0.7, scores > 0.5, scores > 0.3],
        ["EMERGENCY", "URGENT", "MODERATE"],
        default="LOW"
    )

    return [
        {
            "rank":     rank + 1,
            "id":       patient_ids[i],
            "score":    round(float(scores[i]), 3),
            "urgency":  urgency_labels[i],
            "priority": "🚨" if scores[i] > 0.7
                        else "⚠️" if scores[i] > 0.5
                        else "📅" if scores[i] > 0.3
                        else "✅"
        }
        for rank, i in enumerate(sorted_idx)
    ]


# Simulation — 10 patients en salle d'attente
np.random.seed(42)
n = 10

patient_ids   = np.array([f"P{i:03d}"
                           for i in range(1, n+1)])
ages          = np.array([34, 67, 28, 72, 45,
                           19, 55, 38, 81, 42])
n_symptoms    = np.random.randint(1, 6, n)
has_critical  = np.array([1, 0, 0, 1, 0,
                           0, 1, 0, 1, 0])
has_chronic   = np.array([0, 1, 0, 1, 0,
                           0, 0, 1, 1, 0])

scores = compute_risk_scores(
    ages, n_symptoms, has_critical, has_chronic
)
queue  = prioritize_queue(patient_ids, scores)

print("=" * 55)
print(f"{'MEDIROUTE AI — PRIORITY QUEUE':^55}")
print("=" * 55)
print(f"\n  {'Rank':>4} | {'ID':>5} | {'Score':>6} | "
      f"{'Urgency':<10} | Age")
print(f"  {'─'*48}")

for p in queue:
    idx = int(p['id'][1:]) - 1
    print(f"  {p['rank']:>4} | {p['id']:>5} | "
          f"{p['score']:>6.3f} | "
          f"{p['priority']} {p['urgency']:<8} | "
          f"{ages[idx]}")

# Statistiques de la file
print(f"\n  QUEUE STATS:")
print(f"  Emergency : "
      f"{sum(1 for p in queue if p['score']>0.7)}")
print(f"  Urgent    : "
      f"{sum(1 for p in queue if 0.5<p['score']<=0.7)}")
print(f"  Avg score : {scores.mean():.3f}")
print(f"  Max score : {scores.max():.3f}")