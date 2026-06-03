import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from io import BytesIO
 
# 1. تهيئة إعدادات الصفحة (يجب أن تُستدعى مرة واحدة فقط في أول الكود)
st.set_page_config(
    page_title="نظام إدارة الجمعيات المتكامل",
    page_icon="🏢",
    layout="wide"
)

# ===================================
# إدارة قاعدة البيانات بطريقة آمنة
# ===================================
DB_NAME = 'association_system.db'

def run_db_query(query, params=(), is_select=False, fetch_all=True):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        if is_select:
            data = cursor.fetchall() if fetch_all else cursor.fetchone()
            conn.close()
            return data
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"⚠️ خطأ في قاعدة البيانات: {e}")
        return [] if is_select else False

def init_tables():
    # جدول المستودع والمواد للجمعية
    run_db_query('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            available INTEGER,
            issued INTEGER,
            min_limit INTEGER
        )
    ''')
    # جدول الموظفين والعهد
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
    # جدول حركة التوصيل والمراسلات
    run_db_query('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_desc TEXT,
            receiver TEXT,
            status TEXT
        )
    ''')
    
    # إدخال بيانات أولية للمشروع إذا كان فارغاً
    check = run_db_query("SELECT COUNT(*) as count FROM inventory", is_select=True, fetch_all=False)
    if check and check['count'] == 0:
        initial_items = [
            ("أجهزة لاب توب", 20, 5, 3),
            ("سلات غذائية وإغاثية", 150, 40, 10),
            ("قرطاسية ومستندات طبع", 200, 20, 15),
            ("مستلزمات طبية أولية", 40, 5, 8)
        ]
        for item in initial_items:
            run_db_query("INSERT OR IGNORE INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, ?, ?)", item)

# تشغيل التهيأة
init_tables()

