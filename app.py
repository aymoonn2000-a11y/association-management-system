import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
from io import BytesIO
from contextlib import contextmanager
import os

# ====================== إعدادات الصفحة والواجهة ======================
st.set_page_config(
    page_title="نظام إدارة جمعية الحياة والأمل - السحابي الموحد",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# ====================== نظام التصميم والبصريات (CSS) ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    
    html, body, [data-testid="stWidgetFormSubmitButton"], .stMarkdown, .stSelectbox, .stTextInput, .stButton, .stTabs {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    .stMetric {
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
        border: 1px solid #E5E7EB !important;
        border-right: 5px solid #0066cc !important;
    }
    
    .alert-box {
        padding: 14px;
        border-radius: 10px;
        margin: 10px 0;
        font-weight: 500;
        border-right: 5px solid;
    }
    
    .alert-danger { background-color: #FEF2F2; border-right-color: #EF4444; color: #991B1B; }
    .alert-warning { background-color: #FFFBEB; border-right-color: #F59E0B; color: #92400E; }
    .alert-success { background-color: #F0FDF4; border-right-color: #10B981; color: #065F46; }
    .alert-info { background-color: #EFF6FF; border-right-color: #3B82F6; color: #1E40AF; }
    
    h1 { color: #d32f2f; text-align: center; font-weight: 700; }
    h2, h3 { color: #1E3A8A; font-weight: 600; }
    
    /* مظهر مخصص لمركزية الشعار في القائمة الجانبية */
    [data-testid="stSidebar"] .stImage {
        text-align: center;
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== محرك إدارة قاعدة البيانات والأتمتة ======================
class AssociationDatabase:
    def __init__(self, db_name='association_pro.db'):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_name, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.connection() as conn:
            c = conn.cursor()
            # 1. جدول الأصول والمستودع
            c.execute('''CREATE TABLE IF NOT EXISTS assets 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, asset_type TEXT NOT NULL, name TEXT UNIQUE NOT NULL, 
                          quantity INTEGER NOT NULL, location TEXT NOT NULL, status TEXT NOT NULL, 
                          min_quantity INTEGER DEFAULT 5, date_added TEXT NOT NULL, notes TEXT)''')
            # 2. جدول الموردين
            c.execute('''CREATE TABLE IF NOT EXISTS suppliers 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, category TEXT NOT NULL, 
                          phone TEXT NOT NULL, email TEXT, address TEXT, rating INTEGER DEFAULT 5, date_added TEXT NOT NULL)''')
            # 3. جدول الموظفين
            c.execute('''CREATE TABLE IF NOT EXISTS employees 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, national_id TEXT UNIQUE NOT NULL, 
                          phone TEXT NOT NULL, job_title TEXT NOT NULL, department TEXT NOT NULL, salary REAL, 
                          status TEXT DEFAULT '🟢 نشط برأس عمله', date_added TEXT NOT NULL)''')
            # 4. جدول الطلبيات والمشتريات
            c.execute('''CREATE TABLE IF NOT EXISTS orders 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_id INTEGER NOT NULL, item_name TEXT NOT NULL, 
                          qty INTEGER NOT NULL, unit_price REAL, total_price REAL, status TEXT NOT NULL, 
                          order_date TEXT NOT NULL, notes TEXT, FOREIGN KEY(supplier_id) REFERENCES suppliers(id))''')
            # 5. جدول الصيانة الجدولية
            c.execute('''CREATE TABLE IF NOT EXISTS maintenance 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, asset_id INTEGER NOT NULL, m_type TEXT NOT NULL, 
                          description TEXT, m_date TEXT NOT NULL, next_m_date TEXT, cost REAL, status TEXT DEFAULT '⏳ مجدولة',
                          FOREIGN KEY(asset_id) REFERENCES assets(id))''')
            # 6. جدول التنبيهات الذكية
            c.execute('''CREATE TABLE IF NOT EXISTS alerts 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, alert_type TEXT NOT NULL, title TEXT NOT NULL, 
                          message TEXT NOT NULL, severity TEXT DEFAULT 'معلومة', is_read INTEGER DEFAULT 0, created_at TEXT NOT NULL)''')
            # 7. سجل التدقيق والحركات الامنية
            c.execute('''CREATE TABLE IF NOT EXISTS activity_log 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, table_name TEXT NOT NULL, 
                          details TEXT, timestamp TEXT NOT NULL)''')
            conn.commit()

    def log_activity(self, action, table_name, details=""):
        with self.connection() as conn:
            conn.execute("INSERT INTO activity_log (action, table_name, details, timestamp) VALUES (?, ?, ?, ?)",
                         (action, table_name, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def create_alert(self, alert_type, title, message, severity="معلومة"):
        with self.connection() as conn:
            conn.execute("INSERT INTO alerts (alert_type, title, message, severity, created_at) VALUES (?, ?, ?, ?, ?)",
                         (alert_type, title, message, severity, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def add_asset(self, asset_type, name, qty, location, status, min_qty, notes):
        try:
            with self.connection() as conn:
                conn.execute("""INSERT INTO assets (asset_type, name, quantity, location, status, min_quantity, date_added, notes) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                             (asset_type, name.strip(), qty, location.strip(), status, min_qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes.strip()))
                conn.commit()
            self.log_activity("إضافة", "assets", f"إضافة مادة مستودعية: {name}")
            return True, "تم حفظ الأصل والمادة بنجاح في المستودع!"
        except sqlite3.IntegrityError:
            return False, "⚠️ اسم هذا الأصل مسجل مسبقاً، يرجى استخدام اسم مميز أو تحديث كمية الحالي."

    def add_supplier(self, name, category, phone, email, address, rating):
        try:
            with self.connection() as conn:
                conn.execute("""INSERT INTO suppliers (name, category, phone, email, address, rating, date_added) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                             (name.strip(), category, phone.strip(), email.strip(), address.strip(), rating, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
            self.log_activity("إضافة", "suppliers", f"اعتماد مورد: {name}")
            return True, "تم إضافة المورد المعتمد بنجاح!"
        except sqlite3.IntegrityError:
            return False, "⚠️ اسم هذا المورد مسجل مسبقاً في الدليل الحسابي."

    def add_employee(self, name, national_id, phone, title, dept, salary, status):
        try:
            with self.connection() as conn:
                conn.execute("""INSERT INTO employees (name, national_id, phone, job_title, department, salary, status, date_added) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                             (name.strip(), national_id.strip(), phone.strip(), title.strip(), dept, salary, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
            self.log_activity("إضافة", "employees", f"تعيين كادر: {name}")
            return True, "تم قيد بيانات الموظف وإصدار الرقم الوظيفي المالي!"
        except sqlite3.IntegrityError:
            return False, "⚠️ رقم الهوية الوطنية هذا مخصص لموظف مسجل مسبقاً."

    def add_order(self, supplier_id, item_name, qty, unit_price, status, notes):
        total = qty * unit_price
        with self.connection() as conn:
            conn.execute("""INSERT INTO orders (supplier_id, item_name, qty, unit_price, total_price, status, order_date, notes) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                         (supplier_id, item_name.strip(), qty, unit_price, total, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes.strip()))
            conn.commit()
        
        self.log_activity("إضافة", "orders", f"إنشاء أمر شراء للمادة: {item_name}")
        if status == "🟢 تم الاستلام":
            self.sync_order_to_inventory(item_name, qty)
        return True

    def sync_order_to_inventory(self, item_name, qty):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        with self.connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, quantity FROM assets WHERE LOWER(name) = LOWER(?)", (item_name.strip(),))
            res = c.fetchone()
            if res:
                new_qty = res['quantity'] + qty
                c.execute("UPDATE assets SET quantity = ?, date_added = ? WHERE id = ?", (new_qty, now_str, res['id']))
            else:
                c.execute("""INSERT INTO assets (asset_type, name, quantity, location, status, min_quantity, date_added, notes) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                          ("❓ أخرى", item_name.strip(), qty, "المستودع الرئيسي (توريد تلقائي)", "✨ ممتازة", 5, now_str, "مادة تم إدراجها آلياً عبر نظام إدارة المشتريات"))
            conn.commit()
        self.create_alert("تحديث مخزني آلي", "توريد آلي للمخازن", f"تم تغذية رصيد المادة ({item_name}) بزيادة (+{qty} وحدة) نتيجة استلام طلبية شراء ملوثة.", "نجاح")

    def add_maintenance(self, asset_id, m_type, desc, m_date, next_date, cost, status):
        with self.connection() as conn:
            conn.execute("""INSERT INTO maintenance (asset_id, m_type, description, m_date, next_maintenance_date, cost, status) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                         (asset_id, m_type, desc.strip(), m_date, next_date, cost, status))
            conn.commit()
        self.log_activity("إضافة", "maintenance", f"جدولة صيانة للأصل رقم: {asset_id}")

# تهيئة المحرك المركزي للنظام
db = AssociationDatabase()

def to_excel_download(df):
    out = BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return out.getvalue()

# ====================== شريط التنقل الجانبي (مدمج معه الشعار) ======================
with st.sidebar:
    # استخدام الشعار المرجعي المعرف باسم "الحياة والامل.jpg"
    logo_path = "الحياة والامل.jpg"
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        st.warning("⚠️ يرجى التأكد من وجود ملف الشعار باسم 'الحياة والامل.jpg' في مجلد المشروع.")
        
    st.markdown("""
    <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #d32f2f, #f44336); border-radius: 12px; color: white; margin-bottom:15px;'>
        <h3 style='color: white; margin:0; font-size:16px;'>جمعية الحياة والأمل</h3>
        <p style='margin:0; font-size:11px;'>نظام الحوكمة اللوجستية المتكامل</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_unit = st.selectbox(
        "الانتقال الفوري بين الأقسام:",
        [
            "📊 لوحة التحليلات والمؤشرات",
            "📦 إدارة الأصول والمستودعات",
            "🏪 كشوفات الموردين المعتمدين",
            "👥 الموارد البشرية وشؤون الموظفين",
            "📋 إدارة المشتريات والطلبيات",
            "🔧 جدول العمليات والصيانة",
            "⚠️ نظام التنبيهات والرقابة",
            "📜 سجل الحركات والتدقيق (Audit)"
        ]
    )
    
    st.divider()
    st.markdown("### 📊 الحالة الآنية الفورية")
    with db.connection() as conn:
        count_assets = pd.read_sql_query("SELECT COUNT(*) as c FROM assets", conn)['c'][0]
        count_suppliers = pd.read_sql_query("SELECT COUNT(*) as c FROM suppliers", conn)['c'][0]
        count_employees = pd.read_sql_query("SELECT COUNT(*) as c FROM employees", conn)['c'][0]
        count_alerts = pd.read_sql_query("SELECT COUNT(*) as c FROM alerts WHERE is_read = 0", conn)['c'][0]
    
    st.metric("📦 خطوط المواد بالمستودع", count_assets)
    st.metric("🏪 الشركات والموردين", count_suppliers)
    st.metric("👥 قوة الكادر البشري", count_employees)
    st.metric("🔔 الإشعارات الرقابية الجديدة", count_alerts, delta=f"{count_alerts} معلقة" if count_alerts > 0 else None)

# ====================== 1. لوحة التحليلات والمؤشرات المتقدمة ======================
if current_unit == "📊 لوحة التحليلات والمؤشرات":
    st.markdown("<h1>📊 لوحة القيادة التحليلية لجمعية الحياة والأمل</h1>", unsafe_allow_html=True)
    
    with db.connection() as conn:
        tot_assets = pd.read_sql_query("SELECT COUNT(*) as c FROM assets", conn)['c'][0]
        tot_qty = pd.read_sql_query("SELECT SUM(quantity) as s FROM assets", conn)['s'][0] or 0
        pend_orders = pd.read_sql_query("SELECT COUNT(*) as c FROM orders WHERE status = '⏳ قيد الانتظار'", conn)['c'][0]
        danger_stock = pd.read_sql_query("SELECT COUNT(*) as c FROM assets WHERE quantity <= min_quantity", conn)['c'][0]
        
        df_chart_1 = pd.read_sql_query("SELECT asset_type, SUM(quantity) as q_sum FROM assets GROUP BY asset_type", conn)
        df_chart_2 = pd.read_sql_query("SELECT status, COUNT(*) as count FROM orders GROUP BY status", conn)
        df_low_stock = pd.read_sql_query("SELECT name, quantity, min_quantity FROM assets WHERE quantity <= min_quantity", conn)
        df_p_orders = pd.read_sql_query("SELECT o.item_name, o.qty, s.name as s_name FROM orders o JOIN suppliers s ON o.supplier_id = s.id WHERE o.status = '⏳ قيد الانتظار'", conn)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 السلع المخزنية الفريدة", tot_assets)
    c2.metric("📊 إجمالي وحدات المخزون", tot_qty)
    c3.metric("⏳ عقود شراء قيد التوريد", pend_orders)
    c4.metric("⚠️ خطوط مستنفدة مخزنياً", danger_stock, delta=f"{danger_stock} نواقص خطرة" if danger_stock > 0 else "آمن", delta_color="inverse")
    
    st.divider()
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if not df_chart_1.empty:
            fig1 = px.bar(df_chart_1, x='asset_type', y='q_sum', title="📊 رصيد المخزون بناءً على التصنيف", color_discrete_sequence=['#d32f2f'])
            st.plotly_chart(fig1, use_container_width=True)
    with col_g2:
        if not df_chart_2.empty:
            fig2 = px.pie(df_chart_2, values='count', names='status', title="📋 مؤشر كفاءة عقود التوريد والمشتريات")
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.subheader("⚠️ مركز رصد النواقص العاجلة")
        if not df_low_stock.empty:
            for _, r in df_low_stock.iterrows():
                st.markdown(f"<div class='alert-box alert-danger'>🚨 مادة قريبة من النفاد: <b>{r['name']}</b> | الرصيد الحالي: {r['quantity']} (الحد الحرج: {r['min_quantity']})</div>", unsafe_allow_html=True)
        else:
            st.success("✅ كافة مستويات التوفر في المستودعات تقع ضمن النطاق الآمن.")
            
    with col_l2:
        st.subheader("⏳ صفقات التوريد والشراء النشطة")
        if not df_p_orders.empty:
            for _, r in df_p_orders.iterrows():
                st.markdown(f"<div class='alert-box alert-warning'>📦 طلب معلق: <b>{r['item_name']}</b> ({r['qty']} وحدة) من المورد: {r['s_name']}</div>", unsafe_allow_html=True)
        else:
            st.success("✅ تم تصفية واستلام كافة عقود التوريد الجارية.")

# ====================== 2. إدارة الأصول والمستودعات ======================
elif current_unit == "📦 إدارة الأصول والمستودعات":
    st.markdown("<h1>📦 حوكمة المستودعات وأرصدة أصول الجمعية</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["➕ إدخل مادة مخزنية جديدة", "👁️ كشوفات الجرد الفوري والتصدير"])
    with t1:
        with st.form("asset_pro_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            a_type = col1.selectbox("🏷️ تصنيف وجنس الأصل", ["💻 أجهزة حاسوب وتكنولوجيا", "🖨️ طابعات وأحبار ومستهلكات", "🪑 أثاث ومكتبية وتجهيز مقار", "💡 شبكات وأنظمة كهربائية", "🔧 أدوات صيانة ميدانية", "❓ أخرى"])
            a_name = col1.text_input("📝 المعرف الفريد للمادة (الاسم التجاري / الموديل)")
            a_qty = col2.number_input("📊 الكمية الابتدائية بالرف", min_value=0, value=5)
            a_min = col2.number_input("⚠️ حد الإنذار الأدنى قبل النفاد", min_value=1, value=5)
            a_loc = st.text_input("📍 مكان التخزين الدقيق (اسم المقر / رقم الرف الخزني)")
            a_status = st.selectbox("✅ الحالة التشغيلية الفنية", ["✨ ممتازة وجاهزة للاستخدام", "👍 جيدة وتعمل بكفاءة", "⚠️ متوسطة وتحت الفحص الدوري", "🔧 معطلة وتتطلب صيانة فورية"])
            a_notes = st.text_area("📝 شروط تخزين خاصة أو تفاصيل العهدة")
            
            if st.form_submit_button("اعتماد وحفظ المادة في الجرد"):
                if a_name.strip() and a_loc.strip():
                    ok, msg = db.add_asset(a_type, a_name, a_qty, a_loc, a_status, a_min, a_notes)
                    if ok: st.success(msg)
                    else: st.error(msg)
                else: st.error("❌ فشل التسجيل: يرجى كتابة اسم الأصل الفريد وتحديد موقعه بدقة.")
                
    with t2:
        with db.connection() as conn:
            df_assets = pd.read_sql_query("SELECT * FROM assets ORDER BY date_added DESC", conn)
        if not df_assets.empty:
            st.dataframe(df_assets, use_container_width=True, hide_index=True)
            st.download_button("📥 تصدير كشف الجرد الحالي إلى مستند Excel معتمد", to_excel_download(df_assets), "inventory_master_report.xlsx", use_container_width=True)
        else:
            st.info("🔍 لا توجد أصول مسجلة في النظام حتى الآن.")

# ====================== 3. كشوفات الموردين المعتمدين ======================
elif current_unit == "🏪 كشوفات الموردين المعتمدين":
    st.markdown("<h1>🏪 دليل الموردين والشركات المعتمدة للجمعية</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["➕ توثيق واعتماد مورد جديد", "👁️ قاعدة بيانات الشركاء التجاريين"])
    with t1:
        with st.form("supplier_pro_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            s_name = col1.text_input("🏢 الاسم التجاري للمؤسسة القانونية")
            s_phone = col1.text_input("📞 رقم هاتف التواصل والتنسيق الرسمي")
            s_email = col1.text_input("📧 البريد الإلكتروني المعتمد للفواتير")
            s_cat = col2.selectbox("🏷️ تخصص التوريد الرئيسي", ["💻 تكنولوجيا وأجهزة", "📄 مستلزمات قرطاسية ومكتبية", "🔧 مقاولات وخدمات فنية", "🍱 إعاشة ومواد غذائية", "🏗️ إنشائية ومواد بناء", "❓ أخرى"])
            s_addr = col2.text_input("📍 عنوان المقر الرئيسي / الفروع اللوجستية")
            s_rate = col2.slider("⭐ درجة تقييم الالتزام والموثوقية (1-5)", 1, 5, 5)
            
            if st.form_submit_button("تسجيل المورد في الدليل الدائم"):
                if s_name.strip() and s_phone.strip():
                    ok, msg = db.add_supplier(s_name, s_cat, s_phone, s_email, s_addr, s_rate)
                    if ok: st.success(msg)
                    else: st.error(msg)
                else: st.error("❌ فشل الاعتماد: الاسم التجاري ورقم الهاتف متطلبان إجباريان لبناء ملف المورد.")
                
    with t2:
        with db.connection() as conn:
            df_sups = pd.read_sql_query("SELECT * FROM suppliers ORDER BY date_added DESC", conn)
        if not df_sups.empty:
            st.dataframe(df_sups, use_container_width=True, hide_index=True)
            st.download_button("📥 تحميل كشف الموردين المعتمدين كملف Excel", to_excel_download(df_sups), "approved_suppliers.xlsx", use_container_width=True)

# ====================== 4. الموارد البشرية وشؤون الموظفين ======================
elif current_unit == "👥 الموارد البشرية وشؤون الموظفين":
    st.markdown("<h1>👥 نظام إدارة شؤون الموظفين والكوادر البشرية</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["➕ إلحاق وتعيين موظف جديد", "👁️ السجل المركزي للملاك وهياكل الأجور"])
    with t1:
        with st.form("emp_pro_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            e_name = col1.text_input("👤 الاسم الكامل (مطابق لبطاقة الهوية الشخصية)")
            e_nid = col1.text_input("🆔 رقم الهوية الوطنية الفريد")
            e_phone = col1.text_input("📞 رقم الهاتف الخلوي المباشر")
            e_title = col2.text_input("💼 المسمى الوظيفي طبقاً للهيكل التنظيمي")
            e_salary = col2.number_input("💰 الراتب الشهري الصافي المقر (USD)", min_value=0, step=50)
            e_status = col2.selectbox("✅ الوضع الإداري الحالي", ["🟢 نشط برأس عمله", "🟡 في إجازة رسمية / معار", "🔴 متوقف عن العمل / منتهي التعاقد"])
            e_dept = st.selectbox("🏢 القسم الفني / الإدارة التابع لها الكادر", ["👔 الإدارة التنفيذية والمالية", "💻 تكنولوجيا المعلومات والتقنية", "⚙️ إدارة الميدان والعمليات واللوجستيات", "👥 الموارد البشرية والتطوير الأدائي", "❓ أقسام أخرى"])
            
            if st.form_submit_button("إصدار الميزانية الوظيفية وقيد الملف"):
                if e_name.strip() and e_nid.strip():
                    ok, msg = db.add_employee(e_name, e_nid, e_phone, e_title, e_dept, e_salary, e_status)
                    if ok: st.success(msg)
                    else: st.error(msg)
                else: st.error("❌ خطأ حرج: يمنع ترك حقول الهوية والاسم فارغة.")
                
    with t2:
        with db.connection() as conn:
            df_emps = pd.read_sql_query("SELECT * FROM employees ORDER BY date_added DESC", conn)
        if not df_emps.empty:
            st.dataframe(df_emps, use_container_width=True, hide_index=True)
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("💰 إجمالي الميزانية الشهرية للأجور (USD)", f"${int(df_emps['salary'].sum()):,}")
            col_m2.metric("👥 مجموع الكوادر البشرية النشطة", len(df_emps))
            st.download_button("📥 تحميل الهيكل الإداري ومسير الرواتب (Excel)", to_excel_download(df_emps), "hrm_workforce_roster.xlsx", use_container_width=True)

# ====================== 5. إدارة المشتريات والطلبيات المفتوحة ======================
elif current_unit == "📋 إدارة المشتريات والطلبيات":
    st.markdown("<h1>📋 نظام إدارة المشتريات والربط المستودعي التلقائي</h1>", unsafe_allow_html=True)
    
    with db.connection() as conn:
        sups_data = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
        
    if sups_data.empty:
        st.warning("⚠️ تنبيه مالي: يجب أولاً اعتماد وتوثيق مورد واحد على الأقل في قسم (كشوفات الموردين) لتتمكن من ضخ الفواتير.")
    else:
        sup_dict = dict(zip(sups_data['name'], sups_data['id']))
        
        t1, t2 = st.tabs(["➕ إدراج فاتورة شراء جديدة", "👁️ دفتر القيود الحسابية للمشتريات العامة"])
        with t1:
            with st.form("order_pro_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                ch_supplier = col1.selectbox("اختر المورد المتعهد بالعقد", sups_data['name'].tolist())
                o_item = col1.text_input("اسم المادة المشتراة (استخدم اسماً مطابقاً للمستودع لزيادة رصيدها آلياً)")
                o_qty = col2.number_input("الحجم والكمية المطلوبة للشراء", min_value=1, value=1)
                o_price = col2.number_input("تكلفة الوحدة الواحدة المقرة شراءً", min_value=0.0, step=5.0)
                o_status = st.selectbox("حالة الفاتورة والتدفق اللوجستي", ["⏳ قيد الانتظار", "🟢 تم الاستلام", "❌ ملغاة من الإدارة"])
                o_notes = st.text_area("شروط الدفع الآجل أو تفاصيل الفحص العيني للاستلام")
                
                if st.form_submit_button("اعتماد القيد المالي والترحيل المخزني"):
                    if o_item.strip() and o_price > 0:
                        db.add_order(sup_dict[ch_supplier], o_item, o_qty, o_price, o_status, o_notes)
                        st.success("✅ تم قيد مسند الفاتورة بنجاح وتحديث الأرصدة في حال كانت مستلمة!")
                        st.rerun()
                    else:
                        st.error("❌ فشل المراجعة: يجب تحديد اسم البند وتكلفة مالية صحيحة لإتمام العملية.")
                        
        with t2:
            with db.connection() as conn:
                df_orders = pd.read_sql_query("""
                    SELECT o.id, s.name as supplier_name, o.item_name, o.qty, o.unit_price, o.total_price, o.status, o.order_date 
                    FROM orders o JOIN suppliers s ON o.supplier_id = s.id ORDER BY o.order_date DESC
                """, conn)
            if not df_orders.empty:
                st.dataframe(df_orders, use_container_width=True, hide_index=True)
                st.metric("💰 مجموع النفقات المالية المصروفة على المشتريات اللوجستية", f"${df_orders['total_price'].sum():,.2f}")
                st.download_button("📥 تحميل دفتر قيود المشتريات (Excel)", to_excel_download(df_orders), "procurement_invoices_ledger.xlsx", use_container_width=True)

# ====================== 6. جدول العمليات والصيانة ======================
elif current_unit == "🔧 جدول العمليات والصيانة":
    st.markdown("<h1>🔧 خطط وجداول الصيانة الدورية للأصول والمقار</h1>", unsafe_allow_html=True)
    
    with db.connection() as conn:
        assets_data = pd.read_sql_query("SELECT id, name FROM assets", conn)
        
    if assets_data.empty:
        st.warning("⚠️ لا توجد أصول في الجرد لتخصيص جدول صيانة لها. يرجى ملء المستودع أولاً.")
    else:
        asset_dict = dict(zip(assets_data['name'], assets_data['id']))
        
        t1, t2 = st.tabs(["➕ جدولة عملية صيانة", "👁️ جدول المهام الفنية المفتوحة"])
        with t1:
            with st.form("m_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                ch_asset = col1.selectbox("اختر الأصل الفني المعني بالعملية", assets_data['name'].tolist())
                m_type = col1.selectbox("نوع التدخل الفني", ["⚙️ صيانة وقائية دورية", "🚨 إصلاح عطل طارئ", "🧼 تنظيف ومعايرة فنية", "🔄 تحديث وإحلال قطع غيار"])
                m_date = col2.date_input("تاريخ الفحص والعملية الحالية").strftime("%Y-%m-%d")
                next_m_date = col2.date_input("التاريخ المقترح للفحص الوقائي القادم").strftime("%Y-%m-%d")
                m_cost = col2.number_input("التكلفة المالية الإجمالية المدفوعة للإصلاح", min_value=0.0, step=10.0)
                m_status = st.selectbox("حالة المهمة الفنية", ["⏳ مجدولة وقيد التحضير", "⚙️ جارية تحت التنفيذ الفني", "✅ اكتملت بنجاح وتم الاستلام"])
                m_desc = st.text_area("وصف دقيق للأعطال الفنية أو الأعمال المنجزة للتقرير")
                
                if st.form_submit_button("إدراج أمر الصيانة في الخطة"):
                    db.add_maintenance(asset_dict[ch_asset], m_type, m_desc, m_date, next_m_date, m_cost, m_status)
                    st.success("تم إدراج المهمة الفنية بنجاح في جدول أعمال الصيانة المستدامة!")
                    
        with t2:
            with db.connection() as conn:
                df_m = pd.read_sql_query("""
                    SELECT m.id, a.name as asset_name, m.m_type, m.description, m.m_date, m.next_maintenance_date, m.cost, m.status 
                    FROM maintenance m JOIN assets a ON m.asset_id = a.id ORDER BY m.m_date DESC
                """, conn)
            if not df_m.empty:
                st.dataframe(df_m, use_container_width=True, hide_index=True)
                st.download_button("📥 تحميل تقارير الصيانة الدورية (Excel)", to_excel_download(df_m), "maintenance_schedule.xlsx", use_container_width=True)

# ====================== 7. نظام التنبيهات والرقابة ======================
elif current_unit == "⚠️ نظام التنبيهات والرقابة":
    st.markdown("<h1>⚠️ لوحة التحكم بالرقابة الفورية والإشعارات</h1>", unsafe_allow_html=True)
    
    if st.button("🔵 نقل كافة الإشعارات والتحذيرات الراهنة إلى الأرشيف المكتوم", use_container_width=True):
        with db.connection() as conn:
            conn.execute("UPDATE alerts SET is_read = 1")
            conn.commit()
        st.success("تم نقل البيانات وتصفية مركز الإشعارات الفوري.")
        st.rerun()
        
    st.divider()
    with db.connection() as conn:
        df_un = pd.read_sql_query("SELECT * FROM alerts WHERE is_read = 0 ORDER BY created_at DESC", conn)
        df_all = pd.read_sql_query("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 50", conn)
        
    t1, t2 = st.tabs(["🆕 الإخطارات الرقابية الطازجة", "📚 السجل التاريخي للأرشيف التنبيهي"])
    with t1:
        if not df_un.empty:
            for _, r in df_un.iterrows():
                st.markdown(f"<div class='alert-box alert-info'>🔔 <b>{r['title']}</b> - {r['message']}<br><small>توقيت الرصد الآلي: {r['created_at']}</small></div>", unsafe_allow_html=True)
        else:
            st.success("✅ مستويات التشغيل والرقابة ممتازة، لا توجد إخطارات معلقة.")
    with t2:
        if not df_all.empty:
            st.dataframe(df_all, use_container_width=True, hide_index=True)

# ====================== 8. سجل الحركات والتدقيق (Audit Log) ======================
elif current_unit == "📜 سجل الحركات والتدقيق (Audit)":
    st.markdown("<h1>📜 سجل مراجعة التدقيق الداخلي والحركات العميقة (Audit Trail)</h1>", unsafe_allow_html=True)
    st.info("⚠️ هذا السجل يرصد تتبع كافة الحركات التشغيلية والمالية التي تمت على حزم البيانات لضمان أعلى مستويات النزاهة الإدارية.")
    
    with db.connection() as conn:
        df_logs = pd.read_sql_query("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 150", conn)
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    else:
        st.info("سجلات الرقابة خالية تماماً من التحركات السابقة حتى الآن.")

# ====================== تذييل النظام (Footer) ======================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 10px; color: #6B7280; font-size: 13px; font-weight: bold;">
    🏢 البوابة السحابية المتكاملة لحوكمة وإدارة موارد جمعية الحياة والأمل (ERP Suite) | حماية مشددة للبنية التحتية © 2026
</div>
""", unsafe_allow_html=True)
