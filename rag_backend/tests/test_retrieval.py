from src.retrieval.retriever import Retriever


def test_retriever_initialization():
    retriever = Retriever()
    assert retriever is not None
