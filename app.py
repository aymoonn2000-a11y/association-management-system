import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="النظام اللوجستي المحترف",
    page_icon="🏢",
    layout="wide"
)

# ===================================
# إعداد الاتصال بقاعدة البيانات والتحضير
# ===================================
def get_db_connection():
    conn = sqlite3.connect('logistics.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    # جدول المخزن
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            available INTEGER,
            issued INTEGER,
            min_limit INTEGER
        )
    ''')
    # جدول العهد والموظفين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_assigned TEXT,
            emp_name TEXT,
            job_title TEXT,
            program TEXT,
            custody_items TEXT,
            notes TEXT
        )
    ''')
    # جدول مهام حركة المراسل
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_desc TEXT,
            receiver TEXT,
            status TEXT
        )
    ''')
    
    # إضافة بيانات أولية للمخزن إذا كان فارغاً
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            ("لاب توب", 10, 2, 3),
            ("آيباد", 5, 1, 2),
            ("قرطاسية", 100, 20, 15),
            ("تيشيرت الجمعية", 4, 12, 5)
        ]
        cursor.executemany("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, ?, ?)", initial_data)
        
    conn.commit()
    conn.close()

create_tables()

# ===================================
# واجهة وتنسيقات التطبيق
# ===================================
st.markdown("""
<style>
.main { background:#f5f7fb; }
.title { text-align:center; padding:10px; color:#1e3a8a; }
.metric-card {
    background: white; border-radius: 12px; padding: 15px; text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,.05); border-right: 5px solid #2563eb;
}
.metric-number { font-size: 28px; color: #2563eb; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'><h1>🏢 النظام اللوجستي الذكي وقاعدة البيانات الدائمة</h1><p>إدارة حركة المراسلين والمخازن والعهد بدون قلق من ضياع البيانات</p></div>", unsafe_allow_html=True)

# ===================================
# جلب البيانات لحساب الإحصائيات في الأعلى
# ===================================
conn = get_db_connection()
df_inv_stat = pd.read_sql_query("SELECT * FROM inventory", conn)
df_emp_stat = pd.read_sql_query("SELECT * FROM employees", conn)
df_tasks_stat = pd.read_sql_query("SELECT * FROM tasks", conn)
conn.close()

total_emp = len(df_emp_stat)
total_items = df_inv_stat['available'].sum() if not df_inv_stat.empty else 0
shortage_items = sum(1 for _, r in df_inv_stat.iterrows() if r['available'] <= r['min_limit']) if not df_inv_stat.empty else 0
active_deliveries = sum(1 for _, r in df_tasks_stat.iterrows() if r['status'] == "جاري التنفيذ") if not df_tasks_stat.empty else 0

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='metric-card'><div>موظفين بعهد نشطة</div><div class='metric-number'>{total_emp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card'><div>قطع المخزن المتوفرة</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card' style='border-right-color:#ef4444;'><div>مواد تحتاج طلب ⚠️</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card' style='border-right-color:#f59e0b;'><div>مهام حركة معلقة 🏃‍♂️</div><div class='metric-number' style='color:#f59e0b;'>{active_deliveries}</div></div>", unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3 = st.tabs(["🏃‍♂️ حركة وتوصيلات المراسل", "👥 إدارة عهد الموظفين", "📦 مستودع وجرد المواد"])

# ===================================
# التبويب الأول: مهام الحركة
# ===================================
with tab1:
    st.subheader("📋 تسجيل مهمة ميدانية جديدة")
    col1, col2, col3 = st.columns(3)
    with col1: t_desc = st.text_input("وصف الشحنة / الأوراق الموجهة للميدان")
    with col2: t_rec = st.text_input("الجهة المستلمة بالخارج")
    with col3: t_status = st.selectbox("الحالة", ["جاري التنفيذ", "تم التسليم بنجاح", "ملغي"])
    
    if st.button("➕ حفظ المهمة في السجل الدائم"):
        if t_desc and t_rec:
            conn = get_db_connection()
            conn.execute("INSERT INTO tasks (task_date, task_desc, receiver, status) VALUES (?, ?, ?, ?)",
                         (str(datetime.now().date()), t_desc, t_rec, t_status))
            conn.commit()
            conn.close()
            st.success("تم التخزين بنجاح!")
            st.rerun()

    st.write("---")
    st.subheader("🔄 سجل الحركة الحالي (يمكنك تعديل الحالة مباشرة واضغط لأسفل لحفظ التعديل)")
    if not df_tasks_stat.empty:
        # السماح للمراسل بتحديث الحالات وضغط الحفظ
        edited_tasks = st.data_editor(df_tasks_stat, key="tasks_editor", use_container_width=True, disabled=["id", "task_date"])
        if st.button("💾 حفظ تعديلات حالات التوصيل"):
            conn = get_db_connection()
            for _, row in edited_tasks.iterrows():
                conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (row['status'], row['id']))
            conn.commit()
            conn.close()
            st.success("تم تحديث الحالات في قاعدة البيانات")
            st.rerun()

# ===================================
# التبويب الثاني: عهد الموظفين والبرامج
# ===================================
with tab2:
    st.subheader("👤 صرف مواد من المخزن كعهدة موظف")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        e_name = st.text_input("اسم الموظف المستلم")
        e_title = st.text_input("المسمى الوظيفي")
    with col_e2:
        e_prog = st.selectbox("البرنامج التابع له", ["CVA", "MEAL", "WASH", "Shelter", "الإدارة العامّة"])
        inv_items_list = df_inv_stat['item_name'].tolist() if not df_inv_stat.empty else []
        e_custody = st.multiselect("اختر عهدة من المواد المتوفرة", inv_items_list)
        
    e_notes = st.text_area("تفاصيل أو حالة الأجهزة المستلمة")
    
    if st.button("💾 إتمام الصرف والخصم الأوتوماتيكي"):
        if e_name and e_custody:
            conn = get_db_connection()
            cursor = conn.cursor()
            can_issue = True
            
            # التأكد من توفر الكميات أولاً قبل الخصم
            for item in e_custody:
                cursor.execute("SELECT available FROM inventory WHERE item_name = ?", (item,))
                res = cursor.fetchone()
                if res and res['available'] < 1:
                    st.error(f"عذراً، المادة {item} نفدت من المخزن ولا يمكن صرفها!")
                    can_issue = False
            
            if can_issue:
                # 1. اخصم من المخزن
                for item in e_custody:
                    cursor.execute("UPDATE inventory SET available = available - 1, issued = issued + 1 WHERE item_name = ?", (item,))
                # 2. سجل الموظف
                cursor.execute("INSERT INTO employees (date_assigned, emp_name, job_title, program, custody_items, notes) VALUES (?, ?, ?, ?, ?, ?)",
                               (str(datetime.now().date()), e_name, e_title, e_prog, ", ".join(e_custody), e_notes))
                conn.commit()
                st.success(f"تم تسجيل العهدة باسم {e_name} وتحديث الكميات بنجاح!")
                conn.close()
                st.rerun()
            else:
                conn.close()

    st.write("---")
    st.subheader("🔍 استعراض وبحث العهد والبرامج")
    search = st.text_input("🔍 ابحث باسم الموظف الميداني أو العهدة")
    if not df_emp_stat.empty:
        display_df = df_emp_stat.copy()
        if search:
            display_df = display_df[display_df['emp_name'].str.contains(search, case=False) | display_df['custody_items'].str.contains(search, case=False)]
        st.dataframe(display_df, use_container_width=True)

# ===================================
# التبويب الثالث: إدارة المخزن
# ===================================
with tab3:
    st.subheader("📥 مدخلات مستودع المواد اللوجستية")
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1: i_name = st.text_input("اسم الصنف أو المادة")
    with col_i2: i_avail = st.number_input("الكمية الموردة الجديدة", min_value=0, value=0)
    with col_i3: i_min = st.number_input("حد أمان المخزن (التنبيه)", min_value=1, value=5)
    with col_i4: i_direct = st.number_input("صرف مباشر اضطراري بدون موظف", min_value=0, value=0)
    
    if st.button("🔄 إدخال للمستودع"):
        if i_name:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory WHERE item_name = ?", (i_name.strip(),))
            row = cursor.fetchone()
            
            if row:
                cursor.execute("UPDATE inventory SET available = available + ?, issued = issued + ?, min_limit = ? WHERE item_name = ?",
                               (i_avail, i_direct, i_min, i_name.strip()))
            else:
                cursor.execute("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, ?, ?)",
                               (i_name.strip(), i_avail, i_direct, i_min))
            conn.commit()
            conn.close()
            st.success("تم تحديث بيانات المستودع!")
            st.rerun()

    st.write("---")
    st.subheader("📊 جرد المخازن الحالي")
    if not df_inv_stat.empty:
        def highlight_shortage(row):
            return ['background-color: #ffcccc' if row['available'] <= row['min_limit'] else '' for _ in row]
        st.dataframe(df_inv_stat.style.apply(highlight_shortage, axis=1), use_container_width=True)
