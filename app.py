import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title="النظام اللوجستي الذكي المتكامل",
    page_icon="📦",
    layout="wide"
)

# ===================================
# إعداد الاتصال بقاعدة البيانات والتحضير
# ===================================
def get_db_connection():
    conn = sqlite3.connect('logistics_pro.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 1. جدول المخزن
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            available INTEGER,
            issued INTEGER,
            min_limit INTEGER
        )
    ''')
    # 2. جدول العهد والموظفين
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
    # 3. جدول مهام حركة المراسل
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_desc TEXT,
            receiver TEXT,
            status TEXT
        )
    ''')
    
    # بيانات أولية للمخزن إذا كان فارغاً
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            ("لاب توب", 15, 3, 4),
            ("آيباد", 8, 2, 2),
            ("قرطاسية وحبارات", 120, 30, 20),
            ("تيشيرت الجمعية", 50, 10, 15),
            ("أدوات صيانة ومفكات", 10, 1, 3)
        ]
        cursor.executemany("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, ?, ?)", initial_data)
        
    conn.commit()
    conn.close()

create_tables()

# ===================================
# واجهة وتنسيقات التطبيق CSS
# ===================================
st.markdown("""
<style>
.main { background:#f8fafc; }
.title { text-align:center; padding:10px; color:#1e3a8a; }
.metric-card {
    background: white; border-radius: 12px; padding: 15px; text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,.05); border-right: 5px solid #3b82f6;
}
.metric-number { font-size: 28px; color: #1e3a8a; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'><h1>🏢 النظام اللوجستي الداخلي لإدارة الحركة والمخازن</h1><p>تكامل ذكي بين الأقسام باستخدام قاعدة البيانات والرسوم البيانية</p></div>", unsafe_allow_html=True)

# ===================================
# جلب البيانات وتحديثها باستمرار
# ===================================
conn = get_db_connection()
df_inv = pd.read_sql_query("SELECT * FROM inventory", conn)
df_emp = pd.read_sql_query("SELECT * FROM employees", conn)
df_tasks = pd.read_sql_query("SELECT * FROM tasks", conn)
conn.close()

# حساب إحصائيات الـ Metrics
total_emp = len(df_emp)
total_items = df_inv['available'].sum() if not df_inv.empty else 0
shortage_items = sum(1 for _, r in df_inv.iterrows() if r['available'] <= r['min_limit']) if not df_inv.empty else 0
active_deliveries = sum(1 for _, r in df_tasks.iterrows() if r['status'] == "جاري التنفيذ") if not df_tasks.empty else 0

# عرض بطاقات الأداء العلوية
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='metric-card'><div>موظفين بعهد ميدانية</div><div class='metric-number'>{total_emp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card'><div>قطع المخزن المتوفرة</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card' style='border-right-color:#ef4444;'><div>مواد تحتاج طلب فوراً ⚠️</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card' style='border-right-color:#f59e0b;'><div>طلبات حركة معلقة 🏃‍♂️</div><div class='metric-number' style='color:#f59e0b;'>{active_deliveries}</div></div>", unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["🏃‍♂️ حركة وتوصيلات المراسل", "👥 عهد الموظفين والبرامج", "📦 مستودع وجرد المواد", "📊 إحصائيات بيانية لمديرك"])

# ===================================
# التبويب الأول: حركة وتوصيلات المراسل
# ===================================
with tab1:
    st.subheader("📋 تسجيل وتتبع مهمة ميدانية")
    col1, col2, col3 = st.columns(3)
    with col1: t_desc = st.text_input("وصف الشحنة / الأوراق الموجهة للميدان", key="task_in")
    with col2: t_rec = st.text_input("الجهة المستلمة بالخارج (بنوك / وزارات / شركاء)", key="rec_in")
    with col3: t_status = st.selectbox("الحالة الحالية للمهمة", ["جاري التنفيذ", "تم التسليم بنجاح", "ملغي"])
    
    if st.button("➕ حفظ المهمة في السجل اللوجستي"):
        if t_desc and t_rec:
            conn = get_db_connection()
            conn.execute("INSERT INTO tasks (task_date, task_desc, receiver, status) VALUES (?, ?, ?, ?)",
                         (str(datetime.now().date()), t_desc, t_rec, t_status))
            conn.commit()
            conn.close()
            st.success("تم تخزين مهمة الحركة بنجاح!")
            st.rerun()

    st.write("---")
    st.subheader("🔄 جدول الحركة والمتابعة اليومية")
    if not df_tasks.empty:
        # استخدام st.data_editor لتعديل البيانات مباشرة
        edited_tasks = st.data_editor(df_tasks, key="tasks_editor", use_container_width=True, disabled=["id", "task_date"])
        if st.button("💾 حفظ تعديلات حالات التوصيل"):
            conn = get_db_connection()
            for _, row in edited_tasks.iterrows():
                conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (row['status'], row['id']))
            conn.commit()
            conn.close()
            st.success("تم تحديث حالات حركة المراسل بنجاح!")
            st.rerun()
    else:
        st.info("لا توجد مهام حركة مسجلة لليوم.")

# ===================================
# التبويب الثاني: عهد الموظفين والبرامج
# ===================================
with tab2:
    st.subheader("👤 صرف مواد من المخزن كعهدة ميدانية")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        e_name = st.text_input("اسم الموظف المستلم")
        e_title = st.text_input("المسمى الوظيفي")
    with col_e2:
        e_prog = st.selectbox("البرنامج التابع له (الميزانية المخصصة)", ["CVA", "MEAL", "WASH", "Shelter", "الإدارة العامّة"])
        inv_items_list = df_inv['item_name'].tolist() if not df_inv.empty else []
        e_custody = st.multiselect("اختر عهدة من المواد المتوفرة بالمخزن", inv_items_list)
        
    e_notes = st.text_area("ملاحظات إضافية على الأجهزة والقطع")
    
    if st.button("💾 إتمام الصرف والخصم الأوتوماتيكي من المستودع"):
        if e_name and e_custody:
            conn = get_db_connection()
            cursor = conn.cursor()
            can_issue = True
            
            for item in e_custody:
                cursor.execute("SELECT available FROM inventory WHERE item_name = ?", (item,))
                res = cursor.fetchone()
                if res and res['available'] < 1:
                    st.error(f"عذراً، المادة {item} غائبة أو نفدت من المخزن!")
                    can_issue = False
            
            if can_issue:
                for item in e_custody:
                    cursor.execute("UPDATE inventory SET available = available - 1, issued = issued + 1 WHERE item_name = ?", (item,))
                cursor.execute("INSERT INTO employees (date_assigned, emp_name, job_title, program, custody_items, notes) VALUES (?, ?, ?, ?, ?, ?)",
                               (str(datetime.now().date()), e_name, e_title, e_prog, ", ".join(e_custody), e_notes))
                conn.commit()
                st.success(f"تم تسجيل العهدة باسم الموظف {e_name} وخصم المواد تلقائياً!")
                conn.close()
                st.rerun()
            else:
                conn.close()

    st.write("---")
    st.subheader("🔍 استعراض وبحث العهد النشطة")
    search = st.text_input("🔍 ابحث باسم الموظف أو بنوع العهدة المصروفة")
    if not df_emp.empty:
        display_df = df_emp.copy()
        if search:
            display_df = display_df[display_df['emp_name'].str.contains(search, case=False) | display_df['custody_items'].str.contains(search, case=False)]
        st.dataframe(display_df, use_container_width=True)

# ===================================
# التبويب الثالث: إدارة المخزن والتصدير لـ Excel
# ===================================
with tab3:
    st.subheader("📥 مدخلات مستودع المواد اللوجستية والقرطاسية")
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1: i_name = st.text_input("اسم الصنف المُراد تحديثه أو إضافته")
    with col_i2: i_avail = st.number_input("الكمية الموردة الجديدة (الداخلة)", min_value=0, value=0)
    with col_i3: i_min = st.number_input("حد الأمان بالمخزن لتنبيهك قبل النفاد", min_value=1, value=5)
    with col_i4: i_direct = st.number_input("صادر مباشر بدون عهدة موظف (استهلاك/تالف)", min_value=0, value=0)
    
    if st.button("🔄 تحديث بيانات المستودع"):
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
            st.success("تم تحديث المخازن بنجاح!")
            st.rerun()

    st.write("---")
    st.subheader("📊 جرد المخازن الحالي")
    if not df_inv.empty:
        def highlight_shortage(row):
            return ['background-color: #ffcccc' if row['available'] <= row['min_limit'] else '' for _ in row]
        st.dataframe(df_inv.style.apply(highlight_shortage, axis=1), use_container_width=True)
        
        # ميزة تفوق كودك القديم: تصدير Excel حقيقي ومنسق باستخدام openpyxl عبر الذاكرة
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_inv.to_excel(writer, index=False, sheet_name='جرد المخزن')
            df_emp.to_excel(writer, index=False, sheet_name='سجل العهد')
            df_tasks.to_excel(writer, index=False, sheet_name='حركة المراسل')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 تحميل التقرير اللوجستي الشامل كملف Excel",
            data=processed_data,
            file_name=f"Logistics_Report_{datetime.now().date()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ===================================
# التبويب الرابع: إحصائيات بيانية لمديرك (Plotly)
# ===================================
with tab4:
    st.subheader("📊 تحليلات بيانية سريعة لحالة الدعم اللوجستي")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if not df_inv.empty:
            st.write("🔄 **مقارنة بين الكميات المتوفرة مقابل الصادرة في المخزن**")
            # رسم بياني شريطي ذكي من Plotly لبيانات المستودع
            fig_inv = px.bar(df_inv, x="item_name", y=["available", "issued"],
                             labels={"item_name": "المادة", "value": "الكمية", "variable": "الحالة"},
                             barmode="group", color_discrete_sequence=["#3b82f6", "#ef4444"])
            st.plotly_chart(fig_inv, use_container_width=True)
            
    with col_g2:
        if not df_emp.empty:
            st.write("📈 **توزيع العهد واللوجستيات حسب البرامج الإنسانية في الجمعية**")
            # رسم بياني دائري يوضح أي البرامج يستهلك موارد لوجستية أكثر
            program_counts = df_emp['program'].value_counts().reset_index()
            program_counts.columns = ['البرنامج', 'عدد العهد المصروفة']
            fig_pie = px.pie(program_counts, values='عدد العهد المصروفة', names='البرنامج',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("قم بإضافة عهد للموظفين لرؤية توزيع نسب استهلاك البرامج للموارد.")
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title="النظام اللوجستي - نسخة الحماية",
    page_icon="📦",
    layout="wide"
)

# دالة آمنة للاتصال بقاعدة البيانات لمنع انهيار السيرفر
def run_db_query(query, params=(), is_select=False):
    try:
        conn = sqlite3.connect('logistics_safe.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        if is_select:
            data = cursor.fetchall()
            conn.close()
            return data
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        # عرض الخطأ للمستخدم مباشرة على الواجهة بدلاً من إغلاق السيرفر
        st.error(f"⚠️ حدث خطأ في قاعدة البيانات: {e}")
        return [] if is_select else False

# إنشاء الجداول بشكل آمن
try:
    run_db_query('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            available INTEGER,
            issued INTEGER,
            min_limit INTEGER
        )
    ''')
    run_db_query('''
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
    run_db_query('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_desc TEXT,
            receiver TEXT,
            status TEXT
        )
    ''')
    
    # إضافة بيانات أولية إذا كان الجدول فارغاً
    check_empty = run_db_query("SELECT COUNT(*) as count FROM inventory", is_select=True)
    if check_empty and check_empty[0]['count'] == 0:
        run_db_query("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES ('لاب توب', 10, 2, 3)")
        run_db_query("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES ('قرطاسية', 50, 10, 5)")
except Exception as e:
    st.error(f"خطأ أثناء تهيئة النظام: {e}")

# واجهة التطبيق الرئيسية
st.title("🏢 لوحة التحكم اللوجستية الآمنة")
st.write("إذا ظهر أي خطأ برامجي، سيتم عرضه هنا بالأسفل دون توقف التطبيق.")

tab1, tab2 = st.tabs(["📦 المخزن والحركة", "📊 البيانات الإحصائية"])

with tab1:
    st.subheader("جرد المستودع الحالي")
    db_data = run_db_query("SELECT * FROM inventory", is_select=True)
    if db_data:
        df = pd.DataFrame([dict(row) for row in db_data])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("لا توجد بيانات متوفرة حالياً في قاعدة البيانات.")

with tab2:
    st.subheader("الرسوم البيانية (Plotly)")
    if db_data:
        df_graph = pd.DataFrame([dict(row) for row in db_data])
        fig = px.bar(df_graph, x="item_name", y="available", title="الكميات المتوفرة لكل صنف")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("لا توجد بيانات لرسمها بياناً.")
