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
# 2. 공통 함수
# ==================================================
def file_to_base64(file_path: Path) -> str:
    """파일을 Base64 문자열로 변환합니다."""
    return base64.b64encode(
        file_path.read_bytes()
    ).decode("ascii")


def read_text_file(file_path: Path) -> str:
    """UTF-8로 읽고 실패하면 CP949로 읽습니다."""
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
    logo_html = """
    <div class="brief-logo brief-logo-text">
        AI CURATOR
        <small>하루를 시작하는 조간 브리핑</small>
    </div>
    """


# ==================================================
# 5. Streamlit 전체 화면 CSS
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

/* ==================================================
   첫 화면
   ================================================== */
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
    color: #ffffff;
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
    word-break: keep-all;
}}

.brief-hero h1 span {{
    color: #9be7ff;
}}

.brief-hero p {{
    margin: 26px auto 0;
    color: #f0f4ff;
    font-size: clamp(16px, 1.8vw, 20px);
    line-height: 1.8;
    word-break: keep-all;
}}

/* 시작 버튼 */
.st-key-start_briefing {{
    width: min(310px, calc(100% - 40px));
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
    background: #dff6ff !important;
}}

/* ==================================================
   작성기 화면
   빨간색 표시 영역을 없애기 위해 별도 제목 영역을
   만들지 않고 iframe만 표시합니다.
   ================================================== */
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
    box-sizing: border-box;
    width: 100%;
    max-width: 1440px;
    margin: 0 auto;
    padding: 14px 24px 34px;
}}

.st-key-editor_page div[data-testid="stIFrame"] {{
    width: 100%;
    overflow: hidden;
    border: 1px solid #6f8fbd;
    border-radius: 12px;
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
        width: min(280px, calc(100% - 40px));
    }}

    .st-key-start_briefing button,
    .st-key-start_briefing button p,
    .st-key-start_briefing button span {{
        font-size: 29px !important;
    }}

    .st-key-editor_page > div {{
        padding: 8px 6px 20px;
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
        # 요청에 따라 작성기 바깥의 홈 버튼, 제목,
        # 설명 영역은 출력하지 않습니다.

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
                    'GitHub에서 app.py와 같은 폴더에 '
                    '다음 파일 중 하나를 올려 주세요.'
                    '<br><br>'
                    f'{candidate_names}'
                    '</div>'
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

        # ==================================================
        # 작성기 iframe 내부 테마
        # ==================================================
        editor_css = f"""
        <style>
        {font_face_css}

        :root {{
            --navy: #0d1c59;
            --navy-dark: #081442;
            --sky: #9be7ff;
            --sky-soft: #dff6ff;
            --paper: #ffffff;
            --paper-blue: #f3f8ff;
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

        /* HTML 내부 제목 영역 */
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

        /* 상단 기능 막대 */
        .bar {{
            position: sticky;
            top: 0;
            z-index: 50;
            padding: 12px 18px !important;
            background: #0d1c59 !important;
            border-top:
                1px solid rgba(255, 255, 255, 0.12);
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

        .bar button:hover,
        .bar label.file:hover {{
            background: #dff6ff !important;
            border-color: #9be7ff !important;
        }}

        /* ==========================================
           검은색 표시 영역: 왼쪽 사이드 메뉴
           배경을 전체 배경과 같은 남색으로 변경
           ========================================== */
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
        aside strong,
        aside b {{
            color: #ffffff !important;
        }}

        aside h1,
        aside h2,
        aside h3,
        aside h4 {{
            color: #9be7ff !important;
        }}

        aside a {{
            color: #ffffff !important;
            text-decoration: none !important;
        }}

        aside a:hover {{
            color: #9be7ff !important;
        }}

        aside button {{
            background: transparent !important;
            color: #ffffff !important;
            border-color:
                rgba(255, 255, 255, 0.30) !important;
        }}

        aside button:hover {{
            background:
                rgba(255, 255, 255, 0.12) !important;
            color: #9be7ff !important;
            border-color: #9be7ff !important;
        }}

        aside .active,
        aside [aria-current="page"],
        aside button.active,
        aside a.active {{
            background:
                rgba(155, 231, 255, 0.16) !important;
            color: #9be7ff !important;
            border-left:
                3px solid #9be7ff !important;
        }}

        aside .active *,
        aside [aria-current="page"] *,
        aside button.active *,
        aside a.active * {{
            color: #9be7ff !important;
        }}

        /* 카드 */
        .card {{
            background:
                rgba(255, 255, 255, 0.98) !important;
            border:
                1px solid #b7c9e3 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }}

        .card h2,
        .card h3,
        .card h4 {{
            color: #0d1c59 !important;
        }}

        /* 입력 요소 */
        input,
        textarea,
        select {{
            box-sizing: border-box;
            background: #ffffff !important;
            color: #102653 !important;
            border:
                1px solid #aabedc !important;
            border-radius: 7px !important;
        }}

        input:focus,
        textarea:focus,
        select:focus {{
            outline:
                3px solid rgba(79, 181, 255, 0.22) !important;
            border-color: #438bd2 !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #8191aa !important;
        }}

        /* 일반 버튼 */
        button,
        label.file {{
            border:
                1px solid #9eb5d5 !important;
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

        /* 주요 버튼 */
        button.primary {{
            background: #0d1c59 !important;
            border-color: #0d1c59 !important;
            color: #ffffff !important;
        }}

        button.primary:hover {{
            background: #183477 !important;
            border-color: #183477 !important;
        }}

        /* 문서 미리보기 */
        main,
        .preview,
        .paper,
        .page {{
            color: #102653;
        }}

        .paper,
        .page {{
            background: #ffffff !important;
            border-color: #c1cee1 !important;
            box-shadow: none !important;
        }}

        /* 표 */
        table {{
            border-color: #b7c9e3 !important;
        }}

        th {{
            background: #e8f1ff !important;
            color: #0d1c59 !important;
        }}

        td {{
            background: #ffffff;
            color: #102653;
        }}

        /* 카드 내부 보조 문구에만 회색 적용 */
        main small,
        .card small,
        .help,
        .hint,
        .muted {{
            color: #60769b !important;
        }}

        /* 사이드 메뉴의 보조 문구는 다시 흰색 */
        aside small,
        aside .help,
        aside .hint,
        aside .muted {{
            color: #ffffff !important;
        }}

        /* 일반 링크 */
        main a,
        .card a {{
            color: #2267af !important;
        }}

        main a:hover,
        .card a:hover {{
            color: #0d1c59 !important;
        }}

        /* 스크롤바 */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: #dce7f6;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #7895be;
            border: 2px solid #dce7f6;
            border-radius: 8px;
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

            .paper,
            .page {{
                border: 0 !important;
            }}
        }}

        @media (max-width: 760px) {{
            header.top {{
                min-height: 110px;
                padding: 20px 16px !important;
            }}

            .bar {{
                position: static;
                padding: 10px !important;
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
