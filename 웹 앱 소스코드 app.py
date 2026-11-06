import streamlit as st

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="AI큐레이터",
    page_icon="🤖",
    layout="wide"
)

# 2. 메인 헤더 타이틀 (AI큐레이터 중심 UI)
st.title("🤖 AI큐레이터")
st.caption("스마트한 업무 지원 및 텍스트 요약 통합 플랫폼")
st.divider()

# 3. 탭 구성 (단순업무효율화 / 요약형)
tab1, tab2 = st.tabs(["⚡ 단순업무효율화", "📝 요약형 서비스"])

# ---------------------------------------------------------
# [TAB 1] 단순업무효율화 탭
# ---------------------------------------------------------
with tab1:
    st.header("⚡ 업무 효율화 도구")
    st.write("반복적이고 단순한 업무를 빠르게 처리할 수 있는 도구 모음입니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. 이메일/문서 양식 자동 생성")
        email_type = st.selectbox("작성할 문서 종류", ["업무 보고", "미팅 요청", "공지사항", "협조 요청"])
        topic = st.text_input("주요 내용 요약 (키워드)", placeholder="예: 다음 주 월요일 프로젝트 점검 회의")
        
        if st.button("초안 생성하기"):
            st.info(f"[{email_type}] 초안이 생성되었습니다:")
            st.text_area("생성 결과", value=f"제목: [{email_type}] {topic} 관련 건\n\n안녕하세요,\n\n{topic} 관련하여 안내 및 요청드립니다.\n확인 후 피드백 부탁드립니다.\n\n감사합니다.", height=150)

    with col2:
        st.subheader("2. 빠른 계산 및 단위 변환기")
        num1 = st.number_input("숫자 1", value=10000)
        num2 = st.number_input("숫자 2", value=15)
        
        calc_op = st.selectbox("연산 선택", ["퍼센트 계산 (%)", "합계 (+)", "차이 (-)"])
        if st.button("계산 실행"):
            if calc_op == "퍼센트 계산 (%)":
                result = num1 * (num2 / 100)
            elif calc_op == "합계 (+)":
                result = num1 + num2
            else:
                result = num1 - num2
            st.success(f"계산 결과: **{result:,.2f}**")

# ---------------------------------------------------------
# [TAB 2] 요약형 탭
# ---------------------------------------------------------
with tab2:
    st.header("📝 AI 요약 서비스")
    st.write("긴 글이나 문서를 간결하게 핵심 위주로 요약해 드립니다.")
    
    summary_mode = st.radio("요약 방식 선택", ["3줄 핵심 요약", "불렛포인트 형태", "키워드 추출"], horizontal=True)
    
    input_text = st.text_area("요약할 전체 본문을 붙여넣으세요:", height=200, placeholder="이곳에 긴 텍스트를 입력하세요...")
    
    if st.button("요약 실행"):
        if input_text.strip():
            st.subheader("📌 요약 결과")
            if summary_mode == "3줄 핵심 요약":
                st.success("1. 입력된 본문의 핵심 주제입니다.\n2. 주요 진행 상황 및 세부 내용 요약입니다.\n3. 결론 및 향후 조치 사항입니다.")
            elif summary_mode == "불렛포인트 형태":
                st.markdown("- **핵심 1**: 입력 데이터 주요 포인트 1\n- **핵심 2**: 주요 내용 정리 2\n- **핵심 3**: 마무리 결과 3")
            else:
                st.info("🏷️ **추출된 키워드**: #업무효율화 #AI큐레이터 #요약 #자동화")
        else:
            st.warning("요약할 텍스트를 먼저 입력해 주세요.")
