# -*- coding: utf-8 -*-
"""دوال عرض الخدمات التسع (أجسام التبويبات الأصلية محوّلة لدوال بدون تغيير منطقها)."""
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from html import escape
from urllib.parse import quote
import random
from engine import *


def render_0():
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
        
        # كود جدول المقارنات المتقدمة المنسق بالألوان الكونية والزجاجية
        comparison_table_html = """
        <div style="overflow-x: auto; direction: rtl; text-align: right; padding: 10px;">
            <table style="width: 100%; border-collapse: collapse; background: rgba(15, 10, 34, 0.65); border-radius: 12px; border: 1px solid rgba(0, 255, 204, 0.2); backdrop-filter: blur(8px);">
                <thead>
                    <tr style="background: linear-gradient(90deg, #1f1244 0%, #0d0621 100%); color: #00ffcc;">
                        <th style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.15);">الزوج</th>
                        <th style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.15);">نسبة التوافق</th>
                        <th style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.15);">الأبراج</th>
                        <th style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.15);">العناصر</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for i, row in enumerate(st.session_state.comparison_results):
            bg_color = "rgba(0, 255, 204, 0.03)" if i % 2 == 0 else "transparent"
            comparison_table_html += f"""
                    <tr style="background: {bg_color};">
                        <td style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.1); color: #ffffff;">{row['الزوج']}</td>
                        <td style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.1); color: #00ffcc; font-weight: bold;">{row['التوافق الرقمي']}</td>
                        <td style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.1); color: #bb86fc;">{row['الأبراج']}</td>
                        <td style="padding: 12px; border: 1px solid rgba(0, 255, 204, 0.1); color: #ff79c6;">{row['العناصر']}</td>
                    </tr>
            """
        
        comparison_table_html += """
                </tbody>
            </table>
        </div>
        """
        
        st.markdown(comparison_table_html, unsafe_allow_html=True)
        
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



def render_1():
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



def render_2():
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



def render_3():
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



def render_4():
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



def render_5():
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



def render_6():
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



def render_7():
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



def render_8():
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


