# 의미 단위로 분해

def load_and_chunk(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    sections = content.strip().split("\n##")
    # print(sections)

    chunks = []

    # 단락 단위
    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue

        title = lines[0].replace("#", "").strip()
        body = " ".join(line.strip() for line in lines[1:] if line.strip())

        if title and body:
            chunks.append({
                "title": title,
                "content": body,
                "full": f"{title}: {body}"
            })
    return chunks

if __name__ == "__main__":
    chunks = load_and_chunk("guide.txt")
    for i, chunk in enumerate(chunks):
        print(f"[청크 {i+1}] {chunk['title']}")
        print(f" -> {chunk['content'][:60]}...")
        print()

