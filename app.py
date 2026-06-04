import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 1. إعدادات الصفحة والديزاين العام
st.set_page_config(
    page_title="نظام إدارة الجمعية المتكامل",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تطبيق ستايل CSS مخصص متطور للواجهة والبطاقات والشعار
st.markdown("""
<style>
.main { text-align: right; direction: rtl; }
div.stButton > button:first-child {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 2rem;
    font-size: 16px;
    width: 100%;
}
.sidebar .sidebar-content { background-color: #f8f9fa; }
h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

/* تصميم الشعار الاحترافي */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 20px;
    background: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.logo-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #1f77b4, #00d2ff);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
}
.logo-text {
    font-size: 28px;
    font-weight: 800;
    color: #1f77b4;
    letter-spacing: 1px;
    font-family: 'Century Gothic', sans-serif;
}
.logo-subtext {
    font-size: 14px;
    color: #888;
}

/* كرت الترحيب */
.welcome-card {
    background: linear-gradient(135deg, #1f77b4, #00d2ff);
    color: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.info-box {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border-right: 5px solid #1f77b4;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 3. دالات إدارة وحفظ البيانات الدائمة (JSON)
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 4. تهيئة الجلسات وتحميل البيانات المخزنة تلقائياً
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_data('expenses.json')
if 'employees' not in st.session_state:
    st.session_state.employees = load_data('employees.json')
if 'inventory' not in st.session_state:
    st.session_state.inventory = load_data('inventory.json')

# --- نظام تسجيل الدخول ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔒 تسجيل الدخول إلى النظام</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم هنا")
        password = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور هنا")
        login_button = st.button("دخول")
        
        if login_button:
            if username == "aymanyaghi" and password == "12345":
                st.session_state.logged_in = True
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

# --- بعد تسجيل الدخول بنجاح ---
else:
    # عرض الشعار الاحترافي أعلى القائمة الجانبية
    st.sidebar.markdown("""
    <div class="logo-container">
        <div class="logo-icon">A</div>
        <div>
            <div class="logo-text">AYMAN</div>
            <div class="logo-subtext">Management System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<h2 style='text-align: center; color: #1f77b4;'>📋 القائمة الرئيسية</h2>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio(
        "اختر القسم:",
        ["🏠 الشاشة الرئيسية", "💰 المصروفات اليومية", "👥 شؤون الموظفين والعهدة", "📦 جرد وإحصاء المكتب", "🚪 تسجيل الخروج"]
    )
    
    if menu == "🚪 تسجيل الخروج":
        st.session_state.logged_in = False
        st.rerun()

    # --- 1. الشاشة الرئيسية مع لوحة التحليلات البيانية ---
    elif menu == "🏠 الشاشة الرئيسية":
        st.markdown("""
        <div class="welcome-card">
            <h1 style="color: white; margin: 0; font-family: 'Century Gothic', sans-serif;">Hello my dear</h1>
            <p style="font-size: 18px; margin-top: 10px;">مرحباً بك في نظام إدارة الجمعية المتكامل الخاص بك</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <h3 style="margin:0; color:#1f77b4;">📅 التاريخ اليوم</h3>
                <p style="font-size: 20px; font-weight: bold; margin-top: 10px;">{datetime.now().strftime('%A, %Y-%m-%d')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <h3 style="margin:0; color:#1f77b4;">⏰ الوقت الحالي</h3>
                <p style="font-size: 20px; font-weight: bold; margin-top: 10px;">{datetime.now().strftime('%I:%M %p')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><h3>📊 نظرة عامة على مصروفات النظام</h3>", unsafe_allow_html=True)
        
        if st.session_state.expenses:
            df_all = pd.DataFrame(st.session_state.expenses)
            # رسم بياني لتوزيع المصروفات حسب الفئة
            df_chart = df_all.groupby("نوع السلعة")["السعر (شيكل)"].sum().reset_index()
            st.bar_chart(data=df_chart, x="نوع السلعة", y="السعر (شيكل)", use_container_width=True)
        else:
            st.info("لا توجد بيانات مصروفات كافية لعرض الرسم البياني حالياً.")

    # --- 2. قسم المصروفات اليومية والشهرية (مع الحذف) ---
    elif menu == "💰 المصروفات اليومية":
        st.title("💰 إدارة المصروفات اليومية والشهرية")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ إضافة مصروف جديد")
            exp_date = st.date_input("تاريخ الصرف", datetime.now())
            exp_types = st.multiselect("نوع السلعة / الخدمة", ["مواصلات", "مياه", "أخرى"], default=["مواصلات"])
            exp_details = st.text_input("تفاصيل إضافية عن السلعة")
            exp_price = st.number_input("السعر (بشيكل ₪)", min_value=0.0, step=1.0, format="%.2f")
            
            if st.button("حفظ المصروف"):
                if not exp_types or exp_price <= 0:
                    st.warning("الرجاء التحقق من البيانات المدخلة.")
                else:
                    types_str = ", ".join(exp_types)
                    st.session_state.expenses.append({
                        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                        "التاريخ": exp_date.strftime("%Y-%m-%d"),
                        "الشهر المستهدف": exp_date.strftime("%Y-%m"),
                        "نوع السلعة": types_str,
                        "التفاصيل": exp_details,
                        "السعر (شيكل)": exp_price
                    })
                    save_data('expenses.json', st.session_state.expenses)
                    st.success("تم الحفظ!")
                    st.rerun()
        
        with col2:
            st.subheader("📊 كشوفات المصروفات")
            if st.session_state.expenses:
                df_all = pd.DataFrame(st.session_state.expenses)
                available_months = sorted(list(df_all["الشهر المستهدف"].unique()), reverse=True)
                selected_month = st.selectbox("📂 اختر الشهر:", available_months)
                
                df_filtered = df_all[df_all["الشهر المستهدف"] == selected_month].copy()
                st.dataframe(df_filtered.drop(columns=["id", "الشهر المستهدف"]), use_container_width=True)
                
                # خيار حذف مصروف معين برقم تعريفه
                delete_id = st.selectbox("🗑️ اختر سطر لحذفه (حسب التفاصيل):", df_filtered["id"].tolist(), format_func=lambda x: next(item["التفاصيل"] for item in st.session_state.expenses if item["id"] == x))
                if st.button("حذف السطر المحدد"):
                    st.session_state.expenses = [item for item in st.session_state.expenses if item["id"] != delete_id]
                    save_data('expenses.json', st.session_state.expenses)
                    st.success("تم الحذف بنجاح!")
                    st.rerun()

    # --- 3. قسم شؤون الموظفين وتتبع العهدة المستردة ---
    elif menu == "👥 شؤون الموظفين والعهدة":
        st.title("👥 إدارة الموظفين والعهدة والتتبع")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة موظف جديد")
            emp_name = st.text_input("اسم الموظف")
            emp_id = st.text_input("رقم الهوية")
            emp_phone = st.text_input("رقم الجوال")
            emp_title = st.text_input("المسمى الوظيفي")
            emp_program = st.selectbox("البرنامج التابع له", ["Shelter", "CVA", "WASH", "Program", "Administrative Assistant", "Manager"])
            emp_assets = st.multiselect("العهدة المستلمة", ["تيشيرت", "لاب توب", "أيباد", "قرطاسية", "أخرى"])
            asset_status = st.selectbox("حالة العهدة الحالية", ["مستلمة بالكامل", "تم إرجاعها للمخزن"])
            return_date = st.text_input("تاريخ الإرجاع (إن وجد)", placeholder="مثال: 2026-06-04")
            
            if st.button("حفظ بيانات الموظف"):
                if emp_name and emp_id:
                    st.session_state.employees.append({
                        "id": emp_id,
                        "اسم الموظف": emp_name,
                        "رقم الهوية": emp_id,
                        "رقم الجوال": emp_phone,
                        "المسمى الوظيفي": emp_title,
                        "البرنامج": emp_program,
                        "العهدة المستلمة": ", ".join(emp_assets),
                        "حالة العهدة": asset_status,
                        "تاريخ الإرجاع": return_date if return_date else "N/A"
                    })
                    save_data('employees.json', st.session_state.employees)
                    st.success("تم الحفظ!")
                    st.rerun()
                    
        with col2:
            st.subheader("📋 كشف الموظفين وتتبع حالة العهد")
            if st.session_state.employees:
                df_emp = pd.DataFrame(st.session_state.employees)
                st.dataframe(df_emp.drop(columns=["id"]), use_container_width=True)
                
                delete_emp_id = st.selectbox("🗑️ اختر موظف لحذفه:", df_emp["id"].tolist(), format_func=lambda x: next(emp["اسم الموظف"] for emp in st.session_state.employees if emp["id"] == x))
                if st.button("حذف الموظف المحدد"):
                    st.session_state.employees = [emp for emp in st.session_state.employees if emp["id"] != delete_emp_id]
                    save_data('employees.json', st.session_state.employees)
                    st.success("تم الحذف!")
                    st.rerun()

    # --- 4. قسم جرد وإحصاء المكتب مع خيار التعديل والحذف ---
    elif menu == "📦 جرد وإحصاء المكتب":
        st.title("📦 جرد وإحصاء محتويات المكتب")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة مادة للمكتب")
            item_name = st.text_input("اسم المادة / الغرض")
            item_qty = st.number_input("الكمية المتوفرة", min_value=0, step=1)
            item_notes = st.text_area("ملاحظات")
            
            if st.button("إضافة إلى الجرد"):
                if item_name:
                    st.session_state.inventory.append({
                        "id": item_name,
                        "اسم المادة / الغرض": item_name,
                        "الكمية المتوفرة": item_qty,
                        "ملاحظات": item_notes if item_notes else "لا يوجد"
                    })
                    save_data('inventory.json', st.session_state.inventory)
                    st.success("تم الإضافة!")
                    st.rerun()
                    
        with col2:
            st.subheader("📊 قائمة المواد المتوفرة بالمكتب")
            if st.session_state.inventory:
                df_inv = pd.DataFrame(st.session_state.inventory)
                st.dataframe(df_inv.drop(columns=["id"]), use_container_width=True)
                
                delete_item_id = st.selectbox("🗑️ اختر مادة لحذفها:", df_inv["id"].tolist())
                if st.button("حذف المادة المحددة"):
                    st.session_state.inventory = [item for item in st.session_state.inventory if item["id"] != delete_item_id]
                    save_data('inventory.json', st.session_state.inventory)
                    st.success("تم الحذف!")
                    st.rerun()
