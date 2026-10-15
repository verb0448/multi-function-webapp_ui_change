from html import escape

import streamlit as st

GROUP_STYLES = {
    "업무 도구": {
        "cover": "linear-gradient(145deg, #3D2518 0%, #8C6048 100%)",
        "tagline": "문서·데이터 작업을 빠르게",
    },
    "금융·공시": {
        "cover": "linear-gradient(145deg, #102437 0%, #274E68 58%, #8E6E37 100%)",
        "tagline": "시장과 기업을 한눈에",
    },
    "개인 관심사": {
        "cover": "linear-gradient(145deg, #4A214E 0%, #8A3C6E 56%, #E36E68 100%)",
        "tagline": "생활 속 작은 도구",
    },
}

# 기능을 추가할 때는 이 목록에 한 줄을 넣고 pages/ 에 파일만 만들면 내비·홈 카드에 함께 반영된다.
FEATURES = [
    {"key": "프롬프트생성기", "title": "프롬프트생성기", "icon": "auto_awesome", "group": "업무 도구",
     "label": "AI · PROMPT", "desc": "요구사항을 최적화된 AI 프롬프트로 변환"},
    {"key": "가상데이터생성기", "title": "가상데이터생성기", "icon": "theater_comedy", "group": "업무 도구",
     "label": "DATA · MOCK", "desc": "Faker 기반 가상 데이터를 Excel로"},
    {"key": "데이터클렌징", "title": "데이터클렌징", "icon": "cleaning_services", "group": "업무 도구",
     "label": "DATA · CLEAN", "desc": "Excel 행·열 정리, 필터링, 병합"},
    {"key": "대량양식생성기", "title": "대량양식생성기", "icon": "description", "group": "업무 도구",
     "label": "DOC · BULK", "desc": "PDF 양식에 Excel 데이터를 대량 매핑"},
    {"key": "문서스캔변환기", "title": "문서스캔변환기", "icon": "document_scanner", "group": "업무 도구",
     "label": "DOC · SCAN", "desc": "비스듬한 서류 사진을 반듯하게 보정"},
    {"key": "공시정보검색", "title": "공시정보검색", "icon": "plagiarism", "group": "금융·공시",
     "label": "DART", "desc": "DART API로 회사 공시정보 검색"},
    {"key": "주가비교분석기", "title": "주가비교분석", "icon": "show_chart", "group": "금융·공시",
     "label": "STOCK", "desc": "최대 5개 종목의 주가 비교"},
    {"key": "주가지수및환율", "title": "주가지수 및 환율", "icon": "currency_exchange", "group": "금융·공시",
     "label": "ECOS", "desc": "코스피·코스닥·환율 일별 추이"},
    {"key": "음원툴박스", "title": "음원툴박스", "icon": "headphones", "group": "개인 관심사",
     "label": "AUDIO", "desc": "유튜브 MP3 추출, 텍스트 음성 변환",
     "note": "유튜브 정책에 따라 MP3 추출이 안 될 수 있음"},
    {"key": "아파트실거래가조회", "title": "아파트실거래가조회", "icon": "apartment", "group": "개인 관심사",
     "label": "REAL ESTATE", "desc": "지역·기간별 아파트 매매 실거래가"},
]

FEATURES_BY_KEY = {f["key"]: f for f in FEATURES}

MASCOT_SVG = (
    '<svg viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true">'
    '<rect x="6" y="14" width="36" height="28" rx="10" fill="#FFC928"/>'
    '<path d="M17 14v-3a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v3" fill="none" stroke="#5C3824" stroke-width="3.5" stroke-linecap="round"/>'
    '<circle cx="18" cy="27" r="3" fill="#5C3824"/><circle cx="30" cy="27" r="3" fill="#5C3824"/>'
    '<path d="M19 34h10c-1.5 3-3 4-5 4s-3.5-1-5-4Z" fill="{mouth}"/>'
    "</svg>"
)

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0');

