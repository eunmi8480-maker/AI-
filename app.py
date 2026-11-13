from pathlib import Path
from datetime import datetime, timezone, timedelta
import base64
import json
import io
import re
import zipfile
from decimal import Decimal, ROUND_HALF_UP

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
from bs4 import BeautifulSoup

import kepco_collect
import kepco_hwp
import kepco_images
from data_services import (
    fetch_keywords,
    fetch_headlines,
    error_message,
)


# ==================================================
# 1. 기본 설정
# ==================================================
st.set_page_config(
    page_title="AI 큐레이터 | 일일브리핑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
KST = timezone(timedelta(hours=9))
WEEKDAYS = "월화수목금토일"

HTML_CANDIDATES = [
    BASE_DIR / "briefing.html",
    BASE_DIR / "일일브리핑_통합작성기.html",
    BASE_DIR / "조간브리핑_통합작성기_서버연결.html",
    BASE_DIR / "조간브리핑_통합작성기.html",
    BASE_DIR / "완성본_조간브리핑_통합작성기.html",
    BASE_DIR / "조간브리핑_통합편집_130836.html",
]

HTML_PATH = next(
    (path for path in HTML_CANDIDATES if path.is_file()),
    None,
)

LOGO_PATH = BASE_DIR / "ai_curator_logo.png"

# 한국전력공사 자동보고서 프로그램(Windows용) 압축 파일
KEPCO_ZIP_PATH = BASE_DIR / "KepcoReport_v6.zip"
KEPCO_GUIDE_NAME = "KepcoReport_v6/사용방법.txt"

if "page" not in st.session_state:
    st.session_state.page = "home"

if "eff_subtab" not in st.session_state:
    st.session_state.eff_subtab = "monitoring"

if "sum_subtab" not in st.session_state:
    st.session_state.sum_subtab = "mss"


def today_title():
    """오늘 날짜 제목: '26. 11. 13(금)"""
    now = datetime.now(KST)
    return f"'{now:%y}. {now.month}. {now.day}({WEEKDAYS[now.weekday()]})"


# ==================================================
# 2. 화면 및 서브탭 이동
# ==================================================
def go_home():
    st.session_state.page = "home"


def go_editor():
    st.session_state.editor_ready = False
    st.session_state.page = "editor"


def go_efficiency():
    st.session_state.page = "efficiency"


def go_summary():
    st.session_state.page = "summary"


def set_eff_subtab(tab_name):
    st.session_state.eff_subtab = tab_name
