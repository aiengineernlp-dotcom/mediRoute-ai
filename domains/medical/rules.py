"""
MediRoute AI - Medical Domain Configuration
All medical specific rules live here. // tous les regles specifique au medicale sont ici
The core engine never imports this directly - it receives it as configuration //  cet fichier est un utiliser pour la configuration dans le dossier core engine
"""

MEDICAL_CONFIG = {
    "domain": "medical",
    "version": "1.0",
    "language": ["en", "ar", "fr"],

    "urgency_levels": [
        "LOW", "MODERATE", "URGENT", "EMERGENCY"
    ],

    "critical_keywords": ["chest pain", "stroke", "unconscious", "severe bleeding", "difficulty breathing",
                          "heart attack", "anaphylaxis"],

    "specialist_map": {

        "chest": "Cardiologist",
        "heart": "Cardiologist",
        "breathing": "Pulmonologist",
        "headache": "Neurologist",
        "stroke": "Neurologist",
        "skin": "Dermatologist",
        "stomach": "Gastroenterologist",
        "fever": "General Practitioner",
    },
    "market": "UAE/MENA",
    "disclaimer": (
        "MediRoute AI provides orientation only. "
        "Always consults a qualified medical professionnal."
    )
}

# print(MEDICAL_CONFIG["disclaimer"])






