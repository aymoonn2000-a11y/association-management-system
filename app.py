import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة وتوجيه النص من اليمين إلى اليسار (RTL) لدعم اللغة العربية
st.set_page_config(page_title="نظام إدارة مشاريع الجمعية", layout="wide", page_icon="🏢")

# ====================== قاعدة البيانات وتأسيس الجداول ======================
def init_db():
    with sqlite3.connect('association.db') as conn:
        c = conn.cursor()
        
        # جدول موظفي المشاريع (تتضمن قسم المشروع)
        c.execute('''CREATE TABLE IF NOT EXISTS project_employees 
                     (id INTEGER PRIMARY KEY, project_type TEXT, name TEXT, national_id TEXT, phone TEXT, job_title TEXT)''')
        
        # جدول الموردين
        c.execute('''CREATE TABLE IF NOT EXISTS suppliers 
                     (id INTEGER PRIMARY KEY, name TEXT, category TEXT, phone TEXT, email TEXT, address TEXT)''')
        
        # جدول الفواتير والطلبيات بالأسعار والتفاصيل
        c.execute('''CREATE TABLE IF NOT EXISTS invoices 
                     (id INTEGER PRIMARY KEY, supplier_id INTEGER, item_name TEXT, qty INTEGER, total_price REAL, status TEXT, details TEXT, date TEXT)''')
        
        # جدول مخزن المؤسسة (القرطاسية وما شابه)
        c.execute('''CREATE TABLE IF NOT EXISTS inventory 
                     (id INTEGER PRIMARY KEY, item_name TEXT, category TEXT, quantity INTEGER, status TEXT, last_updated TEXT)''')
        
        conn.commit()

init_db()

# ====================== نظام تسجيل الدخول المحمي ======================
# الحسابات الافتراضية لمنسقي المشاريع
USER_CREDENTIALS = {
    "shelter_coord": "shelter2026",
    "cva_coord": "cva2026",
    "meal_coord": "meal2026"
}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

