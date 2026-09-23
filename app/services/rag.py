from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievedDocument:
    source: str
    text: str
    score: float


class MissionRAG:
    """Small, dependency-light RAG layer for the public demo.

    Production replacement: OpenSearch, pgvector, Azure AI Search, or another
    agency-approved vector/search service with document-level ACL filtering.
    """

    def __init__(self, data_dir: str = "data/sample") -> None:
        root = Path(data_dir)
        self.docs: list[tuple[str, str]] = []
        for path in sorted(root.glob("*.txt")):
            self.docs.append((path.name, path.read_text(encoding="utf-8")))
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([d[1] for d in self.docs]) if self.docs else None

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedDocument]:
        if not self.docs or self.matrix is None:
            return []
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranked = scores.argsort()[::-1][:top_k]
        return [
            RetrievedDocument(self.docs[i][0], self.docs[i][1], float(scores[i]))
            for i in ranked
            if scores[i] > 0
        ]
