from pathlib import Path
import base64
import html as html_lib

import streamlit as st
import streamlit.components.v1 as components


# ==================================================
# 1. Streamlit 기본 설정
# ==================================================
st.set_page_config(
    page_title="AI 큐레이터 | 조간 브리핑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent

# 사용할 수 있는 작성기 HTML 파일을 순서대로 찾습니다.
HTML_CANDIDATES = [
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

if "page" not in st.session_state:
    st.session_state.page = "home"


# ==================================================
# 2. 공통 함수
# ==================================================
def file_to_base64(file_path: Path) -> str:
    """파일을 Base64 문자열로 변환합니다."""
    return base64.b64encode(
        file_path.read_bytes()
    ).decode("ascii")


def read_text_file(file_path: Path) -> str:
    """UTF-8을 먼저 사용하고 실패하면 CP949로 읽습니다."""
    try:
        return file_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return file_path.read_text(
            encoding="cp949",
            errors="replace",
        )


# ==================================================
# 3. KoPub돋움체 불러오기
# ==================================================
FONT_CANDIDATES = [
    (
        BASE_DIR / "KoPubDotum.woff2",
        "font/woff2",
        "woff2",
    ),
    (
        BASE_DIR / "KoPubDotum.ttf",
        "font/ttf",
        "truetype",
    ),
]

font_face_css = ""

for font_path, mime_type, font_format in FONT_CANDIDATES:
    if font_path.is_file():
        encoded_font = file_to_base64(font_path)

        font_face_css = f"""
        @font-face {{
            font-family: "KoPubDotum";
            src:
                url("data:{mime_type};base64,{encoded_font}")
                format("{font_format}");
            font-style: normal;
            font-weight: 400;
            font-display: swap;
        }}
        """
        break


# ==================================================
# 4. 홈페이지 로고
# ==================================================
if LOGO_PATH.is_file():
    encoded_logo = file_to_base64(LOGO_PATH)

    logo_html = f"""
    <div class="brief-logo brief-logo-image">
        <img
            src="data:image/png;base64,{encoded_logo}"
            alt="AI CURATOR | 하루를 시작하는 조간 브리핑"
        >
    </div>
    """
else:
    # 이미지 파일이 없어도 앱이 중단되지 않습니다.
    logo_html = """
    <div class="brief-logo brief-logo-text">
        AI CURATOR
        <small>하루를 시작하는 조간 브리핑</small>
    </div>
    """


# ==================================================
# 5. 전체 화면 CSS
# ==================================================
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
    font-family: "KoPubDotum", sans-serif !important;
}}

.block-container {{
    max-width: 100%;
    padding: 0 !important;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

footer {{
    display: none;
}}

/* 첫 화면 */
.st-key-landing {{
    min-height: 100vh;
    color: #ffffff;
    background:
        linear-gradient(
            180deg,
            #0b1957 0%,
            #0b1957 48%,
            #35558e 77%,
            #7895be 100%
        );
}}

/* 상단 로고와 메뉴 */
.brief-nav {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 25px 32px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 24px;
}}

.brief-logo-text {{
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
}}

.brief-logo-text small {{
    display: block;
    margin-top: 8px;
    font-size: 12px;
    font-weight: 400;
    letter-spacing: 0;
}}

.brief-logo-image {{
    width: min(400px, 55vw);
    line-height: 0;
}}

.brief-logo-image img {{
    display: block;
    width: 100%;
    height: auto;
    object-fit: contain;
}}

.brief-menu {{
    display: flex;
    gap: 32px;
    padding-top: 9px;
    color: #e2e9fb;
    font-size: 15px;
    font-weight: 600;
}}

/* 중앙 문구 */
.brief-hero {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 75px 20px 0;
    text-align: center;
}}

.brief-ring {{
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
}}

.brief-hero h1 {{
    margin: 0;
    color: #ffffff;
    font-size: clamp(34px, 4.5vw, 54px);
    font-weight: 800;
    line-height: 1.35;
    word-break: keep-all;
}}

.brief-hero h1 span {{
    color: #a9e6ff;
}}

.brief-hero p {{
    margin: 26px auto 0;
    color: #f0f4ff;
    font-size: clamp(16px, 1.8vw, 20px);
    line-height: 1.8;
    word-break: keep-all;
}}

/* 브리핑 시작 버튼 */
.st-key-start_briefing {{
    width: min(300px, calc(100% - 40px));
    margin: 55px auto 0;
}}

.st-key-start_briefing button {{
    width: 100% !important;
    min-height: 66px !important;
    padding: 6px 8px !important;
    border: 0 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #11245b !important;
    font-family: "KoPubDotum", sans-serif !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
}}

.st-key-start_briefing button p,
.st-key-start_briefing button span {{
    margin: 0 !important;
    padding: 0 !important;
    color: #11245b !important;
    font-family: "KoPubDotum", sans-serif !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
}}

.st-key-start_briefing button:hover {{
    background: #e7f2ff !important;
}}

