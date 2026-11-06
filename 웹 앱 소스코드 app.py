import streamlit as st
import json
import os
import time

# 1. 페이지 메타 설정 (넓은 레이아웃)
st.set_page_config(
    page_title="AI큐레이터 - 통합 시스템",
    page_icon="🤖",
    layout="wide"
)

# 2. 메인 타이틀 및 헤더
st.title("🤖 AI큐레이터")
st.caption("업무 효율화 및 브리핑 통합 관리 플랫폼")
st.divider()

# 3. 메인 탭 구성 (단순업무효율화 / 요약형 브리핑)
tab1, tab2 = st.tabs(["⚡ 단순업무효율화 (RUN)", "📝 요약형 브리핑"])

# =========================================================
# [TAB 1] 단순업무효율화 (RUN 브리핑 실행)
# =========================================================
with tab1:
    st.header("⚡ 조간 및 이슈 브리핑 프로세스")
    st.write("버튼을 누르면 브리핑 생성 및 데이터 처리가 시작됩니다.")
    st.write("")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 실행 옵션")
        briefing_type = st.selectbox(
            "브리핑 유형 선택", 
            ["조간 종합 브리핑", "긴급 이슈 보고", "주간 동향 분석"]
        )
        include_details = st.checkbox("상세 데이터 포함", value=True)
        
        st.write("")
        # 메인 RUN 버튼
        run_btn = st.button("▶️ RUN (브리핑 실행)", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 실행 및 결과물 출력")
        
        if run_btn:
            with st.spinner("데이터 수집 및 통합 브리핑을 생성 중입니다..."):
                time.sleep(1.5)  # 처리 대기 연출
                
            st.success("✅ 브리핑 생성이 성공적으로 완료되었습니다!")
            
            # 텍스트 결과물 예시
            result_content = f"""[ {briefing_type} 리포트 ]
작성일시: 2026-11-06
시스템: AI큐레이터 자동화 엔진

1. 주요 이슈 요약
   - 업무 효율화 프로세스 가동 완료
   - 주요 데이터 자동 집계 및 브리핑 문서 생성 성공

2. 세부 현황
   - 입력 데이터 연동: 정상 (예제입력_시험용.json)
   - 템플릿 서식 적용: 완료

3. 종합 의견
   - 수집된 핵심 항목 분석 완료. 즉시 공유 가능합니다."""

            st.markdown("### 📄 브리핑 결과")
            st.info(result_content)
            
            # 결과 파일 다운로드 기능
            st.download_button(
                label="📥 브리핑 결과물 다운로드 (.txt)",
                data=result_content,
                file_name=f"{briefing_type}_결과.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("👈 왼쪽 패널에서 [▶️ RUN (브리핑 실행)] 버튼을 클릭해 주세요.")

# =========================================================
# [TAB 2] 요약형 브리핑
# =========================================================
with tab2:
    st.header("📝 AI 요약 서비스")
    st.write("긴 본문 텍스트를 핵심 위주로 요약합니다.")
    
    summary_mode = st.radio("요약 형태", ["3줄 요약", "핵심 불렛포인트", "키워드 추출"], horizontal=True)
    input_text = st.text_area("요약할 본문 입력:", height=180, placeholder="이곳에 긴 문서나 뉴스를 입력하세요...")
    
    if st.button("요약 생성하기"):
        if input_text.strip():
            st.subheader("📌 요약 결과물")
            if summary_mode == "3줄 요약":
                st.success("1. 입력된 본문의 주요 핵심 주제입니다.\n2. 세부 내용 및 진행 상황 요약입니다.\n3. 결론 및 향후 처리 방향입니다.")
            elif summary_mode == "핵심 불렛포인트":
                st.markdown("- **포인트 1**: 주요 이슈 항목 첫 번째\n- **포인트 2**: 주요 이슈 항목 두 번째\n- **포인트 3**: 마무리 결과")
            else:
                st.info("🏷️ **추출 키워드**: #AI큐레이터 #업무효율화 #자동요약 #브리핑")
        else:
            st.warning("요약할 텍스트를 입력해 주세요.")
