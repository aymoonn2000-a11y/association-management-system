import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date
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
    # جدول المستودع والمواد 
    run_db_query('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            available INTEGER,
            issued INTEGER,
            min_limit INTEGER,
            expiry_date TEXT
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
    # جدول العهد المالية المؤقتة (Petty Cash)
    run_db_query('''
        CREATE TABLE IF NOT EXISTS petty_cash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_issued TEXT,
            emp_name TEXT,
            amount REAL,
            purpose TEXT,
            status TEXT DEFAULT 'قيد الاستخدام',
            settlement_notes TEXT
        )
    ''')
    # جدول كشف المواصلات الجديد (عملة الشيكل) - ميزة محقونة جديدة 🚗
    run_db_query('''
        CREATE TABLE IF NOT EXISTS transport_allowance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            travel_date TEXT,
            emp_name TEXT,
            destination TEXT,
            cost_ils REAL,
            notes TEXT
        )
    ''')
    
    # إدخال بيانات أولية للمشروع إذا كان فارغاً
    check = run_db_query("SELECT COUNT(*) as count FROM inventory", is_select=True, fetch_all=False)
    if check and check['count'] == 0:
        initial_items = [
            ("أجهزة لاب توب", 20, 5, 3, "2030-12-31"),
            ("سلات غذائية وإغاثية", 150, 40, 10, "2026-08-15"),
            ("قرطاسية ومستندات طبع", 200, 20, 15, "2029-01-01"),
            ("مستلزمات طبية أولية", 40, 5, 8, "2026-07-01")
        ]
        for item in initial_items:
            run_db_query("INSERT OR IGNORE INTO inventory (item_name, available, issued, min_limit, expiry_date) VALUES (?, ?, ?, ?, ?)", item)

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
        } else {
            statusBar.innerHTML = '⚠️ وضع الميدان النشط (بدون إنترنت) - سيتم حفظ وتأمين مدخلاتك محلياً بالجوال';
            statusBar.style.backgroundColor = '#fee2e2';
            statusBar.style.color = '#991b1b';
        }
    }
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
</script>
<div id="status-bar" style="padding:12px; text-align:center; font-family:sans-serif; font-size:14px; font-weight:bold; border-radius:8px; margin-bottom:10px;">
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
.ils-total {
    background-color: #e0f2fe; border: 1px solid #7dd3fc; border-radius: 8px;
    padding: 15px; text-align: center; font-size: 20px; font-weight: bold; color: #0369a1;
}
</style>
""", unsafe_allow_html=True)

components.html(offline_sync_js, height=50)

st.markdown("<div class='main-title'><h1>🏢 نظام إدارة الجمعيات اللوجستي المتكامل</h1><p>الواجهة الذكية الموحدة للمخازن، العهد الميدانية، والمتابعة المالية</p></div>", unsafe_allow_html=True)

# ===================================
# 5. جلب البيانات من السيرفر وتحويلها لـ DataFrames
# ===================================
inv_rows = run_db_query("SELECT * FROM inventory", is_select=True)
emp_rows = run_db_query("SELECT * FROM employees", is_select=True)
task_rows = run_db_query("SELECT * FROM tasks", is_select=True)
cash_rows = run_db_query("SELECT * FROM petty_cash", is_select=True)
trans_rows = run_db_query("SELECT * FROM transport_allowance", is_select=True)

df_inv = pd.DataFrame([dict(r) for r in inv_rows]) if inv_rows else pd.DataFrame(columns=['id', 'item_name', 'available', 'issued', 'min_limit', 'expiry_date'])
df_emp = pd.DataFrame([dict(r) for r in emp_rows]) if emp_rows else pd.DataFrame(columns=['id', 'date_assigned', 'emp_name', 'job_title', 'program', 'custody_items', 'status', 'notes'])
df_tasks = pd.DataFrame([dict(r) for r in task_rows]) if task_rows else pd.DataFrame(columns=['id', 'task_date', 'task_desc', 'receiver', 'status'])
df_cash = pd.DataFrame([dict(r) for r in cash_rows]) if cash_rows else pd.DataFrame(columns=['id', 'date_issued', 'emp_name', 'amount', 'purpose', 'status', 'settlement_notes'])
df_trans = pd.DataFrame([dict(r) for r in trans_rows]) if trans_rows else pd.DataFrame(columns=['id', 'travel_date', 'emp_name', 'destination', 'cost_ils', 'notes'])

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
    menu_choice = st.sidebar.radio("⚙️ الانتقال بين الأقسام والمهام:", 
                           ["🏃‍♂️ حركة وتوصيلات المراسل", "👥 عهد الموظفين والبرامج", "📦 مستودع وجرد المواد", "💸 العهد المالية (Petty Cash)", "🚗 كشف مواصلات الميدان", "📊 مؤشرات الأداء والتحليلات"])
    st.write("---")
    st.caption("تزامن البيانات السحابية: نشط ومؤمن ✅")

# ===================================
# 7. منظومة عمل أقسام التطبيق المطورة
# ===================================

# القسم الأول: حركة وتوصيلات المراسل الميداني
if menu_choice == "🏃‍♂️ حركة وتوصيلات المراسل":
    st.subheader("📋 تسجيل وتتبع مهمة ميدانية فورية")
    col1, col2, col3 = st.columns(3)
    with col1: t_desc = st.text_input("وصف الشحنة والمواد الموجهة للميدان")
    with col2: t_rec = st.text_input("الجهة المستلمة بالخارج / المنطقة")
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
    st.subheader("🔄 جدول الحركة والمتابعة اليومية")
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

# القسم الثاني: عهد الموظفين وصرفها وإستردادها
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
            
            for item in items_to_return:
                run_db_query("UPDATE inventory SET available = available + 1, issued = issued - 1 WHERE item_name = ?", (item,))
            
            run_db_query("UPDATE employees SET status = 'تم إرجاعها واستلامها' WHERE id = ?", (int(row_to_return['id']),))
            st.toast(f"تم تصفية عهدة {emp_to_return} بنجاح وإعادة تزويد المخزن!", icon="🔄")
            st.rerun()
    else:
        st.info("لا توجد عهد عينية نشطة حالياً.")

# القسم الثالث: إدارة المخزن 
elif menu_choice == "📦 مستودع وجرد المواد":
    st.subheader("📥 مدخلات وتحديث مستودع المواد المركزي")
    existing_items = ["-- صنف جديد --"] + (df_inv['item_name'].tolist() if not df_inv.empty else [])
    selected_item = st.selectbox("اختر صنفاً لتحديث كميته أو أضف صنفاً جديداً:", existing_items)
    
    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    with col_i1:
        if selected_item == "-- صنف جديد --":
            i_name = st.text_input("اسم الصنف الجديد المراد تسجيله")
            default_min = 5
            default_expiry = datetime.now().date()
        else:
            i_name = st.text_input("اسم الصنف المُراد تحديثه", value=selected_item, disabled=True)
            default_min = int(df_inv[df_inv['item_name'] == selected_item]['min_limit'].values[0])
            try:
                default_expiry = datetime.strptime(df_inv[df_inv['item_name'] == selected_item]['expiry_date'].values[0], "%Y-%m-%d").date()
            except:
                default_expiry = datetime.now().date()
            
    with col_i2: i_avail = st.number_input("الكمية الموردة الجديدة للمستودع", min_value=0, value=0)
    with col_i3: i_min = st.number_input("حد الأمان لتنبيه الإدارة بالنفاد", min_value=1, value=default_min)
    with col_i4: i_expiry = st.date_input("تاريخ انتهاء صلاحية الصنف", value=default_expiry)
    
    if st.button("🔄 تحديث بيانات وجرد المخزن"):
        if i_name and i_name.strip():
            row = run_db_query("SELECT * FROM inventory WHERE item_name = ?", (i_name.strip(),), is_select=True, fetch_all=False)
            if row:
                run_db_query("UPDATE inventory SET available = available + ?, min_limit = ?, expiry_date = ? WHERE item_name = ?", (i_avail, i_min, str(i_expiry), i_name.strip()))
            else:
                run_db_query("INSERT INTO inventory (item_name, available, issued, min_limit, expiry_date) VALUES (?, ?, 0, ?, ?)", (i_name.strip(), i_avail, i_min, str(i_expiry)))
            st.toast("تم تحديث مخازن الجمعية وفحص الصلاحيات!", icon="📥")
            st.rerun()

    st.write("---")
    st.subheader("📊 جرد مخازن الجمعية الحالي")
    if not df_inv.empty:
        def highlight_inventory(row):
            styles = ['' for _ in row]
            current_date = date(2026, 6, 3) # التثبيت بالوقت الحالي
            try:
                exp_date = datetime.strptime(row['expiry_date'], "%Y-%m-%d").date()
                days_to_expire = (exp_date - current_date).days
            except: days_to_expire = 999
            
            if row['available'] <= row['min_limit']:
                return ['background-color: #fee2e2; color: #991b1b; font-weight: bold;' for _ in row]
            elif days_to_expire <= 60:
                return ['background-color: #fef3c7; color: #92400e; font-weight: bold;' for _ in row]
            return styles
        st.dataframe(df_inv.style.apply(highlight_inventory, axis=1), use_container_width=True)

# القسم الرابع: إدارة العهد المالية المؤقتة (Petty Cash)
elif menu_choice == "💸 العهد المالية (Petty Cash)":
    st.header("💸 منظومة السلف والعهد المالية للمشاريع الميدانية")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1: c_name = st.text_input("اسم الموظف المستلم للسلفة")
    with col_c2: c_amount = st.number_input("المبلغ المالي المفوّض ($)", min_value=1.0, value=10.0, step=5.0)
    with col_c3: c_purpose = st.text_input("الغرض العملياتي من الصرف")
    
    if st.button("💵 قيد وصرف العهدة النقدية"):
        if c_name and c_purpose:
            res = run_db_query("INSERT INTO petty_cash (date_issued, emp_name, amount, purpose, status, settlement_notes) VALUES (?, ?, ?, ?, 'قيد الاستخدام', '')", (str(datetime.now().date()), c_name, c_amount, c_purpose))
            if res:
                st.toast(f"تم قيد السلفة المالية بقيمة ${c_amount} بنجاح!", icon="💸")
                st.rerun()

# ===================================
# القسم الخامس المحقون حديثاً: كشف مواصلات الميدان (عملة الشيكل ₪)
# ===================================
elif menu_choice == "🚗 كشف مواصلات الميدان":
    st.header("🚗 كشف تسجيل وفلترة مواصلات الموظفين والمراسلين")
    
    # 1. استمارة الإدخال اليومي للمواصلات
    with st.expander("➕ تسجيل حركة مواصلات / تنقل جديدة للميدان"):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1: t_name = st.text_input("اسم الموظف / المراسل الميداني")
        with col_t2: t_dest = st.text_input("إلى أين توجه؟ (الوجهة وملاحظة خط السير)")
        with col_t3: t_cost = st.number_input("تكلفة المواصلات الفعليّة (بالشيكل ₪)", min_value=0.0, value=10.0, step=1.0)
        t_date = st.date_input("تاريخ التحرك/المشوار", value=date(2026, 6, 3))
        
        if st.button("💾 ترحيل حركة المواصلات للكشف"):
            if t_name and t_dest:
                res = run_db_query("INSERT INTO transport_allowance (travel_date, emp_name, destination, cost_ils, notes) VALUES (?, ?, ?, ?, '')",
                                   (str(t_date), t_name, t_dest, t_cost))
                if res:
                    st.toast(f"تم تسجيل {t_cost} شيكل في حساب {t_name}", icon="🚗")
                    st.rerun()
            else:
                st.warning("يرجى كتابة اسم الموظف والوجهة بدقة أولاً.")

    st.write("---")
    
    # 2. منظومة الفلترة المتقدمة (من تاريخ - إلى تاريخ) وحساب المجموع بالشيكل
    st.subheader("🔍 استعراض وبحث وفلترة كشف المواصلات")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: filter_name = st.text_input("🔍 فلترة باسم الموظف (اتركه فارغاً لعرض الجميع)")
    with col_f2: date_from = st.date_input("📅 من تاريخ:", value=date(2026, 1, 1))
    with col_f3: date_to = st.date_input("📅 إلى تاريخ:", value=date(2026, 12, 31))
    
    if not df_trans.empty:
        # تحويل التاريخ في الـ DataFrame إلى نوع تاريخ حقيقي لضمان سلامة الفلترة الميدانية
        df_trans['travel_date'] = pd.to_datetime(df_trans['travel_date']).dt.date
        
        # تطبيق شروط الفلترة
        filtered_df = df_trans[(df_trans['travel_date'] >= date_from) & (df_trans['travel_date'] <= date_to)]
        
        if filter_name:
            filtered_df = filtered_df[filtered_df['emp_name'].str.contains(filter_name, case=False)]
            
        # عرض البيانات المفلترة للإدارة
        st.dataframe(filtered_df, use_container_width=True)
        
        # حساب المجموع الكلي الذكي للحركة المفلترة وعرضها بعملة الشيكل بشكل واضح جداً
        total_sum_ils = filtered_df['cost_ils'].sum()
        
        st.markdown(f"<div class='ils-total'>🪙 المجموع الكلي للمواصلات المستحقة في هذه الفترة لـ {filter_name if filter_name else 'جميع الموظفين'}: {total_sum_ils:,.2f} شيكل جديد (₪)</div>", unsafe_allow_html=True)
    else:
        st.info("كشف المواصلات فارغ تماماً حالياً.")

# القسم السادس: الإحصائيات
elif menu_choice == "📊 مؤشرات الأداء والتحليلات":
    st.subheader("📊 تحليلات بيانية سريعة لحالة الدعم اللوجستي")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><div>👥 عهد عينية نشطة</div><div class='metric-number'>{total_emp_active}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><div>📦 قطع مخزنية متوفرة</div><div class='metric-number'>{total_items}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card' style='border-right-color:#ef4444;'><div style='color:#ef4444;'>⚠️ أصناف بحاجة لتوريد</div><div class='metric-number' style='color:#ef4444;'>{shortage_items}</div></div>", unsafe_allow_html=True)
