# =========================================================
# PREMIUM DARK CINEMATIC CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL APP
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(0, 183, 255, 0.14),
            transparent 25%
        ),
        radial-gradient(
            circle at 85% 15%,
            rgba(79, 70, 229, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(0, 255, 200, 0.06),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #030712 0%,
            #050816 45%,
            #020617 100%
        );

    color: #e5f7ff;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {
    max-width: 1350px;
    padding-top: 25px;
    padding-bottom: 60px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero-box {
    position: relative;
    text-align: center;
    padding: 30px 25px;
    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            rgba(10, 25, 45, 0.88),
            rgba(5, 12, 28, 0.82)
        );

    border: 1px solid rgba(0, 200, 255, 0.25);

    box-shadow:
        0 0 40px rgba(0, 180, 255, 0.08),
        inset 0 0 30px rgba(0, 150, 255, 0.035);

    backdrop-filter: blur(18px);
}


/* glowing line */

.hero-box::before {
    content: "";
    position: absolute;
    top: 0;
    left: 12%;
    width: 76%;
    height: 2px;

    background: linear-gradient(
        90deg,
        transparent,
        #00d9ff,
        #6d5dfc,
        #00d9ff,
        transparent
    );

    box-shadow:
        0 0 15px #00d9ff,
        0 0 30px rgba(0, 217, 255, 0.5);

    border-radius: 10px;
}


/* =========================================================
   TITLE
   ========================================================= */

.title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: 2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #5ee7ff,
        #00c8ff,
        #7c6cff,
        #ffffff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 25px rgba(0, 200, 255, 0.25);
}


/* =========================================================
   SUBTITLE
   ========================================================= */

.subtitle {
    color: #9fc8d8;
    font-size: 18px;
    margin-top: 5px;
}


/* =========================================================
   ONLINE BADGE
   ========================================================= */

.online {
    display: inline-block;

    margin-top: 15px;
    padding: 8px 20px;

    border-radius: 30px;

    color: #5dffcb;

    background:
        rgba(0, 255, 180, 0.07);

    border:
        1px solid rgba(0, 255, 180, 0.35);

    font-weight: 700;

    box-shadow:
        0 0 18px rgba(0, 255, 180, 0.08);
}


/* =========================================================
   TAGLINE
   ========================================================= */

.tagline {
    margin-top: 14px;
    color: #6f91a1;
    font-size: 14px;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section {
    font-size: 23px;
    font-weight: 800;

    color: #d9f8ff;

    margin-top: 30px;
    margin-bottom: 15px;

    letter-spacing: 0.3px;

    text-shadow:
        0 0 15px rgba(0, 200, 255, 0.18);
}


/* =========================================================
   SERVICE CARDS
   ========================================================= */

.service-card {
    position: relative;

    text-align: center;

    padding: 20px 7px;

    min-height: 110px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(12, 30, 50, 0.88),
            rgba(4, 14, 28, 0.92)
        );

    border:
        1px solid rgba(0, 190, 255, 0.16);

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.35),
        inset 0 0 20px rgba(0, 160, 255, 0.025);

    transition:
        all 0.25s ease;
}


/* service card hover */

.service-card:hover {
    transform: translateY(-5px);

    border-color:
        rgba(0, 210, 255, 0.5);

    box-shadow:
        0 0 25px rgba(0, 190, 255, 0.12),
        0 12px 30px rgba(0, 0, 0, 0.45);
}


/* =========================================================
   SERVICE ICON
   ========================================================= */

.service-icon {
    font-size: 34px;

    filter:
        drop-shadow(
            0 0 8px rgba(0, 210, 255, 0.3)
        );
}


/* =========================================================
   SERVICE NAME
   ========================================================= */

.service-name {
    color: #b9dbe6;

    font-size: 13px;

    font-weight: 700;

    margin-top: 8px;
}


/* =========================================================
   POPULAR QUESTIONS BOX
   ========================================================= */

.popular {
    padding: 20px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(10, 27, 45, 0.82),
            rgba(3, 12, 25, 0.88)
        );

    border:
        1px solid rgba(0, 190, 255, 0.15);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35);

    backdrop-filter:
        blur(15px);
}


/* =========================================================
   ALL BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;

    min-height: 42px;

    border-radius: 14px;

    border:
        1px solid rgba(0, 200, 255, 0.25);

    background:
        linear-gradient(
            135deg,
            rgba(8, 28, 48, 0.95),
            rgba(5, 17, 32, 0.95)
        );

    color: #c9f5ff;

    font-weight: 700;

    box-shadow:
        0 5px 18px rgba(0, 0, 0, 0.25);

    transition:
        all 0.25s ease;
}


/* BUTTON HOVER */

.stButton > button:hover {

    border-color:
        #00d9ff;

    color:
        #ffffff;

    background:
        linear-gradient(
            135deg,
            rgba(0, 150, 220, 0.18),
            rgba(70, 80, 255, 0.15)
        );

    box-shadow:
        0 0 18px rgba(0, 210, 255, 0.18);

    transform:
        translateY(-2px);
}


/* =========================================================
   CHAT AREA
   ========================================================= */

[data-testid="stChatMessage"] {

    background:
        rgba(5, 18, 32, 0.55);

    border:
        1px solid rgba(0, 190, 255, 0.08);

    border-radius:
        18px;

    margin-bottom:
        10px;

    padding:
        8px 12px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.18);
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

[data-testid="stChatInput"] {

    background:
        rgba(3, 12, 24, 0.85);

    border-radius:
        22px;

    box-shadow:
        0 0 25px rgba(0, 170, 255, 0.06);
}


[data-testid="stChatInput"] textarea {

    background:
        #071321 !important;

    color:
        #e8faff !important;

    border:
        2px solid rgba(0, 200, 255, 0.35) !important;

    border-radius:
        20px !important;

    font-size:
        16px !important;

    caret-color:
        #00d9ff !important;
}


[data-testid="stChatInput"] textarea:focus {

    border:
        2px solid #00d9ff !important;

    box-shadow:
        0 0 18px rgba(0, 217, 255, 0.15) !important;
}


/* =========================================================
   CHAT TEXT
   ========================================================= */

[data-testid="stChatMessage"] p {
    color: #d7edf5;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #020812,
            #030b16,
            #020611
        );

    border-right:
        1px solid rgba(0, 200, 255, 0.12);
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {

    border:
        none;

    height:
        1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(0, 200, 255, 0.25),
            transparent
        );
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align:
        center;

    margin-top:
        45px;

    padding:
        25px;

    color:
        #668392;

    font-size:
        13px;

    border-top:
        1px solid rgba(0, 190, 255, 0.08);
}


/* =========================================================
   STREAMLIT TEXT
   ========================================================= */

.stMarkdown {
    color: #d7edf5;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #020611;
}

::-webkit-scrollbar-thumb {
    background:
        linear-gradient(
            #00bfe7,
            #5d5cff
        );

    border-radius:
        10px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media(max-width: 700px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .title {
        font-size: 30px;
        letter-spacing: 1px;
    }

    .subtitle {
        font-size: 14px;
    }

    .hero-box {
        padding: 20px 12px;
        border-radius: 22px;
    }

    .service-card {
        min-height: 95px;
    }

    .service-icon {
        font-size: 27px;
    }

}

</style>
""",
    unsafe_allow_html=True
)
