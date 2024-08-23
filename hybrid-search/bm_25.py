import math
from rank_bm25 import BM25Okapi


class CustomBM25Okapi:

    def __init__(self, corpus, k = 1, b = 1):
        self.corpus = corpus
        self.k = k
        self.b = b

    def num(self, tf):
        return tf*(self.k + 1)

    def deno(self, Ld, Lavg, tf):
        return ((self.k * (1 - self.b + self.b * (Ld / Lavg))) + tf)

    def get_scores(self, queries):
        N = len(self.corpus)
        L_avg = sum(len(i) for i in self.corpus) / N
        scores = []
        for corpus in self.corpus:
            scores.append(0)
            for query in queries:
                df = sum(query in i for i in self.corpus)
                N_df = math.log(N / df)
                tf = corpus.count(query)
                len_corpus = len(corpus)

                scores[-1] += (N_df) * (self.k + 1) * tf / self.deno(len_corpus, L_avg, tf)
        return scores


corpus = [
    "The cat, commonly referred to as the domestic cat or house cat, is a small domesticated carnivorous mammal.",
    "The dog is a domesticated descendant of the wolf.",
    "Humans are the most common and widespread species of primate, and the last surviving species of the genus Homo.",
    "The scientific name Felis catus was proposed by Carl Linnaeus in 1758"
]
tokenized_corpus = [doc.split(" ") for doc in corpus]


query = "The cat"
tokenized_query = query.split(" ")

bm25 = BM25Okapi(tokenized_corpus)
doc_scores = bm25.get_scores(tokenized_query)

print(doc_scores)

custom_bm25 = CustomBM25Okapi(tokenized_corpus, 1.5, 0.75)
print(custom_bm25.get_scores(tokenized_query))
