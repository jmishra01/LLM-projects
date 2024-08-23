from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

corpus = [
    "The cat, commonly referred to as the domestic cat or house cat, is a small domesticated carnivorous mammal.",
    "The dog is a domesticated descendant of the wolf.",
    "Humans are the most common and widespread species of primate, and the last surviving species of the genus Homo.",
    "The scientific name Felis catus was proposed by Carl Linnaeus in 1758"
]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

document_embeddings = model.encode(corpus)

print(document_embeddings.shape)

query = "The cat"

query_embedding = model.encode(query)

scores = cos_sim(document_embeddings, query_embedding)

print(scores)

query_embedding_feline = model.encode("feline")
scores = cos_sim(document_embeddings, query_embedding_feline)
print(scores)
