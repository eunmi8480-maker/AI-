from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone, timedelta
import json
from data_services import fetch_keywords, fetch_headlines, error_message

# ==================================================
# 1) 기본 설정
# ==================================================
st.set_page_config(
    page_title="AI 큐레이터 | 조간 브리핑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
HTML_CANDIDATES = [
    BASE_DIR / "briefing.html",
    BASE_DIR / "조간브리핑_통합작성기_서버연결.html",
    BASE_DIR / "조간브리핑_통합작성기.html",
    BASE_DIR / "완성본_조간브리핑_통합작성기.html",
    BASE_DIR / "조간브리핑_통합편집_130836.html",
]
HTML_PATH = next((p for p in HTML_CANDIDATES if p.is_file()), None)
LOGO_PATH = BASE_DIR / "ai_curator_logo.png"

if "page" not in st.session_state:
    st.session_state.page = "home"

KST = timezone(timedelta(hours=9))
today_str = datetime.now(KST).strftime("%Y-%m-%d")

# ==================================================
# 2) 화면 이동 함수
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

# ==================================================
# 3) 유틸
# ==================================================
def file_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")

def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp949", errors="replace")

# ==================================================
# 5) 폰트 / 로고
# ==================================================
FONT_CANDIDATES = [
    (BASE_DIR / "KoPubDotum.woff2", "font/woff2", "woff2"),
    (BASE_DIR / "KoPubDotum.ttf", "font/ttf", "truetype"),
]
font_face_css = ""
for fpath, mime, ffmt in FONT_CANDIDATES:
    if fpath.is_file():
        encoded = file_to_base64(fpath)
        font_face_css = f"""
        @font-face {{
            font-family: "KoPubDotum";
            src: url("data:{mime};base64,{encoded}") format("{ffmt}");
            font-style: normal;
            font-weight: 400;
            font-display: swap;
        }}
        """
        break

if LOGO_PATH.is_file():
    logo_html = f'<div class="brief-logo brief-logo-image"><img src="data:image/png;base64,{file_to_base64(LOGO_PATH)}" alt="AI CURATOR"></div>'
else:
    logo_html = '<div class="brief-logo brief-logo-text">AI CURATOR<small>하루를 시작하는 조간 브리핑</small></div>'

D_ICON_SVG = '<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 120px; height: 120px; filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.45));"><defs><linearGradient id="grad-d" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#38bdf8"/><stop offset="50%" stop-color="#818cf8"/><stop offset="100%" stop-color="#4f46e5"/></linearGradient></defs><path d="M20 10 H52 C74 10, 90 26, 90 50 C90 74, 74 90, 52 90 H20 Z" fill="url(#grad-d)"/><path d="M38 28 H50 C62 28, 72 36, 72 50 C72 64, 62 72, 50 72 H38 Z" fill="#0d1c59"/><path d="M46 58 L54 42 L60 48 L48 60 Z" fill="url(#grad-d)"/><circle cx="58" cy="44" r="2" fill="#ffffff"/></svg>'

# ==================================================
# 6) 전역 CSS
# ==================================================
page_css = f"""
<style>
{font_face_css}
:root {{
    --navy: #0d1c59;
    --sky: #9be7ff;
    --sky-soft: #dff6ff;
}}
html, body, .stApp, .stApp button {{
    font-family: "KoPubDotum", sans-serif !important;
}}
.stApp {{ min-height: 100vh; background: var(--navy); }}
.block-container {{ max-width: 100%; padding: 0 !important; }}
header[data-testid="stHeader"] {{ display: none; }}
footer {{ display: none; }}

.st-key-landing {{
    min-height: 100vh;
    color: #ffffff;
    background: linear-gradient(180deg, #0d1c59 0%, #0d1c59 48%, #29477f 77%, #7895be 100%);
}}
.brief-nav {{
    max-width: 1180px; margin: 0 auto; padding: 25px 32px;
    display: flex; justify-content: space-between; align-items: center;
}}
.brief-logo-image {{ width: min(400px, 45vw); }}
.brief-logo-image img {{ width: 100%; height: auto; }}
.brief-logo-text {{
    color: #fff; font-size: 28px; font-weight: 800;
}}
.brief-logo-text small {{
    display: block; margin-top: 8px; font-size: 12px; font-weight: 400;
}}

.brief-hero {{
    max-width: 1000px; margin: 0 auto; padding: 30px 20px 0; text-align: center;
}}
.brief-hero-icon {{
    margin: 0 auto 20px;
}}
.brief-hero h1 {{
    margin: 0; color: #fff; font-size: clamp(20px, 2.2vw, 26px); font-weight: 700; line-height: 1.4;
}}
.brief-hero h1 span {{ color: var(--sky); }}
.brief-hero p {{ margin: 16px auto 0; color: #f0f4ff; font-size: clamp(15px, 1.6vw, 18px); line-height: 1.7; }}

.st-key-main_tabs {{
    max-width: 680px;
    margin: 40px auto 80px;
    padding: 0 20px;
}}
.st-key-main_tabs button {{
    min-height: 54px !important;
    border-radius: 27px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}}

.st-key-tab_daily button {{
    background: rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border: 1px solid #9be7ff !important;
    box-shadow: 0 0 12px rgba(155, 231, 255, 0.3) !important;
}}
.st-key-tab_daily button:hover {{
    background: #ffffff !important;
    color: #0d1c59 !important;
}}

.st-key-tab_efficiency button, .st-key-tab_summary button {{
    background: rgba(255, 255, 255, 0.08) !important;
    color: #c2d6ff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}}
.st-key-tab_efficiency button:hover, .st-key-tab_summary button:hover {{
    background: rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border-color: #9be7ff !important;
}}

.sub-page-container {{
    max-width: 1200px;
    margin: 40px auto;
    padding: 30px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #ffffff;
}}

.st-key-editor_page {{
    min-height: 100vh;
    background: linear-gradient(180deg, #0d1c59 0%, #0d1c59 28%, #29477f 62%, #7895be 100%);
}}
.st-key-editor_page > div {{
    width: 100%; max-width: 1440px; margin: 0 auto; padding: 0 24px 34px;
}}
.st-key-editor_topbar {{
    position: sticky; top: 0; z-index: 1000;
    width: 100%; padding: 12px 0; background: #0d1c59;
    border-bottom: 1px solid rgba(255,255,255,0.18);
}}
.st-key-editor_home button {{
    width: 140px !important; min-height: 44px !important;
    border: 1px solid #fff !important; border-radius: 8px !important;
    background: #fff !important; color: #0d1c59 !important; font-weight: 800 !important;
}}
.st-key-editor_page div[data-testid="stIFrame"] {{
    width: 100%; border: 1px solid #6f8fbd; border-radius: 0 0 12px 12px; background: #fff;
}}
.editor-file-error {{
    margin: 24px; padding: 22px; border: 1px solid #e3cf82; border-radius: 10px; background: #fff8dc;
    color: #5a4914;
}}
</style>
"""
st.markdown(page_css, unsafe_allow_html=True)

# ==================================================
# 7) 홈 화면
# ==================================================
if st.session_state.page == "home":
    with st.container(key="landing"):
        nav_html = f'<div class="brief-nav">{logo_html}</div>'
        hero_html = f'<div class="brief-hero"><div class="brief-hero-icon">{D_ICON_SVG}</div><h1><span>오늘의 뉴스,</span> 한눈에 정리하세요.</h1><p>워드클라우드부터 주요 기사와 정부 동향까지.<br>필요한 내용을 입력하고 조간 브리핑을 완성해 보세요.</p></div>'

        st.markdown(nav_html, unsafe_allow_html=True)
        st.markdown(hero_html, unsafe_allow_html=True)

        with st.container(key="main_tabs"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("일일브리핑", key="tab_daily", on_click=go_editor, use_container_width=True)
            with col2:
                st.button("효율화", key="tab_efficiency", on_click=go_efficiency, use_container_width=True)
            with col3:
                st.button("요약", key="tab_summary", on_click=go_summary, use_container_width=True)

# ==================================================
# 8) 일일브리핑 작성기 화면 (연합뉴스 자동 수집 포함)
# ==================================================
elif st.session_state.page == "editor":
    with st.container(key="editor_page"):
        with st.container(key="editor_topbar"):
            st.button("← 홈으로", key="editor_home", on_click=go_home)

        if HTML_PATH is None:
            st.markdown(
                '<div class="editor-file-error"><strong>작성기 HTML 파일을 찾을 수 없습니다.</strong></div>',
                unsafe_allow_html=True,
            )
            st.stop()

        try:
            html_content = read_text_file(HTML_PATH)
        except Exception as e:
            st.error(f"HTML 파일을 읽을 수 없습니다: {e}")
            st.stop()

        if not st.session_state.get("editor_ready", False):
            st.subheader("일일브리핑 자료 준비")
            selected = st.date_input("보고일", value=datetime.now(KST).date())
            collect = st.checkbox("스크랩마스터 키워드·신문 1면 단어쌍·연합뉴스 07:30 헤드라인 수집", value=True)
            st.caption("선택한 날짜로 조회합니다. 신문 1면 단어쌍은 오늘 자료만 제공합니다. 수집에 실패한 자료는 작성기에서 직접 넣을 수 있습니다.")
            
            if st.button("작성기 열기", key="open_final_editor", type="primary"):
                report_date = selected.strftime("%Y-%m-%d")
                boot = {"version": 1, "date": report_date, "sources": {}}
                messages = []
                
                if collect:
                    with st.spinner("선택한 날짜의 자료를 수집하고 있습니다…"):
                        # 1) 도정 키워드 및 신문 1면 단어쌍 수집
                        for label, target, national in [("도정 키워드", "words", False), ("신문 1면 단어쌍", "nationalWords", True)]:
                            try:
                                pairs = fetch_keywords(report_date, national=national)
                                boot[target] = "\n".join(f"{x['word']},{x['score']:g}" for x in pairs)
                                boot["sources"]["nationalCloud" if national else "cloud"] = report_date
                                messages.append((True, f"{label}: {len(pairs)}개 수집 / {report_date}"))
                            except Exception as exc:
                                messages.append((False, label + ": " + error_message(exc)))
                        
                        # 2) 연합뉴스 07:30 헤드라인 수집
                        try:
                            text, source_url = fetch_headlines(report_date)
                            boot["headlines"] = text
                            boot["sources"]["headlines"] = report_date
                            boot["sources"]["headline_url"] = source_url
                            messages.append((True, "헤드라인: " + report_date + " 07:30 게시시각 검증 완료"))
                        except Exception as exc:
                            messages.append((False, "헤드라인: " + error_message(exc)))
                            
                st.session_state.editor_boot = boot
                st.session_state.editor_messages = messages
                st.session_state.editor_ready = True
                st.rerun()
            st.stop()

        for ok, message in st.session_state.get("editor_messages", []):
            (st.success if ok else st.warning)(message)
        st.caption("홈으로 이동하거나 새로고침하기 전에 작성기 안의 ‘작업 저장’을 눌러 주세요. 입력 내용과 이미지는 작업 JSON으로 보관합니다.")
        
        boot_json = json.dumps(st.session_state.get("editor_boot", {}), ensure_ascii=False).replace("<", "\\u003c")
        html_content = html_content.replace("<!--BOOT-->", '<script type="application/json" id="boot-data">' + boot_json + '</script>')

        editor_css = f"""
        <style>
        {font_face_css}
        html, body {{ font-family: "KoPubDotum", sans-serif !important; }}
        body {{
            background: linear-gradient(180deg, #0d1c59 0, #0d1c59 180px, #29477f 430px, #7895be 100%);
        }}
        header.top {{ background: #0d1c59 !important; color: #fff !important; }}
        header.top h1 {{ color: #9be7ff !important; }}
        aside {{ background: #0d1c59 !important; color: #fff !important; }}
        aside * {{ color: #fff !important; }}
        .card {{ background: #fff !important; border-radius: 10px !important; }}
        textarea, input {{ background: #fff !important; color: #102653 !important; }}
        button.primary {{ background: #0d1c59 !important; color: #fff !important; }}
        </style>
        """

        head_end = html_content.lower().find("</head>")
        if head_end != -1:
            html_content = html_content[:head_end] + editor_css + html_content[head_end:]

        components.html(html_content, height=1100, scrolling=True)

# ==================================================
# 9) 효율화 탭 (빈 공간)
# ==================================================
elif st.session_state.page == "efficiency":
    with st.container(key="editor_topbar"):
        st.button("← 홈으로", key="eff_home", on_click=go_home)
    st.markdown('''
        <div class="sub-page-container">
            <h2>⚙️ 효율화 페이지</h2>
            <p style="margin-top: 15px; color: #a0aec0;">추후 필요한 새로운 기능 및 컴포넌트를 채워 넣으실 수 있는 공간입니다.</p>
        </div>
    ''', unsafe_allow_html=True)

# ==================================================
# 10) 요약 탭 (빈 공간)
# ==================================================
elif st.session_state.page == "summary":
    with st.container(key="editor_topbar"):
        st.button("← 홈으로", key="sum_home", on_click=go_home)
    st.markdown('''
        <div class="sub-page-container">
            <h2>📝 요약 페이지</h2>
            <p style="margin-top: 15px; color: #a0aec0;">추후 요약 기능 및 파일 업로드 컴포넌트를 채워 넣으실 수 있는 공간입니다.</p>
        </div>
    ''', unsafe_allow_html=True)
