from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="조간 브리핑 통합 작성기",
    layout="wide",
)

html_path = Path(__file__).parent / "완성본_조간브리핑_통합작성기.html"

if not html_path.exists():
    st.error(f"양식 파일을 찾을 수 없습니다: {html_path.name}")
    st.stop()

html_content = html_path.read_text(encoding="utf-8-sig")

# 홈페이지가 열리면 양식을 바로 표시합니다.
components.html(html_content, height=1000, scrolling=True)
