# 유사도 검색

from sklearn.metrics.pairwise import cosine_similarity
from chunker import load_and_chunk
from embedder import embed_chunks, model

def search(query, chunks, vectors, top_k=2):
    # 검색어 벡터 변환
    query_vector = model.encode([query])

    # 검색어 벡터 vs 모든 청크 벡터 유사도 계산
    similarities = cosine_similarity(query_vector, vectors)[0]

    ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)

    print(f"\n 검색어: '{query}'")
    print("-" * 40)
    for i, (idx, score) in enumerate(ranked[:top_k]):
        print(f"[{i+1}위] {chunks[idx]['title']}")
        print(f"유사도: {score:.4f}")
        print(f"내용: {chunks[idx]['content'][:50]}...")
        print()

if __name__ == "__main__":
    chunks = load_and_chunk("guide.txt")
    vectors = embed_chunks(chunks)

    search("비밀번호 인증 방법", chunks, vectors)
    search("파일 올리는 방법", chunks, vectors)
    search("접근 권한 설정", chunks, vectors)