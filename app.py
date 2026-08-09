import html as html_lib
import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ExamWise AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

CSS = """
<style>

/* ============================================================
   GLOBAL
============================================================ */

:root {
    --bg: #050816;
    --panel: #0d1428;
    --panel-soft: rgba(15, 23, 42, 0.72);
    --border: rgba(148, 163, 184, 0.13);
    --text: #f8fafc;
    --muted: #94a3b8;
    --muted-dark: #64748b;
    --indigo: #6366f1;
    --purple: #8b5cf6;
    --blue: #38bdf8;
    --green: #22c55e;
}

html {
    scroll-behavior: smooth;
}

.stApp {
    background:
        radial-gradient(
            circle at 12% 10%,
            rgba(99, 102, 241, 0.17),
            transparent 24%
        ),
        radial-gradient(
            circle at 88% 14%,
            rgba(168, 85, 247, 0.13),
            transparent 23%
        ),
        radial-gradient(
            circle at 68% 88%,
            rgba(14, 165, 233, 0.08),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #030712 0%,
            #070b1c 50%,
            #050816 100%
        );

    background-size: 180% 180%;

    animation: backgroundMove 18s ease infinite;
}

@keyframes backgroundMove {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
============================================================ */

[data-testid="stSidebar"] {
    min-width: 305px;
    max-width: 305px;

    background:
        radial-gradient(
            circle at 20% 0%,
            rgba(99, 102, 241, 0.11),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #070b1c 0%,
            #040714 100%
        );

    border-right:
        1px solid rgba(148, 163, 184, 0.10);
}

[data-testid="stSidebarContent"] {
    padding-top: 1rem;
}


/* ---------- BRAND ---------- */

.brand-wrap {
    padding: 18px 10px 27px 10px;
}

.brand-name {
    color: white;

    font-size: 29px;

    font-weight: 900;

    letter-spacing: -1px;
}

.brand-gradient {
    background:
        linear-gradient(
            90deg,
            #a5b4fc,
            #c084fc,
            #38bdf8,
            #a5b4fc
        );

    background-size: 250% 250%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation: brandGradient 5s ease infinite;
}

@keyframes brandGradient {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.brand-subtitle {
    color: #64748b;

    font-size: 11.5px;

    margin-top: 6px;

    letter-spacing: 0.2px;
}


/* ---------- NAVIGATION TITLE ---------- */

.sidebar-label {
    color: #64748b;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 1.8px;

    margin: 14px 11px 11px 11px;
}


/* ============================================================
   SIDEBAR NAVIGATION
============================================================ */

[data-testid="stSidebar"]
div[role="radiogroup"] {

    gap: 7px !important;
}


/* Every menu item */

[data-testid="stSidebar"]
div[role="radiogroup"]
> label {

    min-height: 51px;

    padding:
        0 15px !important;

    border-radius: 13px;

    background:
        rgba(15, 23, 42, 0.20);

    border:
        1px solid transparent;

    cursor: pointer;

    transition:
        transform 0.23s ease,
        background 0.23s ease,
        border-color 0.23s ease,
        box-shadow 0.23s ease;
}


/* Menu text */

[data-testid="stSidebar"]
div[role="radiogroup"]
label p {

    color: #cbd5e1 !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    letter-spacing: 0.05px;

    transition:
        color 0.23s ease;
}


/* Hide Streamlit radio circle */

[data-testid="stSidebar"]
div[role="radiogroup"]
input[type="radio"] {

    display: none !important;
}


/* Hide radio visual */

[data-testid="stSidebar"]
div[role="radiogroup"]
label > div:first-child:not([data-testid="stMarkdownContainer"]) {

    display: none !important;
}


/* Hover */

[data-testid="stSidebar"]
div[role="radiogroup"]
> label:hover {

    transform:
        translateX(4px);

    background:
        linear-gradient(
            90deg,
            rgba(99, 102, 241, 0.13),
            rgba(139, 92, 246, 0.06)
        );

    border-color:
        rgba(129, 140, 248, 0.18);
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:hover p {

    color: #ffffff !important;
}


/* Selected menu */

[data-testid="stSidebar"]
div[role="radiogroup"]
> label:has(input:checked) {

    transform:
        translateX(2px);

    background:
        linear-gradient(
            90deg,
            rgba(99, 102, 241, 0.25),
            rgba(139, 92, 246, 0.13)
        );

    border:
        1px solid rgba(129, 140, 248, 0.30);

    box-shadow:
        inset 3px 0 0 #818cf8,
        0 9px 27px rgba(99, 102, 241, 0.10);
}


[data-testid="stSidebar"]
div[role="radiogroup"]
> label:has(input:checked) p {

    color: #ffffff !important;

    font-weight: 700 !important;
}


/* ---------- AI STATUS ---------- */

.sidebar-status {
    position: relative;

    overflow: hidden;

    margin:
        28px 8px
        10px 8px;

    padding:
        14px 15px;

    border-radius: 13px;

    color: #86efac;

    font-size: 11.5px;

    font-weight: 650;

    background:
        linear-gradient(
            90deg,
            rgba(34, 197, 94, 0.08),
            rgba(16, 185, 129, 0.04)
        );

    border:
        1px solid rgba(34, 197, 94, 0.18);

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.12);
}

.sidebar-status::after {
    content: "";

    position: absolute;

    width: 70px;

    height: 70px;

    right: -35px;

    top: -35px;

    border-radius: 50%;

    background:
        rgba(34, 197, 94, 0.12);

    filter: blur(20px);
}

.status-dot {
    width: 8px;

    height: 8px;

    display: inline-block;

    border-radius: 50%;

    background: #22c55e;

    margin-right: 7px;

    box-shadow:
        0 0 11px rgba(34, 197, 94, 0.95);

    animation:
        statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {

    0%,
    100% {

        opacity: 0.45;

        transform:
            scale(0.9);
    }

    50% {

        opacity: 1;

        transform:
            scale(1.15);
    }
}

.sidebar-footer {
    color: #475569;

    font-size: 10.5px;

    line-height: 1.65;

    padding:
        12px 11px;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    position: relative;

    overflow: hidden;

    padding:
        46px 46px 48px 46px;

    border-radius: 28px;

    background:
        linear-gradient(
            145deg,
            rgba(17, 24, 39, 0.82),
            rgba(15, 23, 42, 0.52)
        );

    border:
        1px solid rgba(148, 163, 184, 0.12);

    box-shadow:
        0 30px 80px rgba(0, 0, 0, 0.25);

    backdrop-filter:
        blur(16px);
}

.hero::before {
    content: "";

    position: absolute;

    width: 360px;

    height: 360px;

    border-radius: 50%;

    right: -130px;

    top: -170px;

    background:
        radial-gradient(
            circle,
            rgba(139, 92, 246, 0.28),
            transparent 70%
        );

    filter: blur(10px);

    animation:
        orbFloat 7s ease-in-out infinite;
}

.hero::after {
    content: "";

    position: absolute;

    width: 270px;

    height: 270px;

    border-radius: 50%;

    left: 35%;

    bottom: -210px;

    background:
        radial-gradient(
            circle,
            rgba(56, 189, 248, 0.16),
            transparent 70%
        );
}

@keyframes orbFloat {

    0%,
    100% {

        transform:
            translateY(0px);
    }

    50% {

        transform:
            translateY(22px);
    }
}

.hero-badge {
    position: relative;

    z-index: 2;

    display: inline-flex;

    align-items: center;

    padding:
        8px 14px;

    border-radius:
        999px;

    color: #c7d2fe;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 0.5px;

    background:
        rgba(99, 102, 241, 0.09);

    border:
        1px solid rgba(129, 140, 248, 0.28);

    animation:
        badgeGlow 3s ease-in-out infinite;
}

@keyframes badgeGlow {

    0%,
    100% {

        box-shadow:
            0 0 10px rgba(99, 102, 241, 0.08);
    }

    50% {

        box-shadow:
            0 0 28px rgba(99, 102, 241, 0.23);
    }
}

.hero-title {
    position: relative;

    z-index: 2;

    max-width: 930px;

    margin-top: 23px;

    color: #f8fafc;

    font-size:
        clamp(48px, 6vw, 76px);

    line-height: 1.02;

    font-weight: 900;

    letter-spacing: -3.5px;
}

.hero-gradient {
    background:
        linear-gradient(
            90deg,
            #818cf8,
            #c084fc,
            #38bdf8,
            #818cf8
        );

    background-size:
        300% 300%;

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;

    animation:
        textGradient 6s ease infinite;
}

@keyframes textGradient {

    0% {
        background-position:
            0% 50%;
    }

    50% {
        background-position:
            100% 50%;
    }

    100% {
        background-position:
            0% 50%;
    }
}

.hero-description {
    position: relative;

    z-index: 2;

    max-width: 830px;

    margin-top: 22px;

    color: #94a3b8;

    font-size: 17px;

    line-height: 1.75;
}

.hero-support {
    position: relative;

    z-index: 2;

    margin-top: 27px;

    display: flex;

    flex-wrap: wrap;

    gap: 9px;
}

.support-pill {
    display: inline-block;

    padding:
        7px 11px;

    border-radius:
        9px;

    color: #a8b4c6;

    font-size: 11px;

    background:
        rgba(15, 23, 42, 0.72);

    border:
        1px solid rgba(148, 163, 184, 0.12);
}


/* ============================================================
   SECTION HEADINGS
============================================================ */

.section-header {
    margin-top: 38px;

    margin-bottom: 19px;
}

.section-kicker {
    color: #818cf8;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.4px;
}

.section-title {
    color: #f8fafc;

    font-size: 27px;

    font-weight: 800;

    letter-spacing: -0.7px;

    margin-top: 4px;
}

.section-description {
    color: #64748b;

    font-size: 13px;

    margin-top: 5px;
}


/* ============================================================
   CAPABILITY CARDS
============================================================ */

.capability-card {
    min-height: 125px;

    padding: 19px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.78),
            rgba(15, 23, 42, 0.48)
        );

    border:
        1px solid rgba(148, 163, 184, 0.11);

    transition:
        transform 0.28s ease,
        border-color 0.28s ease,
        box-shadow 0.28s ease;
}

.capability-card:hover {
    transform:
        translateY(-5px);

    border-color:
        rgba(129, 140, 248, 0.42);

    box-shadow:
        0 16px 38px rgba(0, 0, 0, 0.20);
}

.capability-value {
    font-size: 23px;

    font-weight: 850;

    background:
        linear-gradient(
            90deg,
            #a5b4fc,
            #38bdf8
        );

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;
}

.capability-title {
    color: #e2e8f0;

    font-size: 13px;

    font-weight: 700;

    margin-top: 7px;
}

.capability-sub {
    color: #64748b;

    font-size: 10.5px;

    margin-top: 3px;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.feature-card {
    position: relative;

    min-height: 210px;

    overflow: hidden;

    padding: 24px;

    border-radius: 21px;

    background:
        linear-gradient(
            145deg,
            rgba(18, 27, 52, 0.80),
            rgba(10, 15, 35, 0.70)
        );

    border:
        1px solid rgba(148, 163, 184, 0.11);

    box-shadow:
        0 18px 50px rgba(0, 0, 0, 0.13);

    transition:
        transform 0.32s ease,
        border-color 0.32s ease,
        box-shadow 0.32s ease;
}

.feature-card::after {
    content: "";

    position: absolute;

    width: 130px;

    height: 130px;

    border-radius: 50%;

    right: -70px;

    top: -70px;

    background:
        rgba(99, 102, 241, 0.13);

    filter:
        blur(32px);

    transition:
        0.4s ease;
}

.feature-card:hover {
    transform:
        translateY(-8px);

    border-color:
        rgba(129, 140, 248, 0.48);

    box-shadow:
        0 22px 55px rgba(0, 0, 0, 0.25),
        0 0 25px rgba(99, 102, 241, 0.07);
}

.feature-card:hover::after {
    transform:
        scale(1.4);
}

.feature-icon {
    position: relative;

    z-index: 2;

    width: 50px;

    height: 50px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 14px;

    font-size: 23px;

    background:
        linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.18),
            rgba(168, 85, 247, 0.12)
        );

    border:
        1px solid rgba(129, 140, 248, 0.19);
}

.feature-name {
    position: relative;

    z-index: 2;

    color: #f8fafc;

    font-size: 16px;

    font-weight: 750;

    margin-top: 17px;
}

.feature-desc {
    position: relative;

    z-index: 2;

    color: #94a3b8;

    font-size: 12.5px;

    line-height: 1.65;

    margin-top: 8px;
}


/* ============================================================
   PAGE HEADERS
============================================================ */

.page-badge {
    display: inline-block;

    padding:
        7px 12px;

    border-radius:
        999px;

    color: #c7d2fe;

    background:
        rgba(99, 102, 241, 0.08);

    border:
        1px solid rgba(129, 140, 248, 0.20);

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 0.7px;
}

.page-title {
    color: #f8fafc;

    font-size: 42px;

    font-weight: 850;

    letter-spacing: -1.5px;

    margin-top: 14px;
}

.page-desc {
    color: #94a3b8;

    max-width: 780px;

    font-size: 14px;

    line-height: 1.7;

    margin-top: 7px;

    margin-bottom: 28px;
}


/* ============================================================
   UPLOAD
============================================================ */

.upload-hero {
    position: relative;

    overflow: hidden;

    padding: 31px;

    border-radius: 23px;

    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 75, 0.48),
            rgba(10, 15, 35, 0.64)
        );

    border:
        1px solid rgba(129, 140, 248, 0.19);

    box-shadow:
        0 24px 60px rgba(0, 0, 0, 0.17);
}

.upload-hero::after {
    content: "";

    position: absolute;

    width: 200px;

    height: 200px;

    right: -90px;

    top: -100px;

    border-radius: 50%;

    background:
        rgba(139, 92, 246, 0.16);

    filter:
        blur(40px);
}

.upload-symbol {
    font-size: 38px;
}

.upload-heading {
    color: #f8fafc;

    font-size: 21px;

    font-weight: 780;

    margin-top: 8px;
}

.upload-text {
    color: #94a3b8;

    font-size: 12.5px;

    margin-top: 5px;
}

[data-testid="stFileUploader"] {
    margin-top: 14px;

    padding: 10px;

    border-radius: 18px;

    background:
        rgba(8, 13, 31, 0.58);

    border:
        1px dashed rgba(129, 140, 248, 0.40);

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color:
        #818cf8;

    box-shadow:
        0 0 30px rgba(99, 102, 241, 0.09);
}


/* ============================================================
   FILE CARDS
============================================================ */

.file-card {
    padding:
        15px 17px;

    margin-bottom:
        8px;

    border-radius:
        14px;

    background:
        rgba(15, 23, 42, 0.58);

    border:
        1px solid rgba(148, 163, 184, 0.10);

    transition:
        transform 0.22s ease,
        border-color 0.22s ease;
}

.file-card:hover {
    transform:
        translateX(3px);

    border-color:
        rgba(129, 140, 248, 0.24);
}

.file-name {
    color: #e2e8f0;

    font-size: 13px;

    font-weight: 650;
}

.file-meta {
    color: #64748b;

    font-size: 10.5px;

    margin-top: 3px;
}


/* ============================================================
   BUTTON
============================================================ */

.stButton > button {
    min-height: 49px;

    border: none;

    border-radius: 12px;

    font-weight: 750;

    color: white;

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

    transition:
        transform 0.22s ease,
        box-shadow 0.22s ease;

    box-shadow:
        0 8px 26px rgba(99, 102, 241, 0.20);
}

.stButton > button:hover {
    transform:
        translateY(-2px);

    box-shadow:
        0 13px 34px rgba(99, 102, 241, 0.33);
}


/* ============================================================
   RESULTS
============================================================ */

.result-card {
    padding:
        18px;

    border-radius:
        16px;

    background:
        rgba(15, 23, 42, 0.58);

    border:
        1px solid rgba(148, 163, 184, 0.10);

    margin-top:
        10px;
}

.result-success {
    color: #86efac;

    font-size: 13px;

    font-weight: 700;
}

.result-warning {
    color: #fcd34d;

    font-size: 13px;

    font-weight: 700;
}


/* ============================================================
   EMPTY STATE
============================================================ */

.empty-state {
    margin-top:
        20px;

    padding:
        42px 25px;

    text-align:
        center;

    border-radius:
        20px;

    background:
        rgba(15, 23, 42, 0.45);

    border:
        1px solid rgba(148, 163, 184, 0.10);
}

.empty-icon {
    font-size:
        38px;
}

.empty-title {
    color:
        #e2e8f0;

    font-weight:
        750;

    margin-top:
        10px;
}

.empty-text {
    color:
        #64748b;

    font-size:
        12px;

    margin-top:
        5px;
}


/* ============================================================
   STREAMLIT METRICS
============================================================ */

[data-testid="stMetric"] {
    background:
        rgba(15, 23, 42, 0.55);

    border:
        1px solid rgba(148, 163, 184, 0.10);

    padding:
        18px;

    border-radius:
        16px;
}


/* ============================================================
   TEXT INPUT / TEXT AREA
============================================================ */

textarea {
    border-radius:
        12px !important;
}

[data-testid="stTextInput"] input {
    border-radius:
        12px;
}


/* ============================================================
   RESPONSIVE
============================================================ */

@media (max-width: 900px) {

    .hero {
        padding:
            30px 25px;
    }

    .hero-title {
        font-size:
            48px;

        letter-spacing:
            -2px;
    }

    .feature-card {
        min-height:
            190px;
    }
}


/* ============================================================
   HIDE DEFAULT STREAMLIT UI
============================================================ */

#MainMenu {
    visibility:
        hidden;
}

footer {
    visibility:
        hidden;
}

header {
    background:
        transparent !important;
}

</style>
"""

