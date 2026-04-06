<div align="center">

# 🏥 MediRoute AI

**Décrivez vos symptômes.**
**Recevez une orientation médicale précise en 30 secondes.**

[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Builder](https://img.shields.io/badge/By-Tensoratech-orange)]()

*Un produit [Tensoratech™](https://linkedin.com/company/tensoratech)*

</div>

---

## 🎯 Le Problème

Les gens au UAE et en région MENA cherchent
des réponses médicales sur Google.
Ils obtiennent confusion, anxiété,
et parfois de mauvaises décisions.

**3.2 milliards** de recherches médicales
par an en MENA.
**0** solution locale d'orientation par IA.

---

## 💡 La Solution

MediRoute AI analyse vos symptômes
en langage naturel et vous donne
une action concrète en 30 secondes.
```
Vous décrivez vos symptômes
         ↓
MediRoute AI analyse
         ↓
Niveau d'urgence évalué
         ↓
Spécialiste recommandé
         ↓
Clinique partenaire connectée
         ↓
Rendez-vous confirmé
```

---

## 🏗️ Architecture
```
mediRoute-ai/
│
├── core/          → Moteur central générique
├── domains/       → Modules par domaine
│   ├── medical/   → MediRoute (ACTIF)
│   ├── legal/     → Planifié Q1 2027
│   └── finance/   → Planifié Q2 2027
├── data/          → Data loading & Validation
├── engine/        → ML Classification & Vectors
├── llm/           → LLM Client & Prompt Engine
├── knowledge_base/→ Medical RAG Database
├── agents/        → Autonomous Orchestration
├── api/           → FastAPI Backend
└── app.py         → Streamlit Interface
```

---

## 🛠️ Stack Technique

| Couche | Technologie |
|--------|------------|
| Langage | Python 3.11+ |
| Data | NumPy, Pandas |
| ML | scikit-learn, XGBoost |
| LLM | GPT-4o, LangChain |
| Vector DB | FAISS, ChromaDB |
| API | FastAPI |
| Interface | Streamlit |
| Deployment | Docker, AWS |

---

## 📍 Marché Cible

**UAE / MENA**
- Forte adoption technologique
- Système de santé privatisé
- Barrière linguistique patient/médecin
- Cliniques à la recherche de leads qualifiés

---

## 🗺️ Roadmap

### Phase 1 — Foundation (Mars → Juin 2026)
- [x] Core patient model ✅
- [x] LLM client with retry logic ✅
- [x] Symptom vector engine ✅
- [x] Broadcasting batch processor ✅
- [ ] Pandas data pipeline (Semaine 3)
- [ ] ML urgency classifier (Semaine 8)

### Phase 2 — Intelligence (Juil → Août 2026)
- [ ] RAG medical knowledge base
- [ ] Specialist routing algorithm
- [ ] Risk profiling engine

### Phase 3 — Product (Sept 2026)
- [ ] FastAPI backend
- [ ] Streamlit interface
- [ ] First clinic partner (UAE)
- [ ] MediRoute AI v0.1 launch

---

## 📈 Building in Public

Je construis MediRoute AI en public.
Chaque semaine une mise à jour
sur LinkedIn et GitHub, bientôt sur X aussi.

**Suivez la progression :**
→ [Tensoratech LinkedIn](https://linkedin.com/company/tensoratech)
→ [GitHub](https://github.com/aiengineernlp-dotcom/mediRoute-ai)

---

## ⚠️ Disclaimer

MediRoute AI fournit une **orientation**,
pas un diagnostic médical.
Consultez toujours un professionnel de santé.

---

## 👨‍💻 Auteur

**Erman Willian Tagaintchuem** — Founder @ Tensoratech™

*Building AI solutions for UAE/MENA*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Tensoratech-blue)](https://linkedin.com/company/tensoratech)
```