def login_page():
    st.markdown("<h2 style='text-align: center;'>🔒 تسجيل الدخول إلى نظام الجمعية</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("اسم المستخدم (Coordinator Username)")
            password = st.text_input("كلمة المرور", type="password")
            submit = st.form_submit_button("دخول", use_container_width=True)
            
            if submit:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

if not st.session_state["logged_in"]:
    login_page()
else:
    # شريط علوي لعرض اسم المستخدم وزر تسجيل الخروج
    col_user, col_logout = st.columns([8, 2])
    with col_user:
        st.markdown(f"👋 مرحباً بك: **{st.session_state['username']}**")
    with col_logout:
        if st.button("تسجيل الخروج 🚪", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
            
    st.title("🏢 نظام إدارة مشاريع ومخازن الجمعية المتكامل")
    st.divider()

    # إنشاء التبويبات الرئيسية للنظام حسب المتطلبات الجديدة
    tab_projects, tab_suppliers, tab_inventory = st.tabs([
        "📁 أقسام المشاريع والموظفين", 
        "🏪 الموردين والفواتير بالأسعار", 
        "📦 مخزن المؤسسة والقرطاسية"
    ])

    # ================== 1. تبويب أقسام المشاريع والموظفين ==================
    with tab_projects:
        st.subheader("🛠️ إدارة أقسام وموظفي المشاريع")
        
        # تقسيم داخلي للمشاريع الـ 3 مع الأيقونات الخاصة بها
        proj_tab1, proj_tab2, proj_tab3 = st.tabs(["🏠 Shelter", "💳 CVA", "📊 MEAL"])
        
        # مصفوفة لتسهيل معالجة تكرار الأقسام والتحكم بها بصرياً
        project_details = [
            {"tab": proj_tab1, "name": "Shelter", "icon": "🏠"},
            {"tab": proj_tab2, "name": "CVA", "icon": "💳"},
            {"tab": proj_tab3, "name": "MEAL", "icon": "📊"}
        ]
        
        for project in project_details:
            with project["tab"]:
                st.markdown(f"### {project['icon']} قسم مشروع {project['name']}")
                
                # نموذج إضافة موظف مخصص لهذا المشروع
                with st.expander(f"➕ تسجيل موظف جديد في مشروع {project['name']}", expanded=False):
                    with st.form(f"form_emp_{project['name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            emp_name = st.text_input("اسم الموظف كاملاً")
                            emp_national_id = st.text_input("رقم الهوية الوطنية / الإقامة")
                        with col2:
                            emp_phone = st.text_input("رقم الهاتف والاتصال")
                            emp_job_title = st.text_input("المسمى الوظيفي في المشروع")
                        
                        btn_add_emp = st.form_submit_button("حفظ الموظف في النظام")
                        if btn_add_emp:
                            if emp_name and emp_national_id and emp_phone:
                                with sqlite3.connect('association.db') as conn:
                                    conn.execute("""INSERT INTO project_employees (project_type, name, national_id, phone, job_title) 
                                                    VALUES (?, ?, ?, ?, ?)""", 
                                                 (project['name'], emp_name, emp_national_id, emp_phone, emp_job_title))
                                    conn.commit()
                                st.success(f"✅ تم تسجيل الموظف بنجاح في مشروع {project['name']}!")
                            else:
                                st.error("❌ يرجى ملء البيانات الأساسية للموظف (الاسم، الهوية، الهاتف)")
                
                # عرض الموظفين التابعين للمشروع المحدد حالياً
                st.markdown("#### 👥 الموظفون الحاليون في هذا المشروع")
                with sqlite3.connect('association.db') as conn:
                    df_emp = pd.read_sql_query("SELECT id, name, national_id, phone, job_title FROM project_employees WHERE project_type = ?", conn, params=(project['name'],))
                
                if not df_emp.empty:
                    st.dataframe(df_emp, use_container_width=True, hide_index=True)
                    st.metric(f"إجمالي موظفي {project['name']}", len(df_emp))
                else:
                    st.info(f"لا يوجد موظفون مسجلون في مشروع {project['name']} حتى الآن.")

    # ================== 2. تبويب قائمة الموردين وإضافة الفواتير ==================
    with tab_suppliers:
        st.subheader("🏪 إدارة قائمة الموردين وفواتير الطلبيات")
        
        sub_tab_supp, sub_tab_inv = st.tabs(["📋 قائمة الموردين", "🧾 فواتير وطلبيات الأسعار"])
        
        # --- فرع إدارة الموردين ---
        with sub_tab_supp:
            st.markdown("### ➕ إضافة مورد جديد للقائمة")
            with st.form("supplier_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    s_name = st.text_input("اسم الشركة / المورد")
                    s_category = st.selectbox("تصنيف التوريد", ["أجهزة إلكترونية", "قرطاسية ومستلزمات مكتبية", "مواد بناء وصيانة", "خدمات عامة", "أخرى"])
                with col2:
                    s_phone = st.text_input("رقم التواصل")
                    s_email = st.text_input("البريد الإلكتروني")
                with col3:
                    s_address = st.text_input("العنوان الوطني / المقر الرئيسي")
                
                btn_supplier = st.form_submit_button("إضافة المورد إلى القائمة الرسمية")
                if btn_supplier:
                    if s_name and s_phone:
                        with sqlite3.connect('association.db') as conn:
                            conn.execute("INSERT INTO suppliers (name, category, phone, email, address) VALUES (?, ?, ?, ?, ?)",
                                         (s_name, s_category, s_phone, s_email, s_address))
                            conn.commit()
                        st.success("✅ تم إدراج المورد بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ يرجى تعبئة الحقول الإلزامية للمورد (الاسم والهاتف).")
            
            st.divider()
            st.markdown("### 📋 قائمة الموردين المعتمدين")
            with sqlite3.connect('association.db') as conn:
                df_suppliers = pd.read_sql_query("SELECT * FROM suppliers", conn)
            if not df_suppliers.empty:
                st.dataframe(df_suppliers, use_container_width=True, hide_index=True)
            else:
                st.info("لم يتم تسجيل أي موردين في القائمة المعتمدة بعد.")

        # --- فرع الفواتير وطلبيات الأسعار ---
        with sub_tab_inv:
            st.markdown("### 🧾 إصدار وتسجيل فاتورة طلبية جديدة")
            
            with sqlite3.connect('association.db') as conn:
                suppliers_select_df = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
                
            if suppliers_select_df.empty:
                st.warning("⚠️ لا يمكن إضافة فواتير بدون وجود موردين. يرجى إضافة مورد أولاً من تبويب (قائمة الموردين).")
            else:
                supplier_mapping = dict(zip(suppliers_select_df['name'], suppliers_select_df['id']))
                
                with st.form("invoice_form"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        chosen_supplier = st.selectbox("اختر المورد المتعاقد معه", suppliers_select_df['name'].tolist())
                        inv_item_name = st.text_input("اسم الصنف أو الخدمة المطلوبة")
                    with col2:
                        inv_qty = st.number_input("الكمية المشتراة", min_value=1, value=1, step=1)
                        inv_price = st.number_input("السعر الإجمالي النهائي للفاتورة (بالعملة المحلية)", min_value=0.0, step=0.50)
                    with col3:
                        inv_status = st.selectbox("حالة دفع الفاتورة", ["قيد المعالجة/الطلب", "مدفوعة بالكامل", "مدفوعة جزئياً", "آجل / لم تدفع"])
                        inv_details = st.text_area("تفاصيل السلع المذكورة في الفاتورة أو شروط التوريد")
                        
                    btn_invoice = st.form_submit_button("تسجيل الفاتورة وحفظ القيمة المالية")
                    if btn_invoice:
                        if inv_item_name and inv_price > 0:
                            s_id = supplier_mapping[chosen_supplier]
                            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                            with sqlite3.connect('association.db') as conn:
                                conn.execute("""INSERT INTO invoices (supplier_id, item_name, qty, total_price, status, details, date) 
                                                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                             (s_id, inv_item_name, inv_qty, inv_price, inv_status, inv_details, current_date))
                                conn.commit()
                            st.success("✅ تم قيد وفهرسة الفاتورة والطلبية بنجاح!")
                            st.rerun()
                        else:
                            st.error("❌ يرجى إدخال اسم الصنف وتحديد السعر الإجمالي للفاتورة بشكل صحيح.")
                            
            st.divider()
            st.markdown("### 📊 السجل الشامل للفواتير والطلبيات")
            with sqlite3.connect('association.db') as conn:
                df_invoices = pd.read_sql_query("""
                    SELECT i.id, s.name as supplier_name, i.item_name, i.qty, i.total_price, i.status, i.details, i.date 
                    FROM invoices i
                    LEFT JOIN suppliers s ON i.supplier_id = s.id
                """, conn)
                
            if not df_invoices.empty:
                st.dataframe(df_invoices, use_container_width=True, hide_index=True)
                
                # عرض مؤشرات إحصائية مالية للفواتير والطلبيات
                st.markdown("#### 📐 ملخص مالي سريع")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("إجمالي الفواتير الصادرة", len(df_invoices))
                with c2:
                    st.metric("المبالغ الإجمالية المستحقة/المدفوعة", f"{df_invoices['total_price'].sum():,.2f}")
                with c3:
                    paid_count = len(df_invoices[df_invoices['status'] == 'مدفوعة بالكامل'])
                    st.metric("عدد الفواتير المسددة بالكامل", paid_count)
            else:
                st.info("لا توجد فواتير أو طلبيات مسجلة مالياً في النظام حتى الآن.")

    # ================== 3. تبويب مخزن المؤسسة (القرطاسية وما شابه) ==================
    with tab_inventory:
        st.subheader("📦 إدارة عهد ومخزن المؤسسة الرئيسي")
        st.markdown("### قسم مخصص لتسجيل وإحصاء مستلزمات المكتب من قرطاسية، أحبار، أدوات ضيافة، وغيرها.")
        
        # نموذج إدخال بضائع للمخزن
        with st.form("inventory_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                inv_name = st.text_input("اسم المادة المخزنية (مثال: ورق A4، أقلام، ملفات)")
            with col2:
                inv_cat = st.selectbox("تصنيف المادة المخزنية", ["قرطاسية وأدوات مكتبية", "مستلزمات أحبار وطابعات", "أدوات ومواد تنظيف", "ضيافة ومأكولات للمكتب", "أخرى"])
            with col3:
                inv_quantity = st.number_input("الكمية المتوفرة حالياً في الرف", min_value=0, value=0, step=1)
                
            inv_item_status = st.selectbox("حالة وفرة المخزون", ["متوفر وبحالة جيدة", "يوشك على النفاذ (طلب عاجل)", "مستنفذ تماماً"])
            
            btn_inventory = st.form_submit_button("تحديث / إضافة عهدة للمخزن")
            if btn_inventory:
                if inv_name:
                    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    with sqlite3.connect('association.db') as conn:
                        conn.execute("INSERT INTO inventory (item_name, category, quantity, status, last_updated) VALUES (?, ?, ?, ?, ?)",
                                     (inv_name, inv_cat, inv_quantity, inv_item_status, update_time))
                        conn.commit()
                    st.success("✅ تم تحديث كشوفات مخزن المؤسسة بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ يرجى كتابة اسم المادة المراد جدولتها في المخزن.")
                    
        st.divider()
        st.markdown("### 📋 جدول جرد محتويات مخزن القرطاسية الحالية")
        with sqlite3.connect('association.db') as conn:
            df_inventory = pd.read_sql_query("SELECT * FROM inventory", conn)
            
        if not df_inventory.empty:
            st.dataframe(df_inventory, use_container_width=True, hide_index=True)
            
            # ملخص المخزن والقرطاسية
            st.markdown("#### 📊 إحصائيات الجرد المكتبي")
            i_col1, i_col2, i_col3 = st.columns(3)
            with i_col1:
                st.metric("عدد الأصناف المختلفة المسجلة", len(df_inventory))
            with i_col2:
                st.metric("إجمالي حجم القطع/الكميات بالمخزن", int(df_inventory['quantity'].sum()))
            with i_col3:
                low_stock = len(df_inventory[df_inventory['status'] == 'يوشك على النفاذ (طلب عاجل)'])
                st.metric("أصناف تحت خطر النفاذ", low_stock)
        else:
            st.info("لا توجد أصناف أو عهد مكتبية مسجلة في المخزن حتى الآن.")

# ================== تذييل الصفحة الثابت ==================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 15px; color: gray;">
    <p>💼 نظام إدارة الجمعية المتكامل والمشاريع المخصصة (Shelter / CVA / MEAL) | جميع الحقوق محفوظة © 2026</p>
    <p>بنيت بكل كفاءة باستخدام بايثون و Streamlit</p>
</div>
""", unsafe_allow_html=True)
