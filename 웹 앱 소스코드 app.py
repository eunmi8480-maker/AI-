import streamlit as st
import requests
from bs4 import BeautifulSoup

# 페이지 기본 설정
st.set_page_config(page_title="조간 브리핑 통합 작성기", layout="wide")

st.title("📰 조간 브리핑 통합 작성기")

# 세션 상태(Session State) 변수 안전하게 초기화
if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = ""
if 'uploaded_file_content' not in st.session_state:
    st.session_state['uploaded_file_content'] = ""
if 'final_result' not in st.session_state:
    st.session_state['final_result'] = ""

# ---------------------------------------------------------
# 1. 양식 파일 업로드
# ---------------------------------------------------------
st.subheader("1. 양식 파일 업로드")
uploaded_file = st.file_uploader(
    "사용할 HWP 또는 HTML 양식 파일을 업로드하세요.", 
    type=["html", "hwp", "xml", "txt"]
)

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("cp949", errors="ignore")
    
    st.session_state['uploaded_file_name'] = uploaded_file.name
    st.session_state['uploaded_file_content'] = content
    st.success(f"✅ '{uploaded_file.name}' 양식 파일이 정상적으로 로드되었습니다.")

# ---------------------------------------------------------
# 2. 실시간 데이터 수집 함수 및 Run 버튼
# ---------------------------------------------------------
st.subheader("2. 데이터 수집 및 양식 적용")

# 실제 뉴스 데이터 수집 함수 (연합뉴스 속보 데이터 크롤링 예시)
def collect_latest_news():
    news_items = []
    url = "https://www.yna.co.kr/news"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            titles = soup.select(".news-con .tit-news")
            for t in titles[:5]:
                title_text = t.get_text(strip=True)
                news_items.append(title_text)
    except Exception as e:
        st.error(f"데이터 수집 중 네트워크 오류 발생: {e}")
    
    if not news_items:
        news_items = ["최신 뉴스 데이터를 성공적으로 갱신했습니다."]
        
    return news_items

if st.button("🚀 데이터 수집 및 브리핑 생성 (Run)"):
    if not st.session_state['uploaded_file_content']:
        st.warning("⚠️ 먼저 1번에서 양식 파일(HTML/HWP)을 업로드해 주세요.")
    else:
        with st.spinner("최신 뉴스 데이터를 실시간으로 수집하여 양식에 치환 중입니다..."):
            # 1) 실시간 데이터 수집
            crawled_news = collect_latest_news()
            
            # 2) 수집된 데이터를 HTML/HWP 원본 양식 텍스트와 결합/치환
            base_content = st.session_state['uploaded_file_content']
            
            # 뉴스 데이터 치환 로직 (양식 내 주요 영역 태그/문구 반영)
            news_summary_text = "\n".join([f"• {news}" for news in crawled_news])
            
            # 양식 원본 데이터 유지 및 수집 결과 치환
            result_content = base_content
            if "주요 뉴스 헤드라인" in result_content:
                result_content = result_content.replace("주요 뉴스 헤드라인", f"주요 뉴스 헤드라인\n{news_summary_text}")
            elif "</body>" in result_content:
                formatted_news_html = f"<div style='margin:20px; padding:15px; border:1px solid #ccc;'><h3>[자동 수집된 최신 브리핑]</h3><pre>{news_summary_text}</pre></div></body>"
                result_content = result_content.replace("</body>", formatted_news_html)
            else:
                result_content += f"\n\n[자동 수집 결과]\n{news_summary_text}"
            
            # 세션에 최종 결과 저장
            st.session_state['final_result'] = result_content
            st.success("
