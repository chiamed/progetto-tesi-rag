from retriever.indexer import Indexer

def test_index_document():
    # Test for indexing a valid document
    file_path = "tests/test_files/sample.pdf"
    source_name = "sample_source"
    model = "openai"

    indexer = Indexer()
    indexed_result = indexer.index_document(file_path, source_name, model)

    assert indexed_result is True, "Document should be indexed successfully"