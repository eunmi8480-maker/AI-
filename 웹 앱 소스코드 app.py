from pathlib import Path
import base64

import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------
# 1. 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="조간 브리핑 통합 작성기",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent

# 실제 파일명에 맞는 HTML 파일을 찾습니다.
HTML_CANDIDATES = [
    BASE_DIR / "조간브리핑_통합작성기.html",
    BASE_DIR / "완성본_조간브리핑_통합작성기.html",
]

HTML_PATH = next(
    (path for path in HTML_CANDIDATES if path.is_file()),
    None,
)

if "page" not in st.session_state:
    st.session_state.page = "home"


# --------------------------------------------------
# 2. KoPub돋움체 파일 읽기
#    woff2 또는 ttf 파일을 지원합니다.
# --------------------------------------------------
FONT_CANDIDATES = [
    (BASE_DIR / "KoPubDotum.woff2", "font/woff2", "woff2"),
    (BASE_DIR / "KoPubDotum.ttf", "font/ttf", "truetype"),
]

font_face_css = ""

for font_path, mime_type, font_format in FONT_CANDIDATES:
    if font_path.is_file():
        encoded_font = base64.b64encode(
            font_path.read_bytes()
        ).decode("ascii")

        font_face_css = f"""
        @font-face {{
            font-family: "KoPubDotum";
            src: url("data:{mime_type};base64,{encoded_font}")
                 format("{font_format}");
            font-style: normal;
            font-weight: 400;
            font-display: swap;
        }}
        """
        break


# --------------------------------------------------
# 3. Streamlit 화면 CSS
# --------------------------------------------------
page_css = """
<style>
html,
body,
.stApp,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select {
    font-family: "KoPubDotum", sans-serif !important;
}

.block-container {
    max-width: 100%;
    padding: 0 !important;
}

header[data-testid="stHeader"] {
    background: transparent;
}

footer {
    display: none;
}

/* 첫 번째 화면 전체 */
.st-key-landing {
    min-height: 100vh;
    color: #ffffff;
    background: linear-gradient(
        180deg,
        #0b1957 0%,
        #0b1957 48%,
        #35558e 77%,
        #7895be 100%
    );
}

/* 로고 및 메뉴 */
.brief-nav {
    max-width: 1180px;
    margin: 0 auto;
    padding: 25px 32px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 24px;
}

.brief-logo {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
}

.brief-logo small {
    display: block;
    margin-top: 8px;
    font-size: 12px;
    font-weight: 400;
    letter-spacing: 0;
}

.brief-menu {
    display: flex;
    gap: 32px;
    padding-top: 9px;
    color: #e2e9fb;
    font-size: 15px;
    font-weight: 600;
}

/* 첫 번째 이미지의 중앙 소개 영역 */
.brief-hero {
    max-width: 1000px;
    margin: 0 auto;
    padding: 75px 20px 0;
    text-align: center;
}

.brief-ring {
    width: 82px;
    height: 82px;
    box-sizing: border-box;
    margin: 0 auto 39px;
    border: 17px solid transparent;
    border-radius: 50%;
    background:
        linear-gradient(#0b1957, #0b1957) padding-box,
        linear-gradient(135deg, #a4f5ff, #3188ff) border-box;
    transform: rotate(-28deg) skew(-10deg);
}

.brief-hero h1 {
    margin: 0;
    color: #ffffff;
    font-size: clamp(34px, 4.5vw, 54px);
    font-weight: 800;
    line-height: 1.35;
    word-break: keep-all;
}

.brief-hero h1 span {
    color: #a9e6ff;
}

.brief-hero p {
    margin: 26px auto 0;
    color: #f0f4ff;
    font-size: clamp(16px, 1.8vw, 20px);
    line-height: 1.8;
    word-break: keep-all;
}

.brief-tags {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 52px;
}

.brief-tags span {
    padding: 9px 15px;
    border: 1px solid #d3e0f3;
    border-radius: 7px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
}

/* 소개 화면의 시작 버튼 */
.st-key-landing div[data-testid="stButton"] button {
    width: 100%;
    min-height: 47px;
    border: 0;
    border-radius: 8px;
    background: #ffffff;
    color: #11245b;
    font-size: 16px;
    font-weight: 800;
}

.st-key-landing div[data-testid="stButton"] button:hover {
    background: #e7f2ff;
    color: #11245b;
}

/* 두 번째 화면 */
.st-key-editor_page {
    background: #eef3fb;
    min-height: 100vh;
}

.editor-toolbar {
    padding: 10px 20px 0;
    background: #eef3fb;
}

.st-key-editor_page div[data-testid="stIFrame"] {
    width: 100%;
}

@media (max-width: 640px) {
    .brief-nav {
        padding: 22px 20px;
    }

    .brief-logo {
        font-size: 22px;
    }

    .brief-menu {
        gap: 14px;
        font-size: 13px;
    }

    .brief-hero {
        padding-top: 70px;
    }

    .brief-ring {
        width: 62px;
        height: 62px;
        border-width: 13px;
    }

    .brief-tags {
        margin-top: 42px;
    }
}
</style>
"""