st.markdown(
    CSS,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_html(content):
    """
    Render compact HTML safely.

    We avoid indented multiline HTML because Streamlit Markdown
    can sometimes display it as a code block.
    """
    st.markdown(
        content,
        unsafe_allow_html=True
    )


def feature_card(
    icon,
    title,
    description
):

    icon = html_lib.escape(icon)

    title = html_lib.escape(title)

    description = html_lib.escape(
        description
    )

    content = (
        '<div class="feature-card">'
        f'<div class="feature-icon">{icon}</div>'
        f'<div class="feature-name">{title}</div>'
        f'<div class="feature-desc">{description}</div>'
        '</div>'
    )

    render_html(content)


def capability_card(
    value,
    title,
    subtitle
):

    value = html_lib.escape(value)

    title = html_lib.escape(title)

    subtitle = html_lib.escape(
        subtitle
    )

    content = (
        '<div class="capability-card">'
        f'<div class="capability-value">{value}</div>'
        f'<div class="capability-title">{title}</div>'
        f'<div class="capability-sub">{subtitle}</div>'
        '</div>'
    )

    render_html(content)


def page_header(
    badge,
    title,
    description
):

    badge = html_lib.escape(badge)

    title = html_lib.escape(title)

    description = html_lib.escape(
        description
    )

    content = (
        f'<div class="page-badge">{badge}</div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-desc">{description}</div>'
    )

    render_html(content)


def empty_state(
    icon,
    title,
    description
):

    icon = html_lib.escape(icon)

    title = html_lib.escape(title)

    description = html_lib.escape(
        description
    )

    content = (
        '<div class="empty-state">'
        f'<div class="empty-icon">{icon}</div>'
        f'<div class="empty-title">{title}</div>'
        f'<div class="empty-text">{description}</div>'
        '</div>'
    )

    render_html(content)


# ============================================================
# SESSION STATE
# ============================================================

if "processed_files" not in st.session_state:

    st.session_state.processed_files = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        '<div class="brand-wrap">'
        '<div class="brand-name">'
        '🎓 <span class="brand-gradient">ExamWise</span>'
        '</div>'
        '<div class="brand-subtitle">'
        'AI Question Paper Intelligence'
        '</div>'
        '</div>'
    )

    render_html(
        '<div class="sidebar-label">'
        'NAVIGATION'
        '</div>'
    )

    page = st.radio(
        "Navigation",
        [
            "🏠  Home",
            "📤  Upload Papers",
            "📊  Analysis",
            "🔁  Repeated Questions",
            "🎯  Study Priority",
            "🤖  Ask ExamWise",
        ],
        label_visibility="collapsed",
    )

    render_html(
        '<div class="sidebar-status">'
        '<span class="status-dot"></span>'
        'ExamWise Engine Ready'
        '</div>'
    )

    render_html(
        '<div class="sidebar-footer">'
        'Turn previous question papers into '
        'structured exam intelligence.'
        '</div>'
    )


