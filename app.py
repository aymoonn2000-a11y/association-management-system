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
    
    h1 { color: #d32f2f; text-align: center; font-weight: 700; } /* تم تعديل اللون ليتناسق مع هوية الشعار الأحمر */
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
                conn.execute("""INSERT INTO suppliers (name
