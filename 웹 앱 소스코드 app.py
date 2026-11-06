import streamlit as st

# 1. 페이지 레이아웃을 넓게(wide) 설정
st.set_page_config(
    page_title="나만의 AI 서비스",
    page_icon="🎨",
    layout="wide"  # "centered" 또는 "wide" 선택 가능
)

# 2. 사이드바(왼쪽 메뉴) 구성
with st.sidebar:
    st.header("⚙️ 컨트롤 패널")
    st.write("원하는 설정을 선택하세요.")
    user_choice = st.selectbox("메뉴 선택", ["대시보드", "분석 도구", "도움말"])

# 3. 화면을 2개 또는 3개의 컬럼(열)으로 분할하여 배치
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 왼쪽 카드")
    st.info("이곳에 중요한 정보나 입력 폼을 넣을 수 있습니다.")
    st.button("왼쪽 버튼")

with col2:
    st.subheader("📊 오른쪽 카드")
    st.success("이곳에 실행 결과나 차트를 넣을 수 있습니다.")
    st.metric(label="현재 상태", value="정상 작동 중", delta="100%")

# 4. 이미지 파일이 올라가 있다면 이미지 출력 예시
# st.image("my_image.png", caption="업로드한 이미지")
