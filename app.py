import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="النظام اللوجستي الذكي لإدارة الجمعية",
    page_icon="📦",
    layout="wide"
)

# ===================================
# CSS احترافي وتنسيقات اتجاه النص (RTL)
# ===================================
st.markdown("""
<style>
.main { background:#f5f7fb; }
.title { text-align:center; padding:15px; color:#1e3a8a; }
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,.05);
    border-right: 5px solid #2563eb;
}
.metric-number { font-size: 30px; color: #2563eb; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===================================
# إدارة الجلسات وتخزين البيانات (Session State)
# ===================================
if "employees" not in st.session_state:
    st.session_state.employees = []

if "inventory" not in st.session_state:
    # أضفنا "الحد الأدنى للتنبيه"
    st.session_state.inventory = [
        {"المادة": "لاب توب", "المتوفر": 10, "الصادر": 2, "الحد الأدنى": 3},
        {"المادة": "آيباد", "المتوفر": 5, "الصادر": 1, "الحد الأدنى": 2},
        {"المادة": "قرطاسية", "المتوفر": 100, "الصادر": 20, "الحد الأدنى": 15},
        {"المادة": "تيشيرت الجمعية", "المتوفر": 4, "الصادر": 12, "الحد الأدنى": 5},
    ]

if "delivery_tasks" not in st.session_state:
    st.session_state.delivery_tasks = [
        {"التاريخ": "2026-06-03", "المهمة/الشحنة": "توصيل أوراق مالية بريد سريع", "الجهة/المستلم": "البنك الوطني", "الحالة": "جاري التنفيذ"}
    ]

# ===================================
# عنوان النظام
# ===================================
st.markdown("""
<div class='title'>
<h1>📦 لوحة التحكم اللوجستية وإدارة الحركة</h1>
<p>إدارة العهد الميدانية - المخازن - طلبات حركة المراسلين</p>
</div>
""", unsafe_allow_html=True)

# ===================================
# الحسابات الذكية لبطاقات الإحصائيات
# ===================================
total_emp = len(st.session_state.employees)
total_items = sum(x["المتوفر"] for x in st.session_state.inventory)
# تنبيه الأصناف القريبة من النفاد
shortage_items = sum(1 for x in st.session_state.inventory if x["المتوفر"] <= x["الحد الأدنى"])
active_deliveries = sum(1 for x in st.session_state.delivery_tasks if x["الحالة"] == "جاري التنفيذ")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div>عدد الموظفين مسجلي العهد</div><div class='metric-number'>{total_emp}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div>إجمالي قطع المخزن المتوفرة</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card' style='border-right-color: #ef4444;'><div>مواد تحتاج إعادة طلب ⚠️</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card' style='border-right-color: #f59e0b;'><div>مهام توصيل معلقة 🏃‍♂️</div><div class='metric-number' style='color:#f59e0b;'>{active_deliveries}</div></div>", unsafe_allow_html=True)

st.write("")

# ألسنة التبويب (Tabs) تخدم المهام اللوجستية
tab1, tab2, tab3 = st.tabs([
    "🏃‍♂️ مهام الحركة والتوصيل للمراسل",
    "👥 إدارة عهد الموظفين والبرامج",
    "📦 إدارة المخزن والوارِد"
])

# ===================================
# التبويب الأول: مهام الحركة والتوصيل
# ===================================
with tab1:
    st.subheader("📋 تسجيل وتتبع مهمة توصيل / حركة لوجستية")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        task_name = st.text_input("وصف الشحنة / الأوراق / المهمة")
    with col_t2:
        receiver = st.text_input("الجهة المستلمة / الشخص المستلم")
    with col_t3:
        status = st.selectbox("حالة المهمة المبدئية", ["جاري التنفيذ", "تم التسليم بنجاح", "ملغي"])
        
    if st.button("➕ تسجيل مهمة الحركة"):
        if task_name and receiver:
            st.session_state.delivery_tasks.append({
                "التاريخ": str(datetime.now().date()),
                "المهمة/الشحنة": task_name,
                "الجهة/المستلم": receiver,
                "الحالة": status
            })
            st.success("تم تسجيل المهمة بنجاح")
        else:
            st.error("الرجاء ملء حقول الوصف والمستلم")
            
    st.write("---")
    st.subheader("🔄 سجل حركة المراسل الحالي")
    df_tasks = pd.DataFrame(st.session_state.delivery_tasks)
    if not df_tasks.empty:
        # ميزة تعديل الحالة مباشرة من الجدول عبر Streamlit data_editor
        edited_df = st.data_editor(df_tasks, use_container_width=True)
        st.session_state.delivery_tasks = edited_df.to_dict('records')
    else:
        st.info("لا توجد مهام حركة مسجلة حالياً.")

# ===================================
# التبويب الثاني: الموظفين والعهد (مع الخصم التلقائي)
# ===================================
with tab2:
    st.subheader("👤 صرف عهدة جديدة لموظف")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        name = st.text_input("اسم الموظف المستلم")
        title = st.text_input("المسمى الوظيفي وقسم الموظف")
    with col_e2:
        program = st.selectbox("البرنامج التابع له (الميزانية)", ["CVA", "MEAL", "WASH", "Shelter", "الإدارة العامّة"])
        # جلب قائمة العهد المتوفرة في المخزن ديناميكياً
        available_items_list = [x["المادة"] for x in st.session_state.inventory]
        custody = st.multiselect("اختر المواد المراد صرفها كعهدة", available_items_list)
        
    notes = st.text_area("ملاحظات إضافية على حالة العهدة")
    
    if st.button("💾 إتمام صرف العهدة وحفظ الموظف"):
        if name and custody:
            error_flag = False
            # فحص وتحديث المخزن تلقائياً عند الصرف
            for requested_item in custody:
                for inv_item in st.session_state.inventory:
                    if inv_item["المادة"] == requested_item:
                        if inv_item["المتوفر"] >= 1:
                            inv_item["المتوفر"] -= 1
                            inv_item["الصادر"] += 1
                        else:
                            st.error(f"عذراً! المادة ({requested_item}) غير متوفرة في المخزن حالياً.")
                            error_flag = True
            
            if not error_flag:
                st.session_state.employees.append({
                    "تاريخ الصرف": str(datetime.now().date()),
                    "الاسم": name,
                    "المسمى": title,
                    "البرنامج": program,
                    "العهدة المصروفة": ", ".join(custody),
                    "ملاحظات": notes
                })
                st.success(f"تم تسجيل العهدة باسم {name} وخصم المواد من المخزن بنجاح!")
                st.rerun()
        else:
            st.error("الرجاء إدخال اسم الموظف واختيار مادة واحدة على الأقل للعهدة.")

    st.write("---")
    st.subheader("🔍 سجل العهد النشطة والبحث")
    search = st.text_input("🔍 ابحث باسم الموظف أو المادة المصروفة")
    
    df_emp = pd.DataFrame(st.session_state.employees)
    if not df_emp.empty:
        if search:
            df_emp = df_emp[df_emp["الاسم"].str.contains(search, case=False) | df_emp["العهدة المصروفة"].str.contains(search, case=False)]
        st.dataframe(df_emp, use_container_width=True)
    else:
        st.info("لا توجد عهد مسجلة حالياً.")

# ===================================
# التبويب الثالث: إدارة المخزن والوارد
# ===================================
with tab3:
    st.subheader("📥 توريد وتحديث كميات المخازن")
    
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1:
        item = st.text_input("اسم المادة الجديدة (أو اختر من القائمة لتعديلها)")
        # خيار لتسهيل الاختيار
        st.caption("أمثلة: لابتوب، قرطاسية، أدوات صيانة")
    with col_i2:
        available = st.number_input("الكمية الموردة الجديدة (الداخلة)", min_value=0, value=0)
    with col_i3:
        min_limit = st.number_input("حد الأمان (التنبيه بالنفاد)", min_value=1, value=5)
    with col_i4:
        # إمكانية تسجيل تالف أو صادر مباشر بدون موظف
        direct_issued = st.number_input("صادر مباشر / تالف من المخزن", min_value=0, value=0)
        
    if st.button("🔄 تحديث بيانات المستودع"):
        if item:
            found = False
            for i in st.session_state.inventory:
                if i["المادة"].strip() == item.strip():
                    i["المتوفر"] += available
                    i["الصادر"] += direct_issued
                    i["الحد الأدنى"] = min_limit
                    found = True
                    break
            if not found:
                st.session_state.inventory.append({
                    "المادة": item.strip(),
                    "المتوفر": available,
                    "الصادر": direct_issued,
                    "الحد الأدنى": min_limit
                })
            st.success(f"تم تحديث بيانات المخزن للمادة: {item}")
            st.rerun()
        else:
            st.error("الرجاء كتابة اسم المادة")

    st.write("---")
    st.subheader("📊 جرد المخزن الحالي")
    
    # تحويل بيانات المخزن لجدول مع إضافة تنبيه مرئي للأصناف الناقصة
    df_inv = pd.DataFrame(st.session_state.inventory)
    
    def highlight_shortage(row):
        return ['background-color: #ffcccc' if row['المتوفر'] <= row['الحد الأدنى'] else '' for _ in row]
        
    if not df_inv.empty:
        # استعراض الجدول وتلوين السطور التي تحتاج إعادة طلب باللون الأحمر الخفيف
        st.dataframe(df_inv.style.apply(highlight_shortage, axis=1), use_container_width=True)
        
        # تصدير تقرير المخزن اللوجستي لـ CSV
        csv_data = df_inv.to_csv(index=False).encode('utf-8-sig')
        st.download_button("⬇️ تحميل تقرير جرد المخزن (CSV)", csv_data, "inventory_report.csv", "text/csv")
