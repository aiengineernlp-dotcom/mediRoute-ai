# MediRoute AI — How to Use This Repository

## Pour le mentor AI (début de chaque session)

Envoie ces 3 liens au début de chaque session :
```
Context    : https://github.com/aiengineernlp-dotcom/mediRoute-ai/blob/main/docs/CONTEXT.md
Architecture: https://github.com/aiengineernlp-dotcom/mediRoute-ai/blob/main/docs/ARCHITECTURE.md
Decisions  : https://github.com/aiengineernlp-dotcom/mediRoute-ai/blob/main/docs/DECISIONS.md
```

---

## Structure complète et rôle de chaque fichier
```
mediRoute-ai/
│
├── docs/                        ← Documentation de session
│   ├── CONTEXT.md               ← Qui je suis + où j'en suis
│   ├── ARCHITECTURE.md          ← Décisions d'architecture figées
│   ├── DECISIONS.md             ← Journal des décisions importantes
│   └── HOW_TO_USE.md            ← Ce fichier
│
├── core/                        ← MOTEUR CENTRAL GÉNÉRIQUE
│   ├── __init__.py
│   ├── base.py                  ← Interfaces abstraites (BaseAssessment)
│   ├── engine.py                ← Pipeline principal (analyze→classify→route)
│   ├── classifier.py            ← Classification générique
│   └── router.py                ← Routing générique vers experts
│
├── domains/                     ← PLUGINS DOMAINES (ne jamais toucher core/)
│   ├── __init__.py
│   ├── medical/                 ← MediRoute — ACTIF
│   │   ├── __init__.py
│   │   ├── rules.py             ← Règles médicales + urgence
│   │   ├── vocab.py             ← Vocabulaire symptômes
│   │   └── routing.py          ← Map symptômes → spécialistes
│   ├── legal/                   ← LegalRoute — Planifié Q1 2027
│   │   ├── __init__.py
│   │   └── rules.py             ← Placeholder
│   └── finance/                 ← FinanceRoute — Planifié Q2 2027
│       ├── __init__.py
│       └── rules.py             ← Placeholder
│
├── data/                        ← COUCHE DONNÉES
│   ├── __init__.py
│   ├── loader.py                ← Charger CSV/JSON patients
│   ├── validator.py             ← Valider les inputs avant traitement
│   └── samples/                 ← Données de test (patients fictifs)
│
├── engine/                      ← TRAITEMENT ML + VECTORISATION
│   ├── __init__.py
│   ├── symptom_vectors.py       ← Encoder symptômes en vecteurs NumPy
│   ├── similarity_engine.py     ← Recherche cosinus entre patients
│   ├── patient_scorer.py        ← Score de risque par broadcasting
│   ├── urgency_classifier.py    ← Classifier ML (Jour 30-36)
│   └── rag_search.py            ← Recherche RAG dans knowledge_base (Jour 56)
│
├── llm/                         ← COUCHE LLM
│   ├── __init__.py
│   ├── client.py                ← Appel API OpenAI/Anthropic + retry
│   ├── prompts.py               ← Tous les prompt templates
│   └── parser.py                ← Parser les outputs LLM
│
├── knowledge_base/              ← BASE DE CONNAISSANCES MÉDICALES (Jour 56)
│   ├── __init__.py
│   ├── medical_docs/            ← Documents médicaux bruts
│   └── vector_store/            ← Index FAISS des embeddings
│
├── agents/                      ← ORCHESTRATION AUTONOME (Jour 60)
│   ├── __init__.py
│   └── mediRoute_agent.py       ← Agent LangChain principal
│
├── api/                         ← BACKEND FASTAPI (Jour 58)
│   ├── __init__.py
│   └── routes.py                ← Endpoints REST
│
├── tests/                       ← TESTS
│   └── __init__.py
│
├── app.py                       ← INTERFACE STREAMLIT (Jour 58)
├── requirements.txt             ← Dépendances Python
├── .env.example                 ← Template variables d'environnement
├── .gitignore                   ← Fichiers exclus de Git
└── LICENSE                      ← MIT License
```

---

## Comment les fichiers communiquent
```
app.py
  └── agents/mediRoute_agent.py
        ├── core/engine.py
        │     ├── core/classifier.py
        │     │     ├── domains/medical/rules.py
        │     │     └── engine/urgency_classifier.py
        │     ├── core/router.py
        │     │     └── domains/medical/routing.py
        │     └── engine/symptom_vectors.py
        ├── llm/client.py
        │     ├── llm/prompts.py
        │     └── llm/parser.py
        ├── engine/rag_search.py
        │     └── knowledge_base/
        └── data/loader.py
              └── data/validator.py
```

---

## Règles fondamentales
```
1. Ne jamais modifier core/ pour un domaine
   → modifier uniquement domains/[domaine]/

2. Ne jamais mettre de clés API dans le code
   → utiliser .env uniquement

3. Un commit par session minimum
   → message clair : "feat: [ce que tu as ajouté]"

4. Mettre à jour docs/CONTEXT.md après chaque session
   → changer le jour actuel et le prochain

5. mediRoute_data/ et __pycache__/ ne se committent jamais
   → ils sont dans .gitignore
```

---

## Roadmap des fichiers par jour de batch
```
Jour 7-10  ✅  llm/client.py
               llm/parser.py
               llm/prompts.py
               core/patient.py (dans core/)
               data/loader.py
               data/validator.py
               engine/symptom_vectors.py
               engine/similarity_engine.py
               engine/patient_scorer.py

Jour 11-13     data/loader.py amélioré avec Pandas
               data/validator.py amélioré

Jour 30-36     engine/urgency_classifier.py
               domains/medical/rules.py complété

Jour 49        engine/rag_search.py commencé
               knowledge_base/medical_docs/ rempli

Jour 52        llm/prompts.py complété
               llm/parser.py complété

Jour 56        knowledge_base/ complet
               engine/rag_search.py complet

Jour 58        api/routes.py
               app.py

Jour 60        agents/mediRoute_agent.py
               MediRoute AI v0.1 COMPLET
```