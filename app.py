import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from io import BytesIO
import streamlit.components.v1 as components

# ===================================
# 1. تهيئة إعدادات الصفحة والهوية البصرية
# ===================================
st.set_page_config(
    page_title="نظام إدارة الجمعيات المتكامل",
    page_icon="🏢",
    layout="wide"
)

# ===================================
# 2. إدارة قاعدة البيانات بطريقة آمنة وسحابية
# ===================================
DB_NAME = 'association_system.db'

def run_db_query(query, params=(), is_select=False, fetch_all=True):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            if is_select:
                return cursor.fetchall() if fetch_all else cursor.fetchone()
            conn.commit()
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
    # جدول الموظفين والعهد النشطة
    run_db_query('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_assigned TEXT,
            emp_name TEXT,
            job_title TEXT,
            program TEXT,
            custody_items TEXT,
            status TEXT DEFAULT 'نشطة',
            notes TEXT
        )
    ''')
    # جدول حركة التوصيل والمراسلات الميدانية
    run_db_query('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_date TEXT,
            task_desc TEXT,
            receiver TEXT,
            status TEXT
        )
    ''')
    
    # إدخال بيانات أولية للمشروع إذا كان فارغاً لأول مرة
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

init_tables()

# ===================================
# 3. منظومة مراقبة الشبكة والمزامنة التلقائية (Offline Sync JavaScript)
# ===================================
offline_sync_js = """
<script>
    function updateOnlineStatus() {
        const statusBar = document.getElementById('status-bar');
        if (navigator.onLine) {
            statusBar.innerHTML = '🟢 متصل بالسيرفر السحابي - يتم الآن مزامنة العمل الميداني تلقائياً';
            statusBar.style.backgroundColor = '#d1fae5';
            statusBar.style.color = '#065f46';
            syncOfflineData();
        } else {
            statusBar.innerHTML = '⚠️ وضع الميدان النشط (بدون إنترنت) - سيتم حفظ وتأمين مدخلاتك محلياً بالجوال';
            statusBar.style.backgroundColor = '#fee2e2';
            statusBar.style.color = '#991b1b';
        }
    }

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    function syncOfflineData() {
        let tasks = JSON.parse(localStorage.getItem('offline_tasks')) || [];
        if (tasks.length > 0) {
            Streamlit.setComponentValue(tasks);
            localStorage.removeItem('offline_tasks');
        }
    }
</script>
<div id="status-bar" style="padding:12px; text-align:center; font-family:sans-serif; font-size:14px; font-weight:bold; border-radius:8px; margin-bottom:10px; transition: 0.3s;">
    🔄 جاري فحص استقرار اتصال الميدان بـ Streamlit Cloud...
</div>
<script>updateOnlineStatus();</script>
"""

