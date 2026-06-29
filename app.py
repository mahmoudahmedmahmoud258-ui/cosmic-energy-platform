import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from html import escape
from urllib.parse import quote
import random
import os
import base64
import json

# 1. إعدادات الصفحة العامة للمنصة ذات الطابع الفلكي الاحترافي
st.set_page_config(
    page_title="منصة الطاقة الكونية الشاملة - Cosmic Energy Platform",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# دالة مخصصة لحقن الخلفية الفلكية الجديدة باستخدام الـ CSS
def set_cosmic_background():
    st.markdown(
        """
        <style>
        /* استهداف الحاوية الرئيسية للتطبيق وتغيير خلفيتها */
        .stApp {
            background-image: url("https://wallup.net/wp-content/uploads/2017/11/23/518646-Funerium-space-3D-galaxy-stars-colorful.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            background-attachment: fixed;
        }
        
        /* إضفاء لمسة زجاجية شفافة وناعمة على الأزرار والتبويبات لتندمج مع النجوم */
        .stButton>button, .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(15, 10, 34, 0.65) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# استدعاء الدالة لتفعيل الخلفية فوراً
set_cosmic_background()

# تصميم CSS متقدم يمنح الموقع مظهراً فلكياً غامضاً ومناسباً جداً للبث المباشر
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    html, body, [class*="css"], .stText, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Cairo', sans-serif !important;
        text-align: right;
        direction: rtl;
        color: #f3ebff;
    }
    body {
        min-height: 100vh;
        background: radial-gradient(circle at top center, rgba(123, 69, 255, 0.12), transparent 22%),
                    radial-gradient(circle at 15% 20%, rgba(255, 255, 255, 0.12), transparent 12%),
                    linear-gradient(180deg, #09030f 0%, #100520 40%, #150d33 100%);
        background-attachment: fixed;
    }
    body::before {
        content: "";
        position: fixed;
        inset: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px) 0 0 / 40px 40px;
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
    }
    .main, .block-container {
        background: rgba(8, 4, 20, 0.82) !important;
        box-shadow: 0 25px 90px rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 28px;
        padding: 28px 28px 18px !important;
        backdrop-filter: blur(18px);
        position: relative;
        z-index: 1;
    }
    .hero-section {
        background: rgba(34, 16, 61, 0.85);
        border: 1px solid rgba(187, 134, 252, 0.2);
        border-radius: 28px;
        padding: 32px 24px;
        margin-bottom: 20px;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.35);
    }
    .hero-section h1 {
        font-size: clamp(2rem, 4vw, 4rem);
        letter-spacing: 1.6px;
        margin-bottom: 10px;
        text-shadow: 0 0 28px rgba(187, 134, 252, 0.35);
    }
    .hero-section p {
        color: #f8f3ff;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .section-title {
        display: inline-block;
        background: rgba(154, 97, 255, 0.14);
        border: 1px solid rgba(187, 134, 252, 0.22);
        border-radius: 16px;
        padding: 12px 18px;
        color: #f7ebff;
        margin-bottom: 18px;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
        font-weight: 700;
    }
    .result-box {
        background: rgba(20, 11, 44, 0.72);
        border: 1px solid rgba(255, 121, 198, 0.2);
        border-radius: 24px;
        padding: 34px;
        margin-top: 26px;
        box-shadow: 0 22px 60px rgba(95, 41, 178, 0.18);
        backdrop-filter: blur(14px);
        position: relative;
        overflow: hidden;
    }
    .result-box::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(255, 121, 198, 0.08), transparent 20%),
                    radial-gradient(circle at bottom left, rgba(0, 255, 204, 0.06), transparent 15%);
        pointer-events: none;
    }
    .result-box * {
        position: relative;
        z-index: 1;
    }
    .tarot-card-visual {
        background: linear-gradient(145deg, rgba(29,17,83,0.96), rgba(8,2,24,0.98));
        border: 4px double rgba(255, 205, 72, 0.35);
        border-radius: 28px;
        padding: 36px 28px;
        margin: 28px auto;
        width: 390px;
        max-width: 100%;
        min-height: 560px;
        box-shadow: 0 0 70px rgba(255, 196, 45, 0.28), inset 0 0 30px rgba(145, 88, 255, 0.18);
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        position: relative;
        overflow: visible;
    }
    .tarot-card-visual img {
        width: 100%;
        max-width: 360px;
        height: auto;
        margin: 0 auto;
        border-radius: 22px;
    }
    .tarot-card-visual::before {
        content: "";
        position: absolute;
        top: 16px;
        bottom: 16px;
        left: 16px;
        right: 16px;
        border: 1px dashed rgba(255, 215, 110, 0.16);
        border-radius: 18px;
        pointer-events: none;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff79c6 0%, #bb86fc 100%) !important;
        color: #090819 !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 14px 30px !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        width: 100%;
        box-shadow: 0 8px 30px rgba(187, 134, 252, 0.22);
    }
    .stButton>button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(255, 121, 198, 0.45);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        background-color: rgba(13, 8, 31, 0.7);
        padding: 12px;
        border-radius: 18px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(20, 11, 44, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        color: #d7c6ff !important;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #bb86fc 0%, #ff79c6 100%) !important;
        color: #05020c !important;
        border: none !important;
        box-shadow: 0 12px 30px rgba(255, 121, 198, 0.18);
    }
    .stTabs [aria-selected="true"] span {
        font-weight: 800 !important;
    }
    .stMetric {
        background: rgba(14, 7, 25, 0.86) !important;
        border-radius: 22px !important;
        padding: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.02);
    }
    div[data-testid="stRadio"] label {
        color: #99ffe0 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    .stSelectbox>div>div>div {
        background: rgba(16, 11, 32, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        color: #f5f1ff !important;
    }
    .stTextInput>div>input,
    .stTextArea>div>textarea,
    .stNumberInput>div>input {
        background: rgba(16, 11, 32, 0.92) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #fdf7ff !important;
        border-radius: 16px !important;
        padding: 12px !important;
    }
    .stTextInput>div>input:focus,
    .stTextArea>div>textarea:focus,
    .stNumberInput>div>input:focus {
        box-shadow: 0 0 0 2px rgba(187, 134, 252, 0.25);
        outline: none !important;
    }
    .info-banner {
        background: linear-gradient(90deg, rgba(218, 27, 96, 0.9) 0%, rgba(255, 176, 0, 0.95) 100%);
        color: #ffffff;
        padding: 16px 18px;
        border-radius: 18px;
        text-align: center;
        font-weight: 800;
        margin-bottom: 28px;
        font-size: 1rem;
        box-shadow: 0 12px 30px rgba(255, 176, 0, 0.2);
    }
    .history-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px dotted rgba(255, 215, 0, 0.25);
        border-radius: 18px;
        padding: 18px;
        margin: 14px 0;
        font-size: 0.98rem;
    }
    .error-message,
    .success-message {
        border-radius: 14px;
        margin: 12px 0;
        padding: 16px;
    }
    .error-message {
        background: rgba(255, 58, 106, 0.15);
        border-right: 4px solid #ff5065;
    }
    .success-message {
        background: rgba(0, 255, 204, 0.12);
        border-right: 4px solid #00ffd0;
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    body::after {
        content: "";
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(circle at 10% 10%, rgba(255,255,255,0.12), transparent 6%),
            radial-gradient(circle at 30% 20%, rgba(255,255,255,0.08), transparent 5%),
            radial-gradient(circle at 70% 15%, rgba(255,255,255,0.10), transparent 7%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.07), transparent 4%);
        pointer-events: none;
        opacity: 0.35;
        z-index: 0;
    }
    @media (max-width: 768px) {
        .hero-section {
            padding: 24px 18px;
        }
        .result-box {
            padding: 24px;
            margin-top: 18px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px !important;
            font-size: 13px;
        }
    }
</style>
""", unsafe_allow_html=True)

# الجداول الفلكية وحساب الجمل
abjad_table = {
    'أ': 1, 'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ى': 10, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700,
    'ض': 800, 'ظ': 900, 'غ': 1000, 'ة': 5, 'ؤ': 6, 'ئ': 10, 'ء': 1
}

# === دوال مساعدة جديدة ===
# قائمة النصائح اليومية
daily_insights = [
    "الطاقة تدعم اليوم الإنجازات الكبرى - استثمر وقتك فيما يهمك حقاً",
    "اليوم يوم مثالي للتأمل والتفكير العميق في مسار حياتك",
    "الكون يرسل إشارات للتغيير - كن مستعداً للفرص الجديدة",
    "اجعل قلبك مفتوحاً للحب والعطاء اليوم، الطاقة مواتية",
    "الحدس قوي اليوم - اثق بما تشعر به في أعماق روحك",
    "يوم عظيم للشراكات والتعاون - تواصل مع من تحب",
    "التحديات اليوم فرص ذهبية للنمو والتطور",
    "الطاقة تدعم الشفاء - اعتن بنفسك عاطفياً وجسدياً",
    "اليوم يوم قوة - استخدم إرادتك لتحقيق أهدافك",
    "الكون في جانبك - اتخذ الخطوات التي كنت تخشاها",
    "الراحة والسلام ينتظرانك - أعطِ نفسك فرصة للاسترخاء",
    "يوم الإبداع والابتكار - اترك العنان لخيالك",
    "الطاقة تدعم النجاح المالي - افتح الأبواب للوفرة",
    "اليوم مناسب للمسامحة والتحرر من الأحقاد",
    "الكون يدعوك لحياة أكثر صدقاً مع نفسك",
    "استقبل هذا اليوم بامتنان - كل شيء في مكانه الصحيح",
    "الطاقة تدعم الحب والعلاقات - أظهر مشاعرك",
    "يوم عظيم للتعلم والاستكشاف - طور نفسك",
    "الكون يحضر لك مفاجآت إيجابية - كن جاهزاً",
    "اليوم يوم التحول - اترك القديم وابدأ الجديد"
]

def init_session_state():
    """تهيئة حالة الجلسة لحفظ البيانات"""
    if 'reading_history' not in st.session_state:
        st.session_state.reading_history = []
    if 'last_tarot_card' not in st.session_state:
        st.session_state.last_tarot_card = None
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'dark'
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'reading_stats' not in st.session_state:
        st.session_state.reading_stats = {
            'total_readings': 0,
            'readings_by_type': {},
            'most_drawn_cards': {},
            'most_searched_names': {}
        }
    if 'tarot_rating' not in st.session_state:
        st.session_state.tarot_rating = 3

def validate_arabic_name(name):
    """التحقق من أن الاسم يحتوي على أحرف عربية فقط (مع المسافات والشرطات)"""
    if not name or not name.strip():
        return False, "الاسم فارغ!"
    
    # تنظيف الاسم
    name = name.strip()
    
    # السماح بالأحرف العربية والمسافات والشرطات فقط
    import re
    if not re.match(r'^[\u0600-\u06FF\s\-]+$', name):
        return False, "⚠️ الاسم يجب أن يحتوي على أحرف عربية فقط (بدون أرقام أو علامات خاصة)"
    
    return True, name.strip()

def validate_date(date_obj, min_year=1950):
    """التحقق من صحة التاريخ"""
    if date_obj.year < min_year:
        return False, f"⚠️ التاريخ يجب أن يكون بعد سنة {min_year}"
    if date_obj > datetime.now().date():
        return False, "⚠️ التاريخ لا يمكن أن يكون في المستقبل"
    return True, "صحيح"

def save_to_history(reading_type, result, user_input=""):
    """حفظ القراءة في السجل"""
    init_session_state()
    reading_entry = {
        "type": reading_type,
        "result": result,
        "input": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%d/%m/%Y")
    }
    st.session_state.reading_history.append(reading_entry)

def get_random_variation(base_message):
    """إضافة تنويع للرسائل"""
    variations = [
        f"✨ {base_message}",
        f"🌟 {base_message}",
        f"💫 {base_message}",
        f"🔮 {base_message}"
    ]
    return random.choice(variations)


def generate_karma_reading(name):
    """إنشاء قراءة كرمة ذكية ومتغيرة حتى مع نفس الاسم"""
    clean = name.strip()
    total = sum(abjad_table.get(c, 0) for c in clean)
    seed = f"{clean}|{datetime.now().strftime('%Y%m%d%H%M%S')}"
    rnd = random.Random(seed)

    base_index = (total % 7) + 1
    extra = rnd.randint(0, 2)
    k_score = ((base_index + extra - 1) % 7) + 1

    debt_scale = rnd.randint(1, 5)
    debt_states = {
        1: "رصيد طاقي نقي وخفيف؛ فرص المصالحة والتنظيف متاحة بسهولة.",
        2: "دين طاقي معتدل؛ ينصح بالتركيز على نية الشفاء الداخلي ومسامحة الذات.",
        3: "دين طاقي واضح؛ يحتاج إلى خطوات صغيرة متسقة للتوازن وإطلاق الأوهام القديمة.",
        4: "دين طاقي نشط؛ اوقف الاستنزاف وابدأ بتصفية العلاقات والالتزامات الثقيلة.",
        5: "دين طاقي عميق؛ هناك شحنات قديمة تنتظر فصلها، وعمل الظل مطلوب بصدق شديد."
    }

    karma_labels = {
        1: "كرمة منيرة وميسرة",
        2: "كرمة متحولة ومبشرة",
        3: "كرمة متجددة وداعمة",
        4: "كرمة متوازنة ومحفزة",
        5: "كرمة مهنية وروحية",
        6: "كرمة متكاملة ومنسجمة",
        7: "كرمة كونية متفردة"
    }

    karma_comments = [
        "اليوم يحمل لك رسالة عن تدفق طاقات نظيفة ونداء للعطاء بلا انتظار.",
        "الكون يطلب منك أن تكتشف جذور رغباتك وأن تنقح نواياك لتتلاءم مع هويتك الحقيقية.",
        "تقاربك مع الأشخاص من حولك يعيد ترتيب رصيدك الطاقي بطرق غير مرئية لكنه فاعل.",
        "التركيز على الشكر والثقة سيزيد من انفتاحك لتلقي دعم غير متوقع.",
        "هذه القراءة تنبهك إلى أن دين الطاقة يمكن أن يتحول إلى فرصة إذا أخذت خطوة شجاعة اليوم."
    ]

    karma_message = rnd.choice(karma_comments)
    debt_message = debt_states[debt_scale]
    karma_label = karma_labels[k_score]

    if k_score == 7:
        karma_message = "الطاقة الكونية ترد لك الجميل؛ هذه اللحظة تحمل لك إمكانية تحويل الدين إلى بركة." 
    elif k_score == 1:
        karma_message = "قراءة خفيفة ومشرقة؛ اترك الأوزان القديمة واسمح للكرمة البيضاء بالتجدد." 

    return k_score, karma_label, debt_message, karma_message


def generate_tarot_insight(card, intention="", context=""):
    """إنشاء رسالة ونصيحة طويلة ومتغيرة لقراءة التاروت."""
    seed = f"{card['name']}|{intention}|{context}|{datetime.now().strftime('%Y%m%d%H')}"
    rnd = random.Random(seed)
    prefixes = [
        "الكون يهمس بأن ",
        "الطاقة الكونية تؤكد أن ",
        "رسالة اليوم تقول إن ",
        "الزمرة الروحية تشير إلى أن "
    ]
    suffixes = [
        " وهذه الرسالة تحمل في طياتها طاقة جديدة.",
        " فاستقبلها بقلب مفتوح وعقل صافي.",
        " ويمكن أن تتحول هذه الرؤية إلى خطوة واضحة إذا انتبهت لها.",
        " لأنه حين تغلق الباب عن الماضي، يتفتح لك باب آخر."
    ]
    tarot_message = f"{rnd.choice(prefixes)}{card['message']}{rnd.choice(suffixes)}"

    core_advice = card.get('advice', 'اسمع ما يقول لك قلبك')
    advice_lines = [
        f"الآن هو وقت {rnd.choice(['الوضوح', 'التحول', 'التركيز', 'التوازن'])} لخطوتك التالية.",
        f"احترس من {rnd.choice(['التردد', 'الإفراط في التحليل', 'الهروب من المسؤولية', 'تجاهل الحدس'])}؛ فهو قد يبطئ تقدّمك.",
        f"الطاقة تدعوك لتقبل الحقيقة كما هي والعمل بجرأة محسوبة، فهذا يجعل لكل قرار أثر أعمق.",
    ]
    if context.strip():
        advice_lines.append(f"سياقك الحالي يشير إلى: {context.strip()[:90]}... ولذلك يحتاج انتباهك.")
    advice = "<br>".join(advice_lines[:3])
    return tarot_message, advice


def calculate_name_compatibility(name1, name2):
    """حساب توافق رقمي ذكي متغير بناءً على طاقة الأسماء."""
    clean1 = name1.strip()
    clean2 = name2.strip()
    score1 = sum(abjad_table.get(c, 0) for c in clean1)
    score2 = sum(abjad_table.get(c, 0) for c in clean2)
    common_letters = len(set(clean1) & set(clean2))
    same_name = clean1 == clean2

    base = ((score1 + score2) % 50) + 50
    length_bonus = min(12, (len(clean1) + len(clean2)) // 2)
    common_bonus = min(10, common_letters * 2)
    repetition_penalty = min(8, abs(score1 - score2) % 12)
    variation_seed = f"{clean1}|{clean2}|{datetime.now().strftime('%Y%m%d%H') }"
    randomizer = random.Random(variation_seed)
    dynamic_offset = randomizer.randint(-5, 5)

    percent = max(62, min(99, base + length_bonus + common_bonus - repetition_penalty + dynamic_offset))

    if same_name:
        percent = max(70, min(99, percent + 3))

    if percent >= 92:
        advice = "نسبة التوافق مرتفعة جداً؛ الأسماء تنصهر في نسيج طاقة واحد ويولد رابط عميق من أول نظرة." 
    elif percent >= 82:
        advice = "هناك انسجام قوي في الأحرف والنغمات، ويُظهر هذا الرباط قدرة كبيرة على التواصل والعطاء المتبادل."
    elif percent >= 72:
        advice = "التوافق جيد، لكنه يحتاج إلى وعي وحرية للتطور. حافظ على الانفتاح وعبّر عن نيتك بوضوح."
    else:
        advice = "التوافق يحتاج للعمل المشترك. استخدم هذا الرابط للتعلم من بعضكما البعض وبناء توازن ذهني وروحي." 

    if same_name:
        advice = "حتى لو الاسم نفسه يتكرر، تتغير طاقتكما مع كل يوم، مما يمنح العلاقة رسائل جديدة وديناميكية متجددة." 

    title = "قالب طاقة الاسم المتغير"
    if same_name:
        title = "انعكاس طاقة نفس الاسم"

    return percent, title, advice


def get_zodiac_compatibility(z1, z2):
    """حساب توافق أبراج ذكي متغير يقدم نسبة ونصيحة مختلفة."""
    elem1 = zodiacs[z1]["عنصر"]
    elem2 = zodiacs[z2]["عنصر"]
    idx = list(zodiacs.keys())
    pos1 = idx.index(z1)
    pos2 = idx.index(z2)
    diff = abs(pos1 - pos2)
    if diff > 6:
        diff = 12 - diff

    if elem1 == elem2:
        base = 88
        relation = "توأم طاقة متجانسة"
    elif ("ناري" in elem1 and "هوائي" in elem2) or ("هوائي" in elem1 and "ناري" in elem2):
        base = 84
        relation = "نار وهواء: إشعال حماسي متدفق"
    elif ("ترابي" in elem1 and "مائي" in elem2) or ("مائي" in elem1 and "ترابي" in elem2):
        base = 82
        relation = "تراب وماء: تأسيس مستقر ومتوازن"
    elif ("ترابي" in elem1 and "هوائي" in elem2) or ("هوائي" in elem1 and "ترابي" in elem2):
        base = 72
        relation = "هواء وتراب: تحديات عقلية تتطلب صبرًا وحكمة"
    elif ("ناري" in elem1 and "مائي" in elem2) or ("مائي" in elem1 and "ناري" in elem2):
        base = 74
        relation = "نار وماء: شغف وعاطفة تحتاج إلى تناغم داخلي"
    else:
        base = 78
        relation = "تفاعل كوني متنوع"

    if diff == 0:
        base += 6
        relation = "مرآة نفسية قوية"
    elif diff == 6:
        base += 4
        relation = "توازن الأضداد الكونية"
    elif diff == 2 or diff == 4:
        base += 3
        relation = "توافق منزلي متطور"

    variation_seed = f"{z1}|{z2}|{datetime.now().strftime('%Y%m%d%H%M')}"
    randomizer = random.Random(variation_seed)
    dynamic_offset = randomizer.randint(-6, 6)
    percent = max(65, min(98, base + dynamic_offset))

    if percent >= 92:
        rel_type = "توافق فلكي متميز ومتفرد 🌠"
        rel_desc = f"{z1} و{z2} يحملان ديناميكيات طاقة متناغمة جداً؛ علاقة قادرة على توليد الكثير من الإبداع والدعم المتبادل."
    elif percent >= 82:
        rel_type = "انسجام فلكي داعم 🌙"
        rel_desc = f"{z1} و{z2} يشكلان رابطاً جيداً، مع فرص لتكامل القدرات والطاقة الذهنية والعاطفية إذا وُجهت بنية صافية."
    else:
        rel_type = "تحدي فلكي محفز ⚖️"
        rel_desc = f"{z1} و{z2} يمتلكان طاقة متعددة المعاني؛ يحتاج هذا الثنائي إلى وعي وتأمل لتحقيق التوازن والتحول الإيجابي."

    rel_desc += f"\n✨ العنصران: {elem1} مقابل {elem2}."
    return percent, rel_type, rel_desc


def get_daily_insight():
    """الحصول على نصيحة يومية بناءً على التاريخ"""
    today = datetime.now().day
    return daily_insights[today % len(daily_insights)]

def add_to_favorites(reading_entry):
    """إضافة قراءة للمفضلات"""
    init_session_state()
    reading_entry['saved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.favorites.append(reading_entry)

def remove_from_favorites(index):
    """إزالة قراءة من المفضلات"""
    if 0 <= index < len(st.session_state.favorites):
        st.session_state.favorites.pop(index)

def update_reading_stats(reading_type, user_input="", card_name=""):
    """تحديث إحصائيات القراءات"""
    init_session_state()
    stats = st.session_state.reading_stats
    stats['total_readings'] += 1
    stats['readings_by_type'][reading_type] = stats['readings_by_type'].get(reading_type, 0) + 1
    if card_name:
        stats['most_drawn_cards'][card_name] = stats['most_drawn_cards'].get(card_name, 0) + 1
    if user_input:
        stats['most_searched_names'][user_input] = stats['most_searched_names'].get(user_input, 0) + 1

# ===== الدوال الجديدة للميزات الإضافية =====

def get_ai_recommendations():
    """توصيات ذكية بناءً على تاريخ القراءات"""
    init_session_state()
    stats = st.session_state.reading_stats
    
    recommendations = []
    
    if stats['total_readings'] == 0:
        return ["🌟 ابدأ رحلتك الفلكية الآن - كل قراءة أولى تفتح أبواباً جديدة"]
    
    if stats['readings_by_type'].get('قراءة تاروت', 0) > 10:
        recommendations.append("🔮 أنت قارئ تاروت محنك - حاول نقل هذه الطاقة للآخرين")
    
    if stats['readings_by_type'].get('توافق رقمي', 0) > 5:
        recommendations.append("💖 أسئلة العلاقات تهمك - اثق بطاقات الحب في حياتك")
    
    if stats['total_readings'] > 20:
        recommendations.append("🌙 أنت مكرس للمسار الروحي - استثمر في تطورك الداخلي أكثر")
    
    if len(stats['most_searched_names']) > 5:
        recommendations.append("👥 أسماء متعددة تهمك - ركز على علاقاتك الأساسية")
    
    return recommendations if recommendations else ["✨ تابع قراءاتك - الحكمة تأتي مع التكرار"]

def get_cosmic_background():
    """خلفيات كونية متغيرة بناءً على الوقت"""
    hour = datetime.now().hour
    
    if 6 <= hour < 12:
        return "#140d33"
    elif 12 <= hour < 18:
        return "#1a0f3a"
    elif 18 <= hour < 21:
        return "#0f0820"
    else:
        return "#050314"

def save_feedback(reading_type, rating, comment=""):
    """حفظ تقييمات المستخدمين"""
    init_session_state()
    if 'feedback_data' not in st.session_state:
        st.session_state.feedback_data = []
    
    feedback_entry = {
        "type": reading_type,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.feedback_data.append(feedback_entry)

def get_zodiac_from_date(month, day):
    """حساب البرج من التاريخ بحسابات فلكية دقيقة"""
    zodiacs_dates = [
        (1, 20, "الجدي"), (2, 19, "الدلو"), (3, 21, "الحوت"),
        (4, 20, "الحمل"), (5, 21, "الثور"), (6, 21, "الجوزاء"),
        (7, 23, "السرطان"), (8, 23, "الأسد"), (9, 23, "العذراء"),
        (10, 23, "الميزان"), (11, 22, "العقرب"), (12, 22, "القوس")
    ]
    
    for start_month, start_day, zodiac in zodiacs_dates:
        if month == start_month and day >= start_day:
            return zodiac
        elif month == start_month + 1 and day < start_day:
            return zodiac
    
    return "الجدي"

def activate_premium():
    """تفعيل الاشتراك المميز"""
    if 'is_premium' not in st.session_state:
        st.session_state.is_premium = False
    return st.session_state.is_premium

def get_cosmic_events_today():
    """الحصول على الأحداث الفلكية اليوم"""
    cosmic_events = {
        "29-01": {"event": "🌙 قمر دم كامل", "meaning": "نقطة عطل روحية - وقت للتحولات"},
        "09-02": {"event": "☀️ كسوف شمسي جزئي", "meaning": "بداية جديدة وفرص غير متوقعة"},
        "27-03": {"event": "🪐 اقتران الزهرة والمريخ", "meaning": "طاقة قوية للحب والجاذبية"},
        "15-04": {"event": "🌙 قمر دم كامل", "meaning": "إضاءة الحقائق المخفية"},
        "20-05": {"event": "☀️ موسم الجوزاء", "meaning": "التواصل والحركة والتغيير"},
        "21-06": {"event": "☀️ انقلاب صيفي", "meaning": "نقطة القوة القصوى للسنة"},
        "04-07": {"event": "🪐 عطارد مستقيم", "meaning": "وضوح الرسائل والتفاهم"},
        "15-08": {"event": "🌙 قمر كامل", "meaning": "تحقيق الرغبات والأمنيات"},
        "22-09": {"event": "☀️ انقلاب خريفي", "meaning": "توازن وعدالة وحكمة"},
        "21-12": {"event": "☀️ انقلاب شتوي", "meaning": "تجديد وحيوية نقطة البداية"}
    }
    
    today = datetime.now().strftime("%d-%m")
    return cosmic_events.get(today, None)

def create_birth_chart(birth_name, birth_date, birth_place, birth_time, chart_type="monthly"):
    """رسم خريطة فلكية حقيقية مع 12 بيت"""
    # بيانات الأبراج الـ 12
    zodiacs_order = ["الحمل", "الثور", "الجوزاء", "السرطان", "الأسد", "العذراء", 
                     "الميزان", "العقرب", "القوس", "الجدي", "الدلو", "الحوت"]
    
    # الكواكب (مع رموز)
    planets = ["الشمس ☀️", "القمر 🌙", "عطارد 🧠", "الزهرة 💖", "المريخ 🛑", 
               "المشتري ✨", "زحل 🪐", "أورانوس 🌌", "نبتون 🌊", "بلوتو 🖤"]
    
    # حساب الموضع الكوني
    name_val = sum(abjad_table.get(c, 0) for c in birth_name.strip())
    place_val = sum(abjad_table.get(c, 0) for c in birth_place.strip())
    date_val = sum(int(d) for d in birth_date.strftime("%Y%m%d"))
    time_val = birth_time.hour + birth_time.minute
    
    cosmic_seed = (name_val + place_val + date_val + time_val) % 360
    
    # إنشاء الشكل البياني
    fig = go.Figure()
    
    # رسم دائرة خارجية (البيوت الـ 12)
    angles_outer = np.linspace(0, 360, 13)
    fig.add_trace(go.Scatterpolar(
        r=[10]*13, theta=angles_outer,
        mode='lines', line=dict(color='#ffd700', width=3),
        showlegend=False, name='البيوت الخارجية'
    ))
    
    # رسم البيوت الـ 12
    for i in range(12):
        angle_start = i * 30
        angle_end = (i + 1) * 30
        angle_mid = (angle_start + angle_end) / 2
        
        # خطوط البيوت
        fig.add_trace(go.Scatterpolar(
            r=[0, 10], theta=[angle_start, angle_start],
            mode='lines', line=dict(color='#bb86fc', width=2, dash='dot'),
            showlegend=False
        ))
        
        # أرقام البيوت
        fig.add_trace(go.Scatterpolar(
            r=[11.5], theta=[angle_mid],
            mode='text', text=[f"البيت {i+1}"],
            textfont=dict(size=11, color='#00ffcc', family="Cairo"),
            showlegend=False
        ))
        
        # اسم البرج
        zodiac_name = zodiacs_order[(i + (cosmic_seed // 30)) % 12]
        fig.add_trace(go.Scatterpolar(
            r=[8.5], theta=[angle_mid],
            mode='text', text=[zodiac_name],
            textfont=dict(size=13, color='#ffd700', family="Cairo", weight=600),
            showlegend=False
        ))
    
    # إضافة الكواكب داخل الدائرة
    for i, planet in enumerate(planets[:8]):  # أول 8 كواكب
        angle = (cosmic_seed + (i * 45)) % 360
        radius = 3 + (i % 3) * 2
        
        fig.add_trace(go.Scatterpolar(
            r=[radius], theta=[angle],
            mode='markers+text', 
            marker=dict(size=18, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
                                         '#98D8C8', '#F7DC6F', '#BB86FC', '#00ffcc'][i]),
            text=[planet.split()[0]], 
            textfont=dict(size=10, color='white', family="Cairo"),
            textposition='middle center',
            showlegend=False
        ))
    
    # دائرة داخلية (مركز)
    fig.add_trace(go.Scatterpolar(
        r=[0.8]*13, theta=np.linspace(0, 360, 13),
        mode='lines', line=dict(color='#ff79c6', width=2),
        showlegend=False
    ))
    
    # تحديث التخطيط
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(5, 3, 20, 0.3)',
            radialaxis=dict(visible=False, range=[0, 12]),
            angularaxis=dict(visible=False)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=600,
        font=dict(family="Cairo")
    )
    
    return fig, cosmic_seed

def get_house_meanings():
    """معاني البيوت الـ 12"""
    return {
        1: {"name": "البيت الأول - الذات والطالع", "emoji": "👤", "desc": "هويتك الكونية الحقيقية والمظهر الخارجي"},
        2: {"name": "البيت الثاني - المال والوفرة", "emoji": "💰", "desc": "الثروة والمكاسب المالية والموارد"},
        3: {"name": "البيت الثالث - التواصل والذكاء", "emoji": "🧠", "desc": "الاتصالات والتفكير والأخوة والسفر القصير"},
        4: {"name": "البيت الرابع - المنزل والعائلة", "emoji": "🏠", "desc": "الأسرة والجذور والعقل الباطن"},
        5: {"name": "البيت الخامس - الإبداع والحب", "emoji": "💖", "desc": "الحب والإبداع والأطفال والمتعة"},
        6: {"name": "البيت السادس - الصحة والروتين", "emoji": "🏥", "desc": "الصحة والعمل اليومي والخدمة"},
        7: {"name": "البيت السابع - الشراكات والزواج", "emoji": "👰", "desc": "العلاقات والزواج والشراكات المهنية"},
        8: {"name": "البيت الثامن - التحولات والتشافي", "emoji": "🔄", "desc": "التحولات والوراثة والموت والولادة"},
        9: {"name": "البيت التاسع - الوعي والسفر", "emoji": "✈️", "desc": "السفر البعيد والتعليم والروحانيات"},
        10: {"name": "البيت العاشر - المهنة والسلطة", "emoji": "👑", "desc": "المهنة والشهرة والوضع الاجتماعي"},
        11: {"name": "البيت الحادي عشر - الأمنيات والأصدقاء", "emoji": "👥", "desc": "الأمنيات والأصدقاء والجماعات"},
        12: {"name": "البيت الثاني عشر - الخفايا والروحانيات", "emoji": "🌙", "desc": "الخفايا والعقل الباطن والتطهير الروحي"}
    }


def get_house_badge(house_num, chart_type):
    """Return badge text and color for house summary."""
    if house_num in {1, 3, 5, 10}:
        return "فرصة متقدمة", "#ffd54f"
    if house_num in {2, 4, 6, 11}:
        return "تنبيه عملي", "#ff8a65"
    if house_num in {7, 8, 9, 12}:
        return "توجيه روحي", "#8c9eff"
    return "توجيه مهم", "#80cbc4"


def get_chart_key_points(chart_type, cosmic_seed):
    """Generate three key points summary for the chart."""
    point_sets = {
        "monthly": [
            "الطاقة الحالية تدفعك لاتخاذ خطوة حيوية مع وضوح أكبر.",
            "احترس من الفرص السريعة التي تحتاج مراجعة قبل تنفيذها.",
            "التواصل الذكي يمكن أن يعيد توازن العلاقات المهنية."
        ],
        "yearly": [
            "السنة تبشر بتغيير تدريجي في مكانتك المهنية والشخصية.",
            "الاستقرار يأتي من الالتزام بخطوات صغيرة يومية.",
            "التحول الروحي الحقيقي يبدأ بإعادة ترتيب أولوياتك."
        ]
    }
    choices = point_sets.get(chart_type, point_sets["monthly"])
    return [choices[(int(cosmic_seed) + i) % len(choices)] for i in range(3)]


def analyze_psych_shadow(answers, energy_level):
    """تحليل الحالة النفسية وجانب الظل من خلال الإجابات بطريقة أكثر تنوعاً وديناميكية."""
    mapping = {
        "الخوف من النقد أو عدم تقدير مجهوداتي الصادقة من الآخرين": {
            "mental": "متوتر",
            "emotional": "حساس",
            "social": "منعزل قليلاً",
            "shadow": "الناقد الداخلي",
            "core": "احتياج للاستحقاق الذاتي"
        },
        "الشعور بالمسؤولية المفرطة والثقيلة تجاه سعادة وراحة المحيطين بي": {
            "mental": "مثقل",
            "emotional": "مستنزف",
            "social": "مغالي في العطاء",
            "shadow": "المنقذ",
            "core": "حدود غير واضحة مع الآخرين"
        },
        "القلق المستمر من التغيرات المفاجئة أو الخوف من فقدان الأمان المالي والمهني": {
            "mental": "مشتت",
            "emotional": "قلق",
            "social": "متوجس",
            "shadow": "الخائف من الفقدان",
            "core": "حاجة للأمان"
        },
        "أفضل الابتعاد عن المواجهة وأشعر بأنني أفقد طاقتي عندما يطلبون مني الكثير": {
            "mental": "متردد",
            "emotional": "منسحب",
            "social": "متحفظ",
            "shadow": "الهارب",
            "core": "خوف من الاستنزاف"
        },
        "أشعر بأنني أضطر لإثبات نفسي باستمرار حتى يشعر الآخرون بقيمتي": {
            "mental": "مجهد",
            "emotional": "مضطرب",
            "social": "طالب للقبول",
            "shadow": "المراوغ",
            "core": "اعتماد خارجي على التقدير"
        },
        "أجد صعوبة في وضع حدود واضحة وأقبل الكثير من الطلبات رغم شعوري بعدم الراحة": {
            "mental": "ممزق",
            "emotional": "مرهق",
            "social": "متداخل",
            "shadow": "المُرضي",
            "core": "حدود مهزوزة"
        }
    }

    mental = []
    emotional = []
    social = []
    shadows = []
    cores = []
    answers_text = []

    for answer in answers:
        profile = mapping.get(answer)
        if profile:
            mental.append(profile["mental"])
            emotional.append(profile["emotional"])
            social.append(profile["social"])
            shadows.append(profile["shadow"])
            cores.append(profile["core"])
            answers_text.append(answer)

    def most_common(items):
        return max(set(items), key=items.count) if items else "غير واضح"

    def unique_phrase(items):
        unique_items = list(dict.fromkeys(items))
        if not unique_items:
            return "غير واضح"
        if len(unique_items) == 1:
            return unique_items[0]
        return " و".join(unique_items[:2])

    signature = "|".join(sorted(set(answers_text))) + f"|{energy_level}"
    rnd = random.Random(sum(ord(ch) for ch in signature) + datetime.now().hour)

    mental_state = unique_phrase(mental)
    emotional_state = unique_phrase(emotional)
    social_state = unique_phrase(social)

    shadow_set = list(dict.fromkeys(shadows))
    if len(shadow_set) == 0:
        shadow_pattern = "غير واضح"
    elif len(shadow_set) == 1:
        shadow_pattern = shadow_set[0]
    elif len(shadow_set) == 2:
        shadow_pattern = f"{shadow_set[0]} و{shadow_set[1]}"
    else:
        shadow_pattern = f"{shadow_set[0]} و{shadow_set[1]} مع ظل إضافي"

    core_list = list(dict.fromkeys(cores))
    core_issue = core_list[0] if core_list else "غير واضح"
    if len(core_list) > 1:
        core_issue = f"{core_list[0]} و{core_list[1]}"

    energy_label = {
        1: "منهك جداً ومحتاج إلى توقف فوري",
        2: "متعب وعليك أن تعيد شحن طاقتك",
        3: "متوسط الوضعية؛ بحاجة إلى دعم بسيط",
        4: "قريب من التوازن لكن لا تزال تحتاج وضوحاً",
        5: "طاقة جيدة وأقل مقاومة نفسية"
    }.get(energy_level, "طاقة متقلبة ومفتوحة للتغيير")

    pattern_count = len(shadow_set)
    energy_tags = {
        1: "الضغط العالي يجعل كل خيار أكثر وضوحًا.",
        2: "الطاقة المنخفضة تعزز الحاجة لدعم داخلي.",
        3: "التوازن المتوسط يمنحك فرصة للتأمل في الاختيارات.",
        4: "الطاقة الجيدة تمنحك مساحة للتصالح مع الظلال.",
        5: "الطاقة القوية تساعدك في قيادة التغيير الداخلي."
    }

    dynamic_notes = [
        "هذا التحليل يعتمد على مزيج اختياراتك الحالي، لذلك سيختلف حين تختار تركيبة جديدة.",
        "كل مرة تغير فيها خياراً واحداً يمكن أن يظهر جانباً جديداً من ظلّك الداخلي.",
        "تركيبة إجاباتك تشكل قراءة فريدة؛ لا يوجد نتيجتان متطابقتان تماماً.",
        "الطاقة النفسية متحركة، لذا اعتبر هذا التحليل خريطة مرنة وليست نتيجة واحدة.",
        "وجود أكثر من نمط ظل يعني أنك تواجه تداخلًا بين طرق دفاع مختلفة؛ تابع ما يظهر لك بأناة.",
        "كلما كان نمطك أكثر تركيبًا، زادت فرصة أن تكون الحاجة الأساسية حول الحدود والاعتراف الذاتي.",
        "الخيارات التي اخترتها تكشف عن طبقات متعددة من التحدي النفسي؛ اقرأها كدعوة للوعي أكثر منها كحكم ثابت."
    ]

    base_note = rnd.choice(dynamic_notes)
    energy_note = energy_tags.get(energy_level, "الطاقة الحالية تغذي هذا التحليل.")
    combination_note = (
        "نمط ظل واحد يركز على عمق داخلي واضح." if pattern_count == 1
        else "القراءة تُظهر تداخل أوجه ظل متعددة؛ حاول التعرف إلى أيها يصدُر منك أكثر." if pattern_count == 2
        else "ثلاثة أو أكثر من الظلال تظهر أنك في مرحلة انتقالية نفسية؛ امنح نفسك وقتًا للتأمل في كل منها."
    )

    dynamic_note = f"{base_note} {energy_note} {combination_note}"

    return {
        "mental_state": mental_state,
        "emotional_state": emotional_state,
        "social_state": social_state,
        "shadow_pattern": shadow_pattern,
        "core_issue": core_issue,
        "energy_label": energy_label,
        "dynamic_note": dynamic_note
    }


def get_shadow_therapy(shadow_pattern, energy_level):
    """يوفر خطة علاجية يومية وأسبوعية وروحية وفق نمط الظل أو تركيبة أظل متعددة."""
    plans = {
        "الناقد الداخلي": {
            "daily": "اكتب اليوم 3 عبارات تقدير ذاتي قبل النوم.",
            "weekly": "اختبر أسبوعياً لحظات نجاحك الصغيرة وسجلها بدون مقارنة.",
            "spiritual": "كرر: 'أنا أستحق السلام الذاتي دون أن أكون مثالياً.'"
        },
        "المنقذ": {
            "daily": "راجع قائمة أولوياتك وحدد 3 مهام لك فقط.",
            "weekly": "تعلم قول 'لا' بابتسامة في موقف واحد محدد.",
            "spiritual": "كرر: 'أنا أعتني بنفسي ثم أقدم من طاقة وفيرة.'"
        },
        "الخائف من الفقدان": {
            "daily": "خصص 5 دقائق للتنفس العميق قبل أي قرار مهم.",
            "weekly": "قِس ثقتك بتجربة صغيرة في السلام المالي أو العاطفي.",
            "spiritual": "كرر: 'الكون يدعمني وأمناتي تتحقق بتدفق.'"
        },
        "الهارب": {
            "daily": "شارك مشاعر صغيرة مع شخص تثق به، حتى لو كنت غير مرتاح.",
            "weekly": "حدد خطوة بسيطة في مواجهة أحد مخاوفك الصغيرة.",
            "spiritual": "كرر: 'اقترب من حياتي بشجاعة من دون أن أهرب.'"
        },
        "المراوغ": {
            "daily": "راجع كلمة 'لماذا' قبل أن تتصرف لطلب القبول.",
            "weekly": "اكتب موقفاً شعرت فيه بعدم الراحة وناقشه صديقاً موثوقاً.",
            "spiritual": "كرر: 'أنا كامل حتى بدون موافقة الجميع.'"
        },
        "المُرضي": {
            "daily": "حدد ثلاثة حدود شخصية واضحة وقلها بلطف لنفسك.",
            "weekly": "قم برفض طلب واحد لا يخدمك وراقب شعورك بعد ذلك.",
            "spiritual": "كرر: 'احترامي لذاتي هو بداية شفاءي.'"
        },
        "غير واضح": {
            "daily": "راقب مشاعرك ودونها قبل النوم.",
            "weekly": "اقض وقتاً هادئاً في التأمل أو المشي.",
            "spiritual": "كرر: 'أمنح نفسي وقتاً لأكتشف نفسي بعمق.'"
        }
    }

    def combine_plans(parts):
        combined = {"daily": [], "weekly": [], "spiritual": []}
        for part in parts:
            plan = plans.get(part.strip())
            if plan:
                for key in combined:
                    combined[key].append(plan[key])
        if not combined["daily"]:
            return plans["غير واضح"].copy()
        return {
            "daily": " | ".join(dict.fromkeys(combined["daily"])),
            "weekly": " | ".join(dict.fromkeys(combined["weekly"])),
            "spiritual": " | ".join(dict.fromkeys(combined["spiritual"]))
        }

    if " و" in shadow_pattern or "مع ظل إضافي" in shadow_pattern:
        parts = shadow_pattern.replace(" مع ظل إضافي", "").split(" و")
        plan = combine_plans(parts)
        if len(parts) > 1:
            plan["daily"] += " | ركز اليوم على تحديد الأولويات الخاصة بك قبل خدمة الآخرين."
            plan["weekly"] += " | اختر وقتاً لتقييم أي حدود تحتاج إلى إعادة ضبط."
            plan["spiritual"] += " | اذكر: 'أستحق سلامي بينما أنتقل بين جوانب نفسي المختلفة.'"
    else:
        plan = plans.get(shadow_pattern, plans["غير واضح"]).copy()

    if energy_level <= 2:
        plan["daily"] += " حاول أن تزيد فترات الهدوء والتنفس بعمق."
        plan["weekly"] += " احجز وقتاً لنفسك خارج روتين الآخرين.",
    elif energy_level == 5:
        plan["daily"] += " استفد من طاقتك البانية لتثبيت حدود صحية.",
        plan["weekly"] += " مارس النشاط الذي يعزز احترامك الذاتي باستمرار.",

    return plan


def get_folk_connection(shadow_pattern):
    """يربط نمط الظل بمجال طاقة فلكي أو شاكرا للمستخدم."""
    mapping = {
        "الناقد الداخلي": "مفتاح الشاكرا الحلقية؛ تحدث بصراحة لنفسك اليوم.",
        "المنقذ": "مفتاح الشاكرا القلبية؛ امنح نفسك مساحة للمحبة الذاتية.",
        "الخائف من الفقدان": "مفتاح الشاكرا الجذرية؛ ابحث عن الأمان في توازنك الداخلي.",
        "الهارب": "مفتاح الشاكرا الثالثة؛ اعمل على ثقتك الذاتية خطوة بخطوة.",
        "المراوغ": "مفتاح الشاكرا الحلقية؛ اختر كلماتك بصدق مع نفسك.",
        "المُرضي": "مفتاح الشاكرا القلبية؛ أعِد وضع حدود تحميك.",
        "غير واضح": "الشاكرا التاجية تدعوك للهدوء الداخلي والوضوح العاطفي."
    }
    if " و" in shadow_pattern:
        parts = shadow_pattern.replace(" مع ظل إضافي", "").split(" و")
        labels = [mapping.get(part.strip(), None) for part in parts]
        labels = [lbl for lbl in labels if lbl]
        if labels:
            return " ؛ ".join(labels) + " | تذكّر أن التوازن بين هذه الطاقات هو هدفك الأهم."
    return mapping.get(shadow_pattern, mapping["غير واضح"])


def generate_house_prediction(birth_name, birth_date, birth_place, chart_type, house_num, cosmic_seed):
    """إنشاء توقع فلكي متغير لكل بيت بناءً على بيانات الميلاد والبيت ونوع الخريطة."""
    key = f"{birth_name.strip().lower()}|{birth_place.strip().lower()}|{birth_date.strftime('%Y%m%d')}|{chart_type}|{house_num}|{int(cosmic_seed)}"
    seed = sum(ord(ch) for ch in key) % 1000
    templates = {
        1: {
            'monthly': [
                ["⚠️ بيت الذات يشهد اختباراً لثقتك هذه الأيام.", "👀 قد يحاول شخص في محيط العمل أن يربكك.", "🧠 حافظ على هدوئك ولا تدخل في صراعات غير مفيدة.", "✨ خطوة محسوبة الآن أقوى من قرار سريع."],
                ["🌟 طاقتك الشخصية مرتفعة، لكن هناك منافسة خفية.", "🚫 لا تفتح كل أوراقك أمام من لا تعرف نواياه.", "📌 راقب من يحاول أن يقلل من مكانتك.", "💎 الثبات سيجعل موقفك أكثر قوة لاحقاً."]
            ],
            'yearly': [
                ["🪐 العام يحمل إعادة صياغة لصورتك العامة.", "⚠️ تجنب الظهور السريع على حساب العمق.", "📌 قيّم من يدعمك بصدق قبل أن توسع دائرة تأثيرك.", "🌿 خطواتك الصغيرة هنا تؤدي إلى نجاح أكبر مستقبلاً."],
                ["✨ فرصة لتغيير هويتك العملية تتشكل هذا العام.", "🔍 لا تسلّم زمام الأمور لمن لا تثق به بالكامل.", "🧭 التوازن بين ما تظهره وما تشعر به هو سر ثباتك.", "🌱 التزامك الصحيح يعطيك قوة أكبر في النهاية."]
            ]
        },
        2: {
            'monthly': [
                ["💰 بيت المال يمنحك فرصة، لكنه يتطلب حكمة.", "⚠️ لا تقبل عرضاً مالياً قبل أن تتحقق منه جيداً.", "🧾 راقب مصاريفك وابتعد عن الاندفاع الشرائي.", "🌿 الانضباط المالي يمنحك راحة أكبر لاحقاً."],
                ["🔎 عرض مالي قد يبدو مغرياً، لكنه يحتاج تحليلًا.", "🚫 تجنّب القروض السريعة أو الالتزامات غير الواضحة.", "📊 ضع خطة دقيقة لميزانيتك الشهرية.", "✨ الترشيد أفضل من الإرهاق المالي المفاجئ."]
            ],
            'yearly': [
                ["✨ العام يدعوك لبناء أمان مالي قوي.", "⚠️ لا تدخل في التزامات طويلة الأجل دون دراسة.", "📌 وفر جزءاً من دخلك لمواجهة المفاجآت.", "🌿 التخطيط المستمر يدعمك طوال السنة."],
                ["🪐 عام الوفرة يتطلبك أن تكون واقعياً للغاية.", "💡 كن مرناً في التعامل مع الفرص.", "📈 حافظ على سجل واضح لكل تحرك مالي.", "✨ العقلانية ترفع فرصك المالية أكثر من الاندفاع."]
            ]
        },
        3: {
            'monthly': [
                ["🗣️ كلماتك تحمل قوة، فاتخذها بحكمة.", "⚠️ قد تُفهم بشكل خاطئ إذا لم تكن واضحاً.", "📱 تجنّب الرسائل الحادة أو التسرع في الرد.", "🤝 التواصل الراقي يفتح لك أبواباً أفضل."],
                ["💬 فرصة مهمة للتواصل قد تظهر قريباً.", "🚫 لا تدخل في حديث لا يخدم أهدافك الحقيقية.", "🧠 دوّن ملاحظاتك قبل أن ترد على عروض كبيرة.", "✨ الحوار الواضح يعزز مكانتك ويقلل الالتباس."]
            ],
            'yearly': [
                ["✈️ عام السفر والتعلم يدعوك لتوسيع معرفتك.", "🔍 لا تدخل في نقاشات تشتت تفكيرك.", "🧭 فرص جيدة للتعلم ستظهر إذا كنت مستعداً.", "✨ كلماتك هذا العام تصبح أكبر من مجرد ما تنطق به."],
                ["🌟 قد يُطلب منك هذا العام قيادة محادثات مهمة.", "⚠️ حافظ على مصداقيتك ولا تعد بما لا تستطيع الوفاء به.", "🤲 شارك أفكارك مع من تثق به فقط.", "🌿 المصداقية تعزز مكانتك أكثر من أي جدل."]
            ]
        },
        4: {
            'monthly': [
                ["🏠 بيت العائلة يشير إلى توتر منزلي بسيط.", "⚠️ تجنّب الرد الفوري على الانفعالات.", "🕯️ امنح الجميع مساحة لتخفيف الضغط.", "🌙 كلمات اللطف تعيد الهدوء أسرع مما تتوقع."],
                ["👨‍👩‍👧‍👦 شخص من الأسرة قد يحتاج دعمك اليوم.", "💬 استمع أولاً ولا تستبق الأحداث.", "🧩 التوازن في البيت يبدأ من ترتيب الأولويات البسيطة.", "✨ السلام المنزلي يبدأ بتفاهم بسيط."]
            ],
            'yearly': [
                ["🌙 السنة تدعوك لبناء جو أكثر دفئاً بالبيت.", "⚠️ لا تترك مشكلة صغيرة تكبر بفعل التجاهل.", "🏡 خصص وقتاً حقيقياً لمن تحب.", "✨ التفاهم العائلي هو أفضل استثمار لك."],
                ["✨ هذا العام قد يمكّنك من حل خلاف قديم.", "📌 تعامل معه بحكمة ورحمة.", "🕊️ لا تفرط في سمعة أحد من دون حكمة.", "🌿 الصوت الهادئ في البيت يخفف الكثير."]
            ]
        },
        5: {
            'monthly': [
                ["💖 بيت الحب يمنحك تجربة رومانسية حقيقية.", "⚠️ لا تنجرف وراء الانطباعات الأولى فقط.", "🎨 قيم مشاعرك بموضوعية قبل أن تعطيها أجنحة.", "✨ التوازن بين القلب والعقل يصنع السلام العاطفي."],
                ["🎯 اهتمامك العاطفي قد يجذب شخصاً جاداً.", "🚫 لا تفتح قلبك لمن لا يستحق احترامك.", "🧠 اجعل حدودك واضحة منذ البداية.", "🌿 العلاقة القوية تحتاج وضوحاً وتناغماً."]
            ],
            'yearly': [
                ["🌟 السنة تدعمك لبناء علاقة ثابتة وقوية.", "⚠️ لا تتجاهل العلامات الصغيرة للتباعد.", "💬 المحادثة الصادقة تقيكما من الارتباك.", "✨ استثمر طاقتك في من يبنيك ولا يهدمك."],
                ["✨ العام يشجعك على إطلاق مشروع إبداعي.", "🧠 لا تخش التجربة، لكنها تحتاج خطة واضحة.", "🎯 ركّز على ما يمنحك معنى حقيقياً.", "🌿 الإبداع يحتاج وقتاً وصبراً لينمو."]
            ]
        },
        6: {
            'monthly': [
                ["🏥 بيت الصحة يحذرك من الإجهاد غير المرئي.", "⚠️ لا تتجاهل آلاماً بسيطة، فقد تكبر بسرعة.", "🧘 النوم والنظام أهم الآن من الضغط المستمر.", "🌿 الراحة هي سلاحك الأقوى لهذه الفترة."],
                ["⏳ روتينك قد يحتاج إلى تعديل عاجل.", "🧼 نظافة المكان تعيد صفاء ذهنك.", "🥗 غذاء متوازن أفضل بكثير من الحلول المؤقتة.", "✨ خفف السرعة لتستعيد طاقتك بسلام."]
            ],
            'yearly': [
                ["🪐 السنة تحفزك على بناء عادات صحية جديدة.", "💪 خطوة يومية بسيطة تصنع فرقاً هائلاً.", "⚠️ لا تهمش أعراض التعب البسيطة.", "🌿 التزامك اليوم سيبقى معك العام كله."],
                ["✨ قد يأتي لك دعم مهم لتنظيم صحتك.", "📌 لا تهمل أوقات الاستراحة حتى وسط الانشغالات.", "🧠 الراحة ليست رفاهية، بل ضرورة.", "🌙 استمع لجسمك كما تستمع لعقلك."]
            ]
        },
        7: {
            'monthly': [
                ["🤝 بيت الشراكات يطرح أمامك فجأة فرصة مهمة.", "⚠️ لا توقع دون أن تفهم التزامك تماماً.", "🛡️ احفظ حدودك ولا تترك أحداً يرتبكك.", "🌿 الشراكة الناجحة تعتمد على الوضوح والاحترام."],
                ["💍 عرض مشترك قد يكون جذاباً لكنه يحتاج دراسة.", "🚫 لا تدخل في أي اتفاق بدافع الرغبة فقط.", "🧭 اختر الشخص الذي يستحق طموحك.", "✨ الشراكة القوية ترفعك ولا تثقلك."]
            ],
            'yearly': [
                ["🌟 العام يحمل لك علاقة شراكة قد تعيد ترتيب حياتك.", "📌 احفظ استقلاليتك حتى وأنت تتعاون.", "🤝 اختر من يدعمك من دون أن يسيطر عليك.", "🌿 التوازن في الشراكة هو سر استقرارها."],
                ["🪐 هذا العام قد يحتاجك لمراجعة شركائك.", "💬 بعض العلاقات تحتاج حديثاً صريحاً.", "🧠 لا تدخل في علاقة جديدة فقط لملء فراغ.", "✨ العلاقة الذكية تحدث فرقاً حقيقياً."]
            ]
        },
        8: {
            'monthly': [
                ["🔮 بيت التحول يحمل كشفاً ماديًا أو داخلياً.", "⚠️ لا تدخل في أي صفقة مالية مع معلومات غير واضحة.", "🕯️ راقب التفاصيل الخفية قبل أن توافق.", "🌿 الصبر والتروّي يحفظانك من الخسارة."],
                ["💥 طاقات قوية قد تدفعك لاتخاذ قرار سريع.", "🚫 لا تنفذ خطوة كبيرة دون دعم قانوني أو خبروي.", "🔍 افحص كل بند حتى الصغير منها.", "✨ أحياناً التأجيل هو القرار الأقوى."]
            ],
            'yearly': [
                ["🌙 السنة تجلب فرص تحوّل عميقة في المال أو القوة.", "⚠️ لا تترك الشكوك تُقودك، بل استخدمها للتحقّق.", "🧠 اعمل منطقياً حتى في لحظات الانفعال.", "✨ أنت أقوى عندما تُحسن قراءة الواقع."],
                ["🪐 هذا العام قد يقودك إلى تغيير جذري في الموارد.", "📌 لا تستسلم لضغط الآخرين في قضايا المال.", "🚫 كن حذراً من العروض العالية جداً.", "🌿 القوة في استرجاع سيطرتك على مصادرك."]
            ]
        },
        9: {
            'monthly': [
                ["✈️ بيت السفر يدعوك لاتخاذ قرار مهم عن رحلة أو دراسة.", "⚠️ لا تجعل الخيار مجرد هروب من ضغوطك.", "🧭 اختر الطريق الذي يخدم مستقبلًا أكبر.", "✨ التجربة الآمنة أفضل من المغامرة غير المدروسة."]
                , ["📚 فكرة جديدة قد تفتح لك آفاقاً بعيدة.", "💬 شاركها مع من يقدر طموحك.", "🧠 لا تنس تحديد ماذا تريد أن تكسب من هذه التجربة.", "🌍 الوعي الحقيقي يأتي من التعلم العميق."]
            ],
            'yearly': [
                ["🌟 العام يساعدك على فتح أفق فكري وروحي جديد.", "⚠️ لا تأخذ أي طريق لمجرد أنه يبدو جميلًا.", "📌 ابحث عن معنى واضح وراء كل خطوة.", "✨ الحكمة الحقيقية تنشأ من التجربة المدروسة."],
                ["🪐 هذه السنة تدعوك للتعلم باستمرار.", "💡 اجعل كل رحلة فرصة للنمو.", "🧠 لا تتردد في تغيير مسارك إذا لم يعد يخدمك.", "🌿 السعادة تأتي من الانفتاح الموزون."]
            ]
        },
        10: {
            'monthly': [
                ["💼 بيت العمل يطالبك الآن بالتركيز والانضباط.", "⚠️ قد يبرز منافس يريد تقليل قيمتك.", "📌 اعمل بصمت وكن منتجاً بدلاً من كلام كثير.", "✨ المثابرة أكثر من الظهور تُنتج نتائج أفضل."],
                ["👑 فرصة مهنية مهمة تلوح في الأفق.", "🧠 لا تنجرف وراء الفخاخ المهنية السريعة.", "🤝 تعاونك الصحيح هو مفتاحك للنجاح.", "🌿 سمعتك المهنية أثمن من أي مكافأة وقتية."]
            ],
            'yearly': [
                ["🌟 السنة تشير إلى تقدم مهني محتمل.", "⚠️ لا تقبل أي دور بدون خطة واضحة.", "📌 العمل المستدام أفضل من القفزات المفاجئة.", "✨ النجاح الحقيقي يبنى على رؤية ثابتة."],
                ["🪐 هذه السنة قد تمنحك منصباً أو اعترافاً.", "💬 احفظ تواصلاً محترماً مع قيادتك.", "📌 لا تنس أن تحافظ على توازنك الشخصي.", "🌿 التوازن العملي هو أساس التفوق."]
            ]
        },
        11: {
            'monthly': [
                ["👥 بيت الأصدقاء يحمل دعوة اجتماعية مهمة.", "⚠️ لا تضع ثقتك في أي شخص بسرعة.", "💬 اختر من يساندك ولا يستنزف طاقتك.", "✨ الأصدقاء الداعمون هم كنز هذا الشهر."],
                ["🎯 فرصة للتواصل مع دائرة جديدة.", "🧠 لا تلهك نفسك بمجموعة خاطئة.", "🤝 احفظ استقلاليتك حتى وأنت تتعاون.", "🌿 الصديق الحقيقي يعززك ولا يعيقك."]
            ],
            'yearly': [
                ["🌟 السنة تسعى لبناء علاقة اجتماعية مستقرة.", "⚠️ لا تعتمد على وعد واحد فقط.", "🔮 اختر من يسعد لنجاحاتك حقاً.", "✨ الدعم الصحيح يبني لك فرصاً أكبر."],
                ["🪐 قد يعيد هذا العام ترتيب دوائر معارفك.", "💬 بعض الروابط تحتاج صدقاً أكبر.", "📌 لا تظل في علاقة تستنزفك.", "🌿 الصداقات الحقيقية تظهر في أوقات الحاجة."]
            ]
        },
        12: {
            'monthly': [
                ["🌙 بيت الخفايا يدعوك للعزلة الهادئة.", "⚠️ لا تهمل الرسائل النفسية التي تصل إليك.", "🧘 امنح نفسك وقتاً للصفاء والهدوء.", "✨ التطهير الداخلي يعيد لك توازنك."],
                ["🔮 قد تحلم برسائل تحمل توجيهات مهمة.", "🚫 لا تتجاهل ما يهمس به عقلك الباطن.", "🕯️ سجّل هذه اللحظات لفهم أفضل.", "🌿 السكينة الداخلية تسبق أي قرار كبير."]
            ],
            'yearly': [
                ["🌌 السنة تتطلب تطهيراً روحياً عميقاً.", "⚠️ لا تسمح للضغوط أن تخفي عنك سلامك.", "📌 راقب أفكارك وأحلامك بدقة.", "✨ البدايات الجديدة تبدأ حين تترك ما يثقل قلبك."],
                ["🪐 هذا العام يمنحك فرصة لتخطي أعباء قديمة.", "🧠 لا تعش الماضي كعقبة، بل درساً.", "💡 خذ وقتاً لتتنفس بعمق قبل أي خطوة.", "🌿 السكون الآن هو أعظم قوة تمتلكها."]
            ]
        }
    }
    house_options = templates.get(house_num, templates[1])
    option_list = house_options['monthly'] if 'شهرية' in chart_type else house_options['yearly']
    return option_list[seed % len(option_list)]

def svg_to_data_uri(svg_text):
    svg_bytes = svg_text.encode('utf-8')
    b64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64_svg}"


def generate_tarot_svg(card_name, subtitle, accent_color="#f7d46f"):
    safe_name = escape(card_name)
    safe_subtitle = escape(subtitle)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="800" viewBox="0 0 500 800">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#170a2c" />
      <stop offset="100%" stop-color="#3d0d58" />
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="{accent_color}" />
    </linearGradient>
  </defs>
  <rect x="10" y="10" width="480" height="780" rx="40" ry="40" fill="url(#bg)" stroke="{accent_color}" stroke-width="18" />
  <rect x="40" y="40" width="420" height="720" rx="30" ry="30" fill="rgba(255,255,255,0.06)" />
  <text x="250" y="140" text-anchor="middle" fill="#ffe7aa" font-family="Cairo, sans-serif" font-size="32" font-weight="700">{safe_name}</text>
  <text x="250" y="180" text-anchor="middle" fill="#f0b9e2" font-family="Cairo, sans-serif" font-size="18">{safe_subtitle}</text>
  <rect x="120" y="220" width="260" height="340" rx="30" ry="30" fill="rgba(255,255,255,0.08)" stroke="url(#accent)" stroke-width="10" />
  <circle cx="250" cy="410" r="100" fill="rgba(255,255,255,0.10)" stroke="{accent_color}" stroke-width="8" />
  <path d="M250,320 L250,500" stroke="{accent_color}" stroke-width="18" stroke-linecap="round" />
  <path d="M250,320 L210,380" stroke="{accent_color}" stroke-width="12" stroke-linecap="round" />
  <path d="M250,320 L290,380" stroke="{accent_color}" stroke-width="12" stroke-linecap="round" />
  <text x="250" y="560" text-anchor="middle" fill="#ffdf88" font-family="Cairo, sans-serif" font-size="20" font-weight="600">نصيحة الكارت</text>
</svg>'''
    return svg

major_cards = [
    ("The Fool", "الجاهل"),
    ("The Magician", "الساحر"),
    ("The High Priestess", "الكاهنة الكبرى"),
    ("The Empress", "الإمبراطورة"),
    ("The Emperor", "الإمبراطور"),
    ("The Hierophant", "المعلم الروحي"),
    ("The Lovers", "العشاق"),
    ("The Chariot", "العربة"),
    ("Strength", "القوة"),
    ("The Hermit", "الناسك"),
    ("Wheel of Fortune", "عجلة الحظ"),
    ("Justice", "العدالة"),
    ("The Hanged Man", "المشنوق"),
    ("Death", "الموت"),
    ("Temperance", "الاعتدال"),
    ("The Devil", "الشيطان"),
    ("The Tower", "البرج"),
    ("The Star", "النجم"),
    ("The Moon", "القمر"),
    ("The Sun", "الشمس"),
    ("Judgement", "الحكم"),
    ("The World", "العالم")
]

minor_suits = [
    ("Wands", "العصي", "🔥"),
    ("Cups", "الكؤوس", "🌊"),
    ("Swords", "السيوف", "⚔️"),
    ("Pentacles", "العملات", "🌱")
]

rank_names = [
    ("Ace", "الآس"),
    ("Two", "الاثنان"),
    ("Three", "الثلاثة"),
    ("Four", "الأربعة"),
    ("Five", "الخمسة"),
    ("Six", "الستة"),
    ("Seven", "السبعة"),
    ("Eight", "الثمانية"),
    ("Nine", "التسعة"),
    ("Ten", "العشرة"),
    ("Page", "الصفحة"),
    ("Knight", "الفارس"),
    ("Queen", "الملكة"),
    ("King", "الملك")
]

rank_templates = {
    "Ace": "يعلن بداية جديدة وفرصة لإطلاق طاقتك مع وضوح نية عميق.",
    "Two": "يدعوك للتعاون والموازنة بين وجهتين أو خيارين مهمين.",
    "Three": "يحفزك على الإبداع والمشاركة لتحقيق تقدم ملموس.",
    "Four": "يدعوك للترتيب والثبات وبناء أساس قوي للمستقبل.",
    "Five": "يحذرك من الصراعات ويطلب منك التعلم من التحديات.",
    "Six": "يعدك بدعم يأتي من الآخرين ووقت للتصالح.",
    "Seven": "يشجعك على الثقة بحدسك بينما تتجاوز الشكوك الداخلية.",
    "Eight": "يدعوك للتحرك بسرعة والتغيير بحزم نحو هدف أعلى.",
    "Nine": "يظهر لك أنه الوقت قد اقترب لإتمام مرحلة بنجاح.",
    "Ten": "يحمل رسالة الوفرة أو اكتمال دورة طاقية مهمة.",
    "Page": "يأتيك برسالة جديدة أو فكرة تفتح باباً من الإمكانيات.",
    "Knight": "يدفعك للمغامرة والعمل بشجاعة من أجل حلمك.",
    "Queen": "يدعوك لقيادة طاقتك بحكمة وعناية ناعمة.",
    "King": "يطلب منك التحلي بالمسؤولية والوعي القائد لتحقيق نتائج قوية."
}

# قاموس التفسيرات المتعددة لكل بطاقة (للتنويع)
card_interpretations = {
    "Ace": [
        "بداية جديدة براقة تحمل طاقة إيجابية عالية جداً",
        "فرصة ذهبية لتطبيق حلم طالما انتظرته",
        "إشارة قوية من الكون لبدء مشروع أو علاقة جديدة",
        "تنبيه لاستثمار الطاقة الجديدة بحكمة وقصد"
    ],
    "Two": [
        "توازن وتعاون يحمل طاقة شراكة قوية",
        "اختيار مهم بين خيارين متساويي الأهمية",
        "حوار وتفاهم بين طاقتين مختلفتين",
        "دعوة للاستماع والمرونة في التعامل"
    ],
    "Three": [
        "إبداع وسعادة مشتركة مع فريق متناغم",
        "تقدم ملموس بعد مرحلة من الانتظار",
        "احتفالات أو لحظات فرح قادمة قريباً",
        "طاقة إنتاجية عالية جداً للإنجاز"
    ],
    "Four": [
        "استقرار وأمان بعد فترة من عدم اليقين",
        "أساس متين يدعمك للمستقبل",
        "راحة واستقرار مادي وعاطفي",
        "وقت مناسب للتخطيط طويل الأمد"
    ],
    "Five": [
        "تحديات تعلمك دروساً قيمة جداً",
        "صراعات مؤقتة ستمضي بسرعة",
        "نقاشات حادة لكنها ستؤدي لتطهير الهالة",
        "اختبار لقوتك النفسية والروحية"
    ]
}

suit_descriptions = {
    "Wands": "الإبداع والطاقة والإرادة" ,
    "Cups": "المشاعر والعلاقات والحدس",
    "Swords": "العقل والتحدي والوضوح",
    "Pentacles": "الوفرة والأمان العملي"
}

tarot_images = {
    # الكروت الكبرى
    "the_fool": "RWS_Tarot_00_Fool.jpg",
    "the_magician": "RWS_Tarot_01_Magician.jpg",
    "the_high_priestess": "RWS_Tarot_02_High_Priestess.jpg",
    "the_empress": "RWS_Tarot_03_Empress.jpg",
    "the_emperor": "RWS_Tarot_04_Emperor.jpg",
    "the_hierophant": "RWS_Tarot_05_Hierophant.jpg",
    "the_lovers": "RWS_Tarot_06_Lovers.jpg",
    "the_chariot": "RWS_Tarot_07_Chariot.jpg",
    "strength": "RWS_Tarot_08_Strength.jpg",
    "the_hermit": "RWS_Tarot_09_Hermit.jpg",
    "wheel_of_fortune": "RWS_Tarot_10_Wheel_of_Fortune.jpg",
    "justice": "RWS_Tarot_11_Justice.jpg",
    "the_hanged_man": "RWS_Tarot_12_Hanged_Man.jpg",
    "death": "RWS_Tarot_13_Death.jpg",
    "temperance": "RWS_Tarot_14_Temperance.jpg",
    "the_devil": "RWS_Tarot_15_Devil.jpg",
    "the_tower": "RWS_Tarot_16_Tower.jpg",
    "the_star": "RWS_Tarot_17_Star.jpg",
    "the_moon": "RWS_Tarot_18_Moon.jpg",
    "the_sun": "RWS_Tarot_19_Sun.jpg",
    "judgement": "RWS_Tarot_20_Judgement.jpg",
    "the_world": "RWS_Tarot_21_World.jpg",
    # كروت العصي
    "ace_of_wands": "Wands01.jpg",
    "two_of_wands": "Wands02.jpg",
    "three_of_wands": "Wands03.jpg",
    "four_of_wands": "Wands04.jpg",
    "five_of_wands": "Wands05.jpg",
    "six_of_wands": "Wands06.jpg",
    "seven_of_wands": "Wands07.jpg",
    "eight_of_wands": "Wands08.jpg",
    "nine_of_wands": "Wands09.jpg",
    "ten_of_wands": "Wands10.jpg",
    "page_of_wands": "Wands11.jpg",
    "knight_of_wands": "Wands12.jpg",
    "queen_of_wands": "Wands13.jpg",
    "king_of_wands": "Wands14.jpg",
    # كروت الكؤوس
    "ace_of_cups": "Cups01.jpg",
    "two_of_cups": "Cups02.jpg",
    "three_of_cups": "Cups03.jpg",
    "four_of_cups": "Cups04.jpg",
    "five_of_cups": "Cups05.jpg",
    "six_of_cups": "Cups06.jpg",
    "seven_of_cups": "Cups07.jpg",
    "eight_of_cups": "Cups08.jpg",
    "nine_of_cups": "Cups09.jpg",
    "ten_of_cups": "Cups10.jpg",
    "page_of_cups": "Cups11.jpg",
    "knight_of_cups": "Cups12.jpg",
    "queen_of_cups": "Cups13.jpg",
    "king_of_cups": "Cups14.jpg",
    # كروت السيوف
    "ace_of_swords": "Swords01.jpg",
    "two_of_swords": "Swords02.jpg",
    "three_of_swords": "Swords03.jpg",
    "four_of_swords": "Swords04.jpg",
    "five_of_swords": "Swords05.jpg",
    "six_of_swords": "Swords06.jpg",
    "seven_of_swords": "Swords07.jpg",
    "eight_of_swords": "Swords08.jpg",
    "nine_of_swords": "Swords09.jpg",
    "ten_of_swords": "Swords10.jpg",
    "page_of_swords": "Swords11.jpg",
    "knight_of_swords": "Swords12.jpg",
    "queen_of_swords": "Swords13.jpg",
    "king_of_swords": "Swords14.jpg",
    # كروت العملات
    "ace_of_pentacles": "RWS1909_-_Pentacles_01.jpeg",
    "two_of_pentacles": "RWS1909_-_Pentacles_02.jpeg",
    "three_of_pentacles": "RWS1909_-_Pentacles_03.jpeg",
    "four_of_pentacles": "RWS1909_-_Pentacles_04.jpeg",
    "five_of_pentacles": "RWS1909_-_Pentacles_05.jpeg",
    "six_of_pentacles": "RWS1909_-_Pentacles_06.jpeg",
    "seven_of_pentacles": "RWS1909_-_Pentacles_07.jpeg",
    "eight_of_pentacles": "RWS1909_-_Pentacles_08.jpeg",
    "nine_of_pentacles": "RWS1909_-_Pentacles_09.jpeg",
    "ten_of_pentacles": "RWS1909_-_Pentacles_10.jpeg",
    "page_of_pentacles": "RWS1909_-_Pentacles_11.jpeg",
    "knight_of_pentacles": "RWS1909_-_Pentacles_12.jpeg",
    "queen_of_pentacles": "RWS1909_-_Pentacles_13.jpeg",
    "king_of_pentacles": "RWS1909_-_Pentacles_14.jpeg"
}

def get_tarot_image_url(card_key):
    file_name = tarot_images.get(card_key)
    if not file_name:
        return None
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(file_name, safe='')}"

# قاموس النصائح للبطاقات الكبرى
major_advice = {
    "The Fool": "ثق بحدسك واترك للكون يدلك نحو الطريق الجديد",
    "The Magician": "استخدم قوتك الخاصة وتحكم بمصيرك بجرأة",
    "The High Priestess": "استمع لصوتك الداخلي والحدس العميق فهو لا يخطئ",
    "The Empress": "احتضن نعومتك وطاقتك الأنثوية لجذب الخير والوفرة",
    "The Emperor": "تحلَّ بالقيادة القوية والمسؤولية والحكمة",
    "The Hierophant": "عد للتقاليد الحكيمة واطلب العلم من المعلمين",
    "The Lovers": "اختر بحب وحكمة، والالتزام الحقيقي سيأتي",
    "The Chariot": "انطلق بثقة وأرادة قوية نحو انتصارك",
    "Strength": "قوتك الحقيقية في الهدوء والصبر والتحكم بأعصابك",
    "The Hermit": "خذ وقتاً للتأمل الداخلي والبحث عن الحقيقة",
    "Wheel of Fortune": "الحظ يتحول، ثق بدورات الحياة الطبيعية",
    "Justice": "تحمل المسؤولية عن أفعالك وقرارتك الماضية",
    "The Hanged Man": "تطلب الوضعية جديدة في النظر للحياة وتضحيات ضرورية",
    "Death": "التغيير حتمي، دع القديم يرحل والجديد يأتي",
    "Temperance": "ابحث عن التوازن والاعتدال في كل جوانب حياتك",
    "The Devil": "حرر نفسك من الخوف والقيود الخيالية",
    "The Tower": "التفكك ضروري قبل البناء من جديد بأساس أقوى",
    "The Star": "ثق بأملك والنور يعود إليك قريباً جداً",
    "The Moon": "احذر من الأوهام واثقِ بالنور الحقيقي داخلك",
    "The Sun": "يأتيك النجاح والفرح والنور الساطع قريباً",
    "Judgement": "استيقظ لنداء أعمق وتحول روحي حاسم",
    "The World": "اكتملت دورة، احتفل بإنجازك ثم ابدأ فصل جديد"
}

# قاموس النصائح للبطاقات الصغيرة حسب الرتبة
rank_advice = {
    "Ace": "استقبل هذه الهدية الجديدة بامتنان واستثمرها بحكمة",
    "Two": "اختر بين خيارين بهدوء أو ابحث عن توازن",
    "Three": "شارك طاقتك مع الآخرين والنتائج ستكون رائعة",
    "Four": "خذ وقتك للاستقرار والتخطيط بعناية",
    "Five": "تحديات تعلمك، تعلم منها بدون استسلام",
    "Six": "قبول الدعم من الآخرين جزء من نموك",
    "Seven": "ثق بحدسك حتى لو بدا الطريق غير واضح",
    "Eight": "الوقت للحركة السريعة والقرارات الجريئة",
    "Nine": "أنت قريب جداً من النهاية، استمر بثبات",
    "Ten": "اكتمال ووفرة، احتفل بما أنجزته",
    "Page": "رسالة جديدة أو فرصة تنتظرك",
    "Knight": "تحلَّ بالشجاعة والمغامرة نحو هدفك",
    "Queen": "قيادة بحكمة ورعاية واستقلالية",
    "King": "سلطة وقيادة قوية ومسؤولة"
}

suit_advice = {
    "Wands": "استثمر طاقتك الإبداعية",
    "Cups": "استمع لقلبك والمشاعر الحقيقية",
    "Swords": "استخدم حكمتك وعقلك النير",
    "Pentacles": "اعتني بالعملي والمادي بحكمة"
}

tarot_cards = []
for name, arabic in major_cards:
    tarot_cards.append({
        "name": name,
        "display_name": f"{name} <br>({arabic})",
        "subtitle": arabic,
        "message": f"بطاقة {arabic} تدعو إلى {name.replace('_', ' ').lower()} بحكمة. {('تذكر أن كل تحول يحتاج إلى درجة عالية من الوعي.') if name == 'The World' else 'تعلم من الرسالة هذه وامضِ بثقة نحو هدفك.'}",
        "advice": major_advice.get(name, "اسمع ما يقول لك قلبك")
    })

for suit_en, suit_ar, suit_icon in minor_suits:
    for rank_en, rank_ar in rank_names:
        tarot_cards.append({
            "name": f"{rank_en} of {suit_en}",
            "display_name": f"{rank_en} of {suit_en} {suit_icon} <br>({rank_ar} {suit_ar})",
            "subtitle": f"{rank_ar} {suit_ar}",
            "message": f"بطاقة {rank_ar} {suit_ar} تشير إلى {suit_descriptions[suit_en]}.",
            "advice": rank_advice.get(rank_en, "اسمع ما يقول لك قلبك") + " - " + suit_advice.get(suit_en, "")
        })

zodiacs = {    "الحمل": {"عنصر": "ناري 🔥", "كوكب": "المريخ 🛑", "طبيعة": "قيادي، حماسي، سريع الاشتعال"},
    "الثور": {"عنصر": "ترابي 🌱", "كوكب": "الزهرة 💖", "طبيعة": "ثابت، صبور، يبحث عن الأمان المادي"},
    "الجوزاء": {"عنصر": "هوائي 💨", "كوكب": "عطارد 🧠", "طبيعة": "ذكي، متواصل، متقلب المزاج إيجابياً"},
    "السرطان": {"عنصر": "مائي 🌊", "كوكب": "القمر 🌙", "طبيعة": "عاطفي، حدسي، حامي للمقربين"},
    "الأسد": {"عنصر": "ناري 🔥", "كوكب": "الشمس ☀️", "طبيعة": "كاريزمي، فخور، يحب الظهور والتقدير"},
    "العذراء": {"عنصر": "ترابي 🌱", "كوكب": "عطارد 🧠", "طبيعة": "تحليلي، دقيق، يسعى للمثالية والنظام"},
    "الميزان": {"عنصر": "هوائي 💨", "كوكب": "الزهرة 💖", "طبيعة": "دبلوماسي، محب للسلام والعدل والجمال"},
    "العقرب": {"عنصر": "مائي 🌊", "كوكب": "بلوتو 🖤", "طبيعة": "عميق، غامض، يمتلك قوة تشافي هائلة"},
    "القوس": {"عنصر": "ناري 🔥", "كوكب": "المشتري ✨", "طبيعة": "محب للحرية، متفائل، مستكشف كوني"},
    "الجدي": {"عنصر": "ترابي 🌱", "كوكب": "زحل 🪐", "طبيعة": "طموح، مسؤول، واقعي يبني للمستقبل"},
    "الدلو": {"عنصر": "هوائي 💨", "كوكب": "أورانوس 🌌", "طبيعة": "مبتكر، مستقل، يسبق عصره بأفكاره"},
    "الحوت": {"عنصر": "مائي 🌊", "كوكب": "نبتون 🌊", "طبيعة": "روحاني، حالم، يمتلك فيضاً من المشاعر والحدس"}
}

# قاموس كلمات دلالية لتفسير الأحلام مستوحى من ابن سيرين والنابلسي
dream_dictionary = {
    "طيران": "حسب ابن سيرين، الطيران يرمز إلى السفر، أو نيل سلطان ورفعة، وإذا طار الرائي حتى بلغ السماء فإنه ينال أمنية كبرى.",
    "سقوط": "يشير الإمام النابلسي إلى أن السقوط من مكان مرتفع يعكس تغيراً في الأحوال، أو ارتكاب ذنب، أو خوف باطني من زوال أمر مستقر.",
    "ماء": "الماء الصافي في المنام حياة طيبة، خصوبة، ورزق مبارك. بينما الماء العكر قد يرمز إلى فتنة أو كدر مؤقت يمر به الرائي.",
    "ثعبان": "الحية أو الثعبان في معجم التفسير ترمز إلى عدو ماكر في محيط الرائي، وحجم الثعبان أو لونه يحدد مدى خطورة هذا العداوة.",
    "افعى": "الحية أو الثعبان في معجم التفسير ترمز إلى عدو ماكر في محيط الرائي، وحجم الثعبان أو لونه يحدد مدى خطورة هذا العداوة.",
    "بحر": "البحر يرمز إلى ملك أو سلطان قوي، أو يرمز إلى الدنيا وتقلباتها؛ السباحة فيه بنجاح تعني تجاوز الأزمات الكبرى.",
    "موت": "الموت في المنام غالباً ما يرمز إلى طول العمر، أو الندم على أمر ما وبداية حياة جديدة (ولادة روحية جديدة) وليس دلالة حرفية سيئة.",
    "نار": "النار قد تدل على الفتنة أو الخسارة إن كانت تحرق، لكنها تدل على الهداية والعلم والرفعة إذا كانت للإضاءة والاستئناس.",
    "ذهب": "الذهب في الرؤى قد يرمز إلى الأفراح والمناسبات السعيدة، لكن في بعض الأنماط قد يعكس هماً طفيفاً يزول سريعاً.",
    "نقود": "النقود الورقية تدل على فرج بعد شدة أو أمانة يحملها الشخص، بينما النقود المعدنية الكثيرة قد تدل على لغط أو تشويش ذهني."
}

# واجهة الشعار الرئيسي للموقع
st.markdown("""
<div class="hero-section">
    <h1>� طاقة النجوم 💫</h1>
    <p>بوابتك الرقمية المتكاملة لفك الشفرات الفلكية وتحليل طاقات الوعي</p>
</div>
""", unsafe_allow_html=True)

# الشريط المتحرك العلوي - تحديث Daily Insights
daily_insight_msg = get_daily_insight()
st.markdown(f'<div class="info-banner">💡 نصيحة اليوم: {daily_insight_msg}</div>', unsafe_allow_html=True)

# === نظام حفظ السجل والقراءات ===
init_session_state()

# مربع للإحصائيات
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🔮 إجمالي القراءات", st.session_state.reading_stats['total_readings'])
with col2:
    if st.session_state.reading_stats['most_drawn_cards']:
        top_card = max(st.session_state.reading_stats['most_drawn_cards'], key=st.session_state.reading_stats['most_drawn_cards'].get)
        count = st.session_state.reading_stats['most_drawn_cards'][top_card]
        st.metric("🃏 أكثر بطاقة مسحوبة", f"{top_card[:15]}", f"{count} مرة")
    else:
        st.metric("🃏 أكثر بطاقة", "-")
with col3:
    if st.session_state.favorites:
        st.metric("⭐ المفضلات", len(st.session_state.favorites))
    else:
        st.metric("⭐ المفضلات", "0")
with col4:
    if st.session_state.reading_stats['readings_by_type']:
        top_type = max(st.session_state.reading_stats['readings_by_type'], key=st.session_state.reading_stats['readings_by_type'].get)
        st.metric("🔑 أكثر نوع قراءة", f"{top_type[:12]}", st.session_state.reading_stats['readings_by_type'][top_type])
    else:
        st.metric("🔑 أكثر نوع", "-")

st.divider()

# عرض المفضلات والسجل والإحصائيات (Tabs)
info_tabs = st.tabs(["🔮 القراءات السابقة", "⭐ المفضلات", "📊 الإحصائيات"])

# التاب الأول: القراءات السابقة
with info_tabs[0]:
    if st.session_state.reading_history:
        st.markdown("#### آخر 5 قراءات:")
        for idx, entry in enumerate(st.session_state.reading_history[-5:][::-1]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="history-box">
                    <b>📅 {entry['date']} في {entry['timestamp'].split()[1]}</b><br>
                    <b>نوع القراءة:</b> {entry['type']}<br>
                    <b>النتيجة:</b> {entry['result'][:100]}...
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("❤️", key=f"fav_{idx}"):
                    add_to_favorites(entry)
                    st.success("✅ أضيفت للمفضلات!")
        
        if st.button("🗑️ حذف السجل بالكامل"):
            st.session_state.reading_history = []
            st.rerun()
    else:
        st.info("📭 لا توجد قراءات سابقة حتى الآن. ابدأ القراءة الأولى!")

# التاب الثاني: المفضلات
with info_tabs[1]:
    if st.session_state.favorites:
        st.markdown(f"#### لديك {len(st.session_state.favorites)} قراءة مفضلة:")
        for idx, fav in enumerate(st.session_state.favorites[::-1]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="history-box">
                    <b>⭐ {fav['date']} في {fav['timestamp'].split()[1]}</b><br>
                    <b>نوع:</b> {fav['type']}<br>
                    <b>النتيجة:</b> {fav['result'][:100]}...
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_fav_{idx}"):
                    remove_from_favorites(len(st.session_state.favorites) - 1 - idx)
                    st.rerun()
    else:
        st.info("📄 لم تحفظ أي قراءات كمفضلات بعد. اضغط على ❤️ بجانب أي قراءة!")

# التاب الثالث: الإحصائيات
with info_tabs[2]:
    st.markdown("#### إحصائيات القراءات:")
    
    if st.session_state.reading_stats['readings_by_type']:
        # رسم بياني لأنواع القراءات
        types_data = st.session_state.reading_stats['readings_by_type']
        fig1 = go.Figure(data=[go.Pie(labels=list(types_data.keys()), values=list(types_data.values()), marker=dict(colors=['#ff79c6', '#bb86fc', '#00ffcc', '#ffd700', '#ff6b9d', '#c69cdb', '#7f5af0', '#d945ef', '#74c7ec']))])
        fig1.update_layout(title="📊 توزيع أنواع القراءات", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffd700"))
        st.plotly_chart(fig1, use_container_width=True)
    
    if st.session_state.reading_stats['most_drawn_cards']:
        # رسم بياني لأكثر بطاقات مسحوبة
        cards_data = dict(sorted(st.session_state.reading_stats['most_drawn_cards'].items(), key=lambda x: x[1], reverse=True)[:10])
        fig2 = go.Figure(data=[go.Bar(x=list(cards_data.keys()), y=list(cards_data.values()), marker=dict(color='#ff79c6'))])
        fig2.update_layout(title="🔮 أكثر 10 بطاقات مسحوبة", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffd700"), xaxis_title="اسم البطاقة", yaxis_title="عدد مرات السحب")
        st.plotly_chart(fig2, use_container_width=True)
    
    # إحصائيات عامة
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔮 إجمالي القراءات", st.session_state.reading_stats['total_readings'])
    with col2:
        unique_types = len(st.session_state.reading_stats['readings_by_type'])
        st.metric("🔑 عدد أنواع القراءات", unique_types)
    with col3:
        unique_names = len(st.session_state.reading_stats['most_searched_names'])
        st.metric("👤 أسماء مفردة", unique_names)
    
    if not st.session_state.reading_stats['readings_by_type']:
        st.info("📚 لم تذ أي إحصائيات بعد. ابدأ بعمل بعض القراءات!")

st.divider()

# ===== الميزات الجديدة =====

# 1. التوصيات الذكية
st.markdown("<h3 style='color:#00ffcc; text-align:center;'>🤖 التوصيات الذكية لرحلتك الروحية</h3>", unsafe_allow_html=True)
ai_recs = get_ai_recommendations()
rec_cols = st.columns(len(ai_recs))
for idx, rec in enumerate(ai_recs):
    with rec_cols[idx]:
        st.markdown(f"""<div class="result-box" style="text-align:center; padding:20px;">
        <p style="color:#ffd700; font-size:14px; margin:0;">{rec}</p>
        </div>""", unsafe_allow_html=True)

st.divider()

# 2. الموسيقى الهادئة (Ambient Sound) - ميزة جديدة
st.markdown("<h3 style='color:#bb86fc; text-align:center;'>🎵 موسيقى التأمل والهدوء</h3>", unsafe_allow_html=True)

with st.expander("🎧 اختر موسيقى التأمل المفضلة لديك"):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.checkbox("🌙 موسيقى القمر الهادئة", value=False, key="music_moon"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format='audio/mp3')
            st.caption("موسيقى تأمل هادئة للاسترخاء")
    
    with col2:
        if st.checkbox("🌊 أصوات المحيط الملهمة", value=False, key="music_ocean"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", format='audio/mp3')
            st.caption("موجات المحيط وأصوات البحر")
    
    with col3:
        if st.checkbox("✨ الموسيقى الكونية", value=False, key="music_cosmic"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3", format='audio/mp3')
            st.caption("موسيقى فضاء هادئة وملهمة")

st.divider()

# 3. تقويم الأحداث الفلكية
st.markdown("<h3 style='color:#bb86fc; text-align:center;'>📍 التقويم الفلكي الكوني</h3>", unsafe_allow_html=True)

today_event = get_cosmic_events_today()
if today_event:
    st.markdown(f"""<div class="result-box" style="text-align:center; background:rgba(255,215,0,0.1); border-color:#ffd700;">
    <h4 style="color:#ffd700; margin:0;">🌟 حدث اليوم: {today_event['event']}</h4>
    <p style="color:#00ffcc; margin-top:10px;">{today_event['meaning']}</p>
    </div>""", unsafe_allow_html=True)

with st.expander("📚 أحداث فلكية مهمة في 2026"):
    cosmic_events_full = {
        "29 يناير": {"event": "🌙 قمر دم كامل", "meaning": "نقطة عطل روحية - وقت للتحولات"},
        "9 فبراير": {"event": "☀️ كسوف شمسي جزئي", "meaning": "بداية جديدة وفرص غير متوقعة"},
        "27 مارس": {"event": "🪐 اقتران الزهرة والمريخ", "meaning": "طاقة قوية للحب والجاذبية"},
        "15 أبريل": {"event": "🌙 قمر دم كامل", "meaning": "إضاءة الحقائق المخفية"},
        "20 مايو": {"event": "☀️ موسم الجوزاء", "meaning": "التواصل والحركة والتغيير"},
        "21 يونيو": {"event": "☀️ انقلاب صيفي", "meaning": "نقطة القوة القصوى للسنة"},
        "4 يوليو": {"event": "🪐 عطارد مستقيم", "meaning": "وضوح الرسائل والتفاهم"},
        "15 أغسطس": {"event": "🌙 قمر كامل", "meaning": "تحقيق الرغبات والأمنيات"},
        "22 سبتمبر": {"event": "☀️ انقلاب خريفي", "meaning": "توازن وعدالة وحكمة"},
        "21 ديسمبر": {"event": "☀️ انقلاب شتوي", "meaning": "تجديد وحيوية نقطة البداية"}
    }
    for date, event_info in cosmic_events_full.items():
        st.markdown(f"""
        <div class="history-box">
        <b>{event_info['event']}</b> - {date}<br>
        <span style="color:#00ffcc; font-size:13px;">{event_info['meaning']}</span>
        </div>""", unsafe_allow_html=True)

st.divider()

# 4. نظام الاشتراكات المميز (Subscription Features) - ميزة جديدة
st.markdown("<h3 style='color:#ff79c6; text-align:center;'>💎 نظام الاشتراكات المميز</h3>", unsafe_allow_html=True)

col_free, col_premium = st.columns(2)

with col_free:
    st.markdown("""
    <div class="result-box" style="background:rgba(0,255,204,0.1); border-color:#00ffcc; text-align:center;">
    <h4 style="color:#00ffcc; margin-top:0;">📱 الخطة المجانية</h4>
    <p style="font-size:32px; color:#ffd700; margin:10px 0;">مجاني</p>
    <ul style="text-align:right; color:#ffd700; font-size:14px;">
        <li>✅ قراءات التاروت الأساسية</li>
        <li>✅ حسابات التوافق الرقمي</li>
        <li>✅ تحليل الأحلام</li>
        <li>✅ السجل الشخصي</li>
        <li>❌ المقارنات المتقدمة (متعددة الأشخاص)</li>
        <li>❌ التقارير المفصلة</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col_premium:
    is_premium = st.checkbox("🔓 تفعيل الخطة المميز", key="premium_toggle")
    st.session_state.is_premium = is_premium
    
    if is_premium:
        st.markdown("""
        <div class="result-box" style="background:rgba(255,215,0,0.15); border-color:#ffd700; text-align:center;">
        <h4 style="color:#ffd700; margin-top:0;">👑 الخطة المميز</h4>
        <p style="font-size:28px; color:#ff79c6; margin:10px 0;">مميز 🌟</p>
        <ul style="text-align:right; color:#ffd700; font-size:14px;">
            <li>✅ جميع ميزات الخطة المجانية</li>
            <li>✅ المقارنات المتقدمة (حتى 5 أشخاص)</li>
            <li>✅ التقارير التفصيلية والتصدير</li>
            <li>✅ استشارات مخصصة متقدمة</li>
            <li>✅ سجل متقدم مع تحليلات</li>
            <li>✅ رسائل مخصصة يومية</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.success("✨ مرحباً بك في الخطة المميز!")

st.divider()

# إنشاء أقسام المنصة
tabs = st.tabs([
    "❤️ حاسبة التوافق والاتصال", 
    "🪐 تحليل الاسم والأبراج", 
    "🗺️ الخريطة الفلكية المحدثة",
    "🌙 تفسير الأحلام الذكي",
    "🃏 التاروت والإرشاد البصري",
    "⚖️ حاسبة الكرمة",
    "💊 صيدلية الطاقة والأحجار",
    "🧠 اختبار الحالة والظل",
    "🔢 الرقم الروحي السري"
])

# --- 1. حاسبة التوافق والاتصال ---
with tabs[0]:
    st.subheader("❤️ تحليل الاتصال الطاقي والتوافق الفلكي")
    
    st.markdown("#### 1️⃣ التوافق الرقمي عبر طاقة الأسماء:")
    col1, col2 = st.columns(2)
    with col1:
        name_1 = st.text_input("أدخل الاسم الأول:", placeholder="اكتب الاسم هنا...", key="t1")
    with col2:
        name_2 = st.text_input("أدخل الاسم الثاني:", placeholder="اكتب اسم الطرف الآخر...", key="t2")
        
    if st.button("💖 حساب نسبة التوافق الرقمي"):
        # التحقق من صحة المدخلات
        valid1, msg1 = validate_arabic_name(name_1)
        valid2, msg2 = validate_arabic_name(name_2)
        
        if not valid1:
            st.markdown(f'<div class="error-message">❌ {msg1}</div>', unsafe_allow_html=True)
        elif not valid2:
            st.markdown(f'<div class="error-message">❌ {msg2}</div>', unsafe_allow_html=True)
        else:
                percent, title, advice = calculate_name_compatibility(name_1, name_2)
                
                # حفظ في السجل والإحصائيات
                save_to_history("توافق رقمي", f"{percent}%", f"{name_1} و {name_2}")
                update_reading_stats("توافق رقمي", f"{name_1} و {name_2}")
                
                st.markdown(f"""
                <div class="result-box">
                    <h3 style="color: #ff79c6; text-align: center;">📊 {title}</h3>
                    <h1 style="text-align: center; color: #00ffcc; font-size: 45px; margin: 15px 0;">{percent}%</h1>
                    <p style="font-size: 16px; line-height: 1.6; text-align: center;">{advice}</p>
                    <p style="font-size: 15px; text-align: center; color:#a5a1b8; margin-top:12px;">هذه النسبة تتغير مع كل ساعة لتكشف عن حالة الطاقة الحالية بين الاسمَين.</p>
            """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
    st.markdown("#### 3️⃣ 👥 مقارنات متقدمة - تحليل علاقات متعددة (ميزة جديدة):")
    st.write("قارن توافق شخص مع عدة أشخاص أو مجموعات للتعرف على أفضل التوافقات:")

    num_people = st.number_input(
        "اكتب عدد الأشخاص المراد مقارنتهم:",
        min_value=2,
        max_value=8,
        value=2,
        step=1,
        key="multi_compare_num"
    )

    people_data = []
    for i in range(int(num_people)):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"الاسم {i+1}:", placeholder="اكتب الاسم...", key=f"multi_name_{i}")
        with col2:
            zodiac = st.selectbox(f"البرج {i+1}:", list(zodiacs.keys()), key=f"multi_zodiac_{i}")
        people_data.append({"name": name, "zodiac": zodiac})

    if "comparison_results" not in st.session_state:
        st.session_state.comparison_results = []
        st.session_state.comparison_best = None
        st.session_state.comparison_message = ""
        st.session_state.comparison_warning = ""

    if st.button("🔄 تحليل التوافقات المتعددة", key="compare_multi_button"):
        filtered_people = []
        invalid_message = ""

        for idx, person in enumerate(people_data, start=1):
            if person["name"].strip():
                valid, msg = validate_arabic_name(person["name"])
                if not valid:
                    invalid_message = f"❌ الاسم رقم {idx} غير صالح: {msg}"
                    break
                filtered_people.append(person)

        if invalid_message:
            st.session_state.comparison_results = []
            st.session_state.comparison_best = None
            st.session_state.comparison_message = invalid_message
            st.session_state.comparison_warning = ""
        elif len(filtered_people) < 2:
            st.session_state.comparison_results = []
            st.session_state.comparison_best = None
            st.session_state.comparison_message = ""
            st.session_state.comparison_warning = "⚠️ يرجى إدخال اسمين على الأقل صالحين للمقارنة."
        else:
            comparison_data = []
            for i, p1 in enumerate(filtered_people):
                for j, p2 in enumerate(filtered_people):
                    if i < j:
                        score1 = sum(abjad_table.get(c, 0) for c in p1["name"].strip())
                        score2 = sum(abjad_table.get(c, 0) for c in p2["name"].strip())
                        compatibility = ((score1 + score2) % 41) + 60
                        elem1 = zodiacs[p1["zodiac"]]["عنصر"]
                        elem2 = zodiacs[p2["zodiac"]]["عنصر"]
                        comparison_data.append({
                            "الزوج": f"{p1['name']} ❤️ {p2['name']}",
                            "التوافق الرقمي": f"{compatibility}%",
                            "الأبراج": f"{p1['zodiac']} - {p2['zodiac']}",
                            "العناصر": f"{elem1} & {elem2}"
                        })
                        update_reading_stats("مقارنات متقدمة", f"{p1['name']} و {p2['name']}")

            if comparison_data:
                max_compat = max(int(d["التوافق الرقمي"].rstrip("%")) for d in comparison_data)
                best_pair = next(d for d in comparison_data if int(d["التوافق الرقمي"].rstrip("%")) == max_compat)
                st.session_state.comparison_results = comparison_data
                st.session_state.comparison_best = best_pair
                st.session_state.comparison_message = ""
                st.session_state.comparison_warning = ""
            else:
                st.session_state.comparison_results = []
                st.session_state.comparison_best = None
                st.session_state.comparison_message = ""
                st.session_state.comparison_warning = "⚠️ لا توجد نتائج مقارنة حاليًا. تأكد من إدخال أسماء كافية."

    if st.session_state.comparison_message:
        st.error(st.session_state.comparison_message)
    if st.session_state.comparison_warning:
        st.warning(st.session_state.comparison_warning)

    if st.session_state.comparison_results:
        st.markdown("<h4 id='msfwft-altwafqat-almtqdmt' style='color:#00ffcc; text-align:center;'>📊 مصفوفة التوافقات المتقدمة</h4>", unsafe_allow_html=True)
        st.markdown("<h4 id='tfasyl-almqarnat' style='color:#00ffcc; text-align:center;'>📋 تفاصيل المقارنات</h4>", unsafe_allow_html=True)
        table_html = """
        <table style="width:100%; border-collapse:collapse; text-align:right; direction:rtl; table-layout:fixed;">
            <thead style="background:rgba(255,215,0,0.15); border-bottom:2px solid #ffd700;">
                <tr>
                    <th style="padding:12px; border:1px solid rgba(255,215,0,0.3); color:#ffd700;">الزوج</th>
                    <th style="padding:12px; border:1px solid rgba(255,215,0,0.3); color:#ffd700;">التوافق الرقمي</th>
                    <th style="padding:12px; border:1px solid rgba(255,215,0,0.3); color:#ffd700;">الأبراج</th>
                    <th style="padding:12px; border:1px solid rgba(255,215,0,0.3); color:#ffd700;">العناصر</th>
                </tr>
            </thead>
            <tbody>
        """
        for i, row in enumerate(st.session_state.comparison_results):
            bg_color = "rgba(255,215,0,0.05)" if i % 2 == 0 else "transparent"
            table_html += f"""
                <tr style="background:{bg_color};">
                    <td style="padding:12px; border:1px solid rgba(255,215,0,0.2); color:#00ffcc;">{row['الزوج']}</td>
                    <td style="padding:12px; border:1px solid rgba(255,215,0,0.2); color:#ffd700; font-weight:bold;">{row['التوافق الرقمي']}</td>
                    <td style="padding:12px; border:1px solid rgba(255,215,0,0.2); color:#bb86fc;">{row['الأبراج']}</td>
                    <td style="padding:12px; border:1px solid rgba(255,215,0,0.2); color:#ff79c6;">{row['العناصر']}</td>
                </tr>
            """
        table_html += """
            </tbody>
        </table>
        """
        components.html(f"<div style='overflow-x:auto; width:100%;'>{table_html}</div>", height=330)
        if st.session_state.comparison_best:
            st.markdown(f"""
            <div class="result-box" style="background:rgba(0,255,204,0.1); border-color:#00ffcc;">
                <h4 style="color:#00ffcc;">🌟 أفضل توافق: {st.session_state.comparison_best['الزوج']}</h4>
                <p style="color:#ffd700; font-size:16px;">التوافق: <b>{st.session_state.comparison_best['التوافق الرقمي']}</b></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
    st.markdown("#### 2️⃣ حاسبة التوافق الفلكي بين الأبراج:")
    col_z1, col_z2 = st.columns(2)
    with col_z1:
        z_user1 = st.selectbox("برج الطرف الأول:", list(zodiacs.keys()), key="zu1")
    with col_z2:
        z_user2 = st.selectbox("برج الطرف الثاني:", list(zodiacs.keys()), key="zu2")
        
    if st.button("🪐 تحليل توافق عناصر الأبراج"):
        percent, rel_type, rel_desc = get_zodiac_compatibility(z_user1, z_user2)
        elem1 = zodiacs[z_user1]["عنصر"]
        elem2 = zodiacs[z_user2]["عنصر"]
        
        save_to_history("توافق فلكي", rel_type, f"{z_user1} و {z_user2}")
        update_reading_stats("توافق فلكي", f"{z_user1} و {z_user2}")
        
        st.markdown(f"""
        <div class="result-box">
            <h3 style="color: #ffd700; text-align: center;">🛡️ لوحة التوافق الفلكي الكونية</h3>
            <p style="font-size: 17px; text-align: center;"><b>{z_user1} ({elem1})</b> & <b>{z_user2} ({elem2})</b></p>
            <h1 style="color: #00ffcc; text-align: center; margin: 15px 0;">{percent}%</h1>
            <h4 style="color: #00ffcc; text-align: center; margin: 15px 0;">نوع الرابط: {rel_type}</h4>
            <p style="font-size: 16px; line-height: 1.6;">✨ <b>التحليل الفلكي:</b> {rel_desc}</p>
            <p style="font-size: 15px; text-align: center; color:#a5a1b8; margin-top:12px;">هذه النسبة تتفاعل مع موقعك الكوني الحالي وتكشف عن درجة الانسجام الواقعي والروحي.</p>
        </div>
        """, unsafe_allow_html=True)

# --- 2. تحليل الاسم والأبراج النجمية ---
with tabs[1]:
    st.subheader("🪐 استخراج البرج الباطني وتحليل طاقة حروف الاسم")
    user_name = st.text_input("أدخل الاسم المراد تحليله حالياً:", placeholder="اكتب الاسم هنا...", key="t3")
    if st.button("🔮 ابدأ التحليل الكوني للاسم"):
        valid, msg = validate_arabic_name(user_name)
        
        if not valid:
            st.markdown(f'<div class="error-message">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            name_sum = sum(abjad_table.get(c, 0) for c in user_name.strip())
            zodiac_keys = list(zodiacs.keys())
            detected_zodiac = zodiac_keys[name_sum % 12]
            z_details = zodiacs[detected_zodiac]
            
            save_to_history("تحليل اسم", detected_zodiac, user_name)
            
            st.markdown(f"""
            <div class="result-box">
                <h3 style="color: #ffd700; text-align: center;">📜 لوحة الكشف الفلكي للاسم: {user_name}</h3>
                <p style="font-size: 17px;">🌟 <b>البرج الباطني الحقيقي:</b> <span style="color:#ff79c6; font-weight:bold;">{detected_zodiac}</span></p>
                <p style="font-size: 17px;">💎 <b>العنصر المهيمن:</b> {z_details['عنصر']} | <b>الكوكب الحاكم للطاقة:</b> {z_details['كوكب']}</p>
                <p style="font-size: 17px;">🧬 <b>السمات السلوكية الطاقية:</b> {z_details['طبيعة']}</p>
                <p style="font-size: 16px; line-height: 1.6; margin-top: 10px; color: #a5a1b8;">🛡️ يمتلك هذا الاسم هالة حماية فلكية ممتازة تمنحه القدرة على تجاوز الأنماط المعرقلة في بيئته، ويمتلك جاذبية لافتة للنظر وسط الجمهور.</p>
            </div>
            """, unsafe_allow_html=True)

# --- 3. الخريطة الفلكية المحدثة بالكامل ---
with tabs[2]:
    st.subheader("🗺️ الخريطة الفلكية الحقيقية - 12 بيت كوني")
    
    # إدخالات البيانات
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        birth_name = st.text_input("اسم صاحب الخريطة كاملاً:", placeholder="اكتب الاسم هنا...", key="b_name")
        birth_date = st.date_input("تاريخ الميلاد:", min_value=datetime(1950, 1, 1), key="b_date")
    with col_b2:
        birth_place = st.text_input("مكان الولادة (الدولة/المدينة):", placeholder="مثال: القاهرة، مصر...", key="b_place")
        birth_time = st.time_input("وقت الولادة بدقة (إن وجد):", key="b_time")
    
    # اختيار نوع الخريطة
    st.markdown("---")
    col_chart1, col_chart2, col_chart3 = st.columns(3)
    with col_chart1:
        chart_type = st.radio("نوع الخريطة:", ["📅 شهرية 2026", "🪐 سنوية شاملة"], key="chart_type")
    
    with col_chart2:
        st.write("**✨ معلومة:**")
        st.caption("الخريطة الشهرية تعكس التأثير الفلكي الحالي\nالخريطة السنوية تظهر مسارك الكوني الشامل")
    
    if st.button("🗺️ رسم الخريطة الفلكية"):
        # التحقق من البيانات
        valid_name, msg_name = validate_arabic_name(birth_name)
        valid_place, msg_place = validate_arabic_name(birth_place)
        valid_date, msg_date = validate_date(birth_date)
        
        if not valid_name:
            st.error(f"❌ {msg_name}")
        elif not valid_place:
            st.error(f"❌ {msg_place}")
        elif not valid_date:
            st.error(f"❌ {msg_date}")
        else:
            # حفظ في السجل والإحصائيات
            chart_label = "خريطة فلكية شهرية" if "شهرية" in chart_type else "خريطة فلكية سنوية"
            save_to_history("خريطة فلكية", chart_label, birth_name)
            update_reading_stats("خريطة فلكية", birth_name, chart_label)
            
            # رسم الخريطة
            fig, cosmic_seed = create_birth_chart(birth_name, birth_date, birth_place, birth_time, 
                                                   "monthly" if "شهرية" in chart_type else "yearly")
            
            # عرض معلومات الخريطة
            st.markdown(f"""
            <div class="result-box" style="background:rgba(255,215,0,0.1); border-color:#ffd700; text-align:center;">
            <h2 style="color:#ffd700; margin:10px 0;">🗺️ الخريطة الفلكية</h2>
            <p style="color:#00ffcc; font-size:16px; margin:5px 0;"><b>{birth_name}</b></p>
            <p style="color:#bb86fc; font-size:14px; margin:5px 0;">📍 {birth_place} | 📅 {birth_date}</p>
            <p style="color:#ff79c6; font-size:14px; margin:5px 0;">⏰ {birth_time} | 🔑 الرمز الكوني: {int(cosmic_seed)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # عرض الرسم البياني
            st.plotly_chart(fig, use_container_width=True)
            
            # أهم 3 نقاط للخريطة
            key_points = get_chart_key_points(chart_type, cosmic_seed)
            summary_text_full = f"الخريطة للفلكي: {birth_name}\nالمكان: {birth_place}\nالتاريخ: {birth_date.strftime('%d/%m/%Y')}\nالنوع: {chart_type}\nالرمز الكوني: {int(cosmic_seed)}\n\nأهم 3 نقاط:\n"
            for index, point in enumerate(key_points, 1):
                summary_text_full += f"{index}. {point}\n"
            st.markdown(f"""
            <div style="background:rgba(29,8,70,0.88); border:2px solid #6b4cff; border-radius:20px; padding:22px; margin-top:20px; text-align:right; direction:rtl; color:#f5ecff;">
                <h3 style="color:#ffd700; text-align:center; margin:0 0 14px 0;">📘 أهم 3 نقاط للخريطة</h3>
                <ul style="margin:0; padding-inline-start:20px; font-size:14px; color:#ded4ff; line-height:1.8;">
                    <li>{key_points[0]}</li>
                    <li>{key_points[1]}</li>
                    <li>{key_points[2]}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="💾 تنزيل التوقعات",
                data=summary_text_full,
                file_name="forecast-summary.txt",
                mime="text/plain",
                key="download_forecast"
            )
            st.text_area("📋 النص الجاهز للنسخ", summary_text_full, height=180, key="forecast_text_area")
            
            st.markdown(f"""
            <div style="background:rgba(187,134,252,0.1); border:2px solid #bb86fc; border-radius:12px; padding:20px; margin-top:18px; text-align:right; direction:rtl;">
            <h3 style="color:#bb86fc; text-align:center; margin-top:0;">📖 تحليل البيوت الـ 12 - {chart_type}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            houses_info = get_house_meanings()
            
            # عرض البيوت في expanders ثنائية الأعمدة
            for house_num in range(1, 13):
                if (house_num - 1) % 2 == 0:
                    col1, col2 = st.columns(2)
                
                house_data = houses_info[house_num]
                zodiacs_list = list(zodiacs.keys())
                zodiac_assigned = zodiacs_list[(int(cosmic_seed // 30) + house_num) % 12]
                z_info = zodiacs[zodiac_assigned]
                forecast_list = generate_house_prediction(
                    birth_name,
                    birth_date,
                    birth_place,
                    chart_type,
                    house_num,
                    cosmic_seed
                )
                badge_text, badge_color = get_house_badge(house_num, chart_type)
                
                col_target = col1 if (house_num - 1) % 2 == 0 else col2
                with col_target:
                    with st.expander(f"{house_data['emoji']} {house_data['name']} — {zodiac_assigned}"):
                        st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,217,0,0.18); border-radius:14px; padding:14px; text-align:right; direction:rtl;">
                            <span style="display:inline-block; margin-bottom:10px; padding:5px 12px; border-radius:999px; background:{badge_color}; color:#111; font-weight:700; font-size:12px;">{badge_text}</span>
                            <p style="margin:0 0 8px 0; font-size:13px; color:#ffdd8e;"><b>⚡ العنصر:</b> {z_info['عنصر']}</p>
                            <p style="margin:0 0 10px 0; font-size:12px; color:#c4c0de;"><b>📘 وصف البيت:</b> {house_data['desc']}</p>
                            <div style="background:rgba(0,255,204,0.08); padding:12px; border-radius:12px;">
                                <p style="margin:0 0 8px 0; font-size:13px; color:#b8fff7;"><b>📝 أهم رسالة:</b> {forecast_list[0]}</p>
                                <p style="margin:10px 0 6px 0; font-size:12px; color:#e8e5ff;"><b>💡 نصائح عملية:</b></p>
                                <ul style="margin:0; padding-inline-start:20px; color:#e9e5ff; font-size:12px; line-height:1.6;">
                                    <li>{forecast_list[1]}</li>
                                    <li>{forecast_list[2]}</li>
                                    <li>{forecast_list[3]}</li>
                                </ul>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # زر للحفظ في المفضلات
            col_save1, col_save2 = st.columns([3, 1])
            with col_save1:
                pass
            with col_save2:
                if st.button("❤️ احفظ الخريطة", key="save_chart"):
                    reading_entry = {
                        "type": "خريطة فلكية",
                        "result": f"{birth_name} - {chart_label}",
                        "input": birth_name,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "date": datetime.now().strftime("%d/%m/%Y")
                    }
                    add_to_favorites(reading_entry)
                    st.success("✅ تمت إضافة الخريطة للمفضلات!")

# --- 4. تفسير الأحلام الذكي ---
with tabs[3]:
    st.subheader("🌙 نظام تفسير الأحلام الذكي - معجم ابن سيرين والنابلسي المدمج")
    st.write("اطلب من المتابع كتابة تفاصيل الحلم بدقة في المربع أدناه، ليقوم المحرك بفحص الكلمات الدلالية وربطها بالتفسير التراثي الروحاني:")
    
    user_dream = st.text_area("اكتب تفاصيل الحلم هنا (مثال: رأيت أنني أطير في السماء الصافية وفجأة سقطت في ماء):", placeholder="اكتب الحلم بكلمات واضحة...", height=150)
    
    if st.button("👁️ ابدأ فك شفرة وتفسير الحلم تلقائياً"):
        if not user_dream or len(user_dream.strip()) < 10:
            st.markdown('<div class="error-message">❌ الرجاء كتابة تفاصيل الحلم بشكل كافي (على الأقل 10 أحرف)</div>', unsafe_allow_html=True)
        else:
            found_interpretations = []
            cleaned_dream = user_dream.lower()
            
            for keyword, interpretation in dream_dictionary.items():
                if keyword in cleaned_dream:
                    found_interpretations.append((keyword, interpretation))
            
            save_to_history("تفسير حلم", f"عدد الرموز: {len(found_interpretations)}", user_dream[:50])
            
            st.markdown(f"""
            <div class="result-box">
                <h3 style="color:#ffd700; text-align:center;">🌌 لوحة فك رموز رسائل العقل الباطن</h3>
                <p style="font-size:15px; color:#a5a1b8;"><b>نص الحلم المدخل:</b> "{user_dream}"</p>
                <hr style="border-color: rgba(255,215,0,0.2);">
            """, unsafe_allow_html=True)
            
            if found_interpretations:
                st.markdown("<h4 style='color:#00ffcc;'>📜 الرموز التي تم رصدها وفك شفرتها:</h4>", unsafe_allow_html=True)
                for kw, inter in found_interpretations:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-right: 4px solid #bb86fc;">
                        <b style="color: #ff79c6; font-size: 16px;">🔹 رمز [{kw.upper()}]:</b> 
                        <span style="font-size: 15px; line-height: 1.6; color:#ffffff;">{inter}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                <p style="font-size:15px; color:#00ffcc; margin-top:15px; line-height:1.6;">💡 <b>نصيحة طاقية شاملة:</b> ادمج هذه الرموز معاً؛ فالانتقال من حالة إلى حالة في الحلم يعبر عن مرحلة تحول انتقالية يمر بها وعيك وجانبك النفسي حالياً لتطهير الهالة والارتقاء.</p>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h4 style="color:#ff79c6;">🔮 تحليل روحي عام للحلم:</h4>
                <p style="font-size:16px; line-height:1.6; color:#ffffff;">الحلم يحتوي على دلالات رمزية خاصة بعقلك الباطن. يشير هذا النسق من الرؤى عموماً إلى مرحلة إعادة ترتيب الأفكار والتخلص من الضغوط الفكرية اليومية. يُنصح الرائي ببدء كتابة أحلامه فور الاستيقاظ لتقوية الاتصال بالشاكرات العلوية وتفعيل العين الثالثة للوصول إلى الوضوح الروحي.</p>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

# --- 5. التاروت والإرشاد البصري (تم تحديث التصميم ليغلق بالكامل وبطول مناسب) ---
with tabs[4]:
    st.subheader("🃏 اسحب كارت تاروت ذكي")
    st.write("ركز طاقتك على سؤالك الداخلي واضغط على الزر لسحب كارت تاروت ذكي من مجموعة كاملة، مع رسالة نصيحة لكل بطاقة:")
    
    # أسئلة تفاعلية لتركيز النية (ميزة جديدة)
    with st.expander("❓ ركز نيتك - أجب على سؤال عميق قبل القراءة"):
        user_intention = st.selectbox(
            "اختر السؤال الذي يهمك الآن:",
            [
                "ما السؤال الأعمق في قلبي الآن؟",
                "ماذا تحتاج لتسمعه من الكون اليوم؟",
                "ما المجال في حياتي الذي يحتاج لإضاءة؟",
                "هل أبحث عن توجيه شامل أم إجابة محددة؟",
                "ما الطاقة التي أود استقطابها الآن؟",
                "هل أنا مفتوح لرسالة غير متوقعة من الكون؟"
            ],
            key="tarot_intention_q"
        )
        user_context = st.text_area("💭 شارك سياقك الشخصي (اختياري):", height=80, placeholder="اكتب ما يجول في ذهنك الآن...")
        st.caption("🔮 النية القوية تجعل القراءة أكثر دقة وملاءمة لحالتك الحالية")
    
    if st.button("🔮 اسحب كارت تاروت"):
        chosen_card = random.choice(tarot_cards)
        card_key = chosen_card["name"].lower().replace(" ", "_")
        image_url = get_tarot_image_url(card_key)
        
        # حفظ في السجل والإحصائيات
        reading_result = f"بطاقة {chosen_card['display_name']} - {chosen_card.get('advice', 'اسمع ما يقول لك قلبك')}"
        save_to_history("قراءة تاروت", reading_result, chosen_card["display_name"])
        update_reading_stats("قراءة تاروت", chosen_card["display_name"], chosen_card["name"])
        st.session_state.last_tarot_card = chosen_card
        
        if image_url:
            tarot_message, tarot_advice = generate_tarot_insight(chosen_card, user_intention, user_context)
            st.session_state.tarot_rating = 3
            st.markdown(f"""
            <div class="tarot-card-visual">
                <div style="font-size:15px; color:rgba(255,215,0,0.6); letter-spacing:2px; font-weight:600;">TAROT ORACLE</div>
                <img src="{image_url}" alt="صورة كارت التاروت {chosen_card['name']}" referrerpolicy="no-referrer" loading="lazy" style="width:100%; max-width:360px; height:auto; object-fit:contain; border-radius:18px; border:3px solid rgba(255,255,255,0.18); box-shadow:0 0 55px rgba(255,215,0,0.35); margin-top:18px;" />
                <div style="position:absolute; bottom:24px; left:24px; right:24px; padding:14px; background:rgba(0,0,0,0.24); border:1px solid rgba(255,255,255,0.08); border-radius:18px; backdrop-filter:blur(8px); color:#fde8a6; font-size:14px; line-height:1.6;">{chosen_card['display_name']}<br><span style="color:#ff79c6; font-size:13px;">{chosen_card.get('subtitle', '')}</span></div>
            </div>
            <div class="result-box">
                <h3 style="color:#00ffcc; text-align:center;">📜 رسالة التاروت لك اليوم:</h3>
                <p style="font-size:16px; color:#ffd700; margin-bottom:18px;"><b>🔮 دلالة الكارت:</b> {tarot_message}</p>
                <div style="width:100%; height:1px; background:linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent); margin:18px 0;"></div>
                <p style="font-size:16px; color:#00ffcc; line-height:1.75; margin-top:10px;"><b>✨ النصيحة الكونية:</b><br>{tarot_advice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown("<h4 style='color:#bb86fc; text-align:center;'>⭐ اختر تقييمك من 5 نجوم</h4>", unsafe_allow_html=True)
            star_cols = st.columns(5)
            for idx, star_col in enumerate(star_cols, start=1):
                with star_col:
                    if st.button("★" * idx, key=f"tarot_star_{idx}"):
                        st.session_state.tarot_rating = idx
            rating = st.session_state.get('tarot_rating', 3)
            st.markdown(f"<div style='text-align:center; color:#ffd700; font-size:22px; margin-top: 12px;'>{'★'*rating}{'☆'*(5-rating)}</div>", unsafe_allow_html=True)
            comment = st.text_area("📝 أضف تعليقك (اختياري):", height=80, placeholder="ما رأيك في هذه القراءة؟", key="tarot_comment")
            
            if st.button("📊 حفظ التقييم"):
                save_feedback("قراءة تاروت", rating, comment)
                st.success("✅ شكراً على تقييمك! تساعدنا في تحسين الخدمة")
            
            if st.button("❤️ احفظ هذه القراءة"):
                reading_entry = {
                    "type": "قراءة تاروت",
                    "result": reading_result,
                    "input": chosen_card["display_name"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "date": datetime.now().strftime("%d/%m/%Y")
                }
                add_to_favorites(reading_entry)
                st.success("✅ تمت إضافة القراءة للمفضلات!")

# --- 6. حاسبة الكرمة ---
with tabs[5]:
    st.subheader("⚖️ حاسبة الكرمة والديون الطاقية")
    k_name = st.text_input("أدخل الاسم لمعرفة رصيد ومؤشر الكرمة الحالي:", placeholder="اكتب الاسم هنا...", key="k_n")
    if st.button("⚖️ احسب مؤشر الكرمة الكونية"):
        valid, msg = validate_arabic_name(k_name)
        
        if not valid:
            st.markdown(f'<div class="error-message">❌ {msg}</div>', unsafe_allow_html=True)
        else:
            k_score, karma_label, debt_message, karma_message = generate_karma_reading(k_name)
            save_to_history("حساب الكرمة", f"مؤشر الكرمة: {k_score} | ديون طاقية: {debt_message}", k_name)
            
            st.markdown(f"""
            <div class="result-box">
                <h4 style="color:#ffd700;">⚖️ لوحة توجيه الكرمة الحالية للاسم:</h4>
                <p style="font-size:17px; line-height:1.6; color: #ffffff;"><b>{karma_label}</b></p>
                <p style="font-size:15px; line-height:1.6; color: #a1ffce;">🌗 {debt_message}</p>
                <p style="font-size:16px; margin-top:12px; line-height:1.7; color: #ffffff;">💬 {karma_message}</p>
                <p style="font-size:14px; margin-top:10px; color: #f8f8f2;">🔁 قراءة مُتغيرة تتأثر بالطاقة الزمنية الحالية لهذا اللحظة.</p>
            </div>
            """, unsafe_allow_html=True)

# --- 7. صيدلية الطاقة والأحجار ---
with tabs[6]:
    st.subheader("💎 صيدلية الطاقة وتوصيات الأحجار الكريمة المناسبة")
    energy_states = st.multiselect("ما هي الحالة الطاقية أو التحدي الحالي المراد علاجه وموازنته؟", [
        "التشتت الذهني وضياع التركيز 🧠",
        "الخمول الجسدي ونقص الحماس والاندفاع 🔋",
        "العصبية الزائدة والتوتر العاطفي والقلبي 💢",
        "ضعف الحظوظ وتأخر الفرص المالية والوفرة 💰",
        "القلق والتخوف المستمر 🔍",
        "انخفاض الإبداع والانعزال 🎨",
        "انعدام الحماية والطاقة الواهنة 🛡️"
    ], default=["التشتت الذهني وضياع التركيز 🧠"])

    intention = st.selectbox("ما الطاقة التي تريد استقطابها الآن؟", [
        "الوضوح والتركيز",
        "الحيوية والتحفيز",
        "الهدوء والتوازن العاطفي",
        "الثقة والجاذبية",
        "الحماية والسكينة"
    ])

    stone_db = {
        "التشتت الذهني وضياع التركيز 🧠": {"حجر": "الجمشت البنفسجي (Amethyst) 🔮", "نصيحة": "يعمل على تهدئة ذبذبات العقل وتطهير شاكرا العين الثالثة لزيادة الحكمة، النقاء، والتركيز العالي.", "chakra": "الطرف الثالث"},
        "الخمول الجسدي ونقص الحماس والاندفاع 🔋": {"حجر": "العقيق الأحمر (Carnelian) 🩸", "نصيحة": "يشحن شاكرا الجذر والطاقة الحيوية، ويعيد الشغف المفقود لتنفيذ أهدافك المؤجلة.", "chakra": "الجذر/الحوض"},
        "العصبية الزائدة والتوتر العاطفي والقلبي 💢": {"حجر": "الكوارتز الوردي (Rose Quartz) 💖", "نصيحة": "يساعد في موازنة شاكرا القلب ونشر طاقة السلام الذاتي، الهدوء، والتشافي من الضغوط العاطفية.", "chakra": "القلب"},
        "ضعف الحظوظ وتأخر الفرص المالية والوفرة 💰": {"حجر": "السيترين الذهبي (Citrine) 🪙", "نصيحة": "يجذب الوفرة ويحفز شاكرا الضفيرة الشمسية لفتح أبواب الفرص والنجاح.", "chakra": "الضفيرة الشمسية"},
        "القلق والتخوف المستمر 🔍": {"حجر": "اللابرادوريت (Labradorite) 🌌", "نصيحة": "يوفر حماية نفسية ويقوي الحدس، فيساعدك على تجاوز الخوف والتردد.", "chakra": "الجبهة"},
        "انخفاض الإبداع والانعزال 🎨": {"حجر": "الفلوريت الأخضر (Green Fluorite) 🌿", "نصيحة": "يفتح آفاق الإبداع ويوازن الأفكار، ويعيدك إلى تواصل أكثر وضوحاً مع طاقتك الداخلية.", "chakra": "التاج/الطرف الثالث"},
        "انعدام الحماية والطاقة الواهنة 🛡️": {"حجر": "الترمالين الأسود (Black Tourmaline) 🛡️", "نصيحة": "ينقي الطاقة السلبية ويعزز شعور الأمان والحماية داخل الحقل الطاقي.", "chakra": "الجذر"}
    }
    intention_db = {
        "الوضوح والتركيز": {"حجر": "العقيق الأزرق (Blue Lace Agate) 🔵", "نصيحة": "يطهر طاقة الحنجرة ويساعدك في التعبير الواضح والتفكير الواضح.", "chakra": "الحنجرة"},
        "الحيوية والتحفيز": {"حجر": "حجر الشمس (Sunstone) ☀️", "نصيحة": "يزيد الحافز ويمنحك طاقة متجددة لتجاوز الكسل والتردد.", "chakra": "الشمسية"},
        "الهدوء والتوازن العاطفي": {"حجر": "الكوارتز الوردي (Rose Quartz) 💗", "نصيحة": "يعزز السلام الداخلي وحب الذات، ويدعم توازن الشاكرات العاطفية.", "chakra": "القلب"},
        "الثقة والجاذبية": {"حجر": "عين النمر (Tiger's Eye) 🐯", "نصيحة": "يزيد الثقة بالنفس ويحفز حضورك الشخصي وجاذبيتك.", "chakra": "الشمسية"},
        "الحماية والسكينة": {"حجر": "الترمالين الأسود (Black Tourmaline) 🛡️", "نصيحة": "ينقي المجال ويعزز شعور الأمان والاستقرار الذهني.", "chakra": "الجذر"}
    }

    def render_crystal_recommendation(selected_states, selected_intention):
        if not selected_states:
            selected_states = ["التشتت الذهني وضياع التركيز 🧠"]

        selected_stones = []
        selected_notes = []
        selected_chakras = []
        for state in selected_states:
            info = stone_db[state]
            selected_stones.append(info["حجر"])
            selected_notes.append(f"• {info['حجر']}: {info['نصيحة']}")
            selected_chakras.append(info["chakra"])

        intention_info = intention_db[selected_intention]
        if intention_info["حجر"] not in selected_stones:
            selected_stones.append(intention_info["حجر"])
            selected_notes.append(f"• {intention_info['حجر']}: {intention_info['نصيحة']}")
            selected_chakras.append(intention_info["chakra"])

        if len(selected_states) == 1:
            combo_note = "هذا الحجر هو الخيار الأذكى لحالتك الطاقية الحالية وسيمنحك دعمًا مباشرًا وواضحًا."
        elif len(selected_states) == 2:
            combo_note = "الجمع بين الحجرين يمنحك توازنًا مزدوجًا بين الطاقة العقلية والعاطفية أو الجسدية."
        else:
            combo_note = "هذا المزيج المتعدد يدل على أنك بحاجة إلى صيدلية طاقة اختصاصية؛ استخدم الحجر الأول صباحًا والثاني خلال التأمل."

        combined_stones = "، ".join(dict.fromkeys(selected_stones))
        chakra_set = "، ".join(dict.fromkeys(selected_chakras))

        st.markdown(f"""
        <div class="result-box">
            <h4 style="color:#00ffcc;">💎 الأحجار المقترحة لك الآن:</h4>
            <p style="font-size:16px; color:#ffffff; margin-bottom:8px;"><b>{combined_stones}</b></p>
            <p style="font-size:15px; line-height:1.7; color:#a1ffce;">🔹 توجه الطاقية المستهدفة: <b>{selected_intention}</b></p>
            <p style="font-size:14px; line-height:1.7; color:#dcd6ff;">🔶 الشاكرات الموصى بها للعمل مع هذه المجموعة: <b>{chakra_set}</b></p>
            <p style="font-size:15px; margin-top:12px; line-height:1.7; color:#f8f8ff;">💡 <b>توجيه صيدلية الطاقة الذكية:</b> {combo_note}</p>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:14px; margin-top:12px;">
                <h4 style="color:#ffb86c; margin:0 0 10px 0;">🧪 وصفة الأحجار المختارة</h4>
                <p style="font-size:14px; line-height:1.8; color:#e6e6ff;">{'<br>'.join(selected_notes)}</p>
            </div>
            <div style="font-size:14px; margin-top:14px; color:#c2ffda; line-height:1.6;">
                🔸 إذا استخدمت أكثر من حجر، ابدأ بالحجر الأول في الصباح، ثم احمله معك أو ضع الثاني تحت وسادًة.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    submit = col1.button("💎 استخرج الحجر المناسب والعلاج الطاقي")
    randomize = col2.button("🔀 صيدلية طاقة عشوائية")

    if submit:
        render_crystal_recommendation(energy_states, intention)

    if randomize:
        rand_states = random.sample(list(stone_db.keys()), k=random.randint(1, 3))
        rand_intent = random.choice(list(intention_db.keys()))
        render_crystal_recommendation(rand_states, rand_intent)

# --- 8. اختبار الحالة والظل ---
with tabs[7]:
    st.subheader("🧠 اختبار الحالة النفسية ومواجهة جانب الظل (Shadow Work)")
    st.write("أجب بصدق عن الأسئلة التالية ليكشف لك التحليل شعورك الداخلي، نمط الظل، وخطة العلاج المناسبة:")

    shadow_q1 = st.radio("1. عندما تشعر بضغط نفسي، كيف تتصرف عادة؟", [
        "أتحول إلى نقد نفسي شديد وأشعر بأنني غير كافٍ",
        "أحاول إنقاذ الآخرين وأضع طاقتي جانباً",
        "أبتعد أو أسحب نفسي للحماية",
        "أبحث عن موافقة الآخرين لأشعر بقيمتي"
    ], key="shadow_q1")

    shadow_q2 = st.radio("2. ما هو أكثر ما يزعجك في علاقاتك الحالية؟", [
        "الخوف من النقد أو عدم تقدير مجهوداتي",
        "الشعور بثقل المسؤولية تجاه أحدهم",
        "القلق من فقدان الأمان المالي أو المهني",
        "عدم القدرة على وضع حدود واضحة"
    ], key="shadow_q2")

    shadow_q3 = st.radio("3. كيف تصف حالتك العاطفية في العلاقات اليوم؟", [
        "حساس ومتهيج بسهولة",
        "مرهق ومتردد في التعبير",
        "متوجس من أن يتطلبني الآخرون أكثر من طاقتي",
        "أشعر أنني غير مسموع وأحاول إرضاء الجميع"
    ], key="shadow_q3")

    shadow_q4 = st.radio("4. ما هو أكبر حاجز أمامك الآن؟", [
        "الشعور بالتقصير المستمر",
        "الخوف من الظهور أو الانتقاد",
        "الصعوبة في قول 'لا' للآخرين",
        "التردد في الاعتماد على نفسي فقط"
    ], key="shadow_q4")

    energy_level = st.radio("5. كيف تقيم طاقتك النفسية الآن؟", [
        "1 - منهك جداً ومحتاج إلى توقف فوري",
        "2 - متعب وعليك أن تعيد شحن طاقتك",
        "3 - متوسط الوضعية؛ بحاجة إلى دعم بسيط",
        "4 - قريب من التوازن لكن لا تزال تحتاج وضوحاً",
        "5 - طاقة جيدة وأقل مقاومة نفسية"
    ], index=2, key="shadow_energy")

    if st.button("🔍 كشف وتحليل الحالة النفسية والظل"):
        answer_map = {
            "أتحول إلى نقد نفسي شديد وأشعر بأنني غير كافٍ": "الخوف من النقد أو عدم تقدير مجهوداتي الصادقة من الآخرين",
            "أحاول إنقاذ الآخرين وأضع طاقتي جانباً": "الشعور بالمسؤولية المفرطة والثقيلة تجاه سعادة وراحة المحيطين بي",
            "أبتعد أو أسحب نفسي للحماية": "أفضل الابتعاد عن المواجهة وأشعر بأنني أفقد طاقتي عندما يطلبون مني الكثير",
            "أبحث عن موافقة الآخرين لأشعر بقيمتي": "أشعر بأنني أضطر لإثبات نفسي باستمرار حتى يشعر الآخرون بقيمتي",
            "الخوف من النقد أو عدم تقدير مجهوداتي": "الخوف من النقد أو عدم تقدير مجهوداتي الصادقة من الآخرين",
            "الشعور بثقل المسؤولية تجاه أحدهم": "الشعور بالمسؤولية المفرطة والثقيلة تجاه سعادة وراحة المحيطين بي",
            "القلق من فقدان الأمان المالي أو المهني": "القلق المستمر من التغيرات المفاجئة أو الخوف من فقدان الأمان المالي والمهني",
            "عدم القدرة على وضع حدود واضحة": "أجد صعوبة في وضع حدود واضحة وأقبل الكثير من الطلبات رغم شعوري بعدم الراحة",
            "حساس ومتهيج بسهولة": "الخوف من النقد أو عدم تقدير مجهوداتي الصادقة من الآخرين",
            "مرهق ومتردد في التعبير": "أجد صعوبة في وضع حدود واضحة وأقبل الكثير من الطلبات رغم شعوري بعدم الراحة",
            "متوجس من أن يتطلبني الآخرون أكثر من طاقتي": "الشعور بالمسؤولية المفرطة والثقيلة تجاه سعادة وراحة المحيطين بي",
            "أشعر أنني غير مسموع وأحاول إرضاء الجميع": "أشعر بأنني أضطر لإثبات نفسي باستمرار حتى يشعر الآخرون بقيمتي",
            "الشعور بالتقصير المستمر": "أشعر بأنني أضطر لإثبات نفسي باستمرار حتى يشعر الآخرون بقيمتي",
            "الخوف من الظهور أو الانتقاد": "الخوف من النقد أو عدم تقدير مجهوداتي الصادقة من الآخرين",
            "الصعوبة في قول 'لا' للآخرين": "أجد صعوبة في وضع حدود واضحة وأقبل الكثير من الطلبات رغم شعوري بعدم الراحة",
            "التردد في الاعتماد على نفسي فقط": "أفضل الابتعاد عن المواجهة وأشعر بأنني أفقد طاقتي عندما يطلبون مني الكثير"
        }

        selected_answers = [
            answer_map[shadow_q1],
            answer_map[shadow_q2],
            answer_map[shadow_q3],
            answer_map[shadow_q4]
        ]

        energy_value = int(energy_level.split(" - ")[0]) if isinstance(energy_level, str) else int(energy_level)
        analysis = analyze_psych_shadow(selected_answers, energy_value)
        therapy_plan = get_shadow_therapy(analysis["shadow_pattern"], energy_value)
        folk_connection = get_folk_connection(analysis["shadow_pattern"])

        save_to_history("تحليل الظل", analysis["shadow_pattern"], "; ".join(selected_answers))

        st.markdown(f"""
        <div class="result-box" style="border:2px solid rgba(255,121,198,0.35); padding:22px; background:rgba(20,12,40,0.75);">
            <h3 style="color:#ff79c6; margin-bottom:12px;">🧠 الملف الشخصي النفسي والظل</h3>
            <div style="display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:14px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(187,134,252,0.25); border-radius:14px; padding:14px;">
                    <h4 style="color:#00ffcc; margin:0 0 8px 0;">🧠 الحالة العقلية</h4>
                    <p style="margin:0; color:#e7e1ff;">{analysis['mental_state']}</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,121,198,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#ffd700; margin:0 0 8px 0;">❤️ الحالة العاطفية</h4>
                    <p style="margin:0; color:#e7e1ff;">{analysis['emotional_state']}</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(0,255,204,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#ff79c6; margin:0 0 8px 0;">🤝 الحالة الاجتماعية</h4>
                    <p style="margin:0; color:#e7e1ff;">{analysis['social_state']}</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,183,77,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#b39ddb; margin:0 0 8px 0;">🌑 نمط الظل</h4>
                    <p style="margin:0; color:#e7e1ff;">{analysis['shadow_pattern']}</p>
                </div>
            </div>
            <p style="margin:16px 0 0 0; color:#d9d2ff; font-size:14px;">🔎 السبب الأساسي المفعل: <b>{analysis['core_issue']}</b></p>
            <p style="margin:10px 0 0 0; color:#cbd5ff; font-size:13px;">⚡ مستوى الطاقة النفسية الآن: <b>{analysis['energy_label']}</b></p>
            <p style="margin:12px 0 0 0; color:#a1ffce; font-size:13px;">💡 {analysis['dynamic_note']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box" style="border:2px solid rgba(0,191,165,0.35); padding:22px; background:rgba(8,20,40,0.8); margin-top:18px;">
            <h3 style="color:#00e5ff; margin-bottom:12px;">🛠️ خطة العلاج والدعم النفسي</h3>
            <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:12px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(0,255,189,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#ffcc80; margin:0 0 8px 0;">🌿 يومي</h4>
                    <p style="margin:0; color:#e7f8ff;">{therapy_plan['daily']}</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(103,58,183,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#ffab91; margin:0 0 8px 0;">🗓️ أسبوعي</h4>
                    <p style="margin:0; color:#e7f8ff;">{therapy_plan['weekly']}</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,241,118,0.2); border-radius:14px; padding:14px;">
                    <h4 style="color:#b39ddb; margin:0 0 8px 0;">🔮 روحي</h4>
                    <p style="margin:0; color:#e7f8ff;">{therapy_plan['spiritual']}</p>
                </div>
            </div>
            <p style="margin:16px 0 0 0; color:#c3e8ff; font-size:14px;">{folk_connection}</p>
        </div>
        """, unsafe_allow_html=True)

# --- 9. الرقم الروحي السري ---
with tabs[8]:
    st.subheader("🔢 حساب واستخراج الرقم الروحي السري ورسالته الكونية")
    r_date = st.date_input("اختر تاريخ الميلاد بدقة لاستخراج رقم مسار الحياة المخصص:", min_value=datetime(1950, 1, 1), key="r_d")
    if st.button("🔢 احسب الرقم الروحي السري للقدر"):
        # التحقق من صحة التاريخ
        valid_date, msg_date = validate_date(r_date)
        
        if not valid_date:
            st.markdown(f'<div class="error-message">❌ {msg_date}</div>', unsafe_allow_html=True)
        else:
            date_str = r_date.strftime("%Y%m%d")
            total_digits = sum(int(d) for d in date_str)
            while total_digits > 9:
                total_digits = sum(int(d) for d in str(total_digits))
                
            num_meanings = {
                1: "رقم القائد والمبتكر؛ رسالتك الكونية هي بدء المسارات الجديدة وإلهام غيرك، وعدم السير خلف القطيع.",
                2: "رقم الدبلوماسي والموازن؛ طاقتك تزدهر في الشراكات المتزنة، نشر السلام، وفك النزاعات بحكمة وروية.",
                3: "رقم المتصل والمبدع؛ رسالتك الكونية هي التعبير عن الذات والوعي من خلال الفن، الكتابة، أو صناعة المحتوى والبث.",
                4: "رقم الباني والمنظم؛ قوتك تكمن في وضع الأسس المتينة والالتزام الفائق، وصناعة استقرار مالي طويل الأمد ومثمر.",
                5: "رقم المغامر والمتحرر؛ مسارك مليء بالتحولات السريعة والسفر والتنقل، وقدرتك هائلة على التكيف الجغرافي والروحي الحاد.",
                6: "رقم الحاضن والمعالج؛ طاقتك الفطرية مرتبطة بتحمل المسؤوليات العائلية بنجاح، وتضميد جراح الآخرين النفسية والجسدية.",
                7: "رقم المفكر والمستبصر؛ أنت باحث عميق جداً عن الحقائق وأسرار الكون، وتزدهر طاقتك بالخلوات والروحانيات الخالصة بانتظام.",
                8: "رقم الوفرة والسلطة والقدرة المادية؛ مسارك مرتبط بإتقان التعامل مع القوانين المادية والمالية وتحقيق النجاحات القيادية الكبرى ومساعدة المجتمع.",
                9: "رقم المعلم الكوني والإنساني الشامل؛ وصلت لأعلى درجات النضج الروحي، ورسالتك تقديم الدعم والإرشاد اللامشروط والارتقاء بوعي البشرية."
            }
            
            save_to_history("الرقم الروحي", f"الرقم: {total_digits}", str(r_date))
            
            st.markdown(f"""
            <div class="result-box" style="text-align: center;">
                <h4 style="color:#ffd700;">🔢 رقمك الروحي السري المهيمن هو:</h4>
                <h1 style="color:#00ffcc; font-size:48px; margin:10px 0; font-weight:800;">{total_digits}</h1>
                <p style="font-size:16px; text-align:right; line-height:1.6; color:#ffffff;">✨ <b>الرسالة المقدرة لمسار حياتك الروحاني:</b> {num_meanings[total_digits]}</p>
            </div>
            """, unsafe_allow_html=True)