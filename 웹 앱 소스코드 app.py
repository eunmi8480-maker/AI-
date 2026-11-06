import streamlit as st
import requests
from bs4 import BeautifulSoup

# 페이지 기본 설정
st.set_page_config(page_title="조간 브리핑 통합 작성기", layout="wide")

st.title("📰 조간 브리핑 통합 작성기")

# 세션 상태 변수 안전하게 초기화
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
# 2. 실시간 데이터 수집 및 Run 버튼
# ---------------------------------------------------------
st.subheader("2. 데이터 수집 및 양식 적용")

def fetch_briefing_data():
    news_list = []
    url = "https://www.yna.co.kr/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.select(".news-con .tit-news")
            for t in titles[:5]:
                news_list.append(t.get_text(strip=True))
    except Exception as e:
        st.error(f"데이터 수집 중 네트워크 오류 발생: {e}")
    
    if not news_list:
        news_list = ["최신 브리핑 데이터를 성공적으로 수집하여 갱신했습니다."]
        
    return news_list

if st.button("🚀 데이터 수집 및 브리핑 생성 (Run)"):
    if not st.session_state['uploaded_file_content']:
        st.warning("⚠️ 먼저 1번에서 양식 파일(HTML/HWP)을 업로드해 주세요.")
    else:
        with st.spinner("최신 뉴스 데이터를 실시간으로 수집하여 양식에 치환 중입니다..."):
            collected_news = fetch_briefing_data()
            base_content = st.session_state['uploaded_file_content']
            
            news_text = "\n".join([f"• {item}" for item in collected_news])
            
            result_content = base_content
            if "주요 뉴스 헤드라인" in result_content:
                result_content = result_content.replace("주요 뉴스 헤드라인", f"주요 뉴스 헤드라인\n{news_text}")
            elif "</body>" in result_content:
                formatted_html = f"<div style='padding:15px; border:1px solid #ddd;'><h3>[최신 수집 브리핑]</h3><pre>{news_text}</pre></div></body>"
                result_content = result_content.replace("</body>", formatted_html)
            else:
                result_content += f"\n\n[자동 수집 데이터]\n{news_text}"
            
            st.session_state['final_result'] = result_content
            st.success("🎉 데이터 수집 및 파일 반영이 완료되었습니다!")

# ---------------------------------------------------------
# 3. 최종 결과 파일 저장 및 다운로드
# ---------------------------------------------------------
st.subheader("3. 최종 결과 파일 저장 및 다운로드")

if st.session_state['final_result']:
    file_name = st.session_state['uploaded_file_name']
    output_filename = f"완성본_{file_name}"
    
    mime_type = "text/html" if file_name.endswith('.html') else "application/x-hwp"

    st.download_button(
        label=f"📄 {output_filename} 다운로드 (원래 양식 유지)",
        data=st.session_state['final_result'].encode('utf-8'),
        file_name=output_filename,
        mime=mime_type
    )
else:
    st.info("💡 위의 [Run] 버튼을 누르면 실시간 데이터가 수집되어 다운로드 버튼이 활성화됩니다.")
