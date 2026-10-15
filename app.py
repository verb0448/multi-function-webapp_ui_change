import streamlit as st

import ui

st.set_page_config(page_title="Multi-Function WebApp", page_icon="🧰", layout="wide", initial_sidebar_state="collapsed")
ui.inject_global_css()

pages = {"": [st.Page("pages/홈.py", title="홈", icon=":material/home:", default=True)]}
for feature in ui.FEATURES:
    pages.setdefault(feature["group"], []).append(
        st.Page(f"pages/{feature['key']}.py", title=feature["title"], icon=ui.nav_icon(feature["key"]))
    )

nav = st.navigation(pages, position="top")
nav.run()
