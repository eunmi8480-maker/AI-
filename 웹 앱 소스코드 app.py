import streamlit as st
import json
import os

st.set_page_config(page_title="AI큐레이터 - 브리핑 시스템", layout="wide")

st.title("🤖 AI큐레이터 - 통합 브리핑")
st.caption("웹에서 버튼 한 번으로 브리핑 및 생성을 실행합니다.")
st.divider()

# 탭 구성
tab1, tab2 = st.tabs(["🚀 RUN (실행)", "⚙️ 데이터/설정"])

with tab1:
    st.header("⚡ 브리핑 프로세스 실행")
    st.write("아래 버튼을 누르면 브리핑 생성이 시작됩니다.")
    
    # RUN 버튼 생성
    if st.button("▶️ RUN (브리핑 실행)", type="primary", use_container_width=True):
        with st.spinner("브리핑을 생성하고 있습니다... 잠시만 기다려주세요."):
            # -------------------------------------------------------------
            # 실제 실행할 파이썬 로직 또는 파이썬 함수 작성 위치
            # 예: MorningBriefing 내부 로직이나 데이터 처리 함수 호출
            # -------------------------------------------------------------
            
            # 실행 완료 메시지
            st.success("✅ 브리핑이 정상적으로 완료되었습니다!")
            
            # 결과 보여주기 예시
            st.subheader("📄 생성 결과")
            st.info("결과 리포트 또는 통합 작성기 내용이 여기에 출력됩니다.")

with tab2:
    st.header("📂 데이터 확인")
    # 예제입력_시험용.json 올렸을 경우 불러오기 예시
    if os.path.exists("예제입력_시험용.json"):
        with open("예제입력_시험용.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        st.json(data)
    else:
        st.warning("예제입력_시험용.json 파일이 저장소에 없습니다.")
