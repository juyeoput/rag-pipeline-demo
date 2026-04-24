# 영향 받는 섹션 탐지 및 AI 수정 제안 생성

import anthropic
from chunker import load_and_chunk
from embedder import embed_chunks, model
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv
import os

load_dotenv()

THRESHOLD = 0.5
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_update_suggestion(change_description, affected_chunks):
    chunks_text = "\n".join([
        f"- {c['title']}: {c['content']}"
        for c in affected_chunks
    ])

    prompt = f"""소프트웨어 기능이 다음과 같이 변경되었습니다:
변경 내용: {change_description}

아래 사용자 가이드 섹션들이 영향을 받습니다:
{chunks_text}

각 섹션별로 어떤 내용을 수정해야 하는지 구체적으로 알려주세요."""
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def detect_affected_guides(change_description, chunks, vectors):
    change_vector = model.encode([change_description])
    similarities = cosine_similarity(change_vector, vectors)[0]

    print(f"\n 기능 변경: {change_description}")
    print('=' * 45)

    affected = []
    for idx, score in enumerate(similarities):
        if score >= THRESHOLD:
            affected.append((idx, score, chunks[idx]))

    affected.sort(key=lambda x: x[1], reverse=True)

    if affected:
        print(f"'업데이트 필요한 가이드' :")
        print('-' * 45)
        for idx, score, chunk in affected:
            print(f" {chunk['title']} (유사도: {score:.4f})")

        print("\n AI 수정 제안:")
        print("-" * 45)
        affected_chunks = [c for _,_, c in affected]
        suggestion = generate_update_suggestion(change_description, affected_chunks)
        print(suggestion)
    else:
        print("영향받는 가이드 없음")
    print()


if __name__ == "__main__":
    chunks = load_and_chunk("guide.txt")
    vectors = embed_chunks(chunks)
    
    # 시나리오 1: 로그인 방식 변경
    detect_affected_guides(
        "이메일 로그인 대신 소셜 로그인으로 변경됨",
        chunks, vectors
    )
    
    # 시나리오 2: 파일 크기 제한 변경
    detect_affected_guides(
        "최대 파일 크기가 10MB에서 50MB로 변경됨",
        chunks, vectors
    )
    
    # 시나리오 3: 권한 체계 변경
    # 임베딩 기반 유사도 검색의 한계. 신조어나 새로운 개념 추가될 때 감지 어려움.
    # 보완하기 위해서 키워드 매칭과 병행하거나 threshold 튜닝이 필요
    detect_affected_guides(
        "권한 종류에 '편집자' 등급이 새로 추가됨",
        chunks, vectors
    )