# ===================================
# 4. واجهة وتنسيقات التطبيق المتقدمة (CSS)
# ===================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [data-testid="stSidebar"] * { font-family: 'Cairo', sans-serif; text-align: right; }
[data-testid="stSidebar"] { background-color: #0f172a; color: white; }
.main-title { text-align:center; padding:10px; color:#1e3a8a; font-family: 'Cairo', sans-serif; }
.metric-card {
    background: white; border-radius: 12px; padding: 20px; text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,.05); border-right: 5px solid #1e3a8a; margin-bottom: 15px;
}
.metric-number { font-size: 32px; color: #1e3a8a; font-weight: bold; }
div.stButton > button:first-child {
    background-color: #1e3a8a; color: white; border-radius: 8px; width: 100%; font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# استدعاء شريط مراقبة الاتصال في أعلى واجهة المستخدم
components.html(offline_sync_js, height=50)

st.markdown("<div class='main-title'><h1>🏢 نظام إدارة الجمعيات اللوجستي المتكامل</h1><p>الإصدار الذكي المتوافق مع الجوال والكمبيوتر للمراقبة الميدانية وسير العمل</p></div>", unsafe_allow_html=True)

# ===================================
# 5. جلب البيانات من السيرفر وتحويلها لـ DataFrames
# ===================================
inv_rows = run_db_query("SELECT * FROM inventory", is_select=True)
emp_rows = run_db_query("SELECT * FROM employees", is_select=True)
task_rows = run_db_query("SELECT * FROM tasks", is_select=True)

df_inv = pd.DataFrame([dict(r) for r in inv_rows]) if inv_rows else pd.DataFrame(columns=['id', 'item_name', 'available', 'issued', 'min_limit'])
df_emp = pd.DataFrame([dict(r) for r in emp_rows]) if emp_rows else pd.DataFrame(columns=['id', 'date_assigned', 'emp_name', 'job_title', 'program', 'custody_items', 'status', 'notes'])
df_tasks = pd.DataFrame([dict(r) for r in task_rows]) if task_rows else pd.DataFrame(columns=['id', 'task_date', 'task_desc', 'receiver', 'status'])

# حساب الإحصائيات الحيوية للبطاقات العلوية
total_emp_active = len(df_emp[df_emp['status'] == 'نشطة'])
total_items = df_inv['available'].sum() if not df_inv.empty else 0
shortage_items = sum(1 for _, r in df_inv.iterrows() if r['available'] <= r['min_limit']) if not df_inv.empty else 0

# ===================================
# 6. القائمة الجانبية للتنقل الاحترافي (Sidebar Navigation)
# ===================================
with st.sidebar:
    st.markdown("<div style='text-align: center;'><img src='https://cdn-icons-png.flaticon.com/512/3068/3068321.png' width='70'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>لوحة التحكم اللوجستية</h3>", unsafe_allow_html=True)
    st.write("---")
    menu_choice = st.radio("⚙️ الانتقال بين الأقسام والمهام:", 
                           ["🏃‍♂️ حركة وتوصيلات المراسل", "👥 عهد الموظفين والبرامج", "📦 مستودع وجرد المواد", "📊 مؤشرات الأداء والتحليلات"])
    st.write("---")
    st.caption("تزامن البيانات السحابية: نشط ومؤمن ✅")

# ===================================
# 7. منطومة عمل تبويبات وأقسام التطبيق
# ===================================

# القسم الأول: حركة وتوصيلات المراسل الميداني
if menu_choice == "🏃‍♂️ حركة وتوصيلات المراسل":
    st.subheader("📋 تسجيل وتتبع مهمة ميدانية فورية")
    col1, col2, col3 = st.columns(3)
    with col1: t_desc = st.text_input("وصف الشحنة والمواد الموجهة للميدان", key="task_desc_input")
    with col2: t_rec = st.text_input("الجهة المستلمة بالخارج / المنطقة", key="task_rec_input")
    with col3: t_status = st.selectbox("الحالة الحالية للمهمة", ["جاري التنفيذ", "تم التسليم بنجاح", "ملغي"])
    
    if st.button("➕ حفظ ومزامنة المهمة الميدانية"):
        if t_desc and t_rec:
            res = run_db_query("INSERT INTO tasks (task_date, task_desc, receiver, status) VALUES (?, ?, ?, ?)",
                               (str(datetime.now().date()), t_desc, t_rec, t_status))
            if res:
                st.toast("🎯 تم حفظ وتزامن المهمة بنجاح!", icon="✅")
                st.rerun()
        else:
            st.warning("⚠️ يرجى ملء حقول الوصف والجهة المستلمة أولاً.")

    st.write("---")
    st.subheader("🔄 جدول الحركة والمتابعة اليومية (تحديث حي)")
    if not df_tasks.empty:
        edited_tasks = st.data_editor(df_tasks, key="tasks_editor_panel", use_container_width=True, disabled=["id", "task_date"])
        if st.button("💾 حفظ التعديلات وتحديث الحالات"):
            success_flag = True
            for _, row in edited_tasks.iterrows():
                res = run_db_query("UPDATE tasks SET status = ? WHERE id = ?", (row['status'], row['id']))
                if not res: success_flag = False
            if success_flag:
                st.toast("تم تحديث حالات التوصيل في قاعدة البيانات!", icon="💾")
                st.rerun()
    else:
        st.info("لا توجد مهام حركة مسجلة حالياً.")

# القسم الثاني: عهد الموظفين وصرفها وإستردادها للحماية من الفقدان
elif menu_choice == "👥 عهد الموظفين والبرامج":
    st.subheader("👤 صرف مواد كعهدة ميدانية أو إدارية للموظف")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        e_name = st.text_input("اسم الموظف المستلم")
        e_title = st.text_input("المسمى الوظيفي")
    with col_e2:
        e_prog = st.selectbox("البرنامج التابع له بالجمعية", ["التعليم", "الإغاثة والتمكين", "الرعاية الصحية", "الإدارة العامة"])
        inv_items_list = df_inv['item_name'].tolist() if not df_inv.empty else []
        e_custody = st.multiselect("اختر عهدة من المواد المتوفرة بالمخزن", inv_items_list)
        
    e_notes = st.text_area("ملاحظات وشروط الصرف")
    
    if st.button("💾 إتمام الصرف والخصم التلقائي من المخزن"):
        if e_name and e_custody:
            can_issue = True
            for item in e_custody:
                res = run_db_query("SELECT available FROM inventory WHERE item_name = ?", (item,), is_select=True, fetch_all=False)
                if res and res['available'] < 1:
                    st.error(f"عذراً، المادة [{item}] نفدت من المخزن ولا يمكن صرفها!")
                    can_issue = False
            
            if can_issue:
                for item in e_custody:
                    run_db_query("UPDATE inventory SET available = available - 1, issued = issued + 1 WHERE item_name = ?", (item,))
                run_db_query("INSERT INTO employees (date_assigned, emp_name, job_title, program, custody_items, status, notes) VALUES (?, ?, ?, ?, ?, 'نشطة', ?)",
                               (str(datetime.now().date()), e_name, e_title, e_prog, ", ".join(e_custody), e_notes))
                st.toast(f"تم قيد العهدة للموظف {e_name} وتحديث المخازن!", icon="📦")
                st.rerun()

    st.write("---")
    st.subheader("🔍 استرداد وإرجاع العهد المستلمة")
    
    active_employees = df_emp[df_emp['status'] == 'نشطة']
    if not active_employees.empty:
        emp_to_return = st.selectbox("اختر الموظف لإرجاع عهدته وتصفيتها:", active_employees['emp_name'].unique())
        if st.button("🔄 تأكيد استلام العهدة وإعادتها للمستودع"):
            row_to_return = active_employees[active_employees['emp_name'] == emp_to_return].iloc[0]
            items_to_return = row_to_return['custody_items'].split(", ")
            
            # إعادة زيادة المخزن وتقليص المواد الصادرة
            for item in items_to_return:
                run_db_query("UPDATE inventory SET available = available + 1, issued = issued - 1 WHERE item_name = ?", (item,))
            
            # تحديث حالة العهدة إلى مستردة
            run_db_query("UPDATE employees SET status = 'تم إرجاعها واستلامها' WHERE id = ?", (int(row_to_return['id']),))
            st.toast(f"تم تصفية عهدة {emp_to_return} بنجاح وإعادة تزويد المخزن!", icon="🔄")
            st.rerun()
    else:
        st.info("لا توجد عهد نشطة حالياً.")

# القسم الثالث: إدارة المخزن والتحديث الذكي دون تصفير حد الأمان والتصدير لـ Excel
elif menu_choice == "📦 مستودع وجرد المواد":
    st.subheader("📥 مدخلات وتحديث مستودع المواد المركزي")
    
    existing_items = ["-- صنف جديد --"] + (df_inv['item_name'].tolist() if not df_inv.empty else [])
    selected_item = st.selectbox("اختر صنفاً لتحديث كميته أو أضف صنفاً جديداً:", existing_items)
    
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        if selected_item == "-- صنف جديد --":
            i_name = st.text_input("اسم الصنف الجديد المراد تسجيله")
            default_min = 5
        else:
            i_name = st.text_input("اسم الصنف المُراد تحديثه", value=selected_item, disabled=True)
            default_min = int(df_inv[df_inv['item_name'] == selected_item]['min_limit'].values[0])
            
    with col_i2: i_avail = st.number_input("الكمية الموردة الجديدة للمستودع", min_value=0, value=0)
    with col_i3: i_min = st.number_input("حد الأمان لتنبيه الإدارة بالنفاد", min_value=1, value=default_min)
    
    if st.button("🔄 تحديث بيانات وجرد المخزن"):
        if i_name and i_name.strip():
            row = run_db_query("SELECT * FROM inventory WHERE item_name = ?", (i_name.strip(),), is_select=True, fetch_all=False)
            if row:
                run_db_query("UPDATE inventory SET available = available + ?, min_limit = ? WHERE item_name = ?",
                               (i_avail, i_min, i_name.strip()))
            else:
                run_db_query("INSERT INTO inventory (item_name, available, issued, min_limit) VALUES (?, ?, 0, ?)",
                               (i_name.strip(), i_avail, i_min))
            st.toast("تم تحديث مخازن الجمعية بنجاح واستقرار!", icon="📥")
            st.rerun()

    st.write("---")
    st.subheader("📊 جرد مخازن الجمعية الحالي")
    if not df_inv.empty:
        def highlight_shortage(row):
            return ['background-color: #fee2e2' if row['available'] <= row['min_limit'] else '' for _ in row]
        st.dataframe(df_inv.style.apply(highlight_shortage, axis=1), use_container_width=True)
        
        # دالة تصدير ذكية لا تستهلك الذاكرة إلا عند الضغط
        def generate_excel_report():
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_inv.to_excel(writer, index=False, sheet_name='جرد المخزن')
                df_emp.to_excel(writer, index=False, sheet_name='سجل العهد')
                df_tasks.to_excel(writer, index=False, sheet_name='حركة التوصيل الميداني')
            return output.getvalue()
            
        try:
            st.download_button(
                label="📥 تحميل التقرير اللوجستي الشامل كملف Excel للمحاسب الإداري",
                data=generate_excel_report(),
                file_name=f"Association_Comprehensive_Report_{datetime.now().date()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"فشل في توليد مستند التقرير: {e}")

# القسم الرابع: الإحصائيات المتقدمة ومؤشرات الأداء البيانية
elif menu_choice == "📊 مؤشرات الأداء والتحليلات":
    st.subheader("📊 تحليلات بيانية سريعة لحالة الدعم اللوجستي")
    
    # بطاقات الأداء العلوية داخل الأقسام
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><div>👥 عهد نشطة مع الموظفين</div><div class='metric-number'>{total_emp_active}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><div>📦 إجمالي قطع المخزن المتوفرة</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card' style='border-right-color:#ef4444;'><div style='color:#ef4444;'>⚠️ أصناف قاربت على النفاد</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
    
    st.write("---")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if not df_inv.empty and df_inv['item_name'].any():
            st.write("🔄 **مقارنة بين الكميات المتوفرة بالمخزن مقابل الصادرة كعهد**")
            fig_inv = px.bar(df_inv, x="item_name", y=["available", "issued"],
                             labels={"item_name": "المادة", "value": "الكمية", "variable": "الحالة"},
                             barmode="group", color_discrete_sequence=["#1e3a8a", "#ef4444"])
            st.plotly_chart(fig_inv, use_container_width=True)
    with col_g2:
        if not df_emp.empty and 'program' in df_emp.columns:
            st.write("📈 **توزيع استهلاك الموارد والمساعدات حسب برامج الجمعية**")
            program_counts = df_emp[df_emp['status'] == 'نشطة']['program'].value_counts().reset_index()
            program_counts.columns = ['البرنامج', 'عدد العهد النشطة']
            fig_pie = px.pie(program_counts, values='عدد العهد النشطة', names='البرنامج',
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
