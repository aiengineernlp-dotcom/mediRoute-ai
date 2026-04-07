# MediRoute AI — Architecture Définitive
# Ne jamais changer sans décision explicite

## PRINCIPE FONDAMENTAL
Un seul moteur central générique.
Les domaines sont des plugins indépendants.
On ne duplique jamais le moteur.
On change uniquement les règles du domaine.

## STRUCTURE DÉFINITIVE

mediRoute-ai/
│
├── core/               ← MOTEUR CENTRAL  → Moteur central générique
│   ├── base.py         ← interfaces abstraites
│   ├── engine.py       ← pipeline générique
│   ├── classifier.py   ← classification générique
│   └── router.py       ← routing générique
│── data/               → Data loading & Validation
├── domains/            ← PLUGINS DOMAINES   → Modules par domaine
│   ├── medical/        ← MediRoute (ACTIF)  → MediRoute (ACTIF)
│   │   ├── rules.py
│   │   ├── vocab.py
│   │   └── routing.py
│   ├── legal/          ← Q1 2027 → Planifié Q1 2027
│   └── finance/        ← Q2 2027 → Planifié Q2 2027
│
├── engine/             ← TRAITEMENT  → ML Classification & Vectors
│   ├── symptom_vectors.py
│   ├── similarity_engine.py
│   └── patient_scorer.py
│
├── llm/                ← LLM LAYER → LLM Client & Prompt Engine
│   ├── client.py
│   ├── prompts.py
│   └── parser.py
│── tests/              ← TESTS
├── knowledge_base/     ← RAG (Jour 56) → Medical RAG Database
├── agents/             ← AGENT (Jour 60) → Autonomous Orchestration
├── api/                ← FASTAPI (Jour 58) → FastAPI Backend
└── app.py              ← STREAMLIT (Jour 58)   -> → Streamlit Interface



## DÉCISIONS FIGÉES
1. Moteur générique → jamais dupliqué
2. Medical = premier domaine actif
3. GitHub public + LinkedIn Tensoratech
4. MVP septembre 2026 = Streamlit + LLM
5. Marché cible = UAE/MENA

## ROADMAP PAR JOUR
Jour 1-8   ✅ Python complet
Jour 9-10  ✅ NumPy complet
Jour 11-13 → Pandas → data/loader.py
Jour 30-36 → ML → domains/medical/classifier.py
Jour 49    → RAG → knowledge_base/
Jour 52    → Prompts → llm/prompts.py
Jour 56    → RAG médical complet
Jour 58    → FastAPI + Streamlit → app.py
Jour 60    → Agent → agents/mediRoute_agent.py