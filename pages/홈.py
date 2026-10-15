from pathlib import Path

import streamlit as st

import ui

LOCAL_GUIDE_PATH = Path(__file__).parent.parent / "assets" / "로컬실행_사용방법.txt"

ui.logo_bar("https://i.postimg.cc/vBjqSL4T/logo.png")
ui.hero()
ui.security_notice("외부 서버에 내부 정보가 올라갈 수 있는 기능을 쓸 때 보안이 우려된다면 로컬 서버에서 실행하세요.")

if LOCAL_GUIDE_PATH.exists():
    st.download_button(
        label="로컬 실행 사용방법 다운로드",
        icon=":material/download:",
        data=LOCAL_GUIDE_PATH.read_bytes(),
        file_name="로컬실행_사용방법.txt",
        mime="text/plain",
    )

for group in ui.GROUP_STYLES:
    ui.feature_section(group)
