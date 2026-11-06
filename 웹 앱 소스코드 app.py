import streamlit as st
import json
from datetime import date

# 페이지 기본 설정
st.set_page_config(page_title="조간 브리핑 통합 작성기", layout="wide")

st.title("📰 조간 브리핑 통합 작성기")

# 1. 기본 정보 설정
st.subheader("기본 정보 설정")
col1, col2 = st.columns(2)
with col1:
    briefing_date = st.date_input("작성 일자", value=date.today())
with col2:
    briefing_author = st.text_input("작성자 / 부서", placeholder="예: 대변인실 홍길동")

st.divider()

# 2. 주요 도정 키워드 & 워드클라우드
st.subheader("1. 주요 도정 키워드 & 워드클라우드")
col_kw, col_img = st.columns(2)
with col_kw:
    keywords_input = st.text_area("주요 키워드 (쉼표로 구분)", placeholder="민생경제, 신산업, 지역균형")
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
with col_img:
    uploaded_image = st.file_uploader("워드클라우드 이미지 첨부", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="업로드된 워드클라우드", use_column_width=True)

st.divider()

# 3. 주요 방송보도 목록
st.subheader("2. 주요 방송보도 목록")
broadcast_text = st.text_area(
    "방송보도 입력 (형식: 방송사 | 제목 | URL)",
    placeholder="KBS | 주요 정책 발표 현장 | https://example.com",
    height=100
)

st.divider()

# 4. 주요 일간지 1면 헤드라인
st.subheader("3. 주요 일간지 1면 헤드라인")
headline_text = st.text_area(
    "1면 헤드라인 입력 (형식: 신문사 | 헤드라인 제목)",
    placeholder="조선일보 | 지역 경제 활성화 대책 발표\n중앙일보 | 첨단 산업 단지 조성",
    height=100
)

st.divider()

# 5. 주요 언론 동향
st.subheader("4. 주요 언론 동향")
trend_text = st.text_area("동향 내용 입력", placeholder="[정부] 기획재정부 예산 편성 지침 발표...", height=100)

st.divider()

# 6. 인사 및 부고 소식
st.subheader("5. 인사 및 부고 소식")
notice_text = st.text_area("소식 입력", placeholder="[인사] OO과 OO팀장 발령\n[부고] OO국장 모친상", height=80)

st.divider()

# 실행(Run) / 미리보기 & 데이터 저장 버튼
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🔍 보고서 미리보기 (Run)", type="primary"):
        st.subheader("📋 [ 미리보기 ] 조간 브리핑")
        st.write(f"**작성일자:** {briefing_date} | **작성자:** {briefing_author}")
        st.markdown(f"**1. 주요 키워드:** {', '.join(keywords)}")
        if uploaded_image:
            st.image(uploaded_image, width=400)
        st.markdown("**2. 주요 방송보도:**")
        st.text(broadcast_text)
        st.markdown("**3. 1면 헤드라인:**")
        st.text(headline_text)
        st.markdown("**4. 언론 동향:**")
        st.text(trend_text)
        st.markdown("**5. 인사 및 부고:**")
        st.text(notice_text)

with col_btn2:
    data_to_save = {
        "date": str(briefing_date),
        "author": briefing_author,
        "keywords": keywords,
        "broadcasts": broadcast_text,
        "headlines": headline_text,
        "trends": trend_text,
        "notices": notice_text
    }
    json_string = json.dumps(data_to_save, ensure_ascii=False, indent=2)
    st.download_button(
        label="💾 데이터 저장 (.json)",
        data=json_string,
        file_name=f"조간브리핑_{briefing_date}.json",
        mime="application/json"
    )
import streamlit as st

# 한글 파일 다운로드 버튼 예시
with open("result_briefing.hwp", "rb") as file:
    st.download_button(
        label="📄 완성된 한글파일(.hwp) 다운로드",
        data=file,
        file_name="조간브리핑_최종.hwp",
        mime="application/x-hwp"
    )
