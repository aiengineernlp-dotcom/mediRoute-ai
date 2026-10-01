# assessment_engine.py
"""
MediRoute AI Assessment Engine using OOP + Inheritance.
Use case: Analyze symptoms and route to correct specialist.
MediRoute AI: Core intelligence layer.
"""


class BaseAssessment:
    """
    Abstract base class for all assessments.
    Defines the interface every assessment must implement.
    Mirrors sklearn's BaseEstimator pattern.
    """

    def __init__(self, name: str, version: str = "1.0"):
        self.name    = name
        self.version = version
        self._calls  = 0

    def analyze(self, symptoms: list[str]) -> dict:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement analyze()"
        )

    def __call__(self, symptoms: list[str]) -> dict:
        """Makes the object callable — like sklearn's predict."""
        self._calls += 1
        result = self.analyze(symptoms)
        return {**result, "assessed_by": self.name,
                "version": self.version}

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"(name={self.name}, calls={self._calls})")


class UrgencyClassifier(BaseAssessment):
    """Classifies medical urgency from symptoms."""

    LEVELS = {
        "emergency": {
            "symptoms": {
                "chest pain", "heart attack", "stroke",
                "unconscious", "severe bleeding",
                "difficulty breathing", "anaphylaxis"
            },
            "action":   "🚨 Call 911 immediately",
            "timeframe":"NOW"
        },
        "urgent": {
            "symptoms": {
                "high fever", "severe headache",
                "persistent vomiting", "confusion",
                "severe abdominal pain"
            },
            "action":   "⚠️ Go to urgent care",
            "timeframe":"Within 2-4 hours"
        },
        "moderate": {
            "symptoms": {
                "fever", "cough", "headache",
                "fatigue", "nausea", "dizziness"
            },
            "action":   "📅 See doctor today",
            "timeframe":"Within 24 hours"
        }
    }

    def __init__(self):
        super().__init__("Urgency Classifier", "2.0")

    def analyze(self, symptoms: list[str]) -> dict:
        symptoms_lower = {s.lower() for s in symptoms}

        for level, config in self.LEVELS.items():
            if symptoms_lower & config["symptoms"]:
                matched = list(
                    symptoms_lower & config["symptoms"]
                )
                return {
                    "urgency":   level.upper(),
                    "action":    config["action"],
                    "timeframe": config["timeframe"],
                    "matched":   matched
                }

        return {
            "urgency":   "LOW",
            "action":    "📋 Schedule routine appointment",
            "timeframe": "Within 1 week",
            "matched":   []
        }


class SpecialistRouter(BaseAssessment):
    """Routes patient to appropriate medical specialist."""

    ROUTING_MAP = {
        "Cardiologist":      ["chest", "heart", "palpitation"],
        "Pulmonologist":     ["breathing", "lung", "asthma","cough"],
        "Neurologist":       ["headache", "migraine", "seizure",
                              "confusion", "stroke"],
        "Gastroenterologist":["stomach", "abdominal", "nausea",
                              "vomiting", "digestive"],
        "Dermatologist":     ["skin", "rash", "itching", "acne"],
        "Orthopedist":       ["bone", "joint", "fracture", "back"],
        "Psychiatrist":      ["anxiety", "depression", "mental",
                              "stress"],
        "Endocrinologist":   ["diabetes", "thyroid", "hormonal"],
    }

    def __init__(self):
        super().__init__("Specialist Router", "1.5")

    def analyze(self, symptoms: list[str]) -> dict:
        text = " ".join(symptoms).lower()
        matched = {}

        for specialist, keywords in self.ROUTING_MAP.items():
            hits = [k for k in keywords if k in text]
            if hits:
                matched[specialist] = hits

        if not matched:
            return {
                "specialists": ["General Practitioner"],
                "reason":      "No specific match found",
                "confidence":  "low"
            }

        primary = max(matched, key=lambda k: len(matched[k]))
        return {
            "specialists": list(matched.keys()),
            "primary":     primary,
            "reason":      f"Matched: {matched[primary]}",
            "confidence":  "high" if len(matched[primary]) > 1
                           else "medium"
        }


class RiskProfiler(BaseAssessment):
    """Profiles patient risk based on age and symptoms."""

    def __init__(self):
        super().__init__("Risk Profiler", "1.0")

    def analyze(self, symptoms: list[str],
                age: int = 0) -> dict:
        risk_score = 0

        # Score basé sur symptômes
        high_risk = {"chest pain", "difficulty breathing",
                     "unconscious", "stroke"}
        risk_score += sum(
            3 for s in symptoms
            if s.lower() in high_risk
        )
        risk_score += len(symptoms) * 0.5

        # Score basé sur âge
        if age > 65:   risk_score += 2
        elif age > 45: risk_score += 1

        # Classification
        if risk_score >= 5:
            profile = "HIGH"
        elif risk_score >= 2:
            profile = "MEDIUM"
        else:
            profile = "LOW"

        return {
            "risk_profile": profile,
            "risk_score":   round(risk_score, 1),
            "factors":      len(symptoms)
        }


class MediRouteEngine:
    """
    Main MediRoute AI engine.
    Orchestrates all assessments — like a LangChain chain.
    """

    def __init__(self):
        self.urgency_classifier = UrgencyClassifier()
        self.specialist_router  = SpecialistRouter()
        self.risk_profiler      = RiskProfiler()

    def assess(self, name: str, age: int,
               symptoms: list[str]) -> dict:
        """Full patient assessment pipeline."""
        urgency    = self.urgency_classifier(symptoms)
        routing    = self.specialist_router(symptoms)
        risk       = self.risk_profiler.analyze(symptoms, age)

        return {
            "patient":    {"name": name, "age": age},
            "symptoms":   symptoms,
            "urgency":    urgency,
            "routing":    routing,
            "risk":       risk,
        }

    def display_report(self, result: dict) -> None:
        p = result["patient"]
        print(f"\n{'=' * 55}")
        print(f"{'MEDIROUTE AI — ASSESSMENT REPORT':^55}")
        print("=" * 55)
        print(f"  Patient  : {p['name']} | Age: {p['age']}")
        print(f"  Symptoms : {', '.join(result['symptoms'])}")
        print(f"\n  URGENCY  : {result['urgency']['urgency']}")
        print(f"  Action   : {result['urgency']['action']}")
        print(f"  Timeframe: {result['urgency']['timeframe']}")
        print(f"\n  SPECIALIST: "
              f"{result['routing'].get('primary', 'GP')}")
        print(f"  Confidence: "
              f"{result['routing'].get('confidence', 'low')}")
        print(f"\n  RISK     : {result['risk']['risk_profile']}")
        print(f"  Score    : {result['risk']['risk_score']}")
        print("=" * 55)


# Test MediRoute Engine
engine = MediRouteEngine()

test_cases = [
    ("John",  34, ["chest pain", "difficulty breathing"]),
    ("Sara",  28, ["fever", "cough", "fatigue"]),
    ("Bob",   72, ["headache", "confusion", "dizziness"]),
    ("Alice", 45, ["skin rash", "itching"]),
]

for name, age, symptoms in test_cases:
    result = engine.assess(name, age, symptoms)
    engine.display_report(result)