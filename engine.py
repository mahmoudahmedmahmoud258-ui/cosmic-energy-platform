# -*- coding: utf-8 -*-
"""المحرك: كل البيانات الفلكية ودوال المنطق (مفصولة آلياً من app.py الأصلي بدون تعديل)."""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from html import escape
from urllib.parse import quote
import random
import base64
import json
import re


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

