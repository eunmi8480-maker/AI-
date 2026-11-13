"""Windows 연결 스크립트의 HTTP 조회를 Streamlit 서버에서 수행합니다."""
from datetime import datetime, timezone, timedelta
import math
import re
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

KST = timezone(timedelta(hours=9))
YNA_LIST = "https://www.yna.co.kr/report/headline"
SCRAP_ROOT = "https://dnai.scrapmaster.co.kr/dnai/"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "ko-KR,ko;q=0.9"}


def valid_date(value):
    return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")


def parse_pairs(payload, national=False):
    key = "today_1_word_score_pair" if national else "period_member_word_score_pair"
    rows = payload.get(key) if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("해당 날짜의 키워드 데이터가 없습니다.")
    pairs = []
    for row in rows:
        values = list(row.values()) if isinstance(row, dict) else row
        minimum, wi, si = (2, 0, 1) if national else (3, 1, 2)
        if not isinstance(values, (list, tuple)) or len(values) < minimum:
            continue
        word = str(values[wi]).strip() if values[wi] is not None else ""
        try:
            score = float(str(values[si]).replace(",", ""))
        except (ValueError, TypeError):
            continue
        if word and math.isfinite(score) and score > 0:
            pairs.append({"word": word, "score": score})
    if not pairs:
        raise ValueError("응답에서 키워드와 점수를 읽지 못했습니다.")
    return pairs


def fetch_keywords(date, national=False):
    date = valid_date(date)
    if national and date != datetime.now(KST).strftime("%Y-%m-%d"):
        raise ValueError("신문 1면 단어쌍 API는 오늘 자료만 제공합니다. 과거 자료는 직접 불러오세요.")
    headers = {**HEADERS, "Referer": SCRAP_ROOT + "DNA_wordcloud.jsp?sm3ID=gbpr5v-0",
               "Origin": "https://dnai.scrapmaster.co.kr", "X-Requested-With": "XMLHttpRequest",
               "Accept": "application/json, text/javascript, */*; q=0.01"}
    if national:
        response = requests.get(SCRAP_ROOT + "utils/total_word_score/word_score.jsp",
                                headers=headers, timeout=(5, 20))
    else:
        response = requests.post(SCRAP_ROOT + "utils/total_word_score/word_score_by_today_setting.jsp",
                                 headers=headers, data={"user_seq": "981", "start_date": date,
                                 "end_date": date, "pair_type": "1", "removeChecked": "false"},
                                 timeout=(5, 20))
    response.raise_for_status()
    return parse_pairs(response.json(), national)


def headline_candidates(raw, date):
    """목록에서 당일 07:30 제목과 AKR 날짜가 일치하는 링크만 선택합니다."""
    stamp = valid_date(date).replace("-", "")
    soup = BeautifulSoup(raw, "lxml")
    links = []
    for a in soup.select("a[href]"):
        title = a.get_text(" ", strip=True)
        if "헤드라인" not in title or not re.search(r"(?<!\d)07:30(?!\d)", title):
            continue
        url = urljoin(YNA_LIST, a["href"])
        parsed = urlsplit(url)
        if parsed.hostname != "www.yna.co.kr" or not parsed.path.startswith("/view/AKR" + stamp):
            continue
        url = "https://www.yna.co.kr" + parsed.path
        if url not in links:
            links.append(url)
    return links


def parse_headline_article(raw, date):
    soup = BeautifulSoup(raw, "lxml")
    published = soup.select_one('meta[property="article:published_time"]')
    if published is None or not published.get("content"):
        raise ValueError("기사 게시시각을 확인할 수 없습니다.")
    dt = datetime.fromisoformat(published["content"].replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("기사 게시시각의 시간대를 확인할 수 없습니다.")
    if dt.astimezone(KST).strftime("%Y-%m-%d %H:%M") != date + " 07:30":
        raise ValueError("선택한 날짜의 07:30 기사가 아닙니다.")
    title = soup.select_one("h1.tit, h1.tit-article, h1")
    if title is None or "헤드라인" not in title.get_text() or "07:30" not in title.get_text():
        raise ValueError("07:30 헤드라인 기사 제목을 확인할 수 없습니다.")
    body = soup.select_one(".story-news.article")
    if body is None:
        raise ValueError("기사 본문 영역을 찾지 못했습니다.")
    for node in body.select("script, style, figure, aside, .txt-copyright, .ad, .advertisement"):
        node.decompose()
    lines = []
    started = False
    for paragraph in body.find_all("p"):
        text = paragraph.get_text(" ", strip=True)
        if text.startswith("■"):
            started = True
        if not started or not text:
            continue
        if text.startswith("제보는") or "무단 전재" in text or "재배포 금지" in text:
            break
        for a in paragraph.select("a[href]"):
            link = urljoin(YNA_LIST, a["href"])
            if link.startswith("https://www.yna.co.kr/view/"):
                if re.match(r"전문\s*보기", text):
                    text = "전문보기: " + link
                elif link not in text:
                    text += " " + link
        lines.append(text)
    if not any(line.startswith("■") for line in lines):
        raise ValueError("묶음 기사에서 개별 기사 제목을 찾지 못했습니다.")
    return "\n".join(lines)


def _get_html(url):
    response = requests.get(url, headers=HEADERS, timeout=(5, 20))
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def fetch_headlines(date):
    date = valid_date(date)
    urls = headline_candidates(_get_html(YNA_LIST), date)
    if not urls:
        raise ValueError("목록에서 해당 날짜의 07:30 헤드라인을 찾지 못했습니다. 아직 게시 전이거나 목록에 없을 수 있습니다.")
    last_error = None
    for url in urls[:3]:
        try:
            return parse_headline_article(_get_html(url), date), url
        except ValueError as exc:
            last_error = exc
    raise last_error or ValueError("07:30 기사를 확인하지 못했습니다.")


def error_message(exc):
    if isinstance(exc, requests.Timeout):
        return "응답 시간이 초과됐습니다. 직접 입력하거나 다시 수집해 주세요."
    if isinstance(exc, requests.HTTPError):
        return "사이트 요청 실패 (HTTP %s)." % exc.response.status_code
    if isinstance(exc, requests.RequestException):
        return "서버에서 사이트에 연결하지 못했습니다. 직접 입력할 수 있습니다."
    if isinstance(exc, ValueError):
        # HTML/인증 응답 등 원문은 화면에 노출하지 않습니다.
        return str(exc) if not isinstance(exc, requests.exceptions.JSONDecodeError) else "사이트 응답이 JSON이 아닙니다."
    return "자료를 처리하지 못했습니다. 직접 입력할 수 있습니다."
