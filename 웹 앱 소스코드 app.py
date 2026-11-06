import streamlit as st
import pandas as pd

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="나만의 AI & 데이터 분석 앱", page_icon="✨", layout="wide")

# 2. 사이드바 메인 메뉴 구성
st.sidebar.title("📌 기능 선택")
menu = st.sidebar.radio("원하는 기능을 선택하세요:", ["메인 홈", "텍스트/문서 분석", "데이터 계산기", "설정"])

# 3. 메뉴별 화면 구성을 파이썬 코드로 제어
if menu == "메인 홈":
    st.title("👋 나만의 전용 웹 애플리케이션")
    st.write("이곳은 파이썬으로 동작하는 개인 맞춤형 웹 앱입니다.")
    
    # 사용자 입력 받기
    user_input = st.text_input("오늘의 메모나 아이디어를 입력하세요:")
    if st.button("저장하기"):
        st.success(f"입력하신 내용: '{user_input}' 이(가) 저장되었습니다.")

elif menu == "텍스트/문서 분석":
    st.title("📝 텍스트 글자 수 및 단어 분석")
    text = st.text_area("분석할 텍스트를 입력하세요:", height=150)
    if st.button("분석 실행"):
        char_count = len(text)
        word_count = len(text.split())
        st.metric(label="총 글자 수 (공백 포함)", value=f"{char_count} 자")
        st.metric(label="단어 수", value=f"{word_count} 개")

elif menu == "데이터 계산기":
    st.title("🧮 자동 계산기")
    num1 = st.number_input("첫 번째 숫자", value=10)
    num2 = st.number_input("두 번째 숫자", value=5)
    op = st.selectbox("연산자 선택", ["+", "-", "*", "/"])
    
    if st.button("계산하기"):
        if op == "+": res = num1 + num2
        elif op == "-": res = num1 - num2
        elif op == "*": res = num1 * num2
        elif op == "/": res = num1 / num2 if num2 != 0 else "0으로 나눌 수 없습니다."
        st.subheader(f"결과: {res}")