:root {
  --mf-primary-50: #F7F1ED; --mf-primary-100: #EADCD3; --mf-primary-200: #D5BDAF;
  --mf-primary-500: #5C3824; --mf-primary-600: #4B2D1D; --mf-primary-700: #3D2518;
  --mf-yellow-100: #FFF0AD; --mf-yellow-300: #FFDC61; --mf-yellow-500: #FFC928;
  --mf-bg-subtle: #F7F5F2; --mf-border: #E7E2DD; --mf-border-strong: #C8C1BB;
  --mf-text-1: #241C18; --mf-text-2: #514A46; --mf-text-3: #756B65;
  --mf-warning-bg: #FFF4D6; --mf-warning-fg: #9A6200;
  --mf-radius-md: 14px; --mf-radius-lg: 20px; --mf-radius-xl: 28px;
  --mf-shadow-sm: 0 2px 8px rgba(36,28,24,0.06);
  --mf-shadow-md: 0 10px 28px rgba(36,28,24,0.10);
  --mf-shadow-brand: 0 14px 36px rgba(92,56,36,0.22);
  --mf-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.mf-ic { font-family: 'Material Symbols Rounded'; font-weight: normal; font-style: normal; line-height: 1;
  letter-spacing: normal; text-transform: none; white-space: nowrap; direction: ltr; display: inline-block;
  -webkit-font-feature-settings: 'liga'; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; }

[data-testid="stMainBlockContainer"] { max-width: 1200px; padding-top: 4.5rem; padding-bottom: 4rem; }
[data-testid="stHeader"] { background: #FFFFFF; border-bottom: 1px solid var(--mf-border); }

h1, h2, h3 { letter-spacing: -0.02em; }

.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, [data-testid="stPageLink"] a {
  font-weight: 700; transition: transform 150ms var(--mf-ease-out), background 150ms, box-shadow 150ms;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover { transform: translateY(-1px); }
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover,
.stDownloadButton > button[kind="primary"]:hover { box-shadow: var(--mf-shadow-brand); }
.stButton > button:active, .stDownloadButton > button:active { transform: translateY(0) scale(.98); }

[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within {
  box-shadow: 0 0 0 3px var(--mf-primary-100);
}

[data-testid="stExpander"] details { border-radius: var(--mf-radius-lg); border-color: var(--mf-border); }
[data-testid="stForm"] { border-radius: var(--mf-radius-lg); border-color: var(--mf-border); background: #FFFFFF; }
[data-testid="stFileUploaderDropzone"] { border-radius: var(--mf-radius-md); background: var(--mf-bg-subtle); }
[data-testid="stMetric"] { background: #FFFFFF; border: 1px solid var(--mf-border); border-radius: 16px; padding: 14px 16px; }
[data-testid="stAlert"] { border-radius: var(--mf-radius-md); }

/* 페이지 헤더 */
.mf-crumb { display: flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 600; color: var(--mf-text-3); margin-bottom: 10px; }
.mf-crumb a { color: var(--mf-text-3) !important; text-decoration: none !important; }
.mf-crumb a:hover { color: var(--mf-primary-500) !important; }
.mf-crumb .mf-ic { font-size: 14px; }
.mf-ph { display: flex; align-items: center; gap: 14px; margin-bottom: 1.2rem; }
.mf-ph-tile { width: 52px; height: 52px; flex: none; border-radius: 16px; display: grid; place-items: center; color: #FFFFFF; box-shadow: var(--mf-shadow-sm); }
.mf-ph-tile .mf-ic { font-size: 26px; }
.mf-ph-title { font-size: 1.9rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.15; color: var(--mf-text-1); }
.mf-ph-desc { font-size: 0.9rem; color: var(--mf-text-3); margin-top: 3px; line-height: 1.5; }
.mf-badge { display: inline-flex; align-items: center; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700;
  border: 1px solid var(--mf-primary-200); color: var(--mf-primary-500); white-space: nowrap; margin-left: auto; }

/* 홈 */
.mf-logo-bar { margin-bottom: 1rem; }
.mf-logo { background: #0D1E6C; border-radius: 10px; padding: 6px 12px; display: inline-flex; line-height: 0; }
.mf-logo img { height: 36px; width: auto; max-width: 240px; object-fit: contain; }
.mf-hero { position: relative; overflow: hidden; border-radius: var(--mf-radius-xl); background: linear-gradient(135deg, #5C3824 0%, #36251D 72%, #25201D 100%);
  color: #FFFFFF; padding: 44px 48px; display: grid; grid-template-columns: 1.2fr .8fr; gap: 24px; align-items: center; box-shadow: var(--mf-shadow-brand); }
.mf-hero::before { content: ''; position: absolute; width: 330px; height: 330px; right: -84px; top: -120px; border: 62px solid var(--mf-yellow-500); border-radius: 50%; }
.mf-hero::after { content: ''; position: absolute; width: 190px; height: 190px; left: 38%; bottom: -152px; border: 35px solid rgba(255,255,255,.07); border-radius: 50%; }
.mf-hero-copy { position: relative; z-index: 1; }
.mf-eyebrow { display: inline-flex; align-items: center; gap: 8px; color: var(--mf-yellow-300); font-size: 11px; font-weight: 800; letter-spacing: .12em; }
.mf-eyebrow::before { content: ''; width: 18px; height: 2px; border-radius: 2px; background: currentColor; }
.mf-hero-title { font-size: clamp(30px, 4.4vw, 50px); font-weight: 800; line-height: 1.06; letter-spacing: -0.055em; margin-top: 12px; color: #FFFFFF; }
.mf-hero-lead { margin: 16px 0 0; color: rgba(255,255,255,.76); font-size: 15px; line-height: 1.6; max-width: 460px; }
.mf-hero-stage { position: relative; z-index: 1; min-height: 200px; display: grid; place-items: center; }
.mf-halo { width: 184px; height: 184px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.09);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.12), 0 22px 40px rgba(0,0,0,.18); }
.mf-orbit { position: absolute; display: inline-flex; align-items: center; gap: 6px; padding: 7px 10px; border-radius: 9999px;
  border: 1px solid rgba(255,255,255,.16); background: rgba(255,255,255,.10); color: #FFFFFF; font-size: 10px; font-weight: 800; letter-spacing: .08em; }
.mf-orbit::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--mf-yellow-500); }
.mf-orbit.o1 { left: 6%; top: 18px; } .mf-orbit.o2 { right: 2%; top: 84px; } .mf-orbit.o3 { left: 14%; bottom: 8px; }
.mf-notice { display: flex; gap: 10px; align-items: center; background: var(--mf-warning-bg); border: 1px solid #F3DFA6; border-radius: var(--mf-radius-md);
  padding: 12px 16px; color: var(--mf-warning-fg); font-size: 0.88rem; line-height: 1.5; margin: 1.1rem 0 0.6rem; }
.mf-notice .mf-ic { font-size: 20px; }
.mf-section { display: flex; align-items: flex-end; gap: 12px; margin: 2.2rem 2px 0.9rem; }
.mf-section-title { font-size: 1.4rem; font-weight: 800; letter-spacing: -0.035em; color: var(--mf-text-1); }
.mf-section-sub { font-size: 0.85rem; color: var(--mf-text-3); }
.mf-count { margin-left: auto; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; background: var(--mf-yellow-100); color: var(--mf-primary-700); }
.mf-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 16px; }
.mf-card { display: flex; flex-direction: column; overflow: hidden; border: 1px solid var(--mf-border); border-radius: var(--mf-radius-lg); background: #FFFFFF;
  box-shadow: var(--mf-shadow-sm); text-decoration: none !important; color: inherit !important;
  transition: transform 150ms var(--mf-ease-out), box-shadow 150ms var(--mf-ease-out); }
.mf-card:hover { transform: translateY(-3px); box-shadow: var(--mf-shadow-md); }
.mf-cover { position: relative; overflow: hidden; height: 108px; padding: 16px 18px; display: flex; flex-direction: column; justify-content: flex-end; color: #FFFFFF; }
.mf-cover::before { content: ''; position: absolute; width: 110px; height: 110px; top: -35px; right: -20px; border: 20px solid rgba(255,255,255,.14); border-radius: 50%; }
.mf-cover::after { content: ''; position: absolute; width: 65px; height: 65px; left: -15px; bottom: -24px; border-radius: 20px; background: rgba(255,255,255,.10); transform: rotate(28deg); }
.mf-cover small { position: relative; z-index: 1; font-size: 10px; font-weight: 800; letter-spacing: .1em; opacity: .75; }
.mf-cover .mf-ic { position: relative; z-index: 1; font-size: 28px; margin-top: 4px; }
.mf-meta { padding: 14px 16px 16px; display: flex; align-items: center; gap: 10px; flex: 1; }
.mf-meta-body { min-width: 0; }
.mf-meta h3 { margin: 0 !important; padding: 0 !important; font-size: 15px !important; font-weight: 700 !important; color: var(--mf-text-1) !important; letter-spacing: -0.02em; }
.mf-meta p { margin: 3px 0 0 !important; font-size: 12px; color: var(--mf-text-3); line-height: 1.45; }
.mf-meta .mf-note { color: var(--mf-warning-fg); font-size: 11px; }
.mf-arrow { margin-left: auto; width: 30px; height: 30px; flex: none; border-radius: 50%; border: 1px solid var(--mf-border); display: grid; place-items: center; color: var(--mf-primary-500); }
.mf-arrow .mf-ic { font-size: 18px; }

@media (max-width: 760px) {
  .mf-hero { grid-template-columns: 1fr; padding: 32px 26px; }
  .mf-hero::before { width: 150px; height: 150px; border-width: 28px; right: -64px; top: -70px; }
  .mf-hero-stage { display: none; }
  .mf-ph-title { font-size: 1.5rem; }
  .mf-badge { display: none; }
}
</style>
"""


def inject_global_css():
    st.html(GLOBAL_CSS)


def _icon(name):
    return f'<span class="mf-ic" aria-hidden="true">{name}</span>'


def _href(key):
    return "/" + key


def nav_icon(key):
    return f":material/{FEATURES_BY_KEY[key]['icon']}:"


def page_header(key, desc="", badge=None):
    feature = FEATURES_BY_KEY[key]
    cover = GROUP_STYLES[feature["group"]]["cover"]
    badge_html = f'<span class="mf-badge">{escape(badge)}</span>' if badge else ""
    desc_html = f'<div class="mf-ph-desc">{escape(desc)}</div>' if desc else ""
    html = (
        '<div class="mf-crumb">'
        f'<a href="/" target="_self">홈</a>{_icon("chevron_right")}'
        f'<span>{escape(feature["group"])}</span>{_icon("chevron_right")}'
        f'<span>{escape(feature["title"])}</span>'
        "</div>"
        '<div class="mf-ph">'
        f'<div class="mf-ph-tile" style="background:{cover}">{_icon(feature["icon"])}</div>'
        f'<div><div class="mf-ph-title" role="heading" aria-level="1">{escape(feature["title"])}</div>{desc_html}</div>'
        f"{badge_html}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def logo_bar(src):
    st.markdown(
        f'<div class="mf-logo-bar"><div class="mf-logo"><img src="{src}" alt="회사 로고"></div></div>',
        unsafe_allow_html=True,
    )


def hero():
    html = (
        '<div class="mf-hero">'
        '<div class="mf-hero-copy">'
        '<span class="mf-eyebrow">ONE APP, MANY TOOLS</span>'
        '<div class="mf-hero-title" role="heading" aria-level="1">흩어진 업무 도구를<br>한 곳에서 가볍게</div>'
        '<p class="mf-hero-lead">데이터 정리부터 공시·주가 조회, 문서 변환까지. '
        "필요한 기능을 골라 바로 쓰는 모듈형 Multi-Function 웹앱입니다.</p>"
        "</div>"
        '<div class="mf-hero-stage">'
        f'<div class="mf-halo">{MASCOT_SVG.format(size=132, mouth="#FFFFFF")}</div>'
        '<span class="mf-orbit o1">WORK</span><span class="mf-orbit o2">DATA</span><span class="mf-orbit o3">LIFE</span>'
        "</div>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def security_notice(text):
    st.markdown(f'<div class="mf-notice">{_icon("lock")}<span>{escape(text)}</span></div>', unsafe_allow_html=True)


def feature_section(group):
    style = GROUP_STYLES[group]
    features = [f for f in FEATURES if f["group"] == group]
    cards = []
    for f in features:
        note = f'<p class="mf-note">※ {escape(f["note"])}</p>' if f.get("note") else ""
        # target="_self"를 명시하지 않으면 Streamlit이 target="_blank"를 붙여 새 탭으로 연다.
        cards.append(
            f'<a class="mf-card" href="{_href(f["key"])}" target="_self">'
            f'<div class="mf-cover" style="background:{style["cover"]}"><small>{escape(f["label"])}</small>{_icon(f["icon"])}</div>'
            '<div class="mf-meta"><div class="mf-meta-body">'
            f'<h3>{escape(f["title"])}</h3><p>{escape(f["desc"])}</p>{note}'
            f'</div><span class="mf-arrow">{_icon("arrow_forward")}</span></div>'
            "</a>"
        )
    html = (
        '<div class="mf-section">'
        f'<div><div class="mf-section-title">{escape(group)}</div><div class="mf-section-sub">{escape(style["tagline"])}</div></div>'
        f'<span class="mf-count">{len(features)}개 기능</span>'
        "</div>"
        f'<div class="mf-grid">{"".join(cards)}</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
