"""
keyword_extractor.py
AI 큐레이터 / 조간브리핑용 제목 기반 키워드 추출 모듈

사용 목적
- 기사 본문이 아니라 전달받은 '기사 제목'만 대상으로 분석
- 기본 40개 단일 키워드 추출
- Kiwi 형태소 분석기를 우선 사용하고, 미설치 시 간단한 정규식 방식으로 대체
- 워드클라우드 이미지는 선택적으로 생성

설치:
    pip install kiwipiepy wordcloud matplotlib

기본 사용:
    from keyword_extractor import extract_keywords, create_wordcloud

    titles = ["중소기업 지원 정책 발표", "인공지능 창업기업 투자 확대"]
    keywords = extract_keywords(titles, top_n=40)
    create_wordcloud(keywords, output_path="keyword_wordcloud.png")
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

# 보고서 제목에서 의미가 약하거나 지나치게 일반적인 단어
DEFAULT_STOPWORDS = {
    "오늘", "내일", "어제", "이번", "최근", "지난", "올해", "내년", "작년",
    "관련", "통해", "위해", "대해", "대한", "따라", "따른", "가운데",
    "이후", "이전", "당시", "현재", "계속", "다시", "함께", "모두",
    "기자", "단독", "속보", "종합", "영상", "사진", "전문", "기획",
    "정부", "우리", "한국", "국내", "세계", "가장", "첫", "새로운",
    "것", "수", "등", "및", "때", "곳", "중", "후", "전",
}

# Kiwi 품사 중 제목 키워드로 활용할 품사
_ALLOWED_TAG_PREFIXES = ("NN", "SL", "SH")
_ALLOWED_TAGS = {"XR"}


def _normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"[^0-9A-Za-z가-힣一-龥\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _tokenize_with_kiwi(text: str, kiwi) -> list[str]:
    tokens = []
    for token in kiwi.tokenize(text):
        word = token.form.strip()
        tag = token.tag
        if len(word) < 2:
            continue
        if not (tag.startswith(_ALLOWED_TAG_PREFIXES) or tag in _ALLOWED_TAGS):
            continue
        tokens.append(word)
    return tokens


def _tokenize_fallback(text: str) -> list[str]:
    # Kiwi가 설치되지 않은 환경을 위한 단순 대체 방식.
    # 한국어 형태소 분석 수준의 정확도는 제공하지 않음.
    return re.findall(r"[가-힣]{2,}|[A-Za-z]{2,}|[0-9A-Za-z가-힣]{2,}", text)


def extract_keywords(
    titles: Iterable[str],
    top_n: int = 40,
    stopwords: Iterable[str] | None = None,
    min_count: int = 1,
) -> list[tuple[str, int]]:
    """
    제목 목록에서 빈도순 단일 키워드를 반환한다.

    Args:
        titles: 기사 제목 문자열의 iterable
        top_n: 반환할 키워드 수 (기본 40)
        stopwords: 추가 제외 단어
        min_count: 최소 출현 빈도

    Returns:
        [(키워드, 빈도), ...] 형태의 리스트
    """
    blocked = set(DEFAULT_STOPWORDS)
    if stopwords:
        blocked.update(str(w).strip() for w in stopwords if str(w).strip())

    try:
        from kiwipiepy import Kiwi
        kiwi = Kiwi()
    except ImportError:
        kiwi = None

    counts: Counter[str] = Counter()
    for title in titles:
        normalized = _normalize(title)
        if not normalized:
            continue
        words = (
            _tokenize_with_kiwi(normalized, kiwi)
            if kiwi is not None
            else _tokenize_fallback(normalized)
        )
        for word in words:
            word = word.strip()
            if len(word) < 2 or word in blocked:
                continue
            if word.isdigit():
                continue
            counts[word] += 1

    ranked = [(word, count) for word, count in counts.most_common() if count >= min_count]
    return ranked[:max(0, int(top_n))]


def create_wordcloud(
    keywords: Sequence[tuple[str, int]],
    output_path: str | Path = "keyword_wordcloud.png",
    font_path: str | None = None,
    width: int = 1200,
    height: int = 700,
) -> str:
    """
    추출 결과로 워드클라우드 PNG를 생성하고 저장 경로를 반환한다.
    한글 폰트 경로를 지정하는 것을 권장한다.
    """
    if not keywords:
        raise ValueError("워드클라우드를 만들 키워드가 없습니다.")

    try:
        from wordcloud import WordCloud
    except ImportError as exc:
        raise ImportError(
            "워드클라우드 생성에는 wordcloud 패키지가 필요합니다. "
            "pip install wordcloud 를 실행하세요."
        ) from exc

    frequencies = {word: count for word, count in keywords}
    cloud = WordCloud(
        width=width,
        height=height,
        background_color="white",
        font_path=font_path,
        collocations=False,
        max_words=len(frequencies),
    ).generate_from_frequencies(frequencies)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cloud.to_file(str(destination))
    return str(destination)


def extract_keywords_from_articles(
    articles: Iterable[dict],
    title_key: str = "title",
    top_n: int = 40,
    stopwords: Iterable[str] | None = None,
) -> list[tuple[str, int]]:
    """기사 딕셔너리 목록에서 제목 필드만 뽑아 키워드를 추출하는 편의 함수."""
    titles = [
        str(article.get(title_key, "")).strip()
        for article in articles
        if isinstance(article, dict) and article.get(title_key)
    ]
    return extract_keywords(titles, top_n=top_n, stopwords=stopwords)


if __name__ == "__main__":
    sample_titles = [
        "중소기업 인공지능 전환 지원 확대",
        "인공지능 창업기업 투자 활성화 방안 발표",
        "중소기업 기술혁신과 창업 생태계 강화",
    ]
    result = extract_keywords(sample_titles, top_n=40)
    for keyword, count in result:
        print(f"{keyword}\t{count}")
