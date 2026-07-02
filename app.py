# -*- coding: utf-8 -*-
"""
منصة طاقة النجوم — Cosmic Energy Platform
الواجهة الرئيسية (Router + UI/UX + Branding + بوابة الإعلان + الترويج المتبادل).
كل منطق الحسابات الفلكية موجود في engine.py، ودوال عرض الخدمات في services.py.
"""

import math
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from datetime import datetime

# 1) إعداد الصفحة — يجب أن يكون أول أمر Streamlit
st.set_page_config(
    page_title="طاقة النجوم | منصة الطاقة الكونية الشاملة للتاروت والأبراج والروحانيات",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "منصة طاقة النجوم — بوابتك المتكاملة للتاروت، الأبراج، الخريطة الفلكية، "
                 "تفسير الأحلام، الكرمة، صيدلية الأحجار، والرقم الروحي."
    },
)

# المحرك ودوال الخدمات
from engine import *          # noqa: F401,F403  (البيانات + كل دوال المنطق)
import services               # دوال render_0 .. render_8


# ============================================================
# 2) السيو الأساسي (Meta / Open Graph) — أقصى ما يتيحه Streamlit
# ============================================================
SEO_DESCRIPTION = (
    "منصة طاقة النجوم: اكتشف توافقك العاطفي، حلّل اسمك وبرجك، ارسم خريطتك الفلكية بـ12 بيتاً، "
    "فسّر أحلامك، اسحب التاروت، احسب كرمتك ورقمك الروحي، واختر أحجار الطاقة المناسبة لك — مجاناً وبالعربية."
)
st.markdown(
    f"""
    <meta name="description" content="{SEO_DESCRIPTION}">
    <meta name="keywords" content="تاروت, أبراج, خريطة فلكية, تفسير الأحلام, الكرمة, الرقم الروحي, طاقة, روحانيات, توافق الأسماء, ابن سيرين">
    <meta name="author" content="طاقة النجوم">
    <meta property="og:title" content="طاقة النجوم | منصة الطاقة الكونية الشاملة">
    <meta property="og:description" content="{SEO_DESCRIPTION}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#0b0420">
    <meta name="robots" content="index, follow">
    <html lang="ar" dir="rtl">
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3) نظام التصميم (Design System) — CSS كامل
# ============================================================
CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

:root{
  --bg-0:#070213; --bg-1:#0e0626; --bg-2:#16093a;
  --glass:rgba(20,11,44,0.62); --glass-2:rgba(15,10,34,0.55);
  --stroke:rgba(255,255,255,0.10); --stroke-2:rgba(187,134,252,0.28);
  --gold:#ffd54a; --mag:#ff79c6; --pur:#bb86fc; --cyan:#00e6c3; --blue:#46c8ff;
  --ink:#f4eeff; --muted:#b9aee0;
  --r-lg:26px; --r-md:18px; --r-sm:13px;
  --shadow:0 22px 60px rgba(0,0,0,0.45);
}

/* إخفاء كروت Streamlit الافتراضية ليبدو كموقع حقيقي */
#MainMenu, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], footer {display:none !important;}

html, body, [class*="css"], .stApp, p, h1,h2,h3,h4,h5,h6, label, span, div, input, textarea{
  font-family:'Cairo', sans-serif !important;
}
html, body, [class*="css"]{ direction:rtl; text-align:right; color:var(--ink); }

.stApp{
  background:
    radial-gradient(1200px 600px at 80% -10%, rgba(123,92,255,0.22), transparent 60%),
    radial-gradient(900px 500px at 10% 0%, rgba(0,230,195,0.12), transparent 55%),
    linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
  background-attachment:fixed;
}
/* طبقة نجوم متلألئة */
.stApp::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.5;
  background-image:
    radial-gradient(1.5px 1.5px at 20% 30%, #fff, transparent),
    radial-gradient(1.5px 1.5px at 70% 60%, #fff, transparent),
    radial-gradient(1px 1px at 40% 80%, #fff, transparent),
    radial-gradient(1px 1px at 85% 20%, #fff, transparent),
    radial-gradient(1.5px 1.5px at 55% 12%, #fff, transparent);
  background-repeat:repeat; background-size:340px 340px;
  animation:twinkle 4.5s ease-in-out infinite;
}
@keyframes twinkle{0%,100%{opacity:.35}50%{opacity:.7}}

.block-container{ position:relative; z-index:1; max-width:1220px; padding:14px 22px 40px !important; }

/* ====== الهيدر ====== */
.site-header{
  position:sticky; top:0; z-index:50; margin:0 0 6px 0;
  background:linear-gradient(90deg, rgba(14,6,38,.92), rgba(22,9,58,.86));
  border:1px solid var(--stroke); border-radius:var(--r-md);
  box-shadow:var(--shadow); backdrop-filter:blur(16px);
  padding:14px 22px; display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;
}
.brand{display:flex; align-items:center; gap:14px;}
.brand .logo{
  width:54px; height:54px; border-radius:16px; flex:0 0 auto;
  display:flex; align-items:center; justify-content:center; font-size:28px;
  background:radial-gradient(circle at 30% 25%, #ffe9a8, #ff79c6 45%, #7b5cff);
  box-shadow:0 0 26px rgba(255,121,198,.5), inset 0 0 14px rgba(255,255,255,.35);
}
.brand h1{font-size:1.5rem; margin:0; letter-spacing:.5px; line-height:1.1;
  background:linear-gradient(90deg,#ffd54a,#ff79c6,#bb86fc); -webkit-background-clip:text; background-clip:text; color:transparent;}
.brand small{color:var(--muted); font-size:.78rem; font-weight:600;}
.header-badges{display:flex; gap:8px; flex-wrap:wrap;}
.hb{font-size:.72rem; color:#d9ceff; background:rgba(255,255,255,.06);
  border:1px solid var(--stroke); padding:6px 11px; border-radius:999px;}

/* ====== الهيرو ====== */
.hero{
  margin:14px 0 8px; padding:40px 30px; border-radius:var(--r-lg);
  background:linear-gradient(135deg, rgba(46,16,77,.85), rgba(12,6,30,.85));
  border:1px solid var(--stroke-2); box-shadow:var(--shadow); position:relative; overflow:hidden;
  animation:fadeUp .7s ease both;
}
.hero::after{content:""; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(600px 220px at 85% 0%, rgba(255,121,198,.18), transparent 60%);}
.hero h2{font-size:clamp(1.9rem,4vw,3.2rem); margin:0 0 12px; line-height:1.18;
  text-shadow:0 0 30px rgba(187,134,252,.4);}
.hero h2 .grad{background:linear-gradient(90deg,#ffd54a,#ff79c6,#46c8ff);
  -webkit-background-clip:text; background-clip:text; color:transparent;}
.hero p{color:#efe7ff; font-size:1.06rem; line-height:1.8; max-width:760px; margin:0;}
.hero .pills{margin-top:18px; display:flex; gap:10px; flex-wrap:wrap;}
.hero .pill{background:rgba(255,255,255,.07); border:1px solid var(--stroke);
  padding:8px 14px; border-radius:999px; font-size:.85rem; color:#e9e0ff;}

/* ====== عناوين الأقسام ====== */
.section-title{display:flex; align-items:center; gap:12px; margin:30px 0 14px;}
.section-title .bar{width:6px; height:30px; border-radius:6px;
  background:linear-gradient(180deg,#ffd54a,#ff79c6);}
.section-title h3{margin:0; font-size:1.45rem;}
.section-title small{color:var(--muted); font-size:.85rem; display:block; margin-top:2px;}

/* ====== شريط الفئة ====== */
.cat-head{display:flex; align-items:center; gap:16px; padding:18px 22px; border-radius:var(--r-md);
  border:1px solid var(--stroke); box-shadow:var(--shadow); margin:8px 0 16px; animation:fadeUp .6s ease both;}
.cat-head .ico{width:58px;height:58px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:30px;}
.cat-head h3{margin:0; font-size:1.5rem;}
.cat-head p{margin:4px 0 0; color:#efe7ff; font-size:.95rem;}

/* ====== كروت الخدمات ====== */
.svc-card{
  border-radius:var(--r-md); overflow:hidden; border:1px solid var(--stroke);
  background:var(--glass); box-shadow:var(--shadow); margin-bottom:2px;
  transition:transform .25s ease, box-shadow .25s ease, border-color .25s ease;
  animation:fadeUp .6s ease both; min-height:232px;
}
.svc-card:hover{transform:translateY(-6px); border-color:var(--stroke-2);
  box-shadow:0 26px 70px rgba(123,92,255,.35);}
.svc-thumb{height:96px; display:flex; align-items:center; justify-content:center; position:relative;}
.svc-thumb::after{content:""; position:absolute; inset:0; background:rgba(0,0,0,.12);}
.svc-thumb .svc-ico{font-size:46px; filter:drop-shadow(0 6px 14px rgba(0,0,0,.4)); z-index:1;}
.svc-body{padding:16px 16px 6px;}
.svc-body h3{margin:0 0 8px; font-size:1.15rem; color:#fff;}
.svc-body p{margin:0 0 10px; color:var(--muted); font-size:.9rem; line-height:1.6; min-height:48px;}
.svc-tag{display:inline-block; font-size:.72rem; color:#e9e0ff; background:rgba(255,255,255,.06);
  border:1px solid var(--stroke); padding:4px 10px; border-radius:999px;}

/* ====== الكروت الزجاجية العامة ====== */
.glass{background:var(--glass); border:1px solid var(--stroke); border-radius:var(--r-md);
  padding:18px 20px; box-shadow:var(--shadow); animation:fadeUp .6s ease both;}
.result-box{
  background:rgba(20,11,44,0.72); border:1px solid rgba(255,121,198,0.22); border-radius:var(--r-lg);
  padding:30px; margin-top:20px; box-shadow:0 22px 60px rgba(95,41,178,0.2);
  backdrop-filter:blur(12px); animation:fadeUp .5s ease both;
}
.history-box{background:rgba(255,255,255,0.04); border:1px dotted rgba(255,215,0,0.25);
  border-radius:16px; padding:16px; margin:12px 0; font-size:.95rem;}
.info-banner{background:linear-gradient(90deg, rgba(123,92,255,.95), rgba(255,121,198,.95));
  color:#fff; padding:14px 18px; border-radius:16px; text-align:center; font-weight:800;
  box-shadow:0 12px 30px rgba(123,92,255,.3); margin:6px 0 4px;}
.error-message{background:rgba(255,58,106,.15); border-right:4px solid #ff5065; border-radius:12px; padding:14px; margin:10px 0;}
.success-message{background:rgba(0,230,195,.12); border-right:4px solid #00e6c3; border-radius:12px; padding:14px; margin:10px 0;}

/* ====== بوابة الإعلان ====== */
.ad-wrap{border:1px solid var(--stroke-2); border-radius:var(--r-lg); padding:24px;
  background:linear-gradient(135deg, rgba(30,12,60,.9), rgba(10,5,26,.92)); box-shadow:var(--shadow);
  text-align:center; animation:fadeUp .5s ease both;}
.ad-tag{display:inline-block; font-size:.74rem; letter-spacing:1px; color:#0b0420; font-weight:800;
  background:var(--gold); padding:5px 12px; border-radius:999px;}
.ad-promo{margin:16px auto; max-width:520px; padding:18px; border-radius:var(--r-md);
  border:1px solid var(--stroke); background:rgba(255,255,255,.04);}
.ad-promo h4{margin:0 0 6px; color:var(--gold);}
.ad-promo p{margin:0; color:#e9e0ff; font-size:.92rem; line-height:1.6;}

/* ====== الترويج المتبادل داخل الخدمة ====== */
.cross-sell{margin-top:26px; border-radius:var(--r-md); padding:20px;
  border:1px dashed var(--stroke-2); background:rgba(255,255,255,.035); animation:fadeUp .6s ease both;}
.cross-sell .cs-flex{display:flex; align-items:center; gap:16px; flex-wrap:wrap; justify-content:space-between;}
.cross-sell .cs-ico{width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px;flex:0 0 auto;}
.cross-sell h4{margin:0; color:#fff;}
.cross-sell small{color:var(--gold); font-weight:700;}
.cross-sell p{margin:4px 0 0; color:var(--muted); font-size:.9rem;}

/* ====== الفوتر ====== */
.site-footer{margin-top:40px; padding:28px 24px 18px; border-radius:var(--r-lg);
  background:linear-gradient(180deg, rgba(14,6,38,.9), rgba(8,3,20,.95));
  border:1px solid var(--stroke); box-shadow:var(--shadow);}
.footer-grid{display:grid; grid-template-columns:1.4fr 1fr 1fr; gap:24px;}
.site-footer h4{color:#fff; margin:0 0 12px; font-size:1.05rem;}
.site-footer a, .site-footer span.fl{color:var(--muted); text-decoration:none; display:block; margin:7px 0; font-size:.9rem;}
.site-footer .fbrand{display:flex; align-items:center; gap:12px; margin-bottom:10px;}
.footer-bottom{border-top:1px solid var(--stroke); margin-top:18px; padding-top:14px;
  text-align:center; color:var(--muted); font-size:.82rem;}
.footer-bottom .disc{font-size:.76rem; opacity:.8; margin-top:6px;}

/* ====== أزرار Streamlit ====== */
.stButton>button{
  background:linear-gradient(90deg,#ff79c6 0%,#bb86fc 100%) !important; color:#0a0420 !important;
  font-weight:900 !important; font-size:15px !important; border:none !important; border-radius:14px !important;
  padding:12px 22px !important; width:100%; box-shadow:0 8px 26px rgba(187,134,252,.28);
  transition:transform .22s ease, box-shadow .22s ease, filter .22s ease;
}
.stButton>button:hover{transform:translateY(-3px); box-shadow:0 14px 36px rgba(255,121,198,.5); filter:brightness(1.05);}
.stButton>button[kind="secondary"]{
  background:rgba(255,255,255,.06) !important; color:#eadfff !important; font-weight:800 !important;
  border:1px solid var(--stroke) !important; box-shadow:none;
}
.stButton>button[kind="secondary"]:hover{background:rgba(187,134,252,.18) !important; border-color:var(--stroke-2) !important;}
.stDownloadButton>button{background:linear-gradient(90deg,#00e6c3,#46c8ff)!important; color:#04121a!important; font-weight:900!important; border-radius:14px!important; border:none!important;}

/* ====== التبويبات والمدخلات ====== */
.stTabs [data-baseweb="tab-list"]{gap:8px; justify-content:center; flex-wrap:wrap;
  background:rgba(13,8,31,.6); padding:10px; border-radius:16px;}
.stTabs [data-baseweb="tab"]{background:rgba(20,11,44,.85)!important; border:1px solid var(--stroke)!important;
  border-radius:12px!important; padding:10px 18px!important; color:#d7c6ff!important; font-weight:700;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#bb86fc,#ff79c6)!important; color:#05020c!important; border:none!important;}
.stTextInput>div>input, .stTextArea>div>textarea, .stNumberInput>div>input,
.stDateInput input, .stTimeInput input{
  background:rgba(16,11,32,.92)!important; border:1px solid var(--stroke)!important; color:#fdf7ff!important;
  border-radius:14px!important; padding:11px!important;}
.stSelectbox>div>div>div, .stMultiSelect>div>div{background:rgba(16,11,32,.9)!important;
  border:1px solid var(--stroke)!important; border-radius:14px!important; color:#f5f1ff!important;}
div[data-testid="stRadio"] label{color:#cfe9ff!important; font-weight:700!important;}
[data-testid="stMetric"]{background:rgba(14,7,25,.86)!important; border-radius:18px!important; padding:16px!important;
  border:1px solid var(--stroke)!important;}
[data-testid="stExpander"]{border:1px solid var(--stroke)!important; border-radius:16px!important; background:rgba(255,255,255,.03)!important;}

@keyframes fadeUp{from{opacity:0; transform:translateY(16px)} to{opacity:1; transform:none}}

/* ====== الاستجابة للموبايل ====== */
@media (max-width:820px){
  .block-container{padding:10px 12px 30px !important;}
  .site-header{padding:12px 14px;}
  .brand h1{font-size:1.2rem;}
  .header-badges{display:none;}
  .hero{padding:26px 18px;}
  .footer-grid{grid-template-columns:1fr; gap:14px;}
  .cat-head{flex-direction:row;}
}
</style>
"""
st.markdown(CSS_STYLES, unsafe_allow_html=True)


# ============================================================
# 4) تهيئة حالة الجلسة + الراوتر
# ============================================================
init_session_state()  # من engine.py (سجل القراءات/المفضلات/الإحصائيات)
st.session_state.setdefault("view", "home")           # "home" | ("cat", key) | ("service", id)
st.session_state.setdefault("unlocked_services", {})  # {service_id: True}
st.session_state.setdefault("ad_started", {})         # {service_id: datetime}
st.session_state.setdefault("is_premium", False)

AD_SECONDS = 30


def goto(view):
    st.session_state.view = view
    st.rerun()


# ============================================================
# 5) سجل الفئات والخدمات (قلب الـ ECO System)
# ============================================================
CATEGORIES = {
    "love":       {"name": "الحب والعلاقات", "icon": "💞",
                   "grad": "linear-gradient(135deg,#ff5f9e,#b56bff)",
                   "desc": "حلّل الانسجام الطاقي والعاطفي بينك وبين من تحب.", "services": [0]},
    "identity":   {"name": "هويتك الكونية", "icon": "🪐",
                   "grad": "linear-gradient(135deg,#7b5cff,#46c8ff)",
                   "desc": "اكتشف برجك الباطني ورقمك الروحي وخريطتك الفلكية الكاملة.", "services": [1, 8, 2]},
    "divination": {"name": "العرافة والرؤى", "icon": "🔮",
                   "grad": "linear-gradient(135deg,#a96bff,#ff79c6)",
                   "desc": "اسحب التاروت وفسّر أحلامك برسائل الكون والتراث.", "services": [4, 3]},
    "healing":    {"name": "شفاؤك الداخلي", "icon": "🧘",
                   "grad": "linear-gradient(135deg,#00d4a8,#46c8ff)",
                   "desc": "وازن طاقتك عبر الكرمة وأحجار الشاكرات وعمل الظل.", "services": [6, 5, 7]},
}

SERVICES = {
    0: {"name": "حاسبة التوافق والاتصال", "icon": "❤️", "cat": "love",
        "tagline": "نسبة الانسجام بين اسمين أو برجين، مع مقارنات متعددة الأشخاص.",
        "grad": "linear-gradient(135deg,#ff5f9e,#b56bff)", "render": services.render_0},
    1: {"name": "تحليل الاسم والأبراج", "icon": "🪐", "cat": "identity",
        "tagline": "استخرج البرج الباطني الحقيقي وطاقة حروف اسمك.",
        "grad": "linear-gradient(135deg,#7b5cff,#46c8ff)", "render": services.render_1},
    2: {"name": "الخريطة الفلكية", "icon": "🗺️", "cat": "identity",
        "tagline": "خريطة 12 بيتاً كونياً برسم بياني وتوقعات لكل بيت.",
        "grad": "linear-gradient(135deg,#5b6bff,#a96bff)", "render": services.render_2},
    3: {"name": "تفسير الأحلام الذكي", "icon": "🌙", "cat": "divination",
        "tagline": "فك رموز أحلامك بمعجم ابن سيرين والنابلسي المدمج.",
        "grad": "linear-gradient(135deg,#6b5cff,#ff79c6)", "render": services.render_3},
    4: {"name": "التاروت والإرشاد", "icon": "🃏", "cat": "divination",
        "tagline": "اسحب كارت تاروت ذكي برسالة ونصيحة كونية مخصصة.",
        "grad": "linear-gradient(135deg,#a96bff,#ff79c6)", "render": services.render_4},
    5: {"name": "حاسبة الكرمة", "icon": "⚖️", "cat": "healing",
        "tagline": "اكشف رصيد الكرمة والديون الطاقية الكامنة في اسمك.",
        "grad": "linear-gradient(135deg,#00d4a8,#7b5cff)", "render": services.render_5},
    6: {"name": "صيدلية الطاقة والأحجار", "icon": "💎", "cat": "healing",
        "tagline": "أحجار كريمة وشاكرات موصى بها لموازنة حالتك الطاقية.",
        "grad": "linear-gradient(135deg,#00d4a8,#46c8ff)", "render": services.render_6},
    7: {"name": "اختبار الحالة والظل", "icon": "🧠", "cat": "healing",
        "tagline": "حلّل حالتك النفسية ونمط ظلّك مع خطة علاج عملية.",
        "grad": "linear-gradient(135deg,#7b5cff,#00d4a8)", "render": services.render_7},
    8: {"name": "الرقم الروحي السري", "icon": "🔢", "cat": "identity",
        "tagline": "احسب رقم مسار حياتك واكتشف رسالته الكونية.",
        "grad": "linear-gradient(135deg,#46c8ff,#7b5cff)", "render": services.render_8},
}

# لكل خدمة خدمة شقيقة تُعرض داخلها (ترويج متبادل)
RELATED = {0: 8, 1: 2, 2: 8, 3: 4, 4: 3, 5: 6, 6: 7, 7: 5, 8: 1}


# ============================================================
# 6) مكوّنات الواجهة (Header / Hero / Cards / Footer)
# ============================================================
def render_header():
    st.markdown(
        """
        <div class="site-header">
          <div class="brand">
            <div class="logo">🔮</div>
            <div>
              <h1>طاقة النجوم</h1>
              <small>منصة الطاقة الكونية الشاملة • Cosmic Energy Platform</small>
            </div>
          </div>
          <div class="header-badges">
            <span class="hb">✦ 9 خدمات روحانية</span>
            <span class="hb">✦ عربي بالكامل</span>
            <span class="hb">✦ مجاني</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # شريط تنقّل وظيفي
    nav = st.columns([1.1, 1, 1, 1, 1])
    labels = [
        ("🏠 الرئيسية", "home"),
        ("💞 الحب", ("cat", "love")),
        ("🪐 الهوية", ("cat", "identity")),
        ("🔮 العرافة", ("cat", "divination")),
        ("🧘 الشفاء", ("cat", "healing")),
    ]
    for col, (lbl, target) in zip(nav, labels):
        with col:
            if st.button(lbl, key=f"nav_{lbl}", type="secondary", use_container_width=True):
                goto(target)


def render_footer():
    year = datetime.now().year
    st.markdown(
        f"""
        <div class="site-footer">
          <div class="footer-grid">
            <div>
              <div class="fbrand"><div class="logo" style="width:42px;height:42px;font-size:22px;">🔮</div>
                <div><h4 style="margin:0;">طاقة النجوم</h4>
                <span class="fl">منصتك المتكاملة للوعي الكوني والروحانيات بالعربية.</span></div>
              </div>
              <span class="fl">نقدّم تجربة تفاعلية تجمع التاروت، الأبراج، الخريطة الفلكية، تفسير الأحلام، الكرمة، الأحجار، والأرقام الروحية في مكان واحد.</span>
            </div>
            <div>
              <h4>الخدمات</h4>
              <span class="fl">❤️ حاسبة التوافق</span>
              <span class="fl">🃏 التاروت والإرشاد</span>
              <span class="fl">🗺️ الخريطة الفلكية</span>
              <span class="fl">🌙 تفسير الأحلام</span>
              <span class="fl">💎 صيدلية الأحجار</span>
            </div>
            <div>
              <h4>روابط</h4>
              <span class="fl">📜 سياسة الخصوصية</span>
              <span class="fl">📘 شروط الاستخدام</span>
              <span class="fl">✉️ تواصل معنا</span>
              <span class="fl">⭐ قيّم المنصة</span>
            </div>
          </div>
          <div class="footer-bottom">
            © {year} طاقة النجوم — جميع الحقوق محفوظة.
            <div class="disc">تنويه: المحتوى مقدَّم لأغراض الترفيه والتأمل الذاتي ولا يُعدّ بديلاً عن استشارة طبية أو نفسية أو مالية متخصصة.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=""):
    st.markdown(
        f"""<div class="section-title"><div class="bar"></div>
        <div><h3>{title}</h3>{f'<small>{subtitle}</small>' if subtitle else ''}</div></div>""",
        unsafe_allow_html=True,
    )


def service_card(col, sid):
    s = SERVICES[sid]
    cat = CATEGORIES[s["cat"]]
    with col:
        st.markdown(
            f"""
            <div class="svc-card">
              <div class="svc-thumb" style="background:{s['grad']};"><span class="svc-ico">{s['icon']}</span></div>
              <div class="svc-body">
                <h3>{s['name']}</h3>
                <p>{s['tagline']}</p>
                <span class="svc-tag">{cat['icon']} {cat['name']}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"افتح الخدمة  {s['icon']}", key=f"open_{sid}", use_container_width=True):
            goto(("service", sid))


def render_cards_grid(ids):
    """يرتّب الكروت في صفوف من 3 أعمدة بشكل متجاوب."""
    for row_start in range(0, len(ids), 3):
        row = ids[row_start:row_start + 3]
        cols = st.columns(len(row)) if len(row) < 3 else st.columns(3)
        for i, sid in enumerate(row):
            service_card(cols[i], sid)


def render_category_section(cat_key, with_cards=True):
    cat = CATEGORIES[cat_key]
    st.markdown(
        f"""
        <div class="cat-head" style="background:linear-gradient(120deg, rgba(20,11,44,.85), rgba(10,5,26,.6)), {cat['grad']};">
          <div class="ico" style="background:rgba(0,0,0,.25);">{cat['icon']}</div>
          <div><h3>{cat['name']}</h3><p>{cat['desc']}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if with_cards:
        render_cards_grid(cat["services"])


# ============================================================
# 7) بوابة الإعلان (عدّاد 30 ثانية إجباري) + مكوّن العدّاد
# ============================================================
_COUNTDOWN_TMPL = """
<div style="display:flex;flex-direction:column;align-items:center;font-family:'Cairo',sans-serif;color:#fff;">
  <div style="position:relative;width:170px;height:170px;">
    <svg width="170" height="170">
      <circle cx="85" cy="85" r="72" stroke="rgba(255,255,255,0.12)" stroke-width="11" fill="none"></circle>
      <circle id="ring" cx="85" cy="85" r="72" stroke="#ffd54a" stroke-width="11" fill="none"
        stroke-linecap="round" transform="rotate(-90 85 85)"
        stroke-dasharray="__C__" stroke-dashoffset="0"></circle>
    </svg>
    <div id="num" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
      font-size:46px;font-weight:900;color:#ffd54a;">__REM__</div>
  </div>
  <div id="msg" style="margin-top:12px;font-size:15px;color:#cbbdf0;font-weight:700;">⏳ الإعلان قيد التشغيل…</div>
</div>
<script>
  var total=__TOTAL__, rem=__REM__, C=__C__;
  var ring=document.getElementById('ring'), num=document.getElementById('num'), msg=document.getElementById('msg');
  function tick(){
    var frac = Math.max(0, rem/total);
    ring.setAttribute('stroke-dashoffset', (C*(1-frac)).toFixed(1));
    num.textContent = rem;
    if(rem<=0){
      msg.textContent='✅ انتهى الإعلان — اضغط زر الفتح بالأسفل';
      ring.setAttribute('stroke','#00e6a8'); num.style.color='#00e6a8'; num.textContent='✓';
      return;
    }
    rem--; setTimeout(tick,1000);
  }
  tick();
</script>
"""


def _countdown_html(remaining, total=AD_SECONDS):
    c = 2 * math.pi * 72
    return (_COUNTDOWN_TMPL
            .replace("__TOTAL__", str(total))
            .replace("__REM__", str(int(remaining)))
            .replace("__C__", f"{c:.1f}"))


def ad_gate(sid):
    """يُرجع True إذا كانت الخدمة مفتوحة، وإلا يعرض الإعلان ويُرجع False."""
    s = SERVICES[sid]
    if st.session_state.unlocked_services.get(sid):
        return True

    promo = SERVICES[RELATED[sid]]
    started = st.session_state.ad_started.get(sid)

    st.markdown('<div class="ad-wrap">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <span class="ad-tag">إعلان مُموَّل</span>
        <p style="color:#cbbdf0; margin:14px 0 0; font-size:.92rem;">
          لفتح <b style="color:#fff;">{s['icon']} {s['name']}</b> مجاناً، شاهد هذا الإعلان القصير (30 ثانية).</p>
        <div class="ad-promo">
          <h4>{promo['icon']} جرّب أيضاً: {promo['name']}</h4>
          <p>{promo['tagline']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if started is None:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button(f"▶️ مشاهدة إعلان 30 ثانية لفتح {s['name']}", key=f"adstart_{sid}", use_container_width=True):
                st.session_state.ad_started[sid] = datetime.now()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return False

    elapsed = (datetime.now() - started).total_seconds()
    remaining = max(0, AD_SECONDS - int(elapsed))
    components.html(_countdown_html(remaining), height=240)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        btn_label = "✅ تم — افتح الخدمة الآن" if remaining <= 0 else f"🔓 افتح الخدمة (انتظر {remaining} ث)"
        if st.button(btn_label, key=f"adopen_{sid}", use_container_width=True):
            if (datetime.now() - started).total_seconds() >= AD_SECONDS:
                st.session_state.unlocked_services[sid] = True
                st.rerun()
            else:
                left = AD_SECONDS - int((datetime.now() - started).total_seconds())
                st.warning(f"⏳ لم ينتهِ الإعلان بعد — تبقّى {max(1, left)} ثانية. انتظر العدّاد ثم اضغط مجدداً.")
        if remaining > 0:
            st.caption("سيكتمل العدّاد خلال ثوانٍ — انتظره ثم اضغط زر الفتح.")
    st.markdown("</div>", unsafe_allow_html=True)
    return False


# ============================================================
# 8) الترويج المتبادل داخل الخدمة
# ============================================================
def cross_sell(sid):
    r = RELATED[sid]
    s = SERVICES[r]
    cat = CATEGORIES[s["cat"]]
    st.markdown(
        f"""
        <div class="cross-sell">
          <div class="cs-flex">
            <div style="display:flex; align-items:center; gap:14px;">
              <div class="cs-ico" style="background:{s['grad']};">{s['icon']}</div>
              <div>
                <small>✨ خدمة مقترحة لك</small>
                <h4>{s['name']}</h4>
                <p>{s['tagline']}</p>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([2, 1])
    with c2:
        if st.button(f"جرّبها الآن {s['icon']}", key=f"cross_{sid}", use_container_width=True):
            goto(("service", r))


# ============================================================
# 9) أقسام الصفحة الرئيسية (ECO System)
# ============================================================
def render_hero():
    st.markdown(
        """
        <div class="hero">
          <h2>بوابتك إلى <span class="grad">طاقة الكون</span> ومعرفة الذات</h2>
          <p>منصة عربية متكاملة تجمع التاروت، الأبراج، الخريطة الفلكية، تفسير الأحلام، الكرمة،
          أحجار الطاقة، والأرقام الروحية في تجربة واحدة سلسة وتفاعلية. اختر خدمتك وابدأ رحلتك الآن.</p>
          <div class="pills">
            <span class="pill">🃏 تاروت ذكي</span><span class="pill">🗺️ خريطة 12 بيتاً</span>
            <span class="pill">🌙 تفسير الأحلام</span><span class="pill">💎 أحجار الشاكرات</span>
            <span class="pill">🔢 الرقم الروحي</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🚀 ابدأ رحلتك الكونية", key="hero_start", use_container_width=True):
            goto(("cat", "identity"))
    with c2:
        if st.button("🃏 اسحب تاروت الآن", key="hero_tarot", use_container_width=True):
            goto(("service", 4))


def render_stats_strip():
    stats = st.session_state.reading_stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔮 إجمالي القراءات", stats["total_readings"])
    if stats["most_drawn_cards"]:
        top = max(stats["most_drawn_cards"], key=stats["most_drawn_cards"].get)
        c2.metric("🃏 أكثر بطاقة", top[:14], f"{stats['most_drawn_cards'][top]} مرة")
    else:
        c2.metric("🃏 أكثر بطاقة", "—")
    c3.metric("⭐ المفضلات", len(st.session_state.favorites))
    if stats["readings_by_type"]:
        tt = max(stats["readings_by_type"], key=stats["readings_by_type"].get)
        c4.metric("🔑 أكثر نوع", tt[:12], stats["readings_by_type"][tt])
    else:
        c4.metric("🔑 أكثر نوع", "—")


def render_ecosystem_extras():
    # نصيحة اليوم + حدث فلكي
    section_title("نبض الكون اليوم", "نصيحة يومية وأحداث فلكية تتجدد تلقائياً")
    insight = get_daily_insight()
    st.markdown(f'<div class="info-banner">💡 نصيحة اليوم: {insight}</div>', unsafe_allow_html=True)
    today_event = get_cosmic_events_today()
    if today_event:
        st.markdown(
            f"""<div class="glass" style="text-align:center;">
            <h4 style="color:var(--gold); margin:0;">🌟 حدث اليوم: {today_event['event']}</h4>
            <p style="color:var(--cyan); margin-top:8px;">{today_event['meaning']}</p></div>""",
            unsafe_allow_html=True,
        )

    # التوصيات الذكية
    section_title("توصيات ذكية لرحلتك", "تتكيّف مع تاريخ استخدامك للمنصة")
    recs = get_ai_recommendations()
    rcols = st.columns(len(recs))
    for i, rec in enumerate(recs):
        with rcols[i]:
            st.markdown(
                f'<div class="glass" style="text-align:center; min-height:96px;">'
                f'<p style="color:var(--gold); margin:0; font-size:.92rem;">{rec}</p></div>',
                unsafe_allow_html=True,
            )

    # لوحتي: السجل + المفضلات + الإحصائيات
    section_title("لوحتي الشخصية", "سجلّك ومفضلاتك وإحصائياتك في مكان واحد")
    t1, t2, t3 = st.tabs(["🔮 القراءات السابقة", "⭐ المفضلات", "📊 الإحصائيات"])
    with t1:
        if st.session_state.reading_history:
            for idx, entry in enumerate(st.session_state.reading_history[-5:][::-1]):
                cc1, cc2 = st.columns([4, 1])
                with cc1:
                    st.markdown(
                        f"""<div class="history-box"><b>📅 {entry['date']} — {entry['timestamp'].split()[1]}</b><br>
                        <b>النوع:</b> {entry['type']}<br><b>النتيجة:</b> {entry['result'][:90]}...</div>""",
                        unsafe_allow_html=True,
                    )
                with cc2:
                    if st.button("❤️", key=f"home_fav_{idx}"):
                        add_to_favorites(entry)
                        st.success("أضيفت للمفضلات!")
            if st.button("🗑️ حذف السجل بالكامل", key="home_clear_hist"):
                st.session_state.reading_history = []
                st.rerun()
        else:
            st.info("📭 لا توجد قراءات سابقة بعد — ابدأ خدمتك الأولى!")
    with t2:
        if st.session_state.favorites:
            for idx, fav in enumerate(st.session_state.favorites[::-1]):
                cc1, cc2 = st.columns([4, 1])
                with cc1:
                    st.markdown(
                        f"""<div class="history-box"><b>⭐ {fav['date']} — {fav['timestamp'].split()[1]}</b><br>
                        <b>النوع:</b> {fav['type']}<br><b>النتيجة:</b> {fav['result'][:90]}...</div>""",
                        unsafe_allow_html=True,
                    )
                with cc2:
                    if st.button("🗑️", key=f"home_del_fav_{idx}"):
                        remove_from_favorites(len(st.session_state.favorites) - 1 - idx)
                        st.rerun()
        else:
            st.info("📄 لم تحفظ أي مفضلات بعد — اضغط ❤️ بجانب أي قراءة.")
    with t3:
        stats = st.session_state.reading_stats
        if stats["readings_by_type"]:
            d = stats["readings_by_type"]
            fig = go.Figure(data=[go.Pie(labels=list(d.keys()), values=list(d.values()),
                                         marker=dict(colors=['#ff79c6', '#bb86fc', '#00e6c3', '#ffd54a',
                                                             '#ff6b9d', '#7f5af0', '#46c8ff', '#d945ef', '#74c7ec']))])
            fig.update_layout(title="توزيع أنواع القراءات", template="plotly_dark",
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffd54a"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📚 لا توجد إحصائيات بعد — جرّب بعض الخدمات أولاً.")


def render_subscription():
    section_title("نظام الاشتراكات", "ابدأ مجاناً وارتقِ متى شئت")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """<div class="glass" style="text-align:center; border-color:rgba(0,230,195,.4);">
            <h4 style="color:var(--cyan); margin-top:0;">📱 الخطة المجانية</h4>
            <p style="font-size:30px; color:var(--gold); margin:8px 0;">مجاني</p>
            <ul style="text-align:right; color:#e9e0ff; font-size:.9rem; line-height:1.9;">
              <li>✅ كل الخدمات الأساسية التسع</li><li>✅ السجل والمفضلات</li>
              <li>✅ التوصيات الذكية</li><li>❌ تقارير PDF مفصّلة</li></ul></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        prem = st.checkbox("🔓 تفعيل الخطة المميّزة (تجريبي)", key="premium_toggle", value=st.session_state.is_premium)
        st.session_state.is_premium = prem
        st.markdown(
            f"""<div class="glass" style="text-align:center; border-color:rgba(255,213,74,.45);">
            <h4 style="color:var(--gold); margin-top:0;">👑 الخطة المميّزة {'✅' if prem else ''}</h4>
            <p style="font-size:26px; color:var(--mag); margin:8px 0;">مميّز 🌟</p>
            <ul style="text-align:right; color:#e9e0ff; font-size:.9rem; line-height:1.9;">
              <li>✅ كل ميزات المجانية</li><li>✅ مقارنات متقدمة موسّعة</li>
              <li>✅ تقارير وتحليلات أعمق</li><li>✅ رسائل يومية مخصّصة</li></ul></div>""",
            unsafe_allow_html=True,
        )


def render_home():
    render_hero()
    render_stats_strip()
    section_title("استكشف الخدمات حسب الفئة", "كل خدمة مرتبطة بأخواتها — تنقّل بسلاسة بين العوالم")
    for ck in CATEGORIES:
        render_category_section(ck)
    render_ecosystem_extras()
    render_subscription()


# ============================================================
# 10) صفحات الفئة والخدمة
# ============================================================
def render_category_page(cat_key):
    if st.button("← العودة للرئيسية", key="cat_back", type="secondary"):
        goto("home")
    render_category_section(cat_key)
    # اقتراح فئات أخرى للتنقّل (ECO)
    section_title("فئات أخرى قد تهمّك")
    others = [k for k in CATEGORIES if k != cat_key]
    ocols = st.columns(len(others))
    for i, k in enumerate(others):
        cat = CATEGORIES[k]
        with ocols[i]:
            st.markdown(
                f"""<div class="glass" style="text-align:center;">
                <div style="font-size:34px;">{cat['icon']}</div>
                <h4 style="margin:6px 0;">{cat['name']}</h4>
                <p style="color:var(--muted); font-size:.85rem; min-height:48px;">{cat['desc']}</p></div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"تصفّح {cat['name']}", key=f"goto_cat_{k}", use_container_width=True):
                goto(("cat", k))


def render_service_page(sid):
    s = SERVICES[sid]
    cat = CATEGORIES[s["cat"]]
    # شريط التنقّل (Breadcrumb)
    bc1, bc2 = st.columns([1, 1])
    with bc1:
        if st.button("← الرئيسية", key="svc_back_home", type="secondary"):
            goto("home")
    with bc2:
        if st.button(f"← {cat['icon']} {cat['name']}", key="svc_back_cat", type="secondary"):
            goto(("cat", s["cat"]))

    st.markdown(
        f"""<div class="cat-head" style="background:linear-gradient(120deg, rgba(20,11,44,.85), rgba(10,5,26,.6)), {s['grad']};">
        <div class="ico" style="background:rgba(0,0,0,.25);">{s['icon']}</div>
        <div><h3>{s['name']}</h3><p>{s['tagline']}</p></div></div>""",
        unsafe_allow_html=True,
    )

    # بوابة الإعلان — تفتح الخدمة بعد 30 ثانية
    if not ad_gate(sid):
        return

    # محتوى الخدمة الفعلي (من services.py)
    s["render"]()

    # كرت ترويج متبادل داخل الخدمة
    cross_sell(sid)


# ============================================================
# 11) الراوتر الرئيسي
# ============================================================
render_header()

view = st.session_state.view
if view == "home":
    render_home()
elif isinstance(view, tuple) and view[0] == "cat":
    render_category_page(view[1])
elif isinstance(view, tuple) and view[0] == "service":
    render_service_page(view[1])
else:
    render_home()

render_footer()
