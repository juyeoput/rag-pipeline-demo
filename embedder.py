# 임베딩 생성

from sentence_transformers import SentenceTransformer
from chunker import load_and_chunk

# 한국어 지원 임베딩 모델 로드
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def embed_chunks(chunks):
    texts= [chunk["full"] for chunk in chunks]
    vectors = model.encode(texts)
    return vectors

if __name__ == "__main__":
    chunks = load_and_chunk("guide.txt")
    vectors = embed_chunks(chunks)

    print(f"청크 수: {len(chunks)}")
    print(f"벡터 1개의 크기: {vectors[0].shape}")
    print(f"벡터 샘플 (앞 5개): {vectors[0][:5]}")