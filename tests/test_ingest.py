from pinecrest.ingest import chunk_text, load_documents


def test_chunk_text_splits_long_text():
    assert len(chunk_text("a" * 650)) == 3


def test_documents_load():
    assert len(load_documents()) > 0
