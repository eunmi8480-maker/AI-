import streamlit as st
import os

st.title("📰 조간 브리핑 통합 작성기")

# ---------------------------------------------------------
# 1. 양식 파일 업로드 (HTML 또는 HWP/HWPML 파일)
# ---------------------------------------------------------
st.subheader("1. 양식 파일 업로드")
uploaded_template = st.file_uploader(
    "사용할 HWP 또는 HTML 양식 파일을 업로드하세요.", 
    type=["html", "hwp", "xml", "txt"]
)

template_content = ""
if uploaded_template is not None:
    # 업로드된 파일 읽기
    try:
        template_content = uploaded_template.read().decode("utf-8")
    except UnicodeDecodeError:
        uploaded_template.seek(0)
        template_content = uploaded_template.read().decode("cp949", errors="ignore")
    st.success(f"✅ '{uploaded_template.name}' 양식 파일이 정상적으로 로드되었습니다.")

# ---------------------------------------------------------
# 2. 데이터 수집 실행 (Run 버튼)
# ---------------------------------------------------------
st.subheader("2. 데이터 수집 및 양식 적용")

if st.button("🚀 데이터 수집 및 브리핑 생성 (Run)"):
    if not template_content:
        st.warning("⚠️ 먼저 1번에서 양식 파일(HTML/HWP)을 업로드해 주세요.")
    else:
        with st.spinner("데이터를 수집하고 업로드한 양식에 적용 중입니다..."):
            # TODO: 실제 뉴스 수집 / 데이터 처리 로직 수행
            # 수집된 데이터예시
            collected_data = "수집된 뉴스 데이터 결과..."
            
            # 업로드된 양식 템플릿에 수집된 데이터를 결합/생성하는 로직
            final_result_content = template_content  # 실제 구현 시 치환(replace) 로직 적용
            
            # 생성된 결과 데이터를 세션에 저장
            st.session_state['final_result'] = final_result_content
            st.session_state['file_name'] = uploaded_template.name
            st.success("🎉 데이터 수집 및 양식 적용이 완료되었습니다!")

# ---------------------------------------------------------
# 3. 최종 한글/HTML 파일 생성 및 다운로드 (TXT가 아닌 원본 확장자로 저장)
# ---------------------------------------------------------
st.subheader("3. 최종 결과 파일 저장 및 다운로드")

if 'final_result' in st.session_state:
    result_data = st.session_state['final_result']
    original_name = st.session_state.get('file_name', 'result.hwp')
    
    # 다운로드 파일명 및 MIME 타입 설정
    output_filename = f"완성본_{original_name}"
    
    if original_name.endswith('.html'):
        mime_type = "text/html"
    else:
        mime_type = "application/x-hwp"  # 한글 파일 전용 MIME 타입

    # 텍스트(.txt)가 아닌 원래 한글/HTML 파일 형태로 다운로드 제공
    st.download_button(
        label=f"📄 {output_filename} 다운로드 (원래 양식 유지)",
        data=result_data.encode('utf-8'),
        file_name=output_filename,
        mime=mime_type
    )
else:
    st.info("💡 위의 [Run] 버튼을 눌러 데이터를 수집하면 다운로드 버튼이 활성화됩니다.")
