from app.services.rag import MissionRAG


def test_sector7_retrieval():
    rag = MissionRAG("data/sample")
    docs = rag.retrieve("Sector 7 communications outage", top_k=2)
    assert docs
    assert docs[0].source.startswith("sector7")
