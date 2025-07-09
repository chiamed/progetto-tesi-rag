from processing.chunker import Chunker

def test_split_text_into_chunks():
    chunker = Chunker()

    # Test with a simple text
    text = "This is a test document. It contains several sentences to be split into chunks."
    chunks = chunker.split_text_into_chunks(text, max_words=10, overlap=2)

    assert len(chunks) == 2, "Should create 2 chunks"
    assert chunks[0] == "This is a test document. It contains several sentences to", "First chunk should match"
    assert chunks[1] == "sentences to be split into chunks.", "Second chunk should match"

    # Test with an empty string
    empty_chunks = chunker.split_text_into_chunks("", max_words=10, overlap=2)
    assert empty_chunks == [], "Empty string should return empty list"

    # Test with a single word
    single_word_chunks = chunker.split_text_into_chunks("Word", max_words=10, overlap=2)
    assert single_word_chunks == ["Word"], "Single word should return itself as a chunk"