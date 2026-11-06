# ==================================================
# 7. 홈 화면
# ==================================================
if st.session_state.page == "home":
    with st.container(key="landing"):
        st.markdown(
            (
                '<div class="brief-nav">'
                f'{logo_html}'
                '</div>'
                '<div class="brief-hero">'
                '<div class="brief-ring"></div>'
                '<h1>'
                '<span>오늘의 뉴스,</span><br>'
                '한눈에 정리하세요.'
                '</h1>'
                '<p>'
                '워드클라우드부터 주요 기사와 정부 동향까지.<br>'
                '필요한 내용을 입력하고 조간 브리핑을 '
                '완성해 보세요.'
                '</p>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        st.button(
            "브리핑 작성 시작",
            key="start_briefing",
            on_click=go_editor,
            use_container_width=True,
        )
