import streamlit as st

# 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="내 웹 프로그램", page_icon="🚀")

st.title("파이썬 웹 프로그램")
st.subheader("설치 없이 바로 사용하는 개인 개발 프로그램")

# 사용자 입력 받기
name = st.text_input("이름을 입력하세요:", value="홍길동")

# 버튼 클릭 시 파이썬 로직 실행
if st.button("실행하기"):
    st.success(f"안녕하세요, {name}님! 파이썬 백엔드가 웹에서 정상적으로 실행되었습니다.")
    
    # 예시: 파이썬 데이터 처리 결과 보여주기
    st.write("### 실행 결과 요약")
    st.json({"status": "Success", "user": name, "mode": "Cloud Web App"})