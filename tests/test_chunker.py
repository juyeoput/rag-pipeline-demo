# test_chunker.py
import pytest
from chunker import load_and_chunk

def test_chunk_count():
    chunks = load_and_chunk("guide.txt")
    assert len(chunks) == 5

def test_chunk_has_title():
    chunks = load_and_chunk("guide.txt")
    assert chunks[0]["title"] != ""