# ============================================================
# HOME PAGE
# ============================================================

if page == "🏠  Home":

    render_html(
        '<div class="hero">'
        '<div class="hero-badge">'
        '<span class="status-dot"></span>'
        'AI-POWERED QUESTION PAPER INTELLIGENCE'
        '</div>'
        '<div class="hero-title">'
        'Stop guessing.<br>'
        '<span class="hero-gradient">'
        'Prepare with evidence.'
        '</span>'
        '</div>'
        '<div class="hero-description">'
        'ExamWise analyzes previous-year question papers '
        'to uncover repeated concepts, question similarities, '
        'marks patterns and high-priority areas so students '
        'can prepare more strategically.'
        '</div>'
        '<div class="hero-support">'
        '<span class="support-pill">📄 Text PDF</span>'
        '<span class="support-pill">📷 Scanned PDF</span>'
        '<span class="support-pill">🖼️ JPG / JPEG / PNG</span>'
        '<span class="support-pill">🧠 Semantic AI</span>'
        '<span class="support-pill">📊 Exam Analytics</span>'
        '</div>'
        '</div>'
    )


    # --------------------------------------------------------
    # CAPABILITIES
    # --------------------------------------------------------

    render_html(
        '<div class="section-header">'
        '<div class="section-kicker">'
        'EXAMWISE ENGINE'
        '</div>'
        '<div class="section-title">'
        'Built for real question papers'
        '</div>'
        '<div class="section-description">'
        'One intelligent pipeline for digital papers, '
        'scanned documents and images.'
        '</div>'
        '</div>'
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        capability_card(
            "PDF",
            "Digital Papers",
            "Extract selectable PDF text"
        )

    with c2:

        capability_card(
            "OCR",
            "Scanned Papers",
            "Read image-based documents"
        )

    with c3:

        capability_card(
            "AI",
            "Semantic Matching",
            "Find meaning-level similarity"
        )

    with c4:

        capability_card(
            "DATA",
            "Exam Intelligence",
            "Convert papers into insights"
        )


    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    render_html(
        '<div class="section-header">'
        '<div class="section-kicker">'
        'CORE FEATURES'
        '</div>'
        '<div class="section-title">'
        'Everything you need to prepare smarter'
        '</div>'
        '<div class="section-description">'
        'ExamWise combines document processing, '
        'NLP and analytics in one workflow.'
        '</div>'
        '</div>'
    )

    f1, f2, f3 = st.columns(3)

    with f1:

        feature_card(
            "🔁",
            "Repeated Question Intelligence",
            "Detect questions and concepts that repeatedly "
            "appear across multiple examinations."
        )

    with f2:

        feature_card(
            "🧠",
            "Semantic Similarity",
            "Recognize questions with the same meaning "
            "even when their wording is different."
        )

    with f3:

        feature_card(
            "🎯",
            "Smart Study Priority",
            "Rank topics using repetition, marks, frequency "
            "and historical examination patterns."
        )

    st.write("")

    f4, f5, f6 = st.columns(3)

    with f4:

        feature_card(
            "📷",
            "Smart OCR",
            "Process scanned PDFs and direct question-paper "
            "images such as JPG, JPEG and PNG."
        )

    with f5:

        feature_card(
            "📊",
            "Exam Trend Analytics",
            "Explore topic frequency, marks distribution "
            "and year-wise question-paper patterns."
        )

    with f6:

        feature_card(
            "🤖",
            "Ask ExamWise",
            "Ask questions about analyzed papers and receive "
            "exam-focused insights from your data."
        )


# ============================================================
# UPLOAD PAGE
# ============================================================

elif page == "📤  Upload Papers":

    page_header(
        "QUESTION PAPER ANALYZER",
        "Upload your papers",
        "Add multiple previous-year question papers. "
        "ExamWise automatically checks whether each PDF "
        "contains selectable text or scanned pages."
    )

    render_html(
        '<div class="upload-hero">'
        '<div class="upload-symbol">☁️</div>'
        '<div class="upload-heading">'
        'Drop your question papers here'
        '</div>'
        '<div class="upload-text">'
        'Supports PDF • Scanned PDF • JPG • JPEG • PNG • Multiple files'
        '</div>'
        '</div>'
    )

    uploaded_files = st.file_uploader(
        "Upload question papers",
        type=[
            "pdf",
            "jpg",
            "jpeg",
            "png"
        ],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )


    # ========================================================
    # FILES SELECTED
    # ========================================================

    if uploaded_files:

        render_html(
            '<div class="section-header">'
            '<div class="section-kicker">'
            'FILES READY'
            '</div>'
            f'<div class="section-title">'
            f'{len(uploaded_files)} paper(s) selected'
            '</div>'
            '<div class="section-description">'
            'Review the files below before starting analysis.'
            '</div>'
            '</div>'
        )

        for uploaded_file in uploaded_files:

            safe_name = html_lib.escape(
                uploaded_file.name
            )

            if "." in uploaded_file.name:

                extension = (
                    uploaded_file.name
                    .rsplit(".", 1)[-1]
                    .upper()
                )

            else:

                extension = "FILE"

            size_kb = (
                uploaded_file.size / 1024
            )

            if uploaded_file.name.lower().endswith(
                ".pdf"
            ):

                icon = "📄"

            else:

                icon = "🖼️"

            render_html(
                '<div class="file-card">'
                f'<div class="file-name">'
                f'{icon} {safe_name}'
                '</div>'
                f'<div class="file-meta">'
                f'{extension} • {size_kb:.1f} KB'
                '</div>'
                '</div>'
            )

        st.write("")

        analyze = st.button(
            "✨ Analyze with ExamWise",
            type="primary",
            use_container_width=True
        )


        # ====================================================
        # ANALYZE FILES
        # ====================================================

        if analyze:

            st.session_state.processed_files = []

            render_html(
                '<div class="section-header">'
                '<div class="section-kicker">'
                'PROCESSING'
                '</div>'
                '<div class="section-title">'
                'Analysis results'
                '</div>'
                '<div class="section-description">'
                'ExamWise is inspecting each uploaded file.'
                '</div>'
                '</div>'
            )

            for file_index, uploaded_file in enumerate(
                uploaded_files
            ):

                file_name = (
                    uploaded_file.name
                )


                # ============================================
                # PDF FILE
                # ============================================

                if file_name.lower().endswith(
                    ".pdf"
                ):

                    with st.spinner(
                        f"Reading {file_name}..."
                    ):

                        result = (
                            extract_text_from_pdf(
                                uploaded_file
                            )
                        )


                    # ========================================
                    # TEXT PDF
                    # ========================================

                    if result["success"]:

                        st.session_state.processed_files.append(
                            {
                                "name": file_name,
                                "type": result["type"],
                                "pages": result["page_count"],
                                "text": result["text"]
                            }
                        )

                        safe_file_name = (
                            html_lib.escape(
                                file_name
                            )
                        )

                        render_html(
                            '<div class="result-card">'
                            '<div class="result-success">'
                            f'✓ {safe_file_name} processed successfully'
                            '</div>'
                            '<div class="file-meta">'
                            f'{result["page_count"]} page(s) '
                            f'• {result["type"]}'
                            '</div>'
                            '</div>'
                        )

                        metric1, metric2, metric3 = (
                            st.columns(3)
                        )

                        with metric1:

                            st.metric(
                                "Pages",
                                result[
                                    "page_count"
                                ]
                            )

                        with metric2:

                            st.metric(
                                "Document Type",
                                result[
                                    "type"
                                ]
                            )

                        with metric3:

                            character_count = len(
                                result["text"]
                            )

                            st.metric(
                                "Characters",
                                f"{character_count:,}"
                            )

                        with st.expander(
                            f"👀 View extracted text — {file_name}"
                        ):

                            st.text_area(
                                "Extracted text",
                                value=result["text"],
                                height=350,
                                key=f"pdf_text_{file_index}"
                            )


                    # ========================================
                    # SCANNED PDF
                    # ========================================

                    elif (
                        result["type"]
                        == "Scanned PDF"
                    ):

                        safe_file_name = (
                            html_lib.escape(
                                file_name
                            )
                        )

                        render_html(
                            '<div class="result-card">'
                            '<div class="result-warning">'
                            f'📷 {safe_file_name} '
                            'detected as a scanned PDF'
                            '</div>'
                            '<div class="file-meta">'
                            'No useful selectable text was found. '
                            'This document requires OCR processing.'
                            '</div>'
                            '</div>'
                        )


                    # ========================================
                    # ERROR
                    # ========================================

                    else:

                        st.error(
                            f"Could not process "
                            f"{file_name}."
                        )

                        if result.get(
                            "error"
                        ):

                            with st.expander(
                                "Technical details"
                            ):

                                st.code(
                                    result["error"]
                                )


                # ============================================
                # IMAGE FILE
                # ============================================

                else:

                    safe_file_name = (
                        html_lib.escape(
                            file_name
                        )
                    )

                    render_html(
                        '<div class="result-card">'
                        '<div class="result-warning">'
                        f'🖼️ {safe_file_name} '
                        'detected as an image'
                        '</div>'
                        '<div class="file-meta">'
                        'This image requires OCR processing.'
                        '</div>'
                        '</div>'
                    )


    # ========================================================
    # EMPTY UPLOAD STATE
    # ========================================================

    else:

        empty_state(
            "📚",
            "No papers uploaded yet",
            "Upload one or more PDF or image question "
            "papers to start your analysis."
        )


# ============================================================
# ANALYSIS PAGE
# ============================================================

elif page == "📊  Analysis":

    page_header(
        "ANALYTICS",
        "Intelligence Dashboard",
        "Explore question counts, repeated concepts, "
        "topic frequency, marks distribution and "
        "year-wise examination trends."
    )

    processed_count = len(
        st.session_state.processed_files
    )

    total_pages = sum(
        item.get(
            "pages",
            0
        )
        for item in
        st.session_state.processed_files
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Processed Papers",
            processed_count
        )

    with m2:

        st.metric(
            "Pages",
            total_pages
        )

    with m3:

        st.metric(
            "Questions",
            "—"
        )

    with m4:

        st.metric(
            "Repeated",
            "—"
        )

    if processed_count == 0:

        empty_state(
            "📊",
            "Your dashboard is waiting",
            "Upload and analyze question papers first. "
            "Question-level analytics will be connected "
            "after the parser is built."
        )

    else:

        st.success(
            "Document extraction data is available. "
            "Question detection is the next analysis stage."
        )


# ============================================================
# REPEATED QUESTIONS PAGE
# ============================================================

elif page == "🔁  Repeated Questions":

    page_header(
        "SEMANTIC ANALYSIS",
        "Repeated Questions",
        "ExamWise will compare the meaning of extracted "
        "questions and identify questions that test the "
        "same concept even when their wording changes."
    )

    empty_state(
        "🔁",
        "Semantic matching is waiting",
        "First we will extract individual questions. "
        "Then ExamWise will compare them using "
        "semantic embeddings."
    )


# ============================================================
# STUDY PRIORITY PAGE
# ============================================================

elif page == "🎯  Study Priority":

    page_header(
        "SMART PREPARATION",
        "Study Priority",
        "Combine frequency, repetition, marks and "
        "topic patterns to determine which areas "
        "deserve the most preparation time."
    )

    empty_state(
        "🎯",
        "Priority engine is waiting",
        "Study-priority rankings will become available "
        "after question, topic and marks analysis."
    )


# ============================================================
# ASK EXAMWISE PAGE
# ============================================================

elif page == "🤖  Ask ExamWise":

    page_header(
        "AI ASSISTANT",
        "Ask ExamWise",
        "Ask questions about your analyzed papers, "
        "such as which concepts repeat most or "
        "which topics deserve priority."
    )

    question = st.text_input(
        "Question",
        placeholder=(
            "Example: Which topics should "
            "I prepare first?"
        ),
        label_visibility="collapsed"
    )

    ask_button = st.button(
        "✨ Ask ExamWise",
        type="primary"
    )

    if ask_button:

        if question.strip():

            st.info(
                "The conversational intelligence "
                "engine will be connected after "
                "question extraction and semantic "
                "analysis are ready."
            )

        else:

            st.warning(
                "Enter a question first."
            )