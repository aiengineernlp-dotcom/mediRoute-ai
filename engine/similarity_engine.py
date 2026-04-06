# mediRoute_ai/engine/similarity_engine.py
"""
MediRoute AI — Vectorized Similarity Engine.
Finds similar historical cases using matrix operations.
This is the core of the RAG retrieval system.
Broadcasting replaces all loops.
"""
import numpy as np


def cosine_similarity_matrix(
    queries:   np.ndarray,
    documents: np.ndarray
) -> np.ndarray:
    """
    Compute ALL pairwise similarities at once.

    Args:
        queries   : shape (n_queries, dim)
        documents : shape (n_docs, dim)

    Returns:
        similarity matrix (n_queries, n_docs)

    Broadcasting magic:
        queries @ documents.T
        → every query vs every document
        in ONE operation
    """
    # Normaliser les deux matrices
    q_norms = np.linalg.norm(
        queries, axis=1, keepdims=True
    )
    d_norms = np.linalg.norm(
        documents, axis=1, keepdims=True
    )

    q_normalized = queries   / (q_norms + 1e-8)
    d_normalized = documents / (d_norms + 1e-8)

    # Produit matriciel = toutes les similarités
    return q_normalized @ d_normalized.T


def batch_retrieve(
    query_vectors:    np.ndarray,
    doc_vectors:      np.ndarray,
    doc_metadata:     list[dict],
    top_k:            int = 3
) -> list[list[dict]]:
    """
    Retrieve top-k similar documents
    for EACH query simultaneously.

    Args:
        query_vectors : (n_queries, dim)
        doc_vectors   : (n_docs, dim)
        doc_metadata  : list of doc info dicts
        top_k         : results per query

    Returns:
        list of lists — top_k docs per query
    """
    sim_matrix = cosine_similarity_matrix(
        query_vectors, doc_vectors
    )

    results = []
    for query_sims in sim_matrix:
        top_indices = np.argsort(query_sims)[::-1][:top_k]
        query_results = [
            {
                **doc_metadata[i],
                "similarity": round(
                    float(query_sims[i]), 4
                )
            }
            for i in top_indices
        ]
        results.append(query_results)

    return results


# Simulation — base de connaissances médicales
np.random.seed(42)
DIM = 16  # dimension des embeddings

# Documents médicaux (simulés)
n_docs = 8
doc_vectors = np.random.randn(n_docs, DIM)
doc_metadata = [
    {"id": "D001", "title": "Chest Pain Protocol",
     "specialist": "Cardiologist",    "urgency": "HIGH"},
    {"id": "D002", "title": "Respiratory Infection",
     "specialist": "GP",              "urgency": "LOW"},
    {"id": "D003", "title": "Neurological Emergency",
     "specialist": "Neurologist",     "urgency": "HIGH"},
    {"id": "D004", "title": "Migraine Protocol",
     "specialist": "Neurologist",     "urgency": "MOD"},
    {"id": "D005", "title": "GI Issues",
     "specialist": "Gastroenterologist","urgency":"MOD"},
    {"id": "D006", "title": "Diabetes Management",
     "specialist": "Endocrinologist", "urgency": "LOW"},
    {"id": "D007", "title": "Anxiety Protocol",
     "specialist": "Psychiatrist",    "urgency": "LOW"},
    {"id": "D008", "title": "Cardiac Arrhythmia",
     "specialist": "Cardiologist",    "urgency": "HIGH"},
]

# 3 nouveaux patients simultanés
n_queries    = 3
query_vectors = np.random.randn(n_queries, DIM)
query_labels  = [
    "Patient A: chest pain + breathing",
    "Patient B: headache + confusion",
    "Patient C: fever + cough",
]

# Récupération en batch
results = batch_retrieve(
    query_vectors,
    doc_vectors,
    doc_metadata,
    top_k=2
)

print("=" * 60)
print(f"{'MEDIROUTE AI — BATCH RAG RETRIEVAL':^60}")
print("=" * 60)

for query_label, query_results in zip(
    query_labels, results
):
    print(f"\n  {query_label}")
    for r in query_results:
        print(f"    → [{r['urgency']}] "
              f"{r['title']:<30} "
              f"({r['similarity']:.3f})")
        print(f"       Specialist: {r['specialist']}")

# Matrice de similarité complète
sim_matrix = cosine_similarity_matrix(
    query_vectors, doc_vectors
)
print(f"\n  Similarity matrix shape: {sim_matrix.shape}")
print(f"  ({n_queries} queries × {n_docs} documents)")