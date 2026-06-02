import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from contextlib import contextmanager
import os
import math
from PIL import Image, ImageDraw

# ==================== إنشاء الأيقونة والشعار تلقائياً ====================
def generate_professional_logo():
    """توليد شعار احترافي بتصميم عالي الجودة يعكس الحياة والأمل والاستقرار"""
    logo_path = "app_icon.png"
    if not os.path.exists(logo_path):
        try:
            size = 512
            img = Image.new('RGB', (size, size), color='#ffffff')
            draw = ImageDraw.Draw(img, 'RGBA')
            
            # خلفية تدريجية احترافية
            for y in range(size):
                ratio = y / size
                r = int(100 + (50 - 100) * ratio)
                g = int(200 + (180 - 200) * ratio)
                b = int(255 + (100 - 255) * ratio)
                draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
            
            # شمس الأمل
            sun_x, sun_y = size * 0.75, size * 0.25
            sun_radius = 50
            draw.ellipse([sun_x - sun_radius - 15, sun_y - sun_radius - 15, sun_x + sun_radius + 15, sun_y + sun_radius + 15], fill=(255, 220, 0, 80))
            draw.ellipse([sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius], fill=(255, 200, 0, 255))
            
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x1 = sun_x + (sun_radius + 10) * math.cos(rad)
                y1 = sun_y + (sun_radius + 10) * math.sin(rad)
                x2 = sun_x + (sun_radius + 35) * math.cos(rad)
                y2 = sun_y + (sun_radius + 35) * math.sin(rad)
                draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 0, 255), width=4)
            
            # نبتة الحياة
            roots_x, roots_y = size * 0.25, size * 0.65
            draw.line([(roots_x, roots_y), (roots_x - 30, roots_y + 40)], fill=(139, 69, 19, 255), width=6)
            draw.line([(roots_x, roots_y), (roots_x + 30, roots_y + 40)], fill=(139, 69, 19, 255), width=6)
            draw.line([(roots_x, roots_y), (roots_x, roots_y + 45)], fill=(139, 69, 19, 255), width=8)
            
            stem_x, stem_top = roots_x, size * 0.35
            draw.line([(stem_x, roots_y), (stem_x, stem_top)], fill=(34, 139, 34, 255), width=10)
            
            leaf_height = size * 0.45
            draw.polygon([(stem_x - 5, leaf_height), (stem_x - 80, leaf_height - 60), (stem_x - 60, leaf_height + 20)], fill=(76, 175, 80, 255))
            draw.polygon([(stem_x + 5, leaf_height), (stem_x + 80, leaf_height - 60), (stem_x + 60, leaf_height + 20)], fill=(76, 175, 80, 255))
            
            # زهرة الجمال
            flower_x, flower_y = stem_x, stem_top - 50
            petal_radius = 30
            petal_colors = [(255, 100, 150), (255, 150, 180), (255, 100, 150), (255, 150, 180), (255, 100, 150)]
            for i, color in enumerate(petal_colors):
                angle = (i * 72) * math.pi / 180
                petal_x = flower_x + petal_radius * math.cos(angle)
                petal_y = flower_y - petal_radius * math.sin(angle)
                draw.ellipse([petal_x - 20, petal_y - 20, petal_x + 20, petal_y + 20], fill=color + (255,))
            
            draw.ellipse([flower_x - 15, flower_y - 15, flower_x + 15, flower_y + 15], fill=(255, 255, 0, 255))
            
            # إطار احترافي
            draw.rectangle([5, 5, size - 5, size - 5], outline=(70, 130, 180, 255), width=8)
            
            img.save(logo_path)
        except Exception:
            pass

generate_professional_logo()