# ===================================
# واجهة وتنسيقات التطبيق CSS
# ===================================
st.markdown("""
<style>
.main { background:#f8fafc; }
.title { text-align:center; padding:10px; color:#1e3a8a; }
.metric-card {
    background: white; border-radius: 12px; padding: 15px; text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,.05); border-right: 5px solid #1e3a8a;
}
.metric-number { font-size: 28px; color: #1e3a8a; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'><h1>🏢 نظام إدارة الجمعيات (Association Management System)</h1><p>لوحة تحكم ذكية متكاملة لإدارة الموارد، العهد، والتحركات اللوجستية</p></div>", unsafe_allow_html=True)

# ===================================
# جلب البيانات وتحويلها لـ DataFrames
# ===================================
inv_rows = run_db_query("SELECT * FROM inventory", is_select=True)
emp_rows = run_db_query("SELECT * FROM employees", is_select=True)
task_rows = run_db_query("SELECT * FROM tasks", is_select=True)

df_inv = pd.DataFrame([dict(r) for r in inv_rows]) if inv_rows else pd.DataFrame(columns=['id', 'item_name', 'available', 'issued', 'min_limit'])
df_emp = pd.DataFrame([dict(r) for r in emp_rows]) if emp_rows else pd.DataFrame(columns=['id', 'date_assigned', 'emp_name', 'job_title', 'program', 'custody_items', 'notes'])
df_tasks = pd.DataFrame([dict(r) for r in task_rows]) if task_rows else pd.DataFrame(columns=['id', 'task_date', 'task_desc', 'receiver', 'status'])

# حساب إحصائيات الـ Metrics
total_emp = len(df_emp)
total_items = df_inv['available'].sum() if not df_inv.empty else 0
shortage_items = sum(1 for _, r in df_inv.iterrows() if r['available'] <= r['min_limit']) if not df_inv.empty else 0
active_deliveries = sum(1 for _, r in df_tasks.iterrows() if r['status'] == "جاري التنفيذ") if not df_tasks.empty else 0

# عرض بطاقات الأداء العلوية
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='metric-card'><div>موظفين بعهد نشطة</div><div class='metric-number'>{total_emp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card'><div>إجمالي مواد المخزن</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card' style='border-right-color:#ef4444;'><div>مواد قاربت على النفاد ⚠️</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card' style='border-right-color:#f59e0b;'><div>طلبات حركة ميدانية</div><div class='metric-number' style='color:#f59e0b;'>{active_deliveries}</div></div>", unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["🏃‍♂️ حركة وتوصيلات المراسل", "👥 عهد الموظفين والبرامج", "📦 مستودع وجرد المواد", "📊 إحصائيات بيانية"])

# التبويب الأول: حركة وتوصيلات المراسل
with tab1:
    st.subheader("📋 تسجيل وتتبع مهمة ميدانية")
    col1, col2, col3 = st.columns(3)
    with col1: t_desc = st.text_input("وصف الشحنة / الأوراق الموجهة للميدان", key="task_in")
    with col2: t_rec = st.text_input("الجهة المستلمة بالخارج", key="rec_in")
    with col3: t_status = st.selectbox("الحالة الحالية للمهمة", ["جاري التنفيذ", "تم التسليم بنجاح", "ملغي"])
    
    if st.button("➕ حفظ المهمة في السجل"):
        if t_desc and t_rec:
            res = run_db_query("INSERT INTO tasks (task_date, task_desc, receiver, status) VALUES (?, ?, ?, ?)",
                         (str(datetime.now().date()), t_desc, t_rec, t_status))
            if res:
                st.success("تم تخزين مهمة الحركة بنجاح!")
                st.rerun()

    st.write("---")
    st.subheader("🔄 جدول الحركة والمتابعة اليومية")
    if not df_tasks.empty:
        edited_tasks = st.data_editor(df_tasks, key="tasks_editor", use_container_width=True, disabled=["id", "task_date"])
        if st.button("💾 حفظ تعديلات حالات التوصيل"):
            success_flag = True
            for _, row in edited_tasks.iterrows():
                res = run_db_query("UPDATE tasks SET status = ? WHERE id = ?", (row['status'], row['id']))
                if not res: success_flag = False
            if success_flag:
                st.success("تم تحديث الحالات بنجاح!")
                st.rerun()
    else:
        st.info("لا توجد مهام حركة مسجلة.")

# التبويب الثاني: عهد الموظفين والبرامج
with tab2:
    st.subheader("👤 صرف مواد كعهدة ميدانية أو إدارية")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        e_name = st.text_input("اسم الموظف المستلم")
        e_title = st.text_input("المسمى الوظيفي")
    with col_e2:
        e_prog = st.selectbox("البرنامج التابع له بالجمعية", ["التعليم", "الإغاثة والتمكين", "الرعاية الصحية", "الإدارة العامة"])
        inv_items_list = df_inv['item_name'].tolist() if not df_inv.empty else []
        e_custody = st.multiselect("اختر عهدة من المواد المتوفرة بالمخزن", inv_items_list)
        
    e_notes = st.text_area("ملاحظات إضافية")
    
    if st.button("💾 إتمام الصرف والخصم الأوتوماتيكي"):
        if e_name and e_custody:
            can_issue = True
            for item in e_custody:
                res = run_db_query("SELECT available FROM inventory WHERE item_name = ?", (item,), is_select=True, fetch_all=False)
                if res and res['available'] < 1:
                    st.error(f"عذراً، المادة {item} غائبة أو نفدت من المخزن!")
                    can_issue = False
            
            if can_issue:
                for item in e_custody:
                    run_db_query("UPDATE inventory SET available = available - 1, issued = issued + 1 WHERE item_name = ?", (item,))
                run_db_query("INSERT INTO employees (date_assigned, emp_name, job_title, program, custody_items, notes) VALUES (?, ?, ?, ?, ?, ?)",
                               (str(datetime.now().date()), e_name, e_title, e_prog, ", ".join(e_custody), e_notes))
                st.success(f"تم تسجيل العهدة للموظف {e_name} بنجاح!")
                st.rerun()

    st.write("---")
    st.subheader("🔍 استعراض وبحث العهد النشطة")
    search = st.text_input("🔍 ابحث باسم الموظف أو بنوع العهدة")
    if not df_emp.empty:
        display_df = df_emp.copy()
        if search:
            display_df = display_df[display_df['emp_name'].str.contains(search, case=False) | display_df['custody_items'].str.contains(search, case=False)]
        st.dataframe(display_df, use_container_width=True)

# التبويب الثالث: إدارة المخزن والتصدير لـ Excel
with tab3:
    st.subheader("📥 مدخلات مستودع المواد")
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1: i_name = st.text_input("اسم الصنف المُراد تحديثه أو إضافته")
    with col_i2: i_avail = st.number_input("الكمية الموردة الجديدة", min_value=0, value=0)
    with col_i3: i_min = st.number_input("حد الأمان لتنبيه الإدارة", min_value=1, value=5)
    with col_i4: i_direct = st.number_input("صادر مباشر بدون عهدة", min_value=0, value=0)
    
    if st.button("🔄 تحديث بيانات المخزن"):
        if i_name:
            row = run_db_query("SELECT * FROM inventory WHERE item_name = ?", (i_name.strip(),), is_select=True, fetch_all=False)
            if row:
                run_db_query("UPDATE inventory SET available = available + ?, issued = issued + ?, min_limit = ? WHERE item_name = ?",
                               (i_avail, i_direct, i_min, i_name.strip()))
            else:
                run_db_query("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, ?, ?)",
                               (i_name.strip(), i_avail, i_direct, i_min))
            st.success("تم تحديث مخازن الجمعية بنجاح!")
            st.rerun()

    st.write("---")
    st.subheader("📊 جرد مخازن الجمعية الحالي")
    if not df_inv.empty:
        def highlight_shortage(row):
            return ['background-color: #ffcccc' if row['available'] <= row['min_limit'] else '' for _ in row]
        st.dataframe(df_inv.style.apply(highlight_shortage, axis=1), use_container_width=True)
        
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_inv.to_excel(writer, index=False, sheet_name='جرد المخزن')
                df_emp.to_excel(writer, index=False, sheet_name='سجل العهد')
                df_tasks.to_excel(writer, index=False, sheet_name='حركة التوصيل')
            processed_data = output.getvalue()
            st.download_button(
                label="📥 تحميل التقرير الشامل كملف Excel",
                data=processed_data,
                file_name=f"Association_Report_{datetime.now().date()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"فشل توليد ملف Excel: {e}")

# التبويب الرابع: إحصائيات بيانية (Plotly)
with tab4:
    st.subheader("📊 تحليلات بيانية سريعة لحالة الدعم اللوجستي")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if not df_inv.empty and df_inv['item_name'].any():
            st.write("🔄 **مقارنة بين الكميات المتوفرة مقابل الصادرة**")
            fig_inv = px.bar(df_inv, x="item_name", y=["available", "issued"],
                             labels={"item_name": "المادة", "value": "الكمية", "variable": "الحالة"},
                             barmode="group", color_discrete_sequence=["#1e3a8a", "#ef4444"])
            st.plotly_chart(fig_inv, use_container_width=True)
    with col_g2:
        if not df_emp.empty and 'program' in df_emp.columns:
            st.write("📈 **توزيع استهلاك الموارد حسب البرامج**")
            program_counts = df_emp['program'].value_counts().reset_index()
            program_counts.columns = ['البرنامج', 'عدد العهد']
            fig_pie = px.pie(program_counts, values='عدد العهد', names='البرنامج',
                             color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_pie, use_container_width=True)
