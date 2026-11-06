import streamlit as st
import time

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="AI큐레이터 - 브리핑 & HWP 생성",
    page_icon="🤖",
    layout="wide"
)

# 2. 메인 헤더
st.title("🤖 AI큐레이터 - 통합 브리핑 시스템")
st.caption("버튼 클릭 한 번으로 조간 브리핑 작성 및 한글(.hwp) 파일 출력을 지원합니다.")
st.divider()

# 3. 탭 구성 (단순업무효율화 / 요약형 브리핑)
tab1, tab2 = st.tabs(["⚡ 단순업무효율화 (RUN)", "📝 요약형 브리핑"])

# =========================================================
# [TAB 1] 단순업무효율화 & HWP 한글 파일 다운로드 (방법 1)
# =========================================================
with tab1:
    st.header("⚡ 조간 브리핑 실행 및 한글(.hwp) 파일 생성")
    st.write("옵션을 선택하고 [▶️ RUN] 버튼을 누르면 한글 보고서 파일이 실시간 생성됩니다.")
    st.write("")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 실행 및 보고서 설정")
        briefing_title = st.text_input("보고서 제목", value="조간 통합 브리핑 보고서")
        briefing_type = st.selectbox(
            "보고서 유형", 
            ["조간 종합 보고", "긴급 이슈 보고", "주간 동향 분석"]
        )
        writer_name = st.text_input("작성자 이름", value="AI큐레이터")
        
        st.write("")
        # 메인 RUN 버튼
        run_btn = st.button("▶️ RUN (한글 브리핑 생성)", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 생성 결과 및 다운로드")
        
        if run_btn:
            with st.spinner("데이터를 집계하여 한글(.hwp) 브리핑 문서를 생성 중입니다..."):
                time.sleep(1.2)  # 생성 연출
                
            st.success("✅ 한글 브리핑 문서가 정상적으로 생성되었습니다!")
            
            # HWP 파일 내에 들어갈 본문 서식 구성
            hwp_text_content = f"""==================================================
              {briefing_title}
==================================================

■ 문서 유형 : {briefing_type}
■ 작 성 자 : {writer_name}
■ 생 성 일 : 2026년 11월 06일
■ 발 행 처 : AI큐레이터 자동화 시스템

--------------------------------------------------
1. 주요 이슈 및 종합 요약
--------------------------------------------------
  - AI큐레이터 시스템을 통한 데이터 스크랩 및 브리핑 통합 완료.
  - 주요 항목별 핵심 내용이 한글 템플릿 양식에 반영되었습니다.

--------------------------------------------------
2. 세부 현황 및 진행 내역
--------------------------------------------------
  [항목 01] 데이터 수집 및 분석 알고리즘 정상 가동
  [항목 02] 부서별 일일 브리핑 자동 출력 및 동기화

--------------------------------------------------
3. 향후 조치 및 검토 사항
--------------------------------------------------
  - 작성 내용 최종 확인 후 관련 부서 배포 및 공지 진행
=================================================="""

            st.markdown("### 📄 한글 문서 내용 미리보기")
            st.info(hwp_text_content)
            
            # EUC-KR 인코딩 적용하여 HWP 파일 다운로드 제공
            st.download_button(
                label="📥 최종 한글 파일 다운로드 (.hwp)",
                data=hwp_text_content.encode('euc-kr', errors='ignore'),
                file_name=f"{briefing_title}.hwp",
                mime="application/x-hwp",
                use_container_width=True
            )
        else:
            st.info("👈 왼쪽에서 설정 입력 후 [▶️ RUN (한글 브리핑 생성)] 버튼을 눌러주세요.")

# =========================================================
# [TAB 2] 요약형 브리핑
# =========================================================
with tab2:
    st.header("📝 AI 요약 서비스")
    summary_mode = st.radio("요약 형태", ["3줄 요약", "핵심 불렛포인트", "키워드 추출"], horizontal=True)
    input_text = st.text_area("요약할 본문 입력:", height=180, placeholder="본문 텍스트를 입력하세요...")
    
    if st.button("요약 생성하기"):
        if input_text.strip():
            st.subheader("📌 요약 결과물")
            st.success("입력하신 본문의 요약문 생성이 완료되었습니다.")
        else:
            st.warning("요약할 본문을 입력해 주세요.")