st.markdown(
    font_face_css + page_css,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 4. 첫 번째 화면: 소개 페이지
# --------------------------------------------------
if st.session_state.page == "home":
    with st.container(key="landing"):
        # HTML 태그를 한 줄로 연결하여 코드가 화면에
        # 글자로 출력되는 문제를 방지합니다.
        landing_html = (
            '<div class="brief-nav">'
                '<div class="brief-logo">'
                    'morning brief'
                    '<small>하루를 시작하는 조간 브리핑</small>'
                '</div>'
                '<div class="brief-menu">'
                    '<span>홈</span>'
                    '<span>브리핑 작성</span>'
                '</div>'
            '</div>'
            '<div class="brief-hero">'
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
            '</div>'
        )

        st.markdown(
            landing_html,
            unsafe_allow_html=True,
        )

        # 실제로 동작하는 Streamlit 버튼입니다.
        left, center, right = st.columns([4, 2, 4])

        with center:
            if st.button(
                "브리핑 작성 시작 →",
                key="start_briefing",
                use_container_width=True,
            ):
                st.session_state.page = "editor"
                st.rerun()


# --------------------------------------------------
# 5. 두 번째 화면: 기존 HTML 작성기
# --------------------------------------------------
else:
    with st.container(key="editor_page"):
        with st.container():
            st.markdown(
                '<div class="editor-toolbar"></div>',
                unsafe_allow_html=True,
            )

            if st.button("← 홈으로", key="back_home"):
                st.session_state.page = "home"
                st.rerun()

        if HTML_PATH is None:
            st.error(
                "HTML 양식 파일을 찾을 수 없습니다. "
                "app.py와 같은 폴더에 양식 파일을 넣어 주세요."
            )
            st.stop()

        try:
            html_content = HTML_PATH.read_text(
                encoding="utf-8-sig"
            )
        except UnicodeDecodeError:
            html_content = HTML_PATH.read_text(
                encoding="cp949",
                errors="replace",
            )

        # 기존 작성기 기능은 그대로 두고 화면 색상과 폰트만 덧씌웁니다.
        editor_css = """
        <style>
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
        td {
            font-family: "KoPubDotum", sans-serif !important;
        }

        body {
            background: #eef3fb;
            color: #172b48;
        }

        header.top {
            background: #0b1957;
            color: #ffffff;
        }

        header.top p {
            color: #d9e5ff;
        }

        .bar {
            background: #f8faff;
            border-bottom: 1px solid #cbd8ed;
        }

        button,
        label.file {
            border-color: #b9c9e2;
            color: #153362;
        }

        button:hover,
        label.file:hover {
            background: #e8f1ff;
        }

        button.primary {
            background: #2256a0;
            border-color: #2256a0;
            color: #ffffff;
        }

        button.primary:hover {
            background: #174584;
        }

        aside {
            background: #e5edfa;
        }

        .card {
            background: #ffffff;
            border-color: #d4e0f1;
        }

        input,
        textarea {
            border-color: #c3d1e5;
        }

        @media print {
            body {
                background: #ffffff;
            }
        }
        </style>
        """

        head_end = html_content.lower().find("</head>")

        if head_end != -1:
            styled_html = (
                html_content[:head_end]
                + font_face_css
                + editor_css
                + html_content[head_end:]
            )
        else:
            styled_html = (
                font_face_css
                + editor_css
                + html_content
            )

        components.html(
            styled_html,
            height=1100,
            scrolling=True,
        )
