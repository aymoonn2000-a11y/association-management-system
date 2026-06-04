import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة والديزاين العام
st.set_page_config(
    page_title="نظام إدارة الجمعية المتكامل",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق ستايل CSS مخصص لتحسين المظهر والخطوط
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div.stButton > button:first-child {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 16px;
    }
    .sidebar .sidebar-content { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1f77b4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
""", unsafe_style_html=True)

# تهيئة الجلسات (Session State) لحفظ البيانات مؤقتاً أثناء التشغيل
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'employees' not in st.session_state:
    st.session_state.employees = []
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# --- 1. نظام تسجيل الدخول ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔒 تسجيل الدخول إلى النظام</h1>", unsafe_style_html=True)
    
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
    # القائمة الجانبية للتنقل
    st.sidebar.markdown("<h2 style='text-align: center;'>📋 القائمة الرئيسية</h2>", unsafe_style_html=True)
    st.sidebar.markdown(f"**مرحباً بك:** {st.session_state.get('username', 'aymanyaghi')}")
    
    menu = st.sidebar.radio(
        "اختر القسم:",
        ["💰 المصروفات اليومية", "👥 شؤون الموظفين والعهدة", "📦 جرد وإحصاء المكتب", "🚪 تسجيل الخروج"]
    )
    
    # زر تسجيل الخروج
    if menu == "🚪 تسجيل الخروج":
        st.session_state.logged_in = False
        st.rerun()

    # --- 2. قسم المصروفات اليومية ---
    elif menu == "💰 المصروفات اليومية":
        st.title("💰 إدارة المصروفات اليومية")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ إضافة مصروف جديد")
            exp_date = st.date_input("تاريخ الصرف", datetime.now())
            
            # خيار متعدد للسلع
            exp_types = st.multiselect(
                "نوع السلعة / الخدمة",
                ["مواصلات", "مياه", "أخرى"],
                default=["مواصلات"]
            )
            
            exp_details = st.text_input("تفاصيل إضافية عن السلعة", placeholder="مثال: شراء مياه شرب للمكتب")
            exp_price = st.number_input("السعر (بشيكل ₪)", min_value=0.0, step=1.0, format="%.2f")
            
            if st.button("حفظ المصروف"):
                if not exp_types:
                    st.warning("الرجاء اختيار نوع السلعة واحد على الأقل.")
                elif exp_price <= 0:
                    st.warning("الرجاء إدخال سعر صحيح أكبر من صفر.")
                else:
                    types_str = ", ".join(exp_types)
                    st.session_state.expenses.append({
                        "التاريخ": exp_date.strftime("%Y-%m-%d"),
                        "نوع السلعة": types_str,
                        "التفاصيل": exp_details,
                        "السعر (شيكل)": exp_price
                    })
                    st.success("تم تسجيل المصروف بنجاح!")
        
        with col2:
            st.subheader("📊 جدول المصروفات المسجلة")
            if st.session_state.expenses:
                df_exp = pd.DataFrame(st.session_state.expenses)
                st.dataframe(df_exp, use_container_width=True)
                
                # حساب المجموع الكلي تلقائياً
                total_sum = df_exp["السعر (شيكل)"].sum()
                st.markdown(f"### 🧮 المجموع الكلي: <span style='color:green; font-size:28px;'>{total_sum:.2f} ₪</span>", unsafe_style_html=True)
            else:
                st.info("لا توجد مصروفات مسجلة بعد اليوم.")

    # --- 3. قسم شؤون الموظفين والعهدة ---
    elif menu == "👥 شؤون الموظفين والعهدة":
        st.title("👥 إدارة الموظفين والعهدة الشخصية")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ إضافة موظف وعهدة")
            emp_name = st.text_input("اسم الموظف")
            emp_id = st.text_input("رقم الهوية")
            emp_phone = st.text_input("رقم الجوال")
            emp_title = st.text_input("المسمى الوظيفي")
            
            # اختيار البرنامج التابع له
            emp_program = st.selectbox(
                "البرنامج التابع له",
                ["Shelter", "CVA", "WASH", "Program", "Administrative Assistant", "Manager"]
            )
            
            # اختيار متعدد للعهدة المستلمة
            emp_assets = st.multiselect(
                "العهدة التي تم استلامها من الجمعية",
                ["تيشيرت", "لاب توب", "أيباد", "قرطاسية", "أخرى"]
            )
            
            if st.button("حفظ بيانات الموظف"):
                if not emp_name or not emp_id:
                    st.warning("الرجاء إدخال اسم الموظف ورقم الهوية على الأقل.")
                else:
                    assets_str = ", ".join(emp_assets) if emp_assets else "لا يوجد"
                    st.session_state.employees.append({
                        "اسم الموظف": emp_name,
                        "رقم الهوية": emp_id,
                        "رقم الجوال": emp_phone,
                        "المسمى الوظيفي": emp_title,
                        "البرنامج": emp_program,
                        "العهدة المستلمة": assets_str
                    })
                    st.success(f"تم تسجيل الموظف {emp_name} بنجاح!")
                    
        with col2:
            st.subheader("📋 كشف الموظفين والعهدة")
            if st.session_state.employees:
                df_emp = pd.DataFrame(st.session_state.employees)
                st.dataframe(df_emp, use_container_width=True)
            else:
                st.info("لا توجد بيانات موظفين مسجلة حالياً.")

    # --- 4. قسم جرد وإحصاء المكتب ---
    elif menu == "📦 جرد وإحصاء المكتب":
        st.title("📦 جرد وإحصاء محتويات المكتب")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("➕ إضافة مادة/أصل للمكتب")
            item_name = st.text_input("اسم المادة / الغرض", placeholder="مثال: كراسي، طابعات، ورق A4")
            item_qty = st.number_input("الكمية المتوفرة", min_value=0, step=1)
            item_notes = st.text_area("ملاحظات (إن وجدت)", placeholder="مثال: تحتاج إلى صيانة، أو مخزون قار ب على الانتهاء")
            
            if st.button("إضافة إلى الجرد"):
                if not item_name:
                    st.warning("الرجاء إدخال اسم المادة.")
                else:
                    st.session_state.inventory.append({
                        "اسم المادة / الغرض": item_name,
                        "الكمية المتوفرة": item_qty,
                        "ملاحظات": item_notes if item_notes else "لا يوجد"
                    })
                    st.success(f"تم إضافة {item_name} إلى قائمة الجرد.")
                    
        with col2:
            st.subheader("📊 قائمة المواد المتوفرة بالمكتب")
            if st.session_state.inventory:
                df_inv = pd.DataFrame(st.session_state.inventory)
                st.dataframe(df_inv, use_container_width=True)
            else:
                st.info("قائمة الجرد فارغة حالياً.")
