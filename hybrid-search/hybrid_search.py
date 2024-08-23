import numpy as np
from rank_bm25 import BM25Okapi

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


def scores_to_ranking(scores: list[float]) -> list[int]:
    return list(np.argsort(scores)[::-1] + 1)

def rrf(keyword_rank: int, semantic_rank: int) -> float:
    k = 60
    rrf_score = 1 / (k + keyword_rank) + 1 / (k + semantic_rank)
    return rrf_score

def hybrid_search(
    query: str,
    corpus: list[str],
    encoder_model: SentenceTransformer
) -> list[int]:
    # BM25
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    tokenized_query = query.split(" ")
    bm25 = BM25Okapi(tokenized_corpus)
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_ranking = scores_to_ranking(bm25_scores)

    # Embedding
    document_embeddings = model.encode(corpus)
    query_embedding = model.encode(query)

    cos_sim_scores = cos_sim(
        document_embeddings,
        query_embedding
    ).flatten().tolist()

    cos_sim_ranking = scores_to_ranking(cos_sim_scores)

    # combine rankings into RRF scores
    hybrid_scores = []

    for i, doc in enumerate(corpus):
        document_ranking = rrf(bm25_ranking[i], cos_sim_ranking[i])
        print(f"Document {i} has the rrf score {document_ranking}")

        hybrid_scores.append(document_ranking)

    hybrid_ranking = scores_to_ranking(hybrid_scores)

    return hybrid_ranking

if __name__ == "__main__":
    sent_trans = "sentence-transformers/all-MiniLM-L6-v2"
    sent_trans = "sentence-transformers/all-MiniLM-L12-v2"
    model = SentenceTransformer(sent_trans)
    corpus = [
    "The cat, commonly referred to as the domestic cat or house cat, is a small domesticated carnivorous mammal.",
    "The dog is a domesticated descendant of the wolf.",
    "Humans are the most common and widespread species of primate, and the last surviving species of the genus Homo.",
    "The scientific name Felis catus was proposed by Carl Linnaeus in 1758"]

    hybrid_ranking = hybrid_search(
        query="What is the scientific name for cats?",
        corpus=corpus,
        encoder_model=model
    )

    print(hybrid_ranking)
