# rag-pipeline-demo

소프트웨어 기능 변경 시 수정이 필요한 사용자 가이드 섹션을 자동으로 탐지하고 수정 제안을 생성하는 파이프라인입니다.

## 기술 스택
- Python 3.10
- sentence-transformers
- scikit-learn
- Claude API

## 실행 방법
```bash
pip install sentence-transformers scikit-learn anthropic python-dotenv
```

.env 파일에 API 키 추가:
```
ANTHROPIC_API_KEY=your_api_key
```

```bash
python detector.py
```

## 한계 및 개선 방향
신조어나 새로운 개념이 추가될 때 감지가 어려우며 키워드 매칭을 병행하거나 threshold 튜닝으로 보완할 수 있습니다.
git diff나 릴리즈 노트를 자동으로 파싱하는 것을 통해 자동화가 가능합니다. 
