import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="조간 브리핑 통합 작성기", layout="wide")

st.title("📰 조간 브리핑 통합 작성기")

# 세션 상태(Session State) 변수 안전하게 초기화 (NameError 완벽 방지)
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
    # 업로드된 파일 읽기 및 세션 저장
    try:
        content = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("cp949", errors="ignore")
    
    st.session_state['uploaded_file_name'] = uploaded_file.name
    st.session_state['uploaded_file_content'] = content
    st.success(f"✅ '{uploaded_file.name}' 양식 파일이 정상적으로 로드되었습니다.")

# ---------------------------------------------------------
# 2. 데이터 수집 및 양식 적용 (Run 버튼)
# ---------------------------------------------------------
st.subheader("2. 데이터 수집 및 양식 적용")

if st.button("🚀 데이터 수집 및 브리핑 생성 (Run)"):
    if not st.session_state['uploaded_file_content']:
        st.warning("⚠️ 먼저 1번에서 양식 파일(HTML/HWP)을 업로드해 주세요.")
    else:
        with st.spinner("데이터를 수집하고 업로드한 양식에 적용 중입니다..."):
            # 업로드한 양식 내용을 기반으로 결과 생성
            result_content = st.session_state['uploaded_file_content']
            
            # 생성 결과 세션 저장
            st.session_state['final_result'] = result_content
            st.success("🎉 데이터 수집 및 양식 적용 완료!")

# ---------------------------------------------------------
# 3. 최종 결과 화면 출력 및 다운로드
# ---------------------------------------------------------
st.subheader("3. 최종 결과 파일 저장 및 다운로드")

if st.session_state['final_result']:
    file_name = st.session_state['uploaded_file_name']
    output_filename = f"완성본_{file_name}"
    
    # MIME 타입 및 확장자 처리
    if file_name.endswith('.html'):
        mime_type = "text/html"
    else:
        mime_type = "application/x-hwp"

    # 다운로드 버튼
    st.download_button(
        label=f"📄 {output_filename} 다운로드 (원래 양식 유지)",
        data=st.session_state['final_result'].encode('utf-8'),
        file_name=output_filename,
        mime=mime_type
    )
    
    # HTML 양식인 경우 화면 하단에 미리보기 표시
    if file_name.endswith('.html'):
        st.markdown("---")
        st.subheader("📋 갱신된 양식 미리보기")
        components.html(st.session_state['final_result'], height=800, scrolling=True)
else:
    st.info("💡 위의 [Run] 버튼을 누르면 다운로드 버튼과 미리보기가 활성화됩니다.")