/* 작성기 화면 */
.st-key-editor_page {{
    min-height: 100vh;
    background: #eef3fb;
}}

.st-key-editor_page div[data-testid="stIFrame"] {{
    width: 100%;
}}

/* 안내 영역 */
.editor-guide {{
    margin: 0;
    padding: 10px 16px;
    background: #fff8dc;
    border: 1px solid #e3cf82;
    border-radius: 8px;
    color: #5a4914;
    font-size: 14px;
    line-height: 1.6;
}}

@media (max-width: 640px) {{
    .brief-nav {{
        padding: 22px 20px;
        gap: 12px;
    }}

    .brief-logo-text {{
        font-size: 22px;
    }}

    .brief-logo-image {{
        width: min(270px, 62vw);
    }}

    .brief-menu {{
        gap: 14px;
        padding-top: 5px;
        font-size: 13px;
    }}

    .brief-hero {{
        padding-top: 70px;
    }}

    .brief-ring {{
        width: 62px;
        height: 62px;
        border-width: 13px;
    }}

    .st-key-start_briefing {{
        width: min(270px, calc(100% - 40px));
    }}

    .st-key-start_briefing button,
    .st-key-start_briefing button p,
    .st-key-start_briefing button span {{
        font-size: 30px !important;
    }}
}}
</style>
"""

st.markdown(
    page_css,
    unsafe_allow_html=True,
)


# ==================================================
# 6. 첫 화면
# ==================================================
if st.session_state.page == "home":
    with st.container(key="landing"):
        landing_html = (
            '<div class="brief-nav">'
            f'{logo_html}'
            '<div class="brief-menu">'
            '<span>홈</span>'
            '<span>브리핑 작성</span>'
            '</div>'
            '</div>'
            '<div class="brief-hero">'
            '<div class="brief-ring"></div>'
            '<h1>'
            '<span>오늘의 뉴스,</span><br>'
            '한눈에 정리하세요.'
            '</h1>'
            '<p>'
            '워드클라우드부터 주요 기사와 정부 동향까지.<br>'
            '필요한 내용을 입력하고 조간 브리핑을 '
            '완성해 보세요.'
            '</p>'
            '</div>'
        )

        st.markdown(
            landing_html,
            unsafe_allow_html=True,
        )

        if st.button(
            "브리핑 작성 시작",
            key="start_briefing",
            use_container_width=True,
        ):
            st.session_state.page = "editor"
            st.rerun()


# ==================================================
# 7. 작성기 화면
# ==================================================
else:
    with st.container(key="editor_page"):
        top_left, top_right = st.columns(
            [1, 8],
            vertical_alignment="center",
        )

        with top_left:
            if st.button(
                "← 홈으로",
                key="back_home",
                use_container_width=True,
            ):
                st.session_state.page = "home"
                st.rerun()

        with top_right:
            st.markdown(
                """
                <div class="editor-guide">
                    작성기 화면입니다. 현재 버전은 별도 Python
                    모듈 없이 실행됩니다. 로컬 ScrapMaster 브리지
                    기능은 HTML 작성기의 기존 설정에 따라 작동합니다.
                </div>
                """,
                unsafe_allow_html=True,
            )

        if HTML_PATH is None:
            candidate_names = "<br>".join(
                html_lib.escape(path.name)
                for path in HTML_CANDIDATES
            )

            st.error(
                "작성기 HTML 파일을 찾을 수 없습니다."
            )

            st.markdown(
                (
                    "GitHub에서 `app.py`와 같은 폴더에 "
                    "다음 파일 중 하나를 올려 주세요.<br><br>"
                    f"{candidate_names}"
                ),
                unsafe_allow_html=True,
            )

            st.stop()

        try:
            html_content = read_text_file(HTML_PATH)
        except OSError as error:
            st.error(
                "작성기 HTML 파일을 읽을 수 없습니다."
            )
            st.code(str(error))
            st.stop()

        # 원본 HTML 기능은 그대로 두고 색상과 폰트만 추가합니다.
        editor_css = f"""
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
            font-family: "KoPubDotum", sans-serif !important;
        }}

        body {{
            background: #eef3fb;
            color: #172b48;
        }}

        header.top {{
            background: #0b1957;
            color: #ffffff;
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
            color: #ffffff;
        }}

        button.primary:hover {{
            background: #174584;
        }}

        aside {{
            background: #e5edfa;
        }}

        .card {{
            background: #ffffff;
            border-color: #d4e0f1;
        }}

        input,
        textarea {{
            border-color: #c3d1e5;
        }}

        @media print {{
            body {{
                background: #ffffff;
            }}
        }}
        </style>
        """

        head_end = html_content.lower().find("</head>")

        if head_end != -1:
            styled_html = (
                html_content[:head_end]
                + editor_css
                + html_content[head_end:]
            )
        else:
            styled_html = editor_css + html_content

        components.html(
            styled_html,
            height=1100,
            scrolling=True,
        )
