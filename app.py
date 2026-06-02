import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام إدارة الجمعية", layout="wide", page_icon="🏢")

# ====================== قاعدة البيانات ======================
def init_db():
    conn = sqlite3.connect('association.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS assets 
                 (id INTEGER PRIMARY KEY, asset_type TEXT, name TEXT, quantity INTEGER, 
                  location TEXT, status TEXT, date_added TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers 
                 (id INTEGER PRIMARY KEY, name TEXT, category TEXT, phone TEXT, email TEXT, address TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (id INTEGER PRIMARY KEY, name TEXT, national_id TEXT, phone TEXT, job_title TEXT, department TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY, supplier_id INTEGER, item_name TEXT, qty INTEGER, 
                  status TEXT, date TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

# ====================== الدوال المساعدة ======================
def get_suppliers_list():
    """الحصول على قائمة الموردين"""
    conn = sqlite3.connect('association.db')
    df = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
    conn.close()
    return df

# ====================== الصفحة الرئيسية ======================
st.title("🏢 نظام إدارة الجمعية المتكامل")
st.markdown("### نظام شامل لإدارة الأصول والموردين والموظفين والطلبيات")

tab1, tab2, tab3, tab4 = st.tabs(["إدارة الأصول", "الموردين", "الموظفين", "الطلبيات"])

# ================== تبويب الأصول ==================
with tab1:
    st.subheader("📦 إضافة أصل جديد")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        asset_type = st.selectbox("نوع الأصل", ["لاب توب", "طابعة", "مكتب", "كرسي", "شاشة", "لوحة مفاتيح", "ماوس", "أخرى"])
    with col2:
        asset_name = st.text_input("اسم / موديل الأصل")
    with col3:
        quantity = st.number_input("الكمية", min_value=1, value=1, step=1)
    with col4:
        location = st.text_input("الموقع / القسم")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        status = st.selectbox("حالة الأصل", ["ممتازة", "جيدة", "متوسطة", "تحتاج صيانة"])
    
    if st.button("➕ إضافة الأصل", type="primary", use_container_width=True):
        if asset_name and location:
            conn = sqlite3.connect('association.db')
            conn.execute("INSERT INTO assets (asset_type, name, quantity, location, status, date_added) VALUES (?,?,?,?,?,?)",
                        (asset_type, asset_name, quantity, location, status, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            st.success("✅ تم إضافة الأصل بنجاح!")
        else:
            st.error("❌ يرجى ملء جميع الحقول المطلوبة")

    st.divider()
    st.subheader("📋 جميع الأصول")
    conn = sqlite3.connect('association.db')
    df_assets = pd.read_sql_query("SELECT * FROM assets", conn)
    conn.close()
    
    if not df_assets.empty:
        st.dataframe(df_assets, use_container_width=True, hide_index=True)
        
        # إحصائيات
        st.subheader("📈 الإحصائيات")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("إجمالي الأصول", len(df_assets))
        with col2:
            st.metric("إجمالي الكمية", df_assets['quantity'].sum())
        with col3:
            excellent = len(df_assets[df_assets['status'] == 'ممتازة'])
            st.metric("في حالة ممتازة", excellent)
        with col4:
            needs_maintenance = len(df_assets[df_assets['status'] == 'تحتاج صيانة'])
            st.metric("تحتاج صيانة", needs_maintenance)
    else:
        st.info("لا توجد أصول مسجلة حتى الآن")

# ================== تبويب الموردين ==================
with tab2:
    st.subheader("🏪 إضافة مورد جديد")
    col1, col2, col3 = st.columns(3)
    with col1:
        supplier_name = st.text_input("اسم المورد")
    with col2:
        supplier_category = st.selectbox("فئة المورد", ["أجهزة", "مستلزمات مكتبية", "خدمات", "أخرى"])
    with col3:
        supplier_phone = st.text_input("رقم الهاتف")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        supplier_email = st.text_input("البريد الإلكتروني")
    with col_s2:
        supplier_address = st.text_input("العنوان")
    
    if st.button("➕ إضافة المورد", type="primary", use_container_width=True):
        if supplier_name and supplier_phone:
            conn = sqlite3.connect('association.db')
            conn.execute("INSERT INTO suppliers (name, category, phone, email, address) VALUES (?,?,?,?,?)",
                        (supplier_name, supplier_category, supplier_phone, supplier_email, supplier_address))
            conn.commit()
            conn.close()
            st.success("✅ تم إضافة المورد بنجاح!")
        else:
            st.error("❌ يرجى ملء الحقول المطلوبة (الاسم والهاتف)")

    st.divider()
    st.subheader("📋 جميع الموردين")
    conn = sqlite3.connect('association.db')
    df_suppliers = pd.read_sql_query("SELECT * FROM suppliers", conn)
    conn.close()
    
    if not df_suppliers.empty:
        st.dataframe(df_suppliers, use_container_width=True, hide_index=True)
        
        st.subheader("📊 إحصائيات الموردين")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("إجمالي عدد الموردين", len(df_suppliers))
        with col2:
            categories = df_suppliers['category'].nunique()
            st.metric("عدد الفئات", categories)
    else:
        st.info("لا يوجد موردين مسجلين حتى الآن")

# ================== تبويب الموظفين ==================
with tab3:
    st.subheader("👤 إضافة موظف جديد")
    col1, col2, col3 = st.columns(3)
    with col1:
        emp_name = st.text_input("اسم الموظف")
    with col2:
        emp_national_id = st.text_input("رقم الهوية الوطنية")
    with col3:
        emp_phone = st.text_input("رقم الهاتف")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        emp_job_title = st.text_input("المسمى الوظيفي")
    with col_e2:
        emp_department = st.selectbox("القسم", ["الإدارة", "التقنية", "العمليات", "الموارد البشرية", "المالية", "أخرى"])
    
    if st.button("➕ إضافة الموظف", type="primary", use_container_width=True):
        if emp_name and emp_national_id and emp_phone:
            conn = sqlite3.connect('association.db')
            conn.execute("INSERT INTO employees (name, national_id, phone, job_title, department) VALUES (?,?,?,?,?)",
                        (emp_name, emp_national_id, emp_phone, emp_job_title, emp_department))
            conn.commit()
            conn.close()
            st.success("✅ تم إضافة الموظف بنجاح!")
        else:
            st.error("❌ يرجى ملء جميع الحقول المطلوبة")

    st.divider()
    st.subheader("👥 جميع الموظفين")
    conn = sqlite3.connect('association.db')
    df_employees = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    
    if not df_employees.empty:
        st.dataframe(df_employees, use_container_width=True, hide_index=True)
        
        st.subheader("📊 إحصائيات الموظفين")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي عدد الموظفين", len(df_employees))
        with col2:
            departments = df_employees['department'].nunique()
            st.metric("عدد الأقسام", departments)
        with col3:
            st.metric("الموظفون", len(df_employees))
    else:
        st.info("لا يوجد موظفين مسجلين حتى الآن")

# ================== تبويب الطلبيات ==================
with tab4:
    st.subheader("📦 إضافة طلبية جديدة")
    col1, col2, col3 = st.columns(3)
    
    # الحصول على قائمة الموردين
    conn = sqlite3.connect('association.db')
    suppliers_df = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
    conn.close()
    
    if suppliers_df.empty:
        st.warning("⚠️ يرجى إضافة موردين أولاً قبل إنشاء طلبيات")
    else:
        supplier_names = suppliers_df['name'].tolist()
        supplier_dict = dict(zip(suppliers_df['name'], suppliers_df['id']))
        
        with col1:
            selected_supplier = st.selectbox("اختر المورد", supplier_names, key="supplier_order")
        with col2:
            item_name = st.text_input("اسم الصنف")
        with col3:
            qty = st.number_input("الكمية", min_value=1, value=1, step=1)
        
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            order_status = st.selectbox("حالة الطلبية", ["قيد الانتظار", "تم التأكيد", "تم الشحن", "تم الاستلام", "ملغاة"])
        
        if st.button("➕ إضافة الطلبية", type="primary", use_container_width=True):
            if item_name:
                supplier_id = supplier_dict[selected_supplier]
                conn = sqlite3.connect('association.db')
                conn.execute("INSERT INTO orders (supplier_id, item_name, qty, status, date) VALUES (?,?,?,?,?)",
                            (supplier_id, item_name, qty, order_status, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("✅ تم إضافة الطلبية بنجاح!")
            else:
                st.error("❌ يرجى ملء جميع الحقول")

    st.divider()
    st.subheader("📋 جميع الطلبيات")
    conn = sqlite3.connect('association.db')
    df_orders = pd.read_sql_query("""
        SELECT o.id, s.name as supplier_name, o.item_name, o.qty, o.status, o.date 
        FROM orders o 
        LEFT JOIN suppliers s ON o.supplier_id = s.id
    """, conn)
    conn.close()
    
    if not df_orders.empty:
        # فلتر حسب الحالة
        status_filter = st.selectbox("فلتر حسب الحالة", ["الكل"] + df_orders['status'].unique().tolist())
        
        if status_filter != "الكل":
            df_orders_filtered = df_orders[df_orders['status'] == status_filter]
        else:
            df_orders_filtered = df_orders
        
        st.dataframe(df_orders_filtered, use_container_width=True, hide_index=True)
        
        st.subheader("📊 إحصائيات الطلبيات")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("إجمالي الطلبيات", len(df_orders))
        with col2:
            pending = len(df_orders[df_orders['status'] == 'قيد الانتظار'])
            st.metric("قيد الانتظار", pending)
        with col3:
            confirmed = len(df_orders[df_orders['status'] == 'تم التأكيد'])
            st.metric("تم التأكيد", confirmed)
        with col4:
            received = len(df_orders[df_orders['status'] == 'تم الاستلام'])
            st.metric("تم الاستلام", received)
    else:
        st.info("لا توجد طلبيات مسجلة حتى الآن")

# ================== تذييل الصفحة ==================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>💼 نظام إدارة الجمعية المتكامل | جميع الحقوق محفوظة</p>
    <p>تم التطوير بواسطة Streamlit</p>
</div>
""", unsafe_allow_html=True)
