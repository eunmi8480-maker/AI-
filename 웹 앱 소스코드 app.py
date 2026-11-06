from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="조간 브리핑 통합 작성기",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 기존 HTML 양식 파일을 읽는 방식은 유지합니다.
html_path = Path(__file__).parent / "조간브리핑_통합작성기.html"

st.markdown(
    """
    <style>
    /* Streamlit 기본 여백 조정 */
    .block-container {
        max-width: 100%;
        padding: 0 0 4rem 0;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* 이미지와 비슷한 상단 디자인 */
    .site-wrap {
        color: white;
        background: linear-gradient(
            180deg,
            #0b1957 0%,
            #0b1957 48%,
            #45649c 82%,
            #829cc5 100%
        );
    }

    .site-nav {
        max-width: 1200px;
        margin: 0 auto;
        padding: 22px 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
    }

    .brand {
        color: white !important;
        text-decoration: none !important;
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1;
    }

    .brand small {
        display: block;
        margin-top: 9px;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0;
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 44px;
    }

    .nav-links a {
        color: rgba(255, 255, 255, 0.75) !important;
        text-decoration: none !important;
        font-size: 16px;
        font-weight: 600;
    }

    .nav-links a:hover {
        color: white !important;
    }

    .hero {
        max-width: 1000px;
        min-height: 510px;
        margin: 0 auto;
        padding: 76px 24px 65px;
        box-sizing: border-box;
        text-align: center;
    }

    .hero-ring {
        width: 78px;
        height: 78px;
        margin: 0 auto 38px;
        border: 17px solid transparent;
        border-radius: 50%;
        background:
            linear-gradient(#0b1957, #0b1957) padding-box,
            linear-gradient(135deg, #a3fbff, #2688ff) border-box;
        transform: rotate(-28deg) skew(-10deg);
    }

    .hero h1 {
        margin: 0;
        color: white;
        font-size: clamp(34px, 4.3vw, 54px);
        font-weight: 800;
        line-height: 1.35;
        word-break: keep-all;
    }

    .hero h1 span {
        color: #a9e4ff;
    }

    .hero p {
        margin: 25px auto 0;
        color: rgba(255, 255, 255, 0.94);
        font-size: clamp(16px, 1.8vw, 21px);
        line-height: 1.8;
        word-break: keep-all;
    }

    .hero-tags {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 55px;
    }

    .hero-tags span {
        padding: 9px 16px;
        border: 1px solid rgba(255, 255, 255, 0.45);
        border-radius: 7px;
        font-size: 14px;
        font-weight: 600;
    }

    .hero-cta {
        display: inline-block;
        margin-top: 22px;
        padding: 14px 26px;
        border-radius: 8px;
        background: white;
        color: #11215d !important;
        text-decoration: none !important;
        font-size: 16px;
        font-weight: 800;
    }

    .hero-cta:hover {
        background: #e7f3ff;
    }

    .editor-heading {
        max-width: 1200px;
        margin: 0 auto;
        padding: 42px 24px 14px;
    }

    .editor-heading h2 {
        margin: 0 0 8px;
        font-size: 28px;
    }

    .editor-heading p {
        margin: 0;
        color: #667085;
        font-size: 15px;
    }

    /* 양식 iframe 주변 여백 */
    div[data-testid="stIFrame"] {
        padding: 0 24px;
    }

    @media (max-width: 640px) {
        .site-nav {
            padding: 18px 20px;
        }

        .brand {
            font-size: 24px;
        }

        .nav-links {
            gap: 16px;
        }

        .nav-links a {
            font-size: 13px;
        }

        .hero {
            min-height: 460px;
            padding: 65px 22px 55px;
        }

        .hero-ring {
            width: 58px;
            height: 58px;
            border-width: 13px;
        }
    }
    </style>

    <div class="site-wrap">
        <nav class="site-nav">
            <a class="brand" href="#home">
                morning brief
                <small>하루를 시작하는 조간 브리핑</small>
            </a>
            <div class="nav-links">
                <a href="#home">홈</a>
                <a href="#editor">브리핑 작성</a>
            </div>
        </nav>

        <section class="hero" id="home">
            <div class="hero-ring"></div>
            <h1><span>오늘의 뉴스,</span><br>한눈에 정리하세요.</h1>
            <p>
                워드클라우드부터 주요 기사와 정부 동향까지.<br>
                필요한 내용을 입력하고 조간 브리핑을 완성해 보세요.
            </p>

            <div class="hero-tags">
                <span>#조간브리핑</span>
                <span>#뉴스정리</span>
                <span>#보고서작성</span>
            </div>

            <a class="hero-cta" href="#editor">브리핑 작성 시작 →</a>
        </section>
    </div>

    <div class="editor-heading" id="editor">
        <h2>조간 브리핑 작성기</h2>
        <p>아래 양식에 내용을 입력해 주세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not html_path.exists():
    st.error(f"양식 파일을 찾을 수 없습니다: {html_path.name}")
    st.stop()

html_content = html_path.read_text(encoding="utf-8-sig")

# 기존 양식 표시 기능
components.html(
    html_content,
    height=1100,
    scrolling=True,
)
