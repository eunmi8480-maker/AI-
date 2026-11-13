"""Streamlit 서버에서 ScrapMaster 키워드를 수집하고 HTML iframe에 주입합니다."""
from datetime import date, datetime
import json
import math
import os

import requests
import streamlit as st

ORIGIN = 'https://dnai.scrapmaster.co.kr'
REFERRER = ORIGIN + '/dnai/DNA_wordcloud.jsp?sm3ID=gbpr5v-0'
HEADERS = {
    'Referer': REFERRER,
    'Origin': ORIGIN,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
}


def _user_seq():
    # 배포에서는 Streamlit Secrets에 SCRAPMASTER_USER_SEQ를 등록하세요.
    try:
        value = st.secrets.get('SCRAPMASTER_USER_SEQ')
    except (FileNotFoundError, KeyError):
        value = None
    value = value or os.getenv('SCRAPMASTER_USER_SEQ')
    if not value:
        raise ValueError('Streamlit Secrets에 SCRAPMASTER_USER_SEQ를 등록해 주세요.')
    return str(value)


def _rows_to_pairs(rows, word_column, score_column):
    result = []
    if not isinstance(rows, list):
        raise ValueError('ScrapMaster 응답의 키워드 목록 형식이 바뀌었습니다.')
    for row in rows:
        if isinstance(row, dict):
            row = list(row.values())  # 기존 PowerShell 브리지의 속성 열 순서를 따릅니다.
        if not isinstance(row, (list, tuple)) or len(row) <= max(word_column, score_column):
            continue
        word = str(row[word_column]).strip()
        try:
            score = float(row[score_column])
        except (ValueError, TypeError):
            continue
        if word and math.isfinite(score):
            result.append({'word': word, 'score': score})
    if not result:
        raise ValueError('해당 날짜의 키워드가 없거나 응답 형식이 변경되었습니다.')
    return result


@st.cache_data(ttl=600, show_spinner=False)
def fetch_scrapmaster(selected_date: str, user_seq: str, include_national: bool):
    date.fromisoformat(selected_date)
    with requests.Session() as session:
        response = session.post(
            ORIGIN + '/dnai/utils/total_word_score/word_score_by_today_setting.jsp',
            data={
                'user_seq': user_seq, 'start_date': selected_date,
                'end_date': selected_date, 'pair_type': '1',
                'removeChecked': 'false',
            },
            headers=HEADERS, timeout=40,
        )
        response.raise_for_status()
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as exc:
            raise ValueError('ScrapMaster가 JSON을 반환하지 않았습니다. 로그인이나 접근 권한을 확인해 주세요.') from exc
        pairs = _rows_to_pairs(data.get('period_member_word_score_pair'), 1, 2)
        result = {'date': selected_date, 'pairs': pairs}
        if include_national:
            response = session.get(
                ORIGIN + '/dnai/utils/total_word_score/word_score.jsp',
                headers=HEADERS, timeout=40,
            )
            response.raise_for_status()
            try:
                national = response.json()
            except requests.exceptions.JSONDecodeError as exc:
                raise ValueError('일간지 단어쌍 응답이 JSON이 아닙니다.') from exc
            result['nationalPairs'] = _rows_to_pairs(
                national.get('today_1_word_score_pair'), 0, 1
            )
            # 이 API는 날짜 선택이 없는 '오늘' 데이터입니다. 과거 날짜로 표기하지 않습니다.
            result['nationalDate'] = datetime.now().astimezone().date().isoformat()
    return result


def show_collection_controls():
    st.caption('ScrapMaster 조회는 이 페이지의 Python 서버에서 실행합니다.')
    with st.form('scrapmaster_collection'):
        selected = st.date_input('ScrapMaster 기준일', value=date.today())
        national = st.checkbox('오늘의 주요 일간지 단어쌍도 함께 조회')
        submitted = st.form_submit_button('서버에서 키워드 수집 및 이미지 만들기')
    if submitted:
        # iframe이 다시 그려지므로 기존 작성기 입력은 먼저 작업 저장(JSON)해 주세요.
        try:
            with st.spinner('ScrapMaster에서 키워드를 조회하고 있습니다…'):
                st.session_state.scrapmaster_payload = fetch_scrapmaster(
                    selected.isoformat(), _user_seq(), national
                )
            st.success('수집 완료. 아래 작성기에 키워드와 워드클라우드를 반영했습니다.')
        except (requests.RequestException, ValueError) as exc:
            st.error(f'서버 조회 실패: {exc}')
    return st.session_state.get('scrapmaster_payload')


def inject_payload(html_content: str, payload: dict | None):
    if not payload:
        return html_content
    # script 태그 탈출 방지. HTML은 id=server-scrapmaster-data를 읽습니다.
    encoded = json.dumps(payload, ensure_ascii=False).replace('<', '\u003c')
    encoded = encoded.replace('>', '\u003e').replace('&', '\u0026')
    tag = '<script id="server-scrapmaster-data" type="application/json">' + encoded + '</script>'
    index = html_content.lower().find('</head>')
    if index == -1:
        raise ValueError('작성기 HTML에서 </head>를 찾을 수 없습니다.')
    return html_content[:index] + tag + html_content[index:]
