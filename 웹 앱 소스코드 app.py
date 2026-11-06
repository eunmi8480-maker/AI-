from pathlib import Path
import base64

import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------
# 1. 기본 설정 및 파일 위치
# --------------------------------------------------
st.set_page_config(
    page_title="조간 브리핑 통합 작성기",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "조간브리핑_통합작성기.html"
FONT_PATH = BASE_DIR / "KoPubDotum.woff2"


# --------------------------------------------------
# 2. KoPub돋움체 불러오기
# --------------------------------------------------
font_face_css = ""

if FONT_PATH.is_file():
    font_base64 = base64.b64encode(
        FONT_PATH.read_bytes()
    ).decode("ascii")

    font_face_css = f"""
    @font-face {{
        font-family: 'KoPubDotum';
        src: url('data:font/woff2;base64,{font_base64}') format('woff2');
        font-style: normal;
        font-weight: 400;
        font-display: swap;
    }}
    """
else:
    st.warning(
        "KoPubDotum.woff2 파일을 찾지 못했습니다. "
        "파일을 app.py와 같은 폴더에 넣으면 KoPub돋움체가 적용됩니다."
    )


# --------------------------------------------------
# 3. Streamlit 홈페이지 디자인
# --------------------------------------------------
page_css = f"""
<style>
{font_face_css}

html,
body,
.stApp,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select {{
    font-family: 'KoPubDotum', sans-serif !important;
}}

.block-container {{
    max-width: 100%;
    padding: 0 0 4rem 0;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

.brief-home {{
    color: #fff;
    background: linear-gradient(
        180deg,
        #0b1957 0%,
        #0b1957 50%,
        #34558f 78%,
        #7894bf 100%
    );
}}

.brief-nav {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}}

.brief-logo {{
    color: #fff !important;
    text-decoration: none !important;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.15;
}}

.brief-logo small {{
    display: block;
    margin-top: 7px;
    font-size: 12px;
    font-weight: 400;
    letter-spacing: 0;
}}

.brief-menu {{
    display: flex;
    gap: 32px;
}}

.brief-menu a {{
    color: #e1e9fa !important;
    text-decoration: none !important;
    font-weight: 600;
}}

.brief-hero {{
    max-width: 1050px;
    min-height: 510px;
    margin: 0 auto;
    padding: 68px 24px 72px;
    text-align: center;
    box-sizing: border-box;
}}

.brief-ring {{
    width: 82px;
    height: 82px;
    margin: 0 auto 38px;
    border: 17px solid transparent;
    border-radius: 50%;
    background:
        linear-gradient(#0b1957, #0b1957) padding-box,
        linear-gradient(135deg, #a9f8ff, #3185ff) border-box;
    transform: rotate(-28deg) skew(-10deg);
}}

.brief-hero h1 {{
    margin: 0;
    color: #fff;
    font-size: clamp(34px, 4.4vw, 54px);
    line-height: 1.35;
    font-weight: 800;
    word-break: keep-all;
}}

.brief-hero h1 span {{
    color: #a9e4ff;
}}

.brief-hero p {{
    margin: 25px auto 0;
    color: #edf3ff;
    font-size: clamp(16px, 1.8vw, 21px);
    line-height: 1.8;
    word-break: keep-all;
}}

.brief-tags {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 48px;
}}

.brief-tags span {{
    padding: 9px 15px;
    border: 1px solid #d2e0f4;
    border-radius: 7px;
    font-size: 14px;
}}

.brief-start {{
    display: inline-block;
    margin-top: 22px;
    padding: 13px 25px;
    border-radius: 8px;
    background: #fff;
    color: #10245d !important;
    text-decoration: none !important;
    font-weight: 800;
}}

.brief-section-title {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 43px 24px 18px;
}}

.brief-section-title h2 {{
    margin: 0 0 8px;
    font-size: 27px;
}}

.brief-section-title p {{
    margin: 0;
    color: #667085;
}}

div[data-testid="stIFrame"] {{
    padding: 0 24px;
}}

@media (max-width: 640px) {{
    .brief-nav {{
        padding: 20px;
    }}

    .brief-logo {{
        font-size: 22px;
    }}

    .brief-menu {{
        gap: 14px;
    }}

    .brief-menu a {{
        font-size: 13px;
    }}

    .brief-hero {{
        min-height: 470px;
        padding: 65px 20px 55px;
    }}
}}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)


# --------------------------------------------------
# 4. 홈페이지 상단 영역
# HTML을 한 덩어리로 만들어 코드가 화면에 노출되지 않게 합니다.
# --------------------------------------------------
home_html = (
    '<div class="brief-home" id="home">'
        '<nav class="brief-nav">'
            '<a class="brief-logo" href="#home">'
                'morning brief'
                '<small>하루를 시작하는 조간 브리핑</small>'
            '</a>'
            '<div class="brief-menu">'
                '<a href="#home">홈</a>'
                '<a href="#editor">브리핑 작성</a>'
            '</div>'
        '</nav>'
        '<section class="brief-hero">'
            '<div class="brief-ring"></div>'
            '<h1><span>오늘의 뉴스,</span><br>한눈에 정리하세요.</h1>'
            '<p>'
                '워드클라우드부터 주요 기사와 정부 동향까지.<br>'
                '필요한 내용을 입력하고 조간 브리핑을 완성해 보세요.'
            '</p>'
            '<div class="brief-tags">'
                '<span>#조간브리핑</span>'
                '<span>#뉴스정리</span>'
                '<span>#보고서작성</span>'
            '</div>'
            '<a class="brief-start" href="#editor">'
                '브리핑 작성 시작 →'
            '</a>'
        '</section>'
    '</div>'
    '<div class="brief-section-title" id="editor">'
        '<h2>조간 브리핑 작성기</h2>'
        '<p>아래 양식에 내용을 입력해 주세요.</p>'
    '</div>'
)

st.markdown(home_html, unsafe_allow_html=True)


# --------------------------------------------------
# 5. 기존 HTML 작성기 파일 불러오기
# --------------------------------------------------
if not HTML_PATH.is_file():
    st.error(f"양식 파일을 찾을 수 없습니다: {HTML_PATH.name}")
    st.stop()

try:
    html_content = HTML_PATH.read_text(encoding="utf-8-sig")
except UnicodeDecodeError:
    html_content = HTML_PATH.read_text(
        encoding="cp949",
        errors="replace",
    )


# --------------------------------------------------
# 6. 작성기 내부에 색상과 KoPub돋움체 적용
# 원본 HTML 파일 자체는 수정하지 않습니다.
# --------------------------------------------------
editor_style = f"""
<style>
{font_face_css}

html,
body,
button,
input,
textarea,
select,
h1,
h2,
h3,
h4,
p,
a,
label,
th,
td {{
    font-family: 'KoPubDotum', sans-serif !important;
}}

body {{
    background: #eef3fb;
    color: #172b48;
}}

header.top {{
    background: #0b1957;
    color: #fff;
}}

header.top p {{
    color: #d9e5ff;
}}

.bar {{
    background: #f8faff;
    border-bottom: 1px solid #cbd8ed;
}}

button,
label.file {{
    border-color: #b9c9e2;
    color: #153362;
}}

button:hover,
label.file:hover {{
    background: #e8f1ff;
}}

button.primary {{
    background: #2256a0;
    border-color: #2256a0;
    color: #fff;
}}

button.primary:hover {{
    background: #174584;
}}

aside {{
    background: #e5edfa;
}}

aside nav a {{
    color: #193762;
}}

aside nav a:hover {{
    background: #d3e3fb;
}}

.card {{
    background: #fff;
    border-color: #d4e0f1;
}}

.card h2 {{
    color: #112d5e;
}}

input,
textarea {{
    border-color: #c3d1e5;
}}

input:focus,
textarea:focus {{
    outline: 2px solid #4787db;
    outline-offset: 1px;
}}

@media print {{
    body {{
        background: #fff;
    }}
}}
</style>
"""

head_end = html_content.lower().find("</head>")

if head_end != -1:
    styled_html = (
        html_content[:head_end]
        + editor_style
        + html_content[head_end:]
    )
else:
    styled_html = editor_style + html_content


# --------------------------------------------------
# 7. 작성기를 홈페이지에 표시
# --------------------------------------------------
components.html(
    styled_html,
    height=1100,
    scrolling=True,
)
