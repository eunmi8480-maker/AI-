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
# 2. 화면 이동 함수
# ==================================================
def go_home():
    st.session_state.page = "home"


def go_editor():
    st.session_state.page = "editor"


# ==================================================
# 3. 공통 함수
# ==================================================
def file_to_base64(file_path: Path) -> str:
    return base64.b64encode(
        file_path.read_bytes()
    ).decode("ascii")


def read_text_file(file_path: Path) -> str:
    try:
        return file_path.read_text(
            encoding="utf-8-sig",
        )
    except UnicodeDecodeError:
        return file_path.read_text(
            encoding="cp949",
            errors="replace",
        )


# ==================================================
# 4. KoPub돋움체 불러오기
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
# 5. 홈페이지 로고
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
    logo_html = """
    <div class="brief-logo brief-logo-text">
        AI CURATOR
        <small>하루를 시작하는 조간 브리핑</small>
    </div>
    """


# ==================================================
# 6. Streamlit 전체 CSS
# ==================================================
page_css = f"""
<style>
{font_face_css}

:root {{
    --navy: #0d1c59;
    --navy-dark: #081442;
    --sky: #9be7ff;
    --sky-soft: #dff6ff;
    --line: #b7c9e3;
}}

html,
body,
.stApp,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select {{
    font-family: "KoPubDotum", sans-serif !important;
}}

.stApp {{
    min-height: 100vh;
    background: #0d1c59;
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

/* 홈 화면 */
.st-key-landing {{
    min-height: 100vh;
    color: #ffffff;
    background:
        linear-gradient(
            180deg,
            #0d1c59 0%,
            #0d1c59 48%,
            #29477f 77%,
            #7895be 100%
        );
}}

.brief-nav {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 25px 32px 0;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 24px;
}}

.brief-logo-text {{
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.1;
}}

.brief-logo-text small {{
    display: block;
    margin-top: 8px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 400;
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
        linear-gradient(#0d1c59, #0d1c59) padding-box,
        linear-gradient(135deg, #a4f5ff, #3188ff) border-box;
    transform: rotate(-28deg) skew(-10deg);
}}

.brief-hero h1 {{
    margin: 0;
    color: #ffffff;
    font-size: clamp(34px, 4.5vw, 54px);
    font-weight: 800;
    line-height: 1.35;
}}

.brief-hero h1 span {{
    color: #9be7ff;
}}

.brief-hero p {{
    margin: 26px auto 0;
    color: #f0f4ff;
    font-size: clamp(16px, 1.8vw, 20px);
    line-height: 1.8;
}}

/* 홈 화면 상단 메뉴 */
.st-key-home_navigation {{
    position: absolute;
    top: 21px;
    right: max(32px, calc((100vw - 1180px) / 2 + 32px));
    z-index: 10;
    display: flex;
    gap: 12px;
}}

.st-key-home_navigation div[data-testid="stHorizontalBlock"] {{
    gap: 12px;
}}

.st-key-nav_home button,
.st-key-nav_editor button {{
    min-height: 38px !important;
    padding: 4px 14px !important;
    border: 0 !important;
    background: transparent !important;
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}}

.st-key-nav_home button:hover,
.st-key-nav_editor button:hover {{
    color: #9be7ff !important;
}}

/* 시작 버튼 */
.st-key-start_briefing {{
    width: min(310px, calc(100% - 40px));
    margin: 55px auto 0;
}}

.st-key-start_briefing button {{
    width: 100% !important;
    min-height: 66px !important;
    border: 0 !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    color: #11245b !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}}

.st-key-start_briefing button p,
.st-key-start_briefing button span {{
    margin: 0 !important;
    color: #11245b !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}}

.st-key-start_briefing button:hover {{
    background: #dff6ff !important;
}}

/* 작성기 화면 */
.st-key-editor_page {{
    box-sizing: border-box;
    min-height: 100vh;
    background:
        linear-gradient(
            180deg,
            #0d1c59 0%,
            #0d1c59 28%,
            #29477f 62%,
            #7895be 100%
        );
}}

.st-key-editor_page > div {{
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 24px 34px;
    box-sizing: border-box;
}}

/* 작성기 최상단 홈 버튼 줄 */
.st-key-editor_topbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    box-sizing: border-box;
    width: 100%;
    padding: 12px 0;
    background: #0d1c59;
    border-bottom: 1px solid rgba(255, 255, 255, 0.18);
}}

.st-key-editor_home button {{
    width: 140px !important;
    min-height: 44px !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    color: #0d1c59 !important;
    font-weight: 800 !important;
}}

.st-key-editor_home button p,
.st-key-editor_home button span {{
    color: #0d1c59 !important;
    font-weight: 800 !important;
}}

.st-key-editor_home button:hover {{
    background: #dff6ff !important;
}}

.st-key-editor_page div[data-testid="stIFrame"] {{
    width: 100%;
    overflow: hidden;
    border: 1px solid #6f8fbd;
    border-radius: 0 0 12px 12px;
    background: #ffffff;
}}

.editor-file-error {{
    margin: 24px;
    padding: 22px;
    border: 1px solid #e3cf82;
    border-radius: 10px;
    background: #fff8dc;
    color: #5a4914;
    line-height: 1.7;
}}

@media (max-width: 640px) {{
    .brief-nav {{
        padding: 22px 20px 0;
    }}

    .brief-logo-image {{
        width: min(250px, 58vw);
    }}

    .st-key-home_navigation {{
        top: 16px;
        right: 14px;
    }}

    .st-key-nav_home button,
    .st-key-nav_editor button {{
        padding: 4px 6px !important;
        font-size: 13px !important;
    }}

    .brief-hero {{
        padding-top: 75px;
    }}

    .brief-ring {{
        width: 62px;
        height: 62px;
        border-width: 13px;
    }}

    .st-key-editor_page > div {{
        padding: 0 6px 20px;
    }}

    .st-key-editor_home button {{
        width: 120px !important;
    }}
}}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)


# ==================================================
# 7. 홈 화면
# ==================================================
if st.session_state.page == "home":
    with st.container(key="landing"):
        st.markdown(
            (
                '<div class="brief-nav">'
                f'{logo_html}'
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
            ),
            unsafe_allow_html=True,
        )

        with st.container(key="home_navigation"):
            nav_home_col, nav_editor_col = st.columns(2)

            with nav_home_col:
                st.button(
                    "홈",
                    key="nav_home",
                    on_click=go_home,
                    use_container_width=True,
                )

            with nav_editor_col:
                st.button(
                    "브리핑 작성",
                    key="nav_editor",
                    on_click=go_editor,
                    use_container_width=True,
                )

        st.button(
            "브리핑 작성 시작",
            key="start_briefing",
            on_click=go_editor,
            use_container_width=True,
        )


# ==================================================
# 8. 작성기 화면
# ==================================================
else:
    with st.container(key="editor_page"):
        # 최상단 홈 버튼
        with st.container(key="editor_topbar"):
            st.button(
                "← 홈으로",
                key="editor_home",
                on_click=go_home,
            )

        if HTML_PATH is None:
            candidate_names = "<br>".join(
                html_lib.escape(path.name)
                for path in HTML_CANDIDATES
            )

            st.markdown(
                (
                    '<div class="editor-file-error">'
                    '<strong>작성기 HTML 파일을 찾을 수 '
                    '없습니다.</strong><br><br>'
                    'app.py와 같은 폴더에 다음 파일 중 '
                    '하나를 올려 주세요.<br><br>'
                    f'{candidate_names}'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )
            st.stop()

        try:
            html_content = read_text_file(HTML_PATH)
        except OSError as error:
            st.error("작성기 HTML 파일을 읽을 수 없습니다.")
            st.code(str(error))
            st.stop()

        # ==================================================
        # 작성기 iframe 내부 스타일
        # ==================================================
        editor_css = f"""
        <style>
        {font_face_css}

        :root {{
            --navy: #0d1c59;
            --sky: #9be7ff;
            --sky-soft: #dff6ff;
            --line: #b7c9e3;
            --text: #102653;
            --muted: #60769b;
        }}

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

        html {{
            min-height: 100%;
            background: #0d1c59;
        }}

        body {{
            min-height: 100vh;
            margin: 0;
            color: var(--text);
            background:
                linear-gradient(
                    180deg,
                    #0d1c59 0,
                    #0d1c59 180px,
                    #29477f 430px,
                    #7895be 100%
                );
        }}

        header.top {{
            box-sizing: border-box;
            min-height: 130px;
            padding: 26px 32px !important;
            color: #ffffff !important;
            background: #0d1c59 !important;
            border-bottom:
                1px solid rgba(255, 255, 255, 0.14);
        }}

        header.top h1,
        header.top h2,
        header.top h3 {{
            margin-top: 0;
            color: #9be7ff !important;
            font-weight: 800 !important;
        }}

        header.top p {{
            color: #eef5ff !important;
        }}

        .bar {{
            position: sticky;
            top: 0;
            z-index: 50;
            padding: 12px 18px !important;
            background: #0d1c59 !important;
            border-bottom:
                1px solid #426196 !important;
        }}

        .bar button,
        .bar label.file {{
            background: #ffffff !important;
            border: 1px solid #ffffff !important;
            color: #0d1c59 !important;
            font-weight: 800 !important;
        }}

        aside {{
            background: #0d1c59 !important;
            color: #ffffff !important;
            border-right:
                1px solid rgba(255, 255, 255, 0.22) !important;
        }}

        aside *,
        aside p,
        aside span,
        aside div,
        aside small,
        aside label,
        aside li,
        aside strong {{
            color: #ffffff !important;
        }}

        aside a {{
            color: #ffffff !important;
            text-decoration: none !important;
        }}

        aside a:hover {{
            color: #9be7ff !important;
        }}

        aside .active,
        aside [aria-current="page"],
        aside a.active {{
            background:
                rgba(155, 231, 255, 0.16) !important;
            color: #9be7ff !important;
            border-left:
                3px solid #9be7ff !important;
        }}

        .card {{
            background: #ffffff !important;
            border: 1px solid #b7c9e3 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }}

        input,
        textarea,
        select {{
            box-sizing: border-box;
            background: #ffffff !important;
            color: #102653 !important;
            border: 1px solid #aabedc !important;
            border-radius: 7px !important;
        }}

        button,
        label.file {{
            border: 1px solid #9eb5d5 !important;
            border-radius: 7px !important;
            background: #f5f9ff !important;
            color: #0d1c59 !important;
            font-weight: 700 !important;
            box-shadow: none !important;
        }}

        button:hover,
        label.file:hover {{
            background: #dff6ff !important;
            border-color: #5da9df !important;
        }}

        button.primary {{
            background: #0d1c59 !important;
            border-color: #0d1c59 !important;
            color: #ffffff !important;
        }}

        .paper,
        .page {{
            background: #ffffff !important;
            border-color: #c1cee1 !important;
            box-shadow: none !important;
        }}

        th {{
            background: #e8f1ff !important;
            color: #0d1c59 !important;
        }}

        td {{
            background: #ffffff;
            color: #102653;
        }}

        aside small,
        aside .help,
        aside .hint,
        aside .muted {{
            color: #ffffff !important;
        }}

        @media print {{
            html,
            body {{
                background: #ffffff !important;
            }}

            header.top,
            .bar,
            aside {{
                display: none !important;
            }}
        }}

        @media (max-width: 760px) {{
            .bar {{
                position: static;
            }}

            aside {{
                border-right: 0 !important;
                border-bottom:
                    1px solid rgba(
                        255,
                        255,
                        255,
                        0.22
                    ) !important;
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