# ====================== إعدادات الصفحة الاحترافية ======================
st.set_page_config(
    page_title="نظام إدارة جمعية الحياة والأمل - ERP متكامل",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# ====================== تصميم CSS احترافي متقدم ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.1) !important;
        border-left: 6px solid #0066cc !important;
        transition: transform 0.3s, box-shadow 0.3s !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.2) !important;
    }
    
    .alert-box {
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        font-weight: 500;
        border-right: 5px solid;
    }
    
    .alert-danger { background-color: #FEF2F2; border-right-color: #EF4444; color: #991B1B; }
    .alert-success { background-color: #F0FDF4; border-right-color: #10B981; color: #065F46; }
    .alert-warning { background-color: #FFFBEB; border-right-color: #F59E0B; color: #92400E; }
    
    h1 {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
    }
    
    h2, h3 {
        color: #1E3A8A;
        font-weight: 700;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 10px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 102, 204, 0.3);
    }
    
    .stForm {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ====================== محرك قاعدة البيانات الاحترافي ======================
class DatabaseManager:
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
            c.execute('''CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT NOT NULL,
                name TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                location TEXT NOT NULL,
                status TEXT NOT NULL,
                min_quantity INTEGER DEFAULT 5,
                date_added TEXT NOT NULL,
                date_modified TEXT,
                notes TEXT
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                rating INTEGER DEFAULT 5,
                date_added TEXT NOT NULL
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                national_id TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                job_title TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL,
                status TEXT DEFAULT '🟢 نشط برأس عمله',
                date_added TEXT NOT NULL
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS employee_custody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                handover_date TEXT NOT NULL,
                notes TEXT,
                status TEXT DEFAULT 'مستلمة',
                FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                qty INTEGER NOT NULL,
                unit_price REAL,
                total_price REAL,
                status TEXT NOT NULL,
                order_date TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY(supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER NOT NULL,
                m_type TEXT NOT NULL,
                description TEXT,
                m_date TEXT NOT NULL,
                cost REAL,
                status TEXT DEFAULT '⏳ مجدولة',
                FOREIGN KEY(asset_id) REFERENCES assets(id) ON DELETE CASCADE
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT DEFAULT 'معلومة',
                is_read INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )''')
            conn.commit()
    
    def log_activity(self, action, table_name, details=""):
        with self.connection() as conn:
            conn.execute(
                "INSERT INTO activity_log (action, table_name, details, timestamp) VALUES (?, ?, ?, ?)",
                (action, table_name, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            
    def create_alert(self, alert_type, title, message, severity="معلومة"):
        with self.connection() as conn:
            conn.execute(
                "INSERT INTO alerts (alert_type, title, message, severity, created_at) VALUES (?, ?, ?, ?, ?)",
                (alert_type, title, message, severity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

    def add_asset(self, asset_type, name, qty, location, status, min_qty, notes):
        try:
            with self.connection() as conn:
                conn.execute(
                    "INSERT INTO assets (asset_type, name, quantity, location, status, min_quantity, date_added, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (asset_type, name.strip(), qty, location.strip(), status, min_qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes.strip())
                )
                conn.commit()
            self.log_activity("إضافة أصل", "assets", f"المادة: {name}")
            return True, "✅ تم حفظ المادة بنجاح!"
        except sqlite3.IntegrityError:
            return False, "⚠️ هذه المادة مسجلة مسبقاً!"

    def add_supplier(self, name, category, phone, email, address, rating):
        try:
            with self.connection() as conn:
                conn.execute(
                    "INSERT INTO suppliers (name, category, phone, email, address, rating, date_added) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name.strip(), category, phone.strip(), email.strip(), address.strip(), rating, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
            self.log_activity("إضافة مورد", "suppliers", f"المورد: {name}")
            return True, "✅ تم إضافة المورد بنجاح!"
        except sqlite3.IntegrityError:
            return False, "⚠️ هذا المورد مسجل مسبقاً!"

    def add_employee(self, name, national_id, phone, title, dept, salary, status):
        try:
            with self.connection() as conn:
                conn.execute(
                    "INSERT INTO employees (name, national_id, phone, job_title, department, salary, status, date_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name.strip(), national_id.strip(), phone.strip(), title.strip(), dept, salary, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
            self.log_activity("إضافة موظف", "employees", f"الموظف: {name}")
            return True, "✅ تم تسجيل بيانات الموظف بنجاح!"
        except sqlite3.IntegrityError:
            return False, "⚠️ رقم الهوية مسجل مسبقاً!"

    def add_custody(self, employee_id, emp_name, item_type, item_name, qty, handover_date, notes):
        with self.connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, quantity, min_quantity FROM assets WHERE name = ?", (item_name,))
            asset = c.fetchone()
            
            if not asset: return False, "❌ هذه المادة غير معرفة في المستودع!"
            if asset['quantity'] < qty: return False, f"❌ رصيد غير كافٍ! المتاح: {asset['quantity']} وحدات."
            
            new_qty = asset['quantity'] - qty
            c.execute("UPDATE assets SET quantity = ? WHERE id = ?", (new_qty, asset['id']))
            c.execute(
                "INSERT INTO employee_custody (employee_id, item_type, item_name, quantity, handover_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (employee_id, item_type, item_name, qty, handover_date, notes.strip())
            )
            conn.commit()
            
            if new_qty <= asset['min_quantity']:
                self.create_alert("⚠️ رصيد منخفض", f"نفاد وشيك من {item_name}", f"الرصيد المتبقي: {new_qty} وحدة فقط!", "عالي")
            
            self.log_activity("صرف عهدة", "employee_custody", f"صرف {qty} من {item_name} للموظف {emp_name}")
            return True, "✅ تم تسجيل المستلمات وتحديث المخزن فورياً!"

    def add_order(self, supplier_id, item_name, qty, unit_price, status, notes):
        total = qty * unit_price
        with self.connection() as conn:
            conn.execute(
                "INSERT INTO orders (supplier_id, item_name, qty, unit_price, total_price, status, order_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (supplier_id, item_name.strip(), qty, unit_price, total, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes.strip())
            )
            conn.commit()
        
        if status == "🟢 تم الاستلام":
            self.sync_order_to_inventory(item_name, qty)
        self.log_activity("إنشاء طلبية", "orders", f"المادة: {item_name}")
        return True

    def sync_order_to_inventory(self, item_name, qty):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        with self.connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, quantity FROM assets WHERE LOWER(name) = LOWER(?)", (item_name.strip(),))
            res = c.fetchone()
            if res:
                new_qty = res['quantity'] + qty
                c.execute("UPDATE assets SET quantity = ?, date_modified = ? WHERE id = ?", (new_qty, now_str, res['id']))
            else:
                c.execute(
                    "INSERT INTO assets (asset_type, name, quantity, location, status, min_quantity, date_added, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    ("🗂️ مستلمات توريد", item_name.strip(), qty, "المستودع الرئيسي", "✨ ممتازة", 5, now_str, "توريد تلقائي")
                )
            conn.commit()

db = DatabaseManager()

def to_excel_download(df):
    out = BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return out.getvalue()

# ====================== الشريط الجانبي الاحترافي ======================
with st.sidebar:
    if os.path.exists("app_icon.png"):
        st.image("app_icon.png", width=200)
    
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #d32f2f, #f44336); border-radius: 15px; color: white; margin-bottom: 20px;'>
        <h3 style='color: white; margin:5px 0; font-size:18px;'>🏢 جمعية الحياة والأمل</h3>
        <p style='margin:5px 0; font-size:12px;'>نظام الحوكمة المتكامل v3.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_unit = st.selectbox(
        "🚀 الانتقال السريع بين الأقسام:",
        [
            "📊 لوحة التحليلات والمؤشرات",
            "📦 إدارة الأصول والمستودعات",
            "👥 الكوادر ومستلمات الموظفين",
            "🏪 كشوفات الموردين المعتمدين",
            "📋 إدارة المشتريات والطلبيات",
            "🔧 جدول العمليات والصيانة",
            "⚠️ نظام التنبيهات والرقابة",
            "📜 سجل الحركات والتدقيق"
        ],
        key="nav"
    )
    
    st.markdown("---")
    st.markdown("### 📊 الحالة الآنية الفورية")
    with db.connection() as conn:
        count_assets = pd.read_sql_query("SELECT COUNT(*) as c FROM assets", conn)['c'][0]
        count_suppliers = pd.read_sql_query("SELECT COUNT(*) as c FROM suppliers", conn)['c'][0]
        count_employees = pd.read_sql_query("SELECT COUNT(*) as c FROM employees", conn)['c'][0]
        count_alerts = pd.read_sql_query("SELECT COUNT(*) as c FROM alerts WHERE is_read = 0", conn)['c'][0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 مواد", count_assets)
        st.metric("👥 موظفين", count_employees)
    with col2:
        st.metric("🏪 موردين", count_suppliers)
        st.metric("🔔 تنبيهات نشطة", count_alerts)

# ====================== 1. لوحة التحليلات والمؤشرات ======================
if current_unit == "📊 لوحة التحليلات والمؤشرات":
    st.markdown("<h1>📊 لوحة القيادة التحليلية</h1>", unsafe_allow_html=True)
    
    with db.connection() as conn:
        tot_assets = pd.read_sql_query("SELECT COUNT(*) as c FROM assets", conn)['c'][0]
        tot_qty = pd.read_sql_query("SELECT SUM(quantity) as s FROM assets", conn)['s'][0] or 0
        pend_orders = pd.read_sql_query("SELECT COUNT(*) as c FROM orders WHERE status = '⏳ قيد الانتظار'", conn)['c'][0]
        danger_stock = pd.read_sql_query("SELECT COUNT(*) as c FROM assets WHERE quantity <= min_quantity", conn)['c'][0]
        total_spent = pd.read_sql_query("SELECT SUM(total_price) as s FROM orders WHERE status = '🟢 تم الاستلام'", conn)['s'][0] or 0
        
        df_chart_1 = pd.read_sql_query("SELECT asset_type, SUM(quantity) as q_sum FROM assets GROUP BY asset_type", conn)
        df_chart_2 = pd.read_sql_query("SELECT status, COUNT(*) as count FROM orders GROUP BY status", conn)
        df_low_stock = pd.read_sql_query("SELECT name, quantity, min_quantity FROM assets WHERE quantity <= min_quantity ORDER BY quantity ASC", conn)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 سلع فريدة", tot_assets)
    c2.metric("📊 وحدات مخزن", tot_qty)
    c3.metric("⏳ طلبيات معلقة", pend_orders)
    c4.metric("⚠️ نواقص خطرة", danger_stock)
    c5.metric("💰 إنفاق معتمد", f"${total_spent:,.2f}")
    
    st.divider()
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if not df_chart_1.empty:
            fig1 = px.bar(df_chart_1, x='asset_type', y='q_sum', title="📊 توزيع رصيد المخزون حسب التصنيف", color='q_sum', color_continuous_scale="Blues")
            st.plotly_chart(fig1, use_container_width=True)
    with col_g2:
        if not df_chart_2.empty:
            fig2 = px.pie(df_chart_2, values='count', names='status', title="📋 مؤشر الحالات الإجمالية للطلبيات")
            st.plotly_chart(fig2, use_container_width=True)
            
    st.divider()
    st.subheader("⚠️ مركز رصد النواقص العاجلة")
    if not df_low_stock.empty:
        for _, r in df_low_stock.iterrows():
            st.markdown(f"<div class='alert-box alert-danger'>🚨 <b>{r['name']}</b> | الرصيد الحالي: {r['quantity']} وحدة (الحد الأدنى الحرج: {r['min_quantity']})</div>", unsafe_allow_html=True)
    else:
        st.success("✅ جميع مستويات المخزن آمنة وضمن النطاق الأخضر المعتمد!")

# ====================== 2. إدارة الأصول والمستودعات ======================
elif current_unit == "📦 إدارة الأصول والمستودعات":
    st.markdown("<h1>📦 إدارة جرد المخازن المتكامل</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["➕ إدخال مادة جديدة", "👁️ كشف الجرد الحالي"])
    
    with t1:
        with st.form("asset_form", clear_on_submit=True):
            st.subheader("📝 نموذج إضافة مادة مخزنية جديدة")
            col1, col2 = st.columns(2)
            with col1:
                a_type = st.selectbox("🏷️ تصنيف المادة", ["🗂️ قرطاسية ومكتبية", "☕ شاي وقهوة وسكر", "🧼 مواد تنظيف ومعقمات", "💻 أجهزة حاسوب", "💳 فيزت وبطاقات", "🪑 أثاث", "❓ أخرى"])
                a_name = st.text_input("📝 اسم المادة بدقة (مثال: ورق A4 أبيض)")
            with col2:
                a_qty = st.number_input("📊 الكمية الحالية", min_value=0, value=10, step=1)
                a_min = st.number_input("⚠️ حد الإنذار الأدنى", min_value=1, value=5, step=1)
            
            col3, col4 = st.columns(2)
            with col3:
                a_loc = st.text_input("📍 موقع التخزين (رقم الرف/الخزانة)")
                a_status = st.selectbox("✅ الحالة الفنية", ["✨ ممتازة", "👍 جيدة", "⚠️ متوسطة", "❌ تحتاج صيانة"])
            with col4:
                a_notes = st.text_area("📝 ملاحظات إضافية")
                
            if st.form_submit_button("💾 حفظ المادة في جرد المخزن", use_container_width=True):
                if a_name.strip() and a_loc.strip():
                    ok, msg = db.add_asset(a_type, a_name, a_qty, a_loc, a_status, a_min, a_notes)
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
                else: st.error("❌ يرجى ملء اسم المادة وموقع التخزين")
                
    with t2:
        st.subheader("📊 كشف الجرد الحالي للمستودع الرئيسي")
        with db.connection() as conn:
            df_assets = pd.read_sql_query("SELECT * FROM assets ORDER BY date_added DESC", conn)
        
        if not df_assets.empty:
            search = st.text_input("🔍 بحث سريع بالاسم:")
            filtered_df = df_assets[df_assets['name'].str.contains(search, case=False, na=False)] if search else df_assets
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.download_button("📥 تصدير كشف الجرد (Excel)", to_excel_download(filtered_df), "inventory_report.xlsx", use_container_width=True)
        else:
            st.info("🔍 لا توجد مواد مسجلة حتى الآن")

# ====================== 3. الكوادر ومستلمات الموظفين ======================
elif current_unit == "👥 الكوادر ومستلمات الموظفين":
    st.markdown("<h1>👥 إدارة ملفات الموظفين والعهود</h1>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["➕ تسجيل موظف", "🎁 صرف عهدة", "👁️ كشف شامل"])
    
    with t1:
        with st.form("emp_form", clear_on_submit=True):
            st.subheader("👤 نموذج تسجيل موظف جديد")
            col1, col2 = st.columns(2)
            with col1:
                e_name = st.text_input("👤 الاسم الكامل")
                e_nid = st.text_input("🆔 رقم الهوية الوطنية")
                e_phone = st.text_input("📞 رقم الهاتف")
            with col2:
                e_title = st.text_input("💼 المسمى الوظيفي")
                e_salary = st.number_input("💰 الراتب الشهري (USD)", min_value=0, step=50)
                e_status = st.selectbox("✅ الوضع الإداري", ["🟢 نشط", "🟡 إجازة", "🔴 منتهي"])
            
            e_dept = st.selectbox("🏢 القسم", ["👔 الإدارة", "💻 التقنية", "⚙️ العمليات", "👥 الموارد البشرية", "💼 المبيعات"])
            
            if st.form_submit_button("💾 حفظ بيانات الموظف", use_container_width=True):
                if e_name.strip() and e_nid.strip():
                    ok, msg = db.add_employee(e_name, e_nid, e_phone, e_title, e_dept, e_salary, e_status)
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
                else: st.error("❌ يرجى تعبئة الاسم الكامل ورقم الهوية")
                
    with t2:
        st.subheader("🎁 صرف وتسليم مستلمات للموظفين")
        with db.connection() as conn:
            emps_df = pd.read_sql_query("SELECT id, name, department FROM employees WHERE status != '🔴 منتهي'", conn)
            items_df = pd.read_sql_query("SELECT name, quantity FROM assets WHERE quantity > 0", conn)
            
        if emps_df.empty or items_df.empty:
            st.warning("⚠️ يجب توفر موظفين ومواد مخزنية نشطة أولاً لإتمام عملية الصرف")
        else:
            emp_dict = dict(zip(emps_df['name'] + " [" + emps_df['department'] + "]", emps_df['id']))
            emp_names_dict = dict(zip(emps_df['id'], emps_df['name']))
            
            with st.form("custody_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    selected_emp_str = st.selectbox("اختر الموظف المستلم", list(emp_dict.keys()))
                    selected_item = st.selectbox("اختر المادة من المخزن", items_df['name'].tolist())
                with col2:
                    custody_type = st.selectbox("نوع المستلمات", ["💻 أجهزة", "🗂️ قرطاسية", "💳 بطاقات", "☕ ضيافة"])
                    qty_to_give = st.number_input("الكمية المراد صرفها", min_value=1, value=1, step=1)
                
                notes_cust = st.text_input("📝 سبب أو بيان الصرف")
                if st.form_submit_button("🚀 إتمام عملية التسليم الفوري"):
                    eid = emp_dict[selected_emp_str]
                    ename = emp_names_dict[eid]
                    ok, msg = db.add_custody(eid, ename, custody_type, selected_item, qty_to_give, datetime.now().strftime("%Y-%m-%d"), notes_cust)
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
                    
    with t3:
        st.subheader("👁️ الكشوفات والتقارير الشاملة")
        with db.connection() as conn:
            df_e = pd.read_sql_query("SELECT * FROM employees", conn)
            df_c = pd.read_sql_query("SELECT * FROM employee_custody", conn)
        
        st.write("### 🗂️ سجل الموظفين الحاليين")
        st.dataframe(df_e, use_container_width=True, hide_index=True)
        st.write("### 🎁 كشف بعهد ومستلمات الموظفين")
        st.dataframe(df_c, use_container_width=True, hide_index=True)

# ====================== 4. كشوفات الموردين المعتمدين ======================
elif current_unit == "🏪 كشوفات الموردين المعتمدين":
    st.markdown("<h1>🏪 إدارة الموردين والشركاء المعتمدين</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["➕ إضافة مورد جديد", "👁️ كشف الموردين الحليين"])
    
    with t1:
        with st.form("supplier_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                s_name = st.text_input("🏪 اسم الشركة أو المورد")
                s_cat = st.selectbox("🏷️ مجال التوريد الرئيس", ["تجهيزات مكتبية", "مواد تموينية وضيافة", "أجهزة إلكترونية وصيانة", "خدمات لوجستية", "أخرى"])
                s_phone = st.text_input("📞 رقم هاتف المورد")
            with col2:
                s_email = st.text_input("📧 البريد الإلكتروني")
                s_address = st.text_input("📍 العنوان الجغرافي للشركة")
                s_rating = st.slider("⭐ تقييم جودة المورد", 1, 5, 5)
                
            if st.form_submit_button("💾 اعتماد المورد رسمياً"):
                if s_name.strip() and s_phone.strip():
                    ok, msg = db.add_supplier(s_name, s_cat, s_phone, s_email, s_address, s_rating)
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
                else: st.error("❌ يرجى ملء اسم المورد ورقم الهاتف على الأقل")
                
    with t2:
        st.subheader("📋 قائمة الموردين المتعاقد معهم رسمياً")
        with db.connection() as conn:
            df_suppliers = pd.read_sql_query("SELECT * FROM suppliers ORDER BY rating DESC", conn)
        if not df_suppliers.empty:
            st.dataframe(df_suppliers, use_container_width=True, hide_index=True)
        else:
            st.info("🔍 لا يوجد أي مورد معتمد حالياً في النظام")

# ====================== 5. إدارة المشتريات والطلبيات ======================
elif current_unit == "📋 إدارة المشتريات والطلبيات":
    st.markdown("<h1>📋 نظام إدارة المشتريات والتوريد</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["➕ إنشاء طلب شراء جديد", "👁️ سجل حركة المشتريات"])
    
    with db.connection() as conn:
        sups_df = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
        
    with t1:
        if sups_df.empty:
            st.warning("⚠️ يجب إدخال الموردين في النظام أولاً قبل إنشاء طلبات التوريد.")
        else:
            sup_dict = dict(zip(sups_df['name'], sups_df['id']))
            with st.form("order_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    sel_sup = st.selectbox("اختر المورد المستهدف", list(sup_dict.keys()))
                    o_item = st.text_input("📝 البيان / اسم المادة المطلوبة توريدها")
                    o_qty = st.number_input("📊 الكمية المطلوبة", min_value=1, value=1)
                with col2:
                    o_price = st.number_input("💰 سعر الوحدة الواحد التقديري", min_value=0.0, value=0.0, format="%.2f")
                    o_status = st.selectbox("🚦 حالة الطلب الحالية", ["⏳ قيد الانتظار", "🟢 تم الاستلام", "❌ ملغي"])
                    o_notes = st.text_input("📝 شروط التوريد أو ملاحظات")
                    
                if st.form_submit_button("🚀 إرسال واعتماد طلب الشراء"):
                    if o_item.strip():
                        sid = sup_dict[sel_sup]
                        db.add_order(sid, o_item, o_qty, o_price, o_status, o_notes)
                        st.success("✅ تم تسجيل أمر المشتريات ومزامنة المخازن تلقائياً عند الاقتضاء!")
                        st.rerun()
                    else:
                        st.error("❌ يرجى كتابة اسم المادة المطلوبة لتسجيل الحركة")
                        
    with t2:
        st.subheader("📜 كشف أوامر التوريد الصادرة")
        with db.connection() as conn:
            df_orders = pd.read_sql_query("""
                SELECT orders.id, suppliers.name as supplier_name, orders.item_name, orders.qty, 
                       orders.unit_price, orders.total_price, orders.status, orders.order_date, orders.notes
                FROM orders 
                LEFT JOIN suppliers ON orders.supplier_id = suppliers.id 
                ORDER BY orders.order_date DESC
            """, conn)
        if not df_orders.empty:
            st.dataframe(df_orders, use_container_width=True, hide_index=True)
        else:
            st.info("🔍 لا توجد طلبات شراء مسجلة حالياً")

# ====================== 6. جدول العمليات والصيانة ======================
elif current_unit == "🔧 جدول العمليات والصيانة":
    st.markdown("<h1>🔧 إدارة صيانة أصول ومرافق الجمعية</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["➕ جدولة عملية صيانة", "👁️ سجل وحالات الصيانة"])
    
    with db.connection() as conn:
        assets_df = pd.read_sql_query("SELECT id, name FROM assets", conn)
        
    with t1:
        if assets_df.empty:
            st.warning("⚠️ يجب تسجيل الأصول والمواد في المستودع أولاً للتمكن من جدولة الصيانة لها.")
        else:
            asset_dict = dict(zip(assets_df['name'], assets_df['id']))
            with st.form("maintenance_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    sel_asset = st.selectbox("اختر الأصل المراد صيانته", list(asset_dict.keys()))
                    m_type = st.selectbox("🛠️ نوع الصيانة", ["وقائية دائرية", "إصلاح طارئ", "تحديث وتطوير"])
                    m_desc = st.text_area("📝 تفاصيل دقيقة للعطل أو الإجراء المطلوب")
                with col2:
                    m_cost = st.number_input("💰 تكلفة الصيانة المقدرة/الفعلية", min_value=0.0, value=0.0, format="%.2f")
                    m_status = st.selectbox("🚦 الموقف الحالي", ["⏳ مجدولة", "⚙️ قيد التنفيذ", "🟢 تم الإنجاز"])
                    
                if st.form_submit_button("💾 قيد عملية الصيانة في جدول الأعمال"):
                    aid = asset_dict[sel_asset]
                    with db.connection() as conn:
                        conn.execute(
                            "INSERT INTO maintenance (asset_id, m_type, description, m_date, cost, status) VALUES (?, ?, ?, ?, ?, ?)",
                            (aid, m_type, m_desc.strip(), datetime.now().strftime("%Y-%m-%d"), m_cost, m_status)
                        )
                        conn.commit()
                    db.log_activity("جدولة صيانة", "maintenance", f"الأصل: {sel_asset}")
                    st.success("✅ تم جدولة وتثبيت أمر الصيانة الفني بنجاح!")
                    st.rerun()
                    
    with t2:
        st.subheader("📋 السجل الفني لعمليات صيانة الأصول والمعدات")
        with db.connection() as conn:
            df_maint = pd.read_sql_query("""
                SELECT maintenance.id, assets.name as asset_name, maintenance.m_type, 
                       maintenance.description, maintenance.m_date, maintenance.cost, maintenance.status
                FROM maintenance
                JOIN assets ON maintenance.asset_id = assets.id
                ORDER BY maintenance.m_date DESC
            """, conn)
        if not df_maint.empty:
            st.dataframe(df_maint, use_container_width=True, hide_index=True)
        else:
            st.info("🔍 لا توجد عمليات صيانة مجدولة أو مسجلة في السجل")

# ====================== 7. نظام التنبيهات والرقابة ======================
elif current_unit == "⚠️ نظام التنبيهات والرقابة":
    st.markdown("<h1>🔔 مركز الرقابة والتنبيهات الذكية</h1>", unsafe_allow_html=True)
    
    with db.connection() as conn:
        if st.button("🧹 تعيين كافة التنبيهات كمقروءة", use_container_width=True):
            conn.execute("UPDATE alerts SET is_read = 1")
            conn.commit()
            st.success("✅ تم تصفير لوحة التنبيهات النشطة.")
            st.rerun()
            
        df_alerts = pd.read_sql_query("SELECT * FROM alerts ORDER BY created_at DESC", conn)
        
    if not df_alerts.empty:
        for _, alert in df_alerts.iterrows():
            box_style = "alert-danger" if alert['severity'] == "عالي" else "alert-warning"
            st.markdown(
                f"<div class='alert-box {box_style}'>"
                f"<b>[{alert['alert_type']}] {alert['title']}</b> ({alert['created_at']})<br/>"
                f"{alert['message']}"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.success("🟢 لوحة الرقابة نظيفة تماماً، لا توجد أي إشعارات أو مشاكل حالية!")

# ====================== 8. سجل الحركات والتدقيق ======================
elif current_unit == "📜 سجل الحركات والتدقيق":
    st.markdown("<h1>📜 سجل الأمن والتدقيق العام للشاشات (Audit Log)</h1>", unsafe_allow_html=True)
    st.subheader("🔍 مراجعة فورية لكافة العمليات المنفذة على النظام لضمان الحوكمة")
    
    with db.connection() as conn:
        df_logs = pd.read_sql_query("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 500", conn)
        
    if not df_logs.empty:
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
        st.download_button("📥 تصدير سجل الأمان بالكامل لغايات التدقيق والمراجعة", to_excel_download(df_logs), "system_audit_log.xlsx", use_container_width=True)
    else:
        st.info("🔍 السجل فارغ، لم يتم رصد أي عمليات حتى اللحظة")
