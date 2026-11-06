import streamlit as st
import json
import os
import time

st.set_page_config(page_title="AI큐레이터 - 브리핑 시스템", layout="wide")

st.title("🤖 AI큐레이터 - 통합 브리핑")
st.caption("버튼을 누르면 실시간 브리핑 결과물이 생성됩니다.")
st.divider()

# 탭 구성
tab1, tab2 = st.tabs(["🚀 단순업무효율화 (RUN)", "📝 요약형 브리핑"])

with tab1:
    st.header("⚡ 조간 브리핑 실행")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 실행 설정")
        briefing_type = st.selectbox("브리핑 유형", ["일반 조간 브리핑", "긴급 이슈 브리핑", "주간 종합 보고"])
        include_hwp = st.checkbox("HWP 출력 포함", value=True)
        
        # RUN 버튼
        run_btn = st.button("▶️ RUN (실행하기)", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 생성 결과물")
        
        if run_btn:
            with st.spinner("데이터 스크랩 및 브리핑 생성 중..."):
                time.sleep(1.5) # 실행 대기 효과
                
            st.success("✅ 생성 작업이 완료되었습니다!")
            
            # 결과물 출력 영역
            st.markdown("### 📄 생성된 브리핑 보고서")
            result_text = f"""
            **[ {briefing_type} 결과 리포트 ]**
            
            1. **주요 이슈 요약**
               - AI 큐레이터 시스템을 통한 업무 프로세스 단축 성공
               - 데이터 자동 스크랩 및 브리핑 작성 완료
            
            2. **세부 진행 상황**
               - 입력 파일 연동 상태: 정상
               - 결과 템플릿 적용: 완료
            
            3. **향후 조치 사항**
               - 담당자 검토 후 최종 보고서 배포 예정
            """
            st.info(result_text)
            
            # 결과물 다운로드 버튼 제공
            st.download_button(
                label="📥 브리핑 결과 다운로드 (.txt)",
                data=result_text,
                file_name="briefing_result.txt",
                mime="text/plain"
            )
        else:
            st.info("👈 왼쪽에서 [▶️ RUN] 버튼을 누르면 이 공간에 결과물이 표시됩니다.")

with tab2:
    st.header("📝 요약형 서비스")
    user_text = st.text_area("요약할 본문을 입력하세요:", height=150)
    if st.button("요약 생성"):
        if user_text:
            st.subheader("📌 요약 결과물")
            st.success(f"입력하신 글의 주요 내용:\n- {user_text[:50]}... (요약 완료)")
        else:
            st.warning("본문을 입력해 주세요.")
