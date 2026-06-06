import streamlit as st
import pandas as pd
import json
import os
import hashlib
import io
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# 1. إعدادات الصفحة والديزاين المتجاوب مع اللاب توب والجوال
st.set_page_config(
    page_title="نظام إدارة الجمعية المتكامل - نسخة متطورة",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة تشفير كلمة المرور لحماية وأمن البيانات (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# قاعدة بيانات المستخدمين والصلاحيات المتعددة
USERS = {
    "aymanyaghi": {"password": hash_password("12345"), "role": "مدير عام", "icon": "👑"},
    "accountant": {"password": hash_password("fin123"), "role": "محاسب مالي", "icon": "💰"},
    "storekeeper": {"password": hash_password("store123"), "role": "أمين المخزن", "icon": "📦"}
}

# ستايل واجهة المستخدم
st.markdown("""
<style>
.main { text-align: right; direction: rtl; }
[data-testid="stSidebar"] { direction: rtl; }
div.stButton > button:first-child {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-size: 16px;
    width: 100%;
    font-weight: bold;
}
h1, h2, h3, p, span, div {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    text-align: right;
}
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 20px;
    background: #ffffff;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.logo-icon {
    width: 45px;
    height: 45px;
    background: linear-gradient(135deg, #1f77b4, #00d2ff);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: bold;
}
.logo-text {
    font-size: 16px;
    font-weight: 800;
    color: #1f77b4;
}
.welcome-card {
    background: linear-gradient(135deg, #1f77b4, #00d2ff);
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
}
.log-box {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 8px;
    border-right: 5px solid #ff4b4b;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# 2. إدارة البيانات والتخزين المحلي المباشر (JSON)
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# دالة استخراج ملف Excel الاحترافي مع دعم العملات المختلفة
def export_to_styled_excel(dataframe, title_report="تقرير", is_transport=False):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "البيانات المسجلة"
    ws.views.sheetView[0].rightToLeft = True 
    
    header_fill = PatternFill(start_color="1F77B4", end_color="1F77B4", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Segoe UI", size=10)
    accent_fill = PatternFill(start_color="F0F8FF", end_color="F0F8FF", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color='D3D3D3'), right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'), bottom=Side(style='thin', color='D3D3D3')
    )
    
    current_row = 1
    if is_transport:
        ws.cell(row=1, column=2, value="جمعية الحياة والأمل").font = Font(name="Segoe UI", size=12, bold=True)
        ws.cell(row=1, column=6, value="Life and Hope Association").font = Font(name="Segoe UI", size=12, bold=True)
        ws.cell(row=2, column=2, value="محافظة شمال غزة").font = Font(name="Segoe UI", size=10, italic=True)
        ws.merge_cells("A4:H4")
        title_cell = ws.cell(row=4, column=1, value=f"كشف مواصلات فردي - {title_report}")
        title_cell.font = Font(name="Segoe UI", size=14, bold=True, color="1F77B4")
        title_cell.alignment = Alignment(horizontal="center")
        current_row = 6
    else:
        ws.cell(row=1, column=1, value=title_report).font = Font(name="Segoe UI", size=14, bold=True)
        current_row = 3
        
    columns = list(dataframe.columns)
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=current_row, column=col_num, value=column_title)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    
    start_data_row = current_row + 1
    current_row += 1
    
    for index, row in dataframe.iterrows():
        for col_num, cell_value in enumerate(columns, 1):
            cell = ws.cell(row=current_row, column=col_num, value=row[cell_value])
            cell.font = data_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
            if index % 2 == 0:
                cell.fill = accent_fill
        current_row += 1
        
    end_data_row = current_row - 1
    ws.auto_filter.ref = f"A{start_data_row-1}:{get_column_letter(len(columns))}{end_data_row}"
    
    if is_transport and "المبلغ" in dataframe.columns:
        amount_col_idx = dataframe.columns.get_loc("المبلغ") + 1
        current_row += 1
        ws.cell(row=current_row, column=amount_col_idx-1, value="الإجمالي الفعلي:").font = Font(name="Segoe UI", size=10, bold=True)
        sum_cell = ws.cell(row=current_row, column=amount_col_idx, value=f"=SUM({get_column_letter(amount_col_idx)}{start_data_row}:{get_column_letter(amount_col_idx)}{end_data_row})")
        sum_cell.font = Font(name="Segoe UI", size=11, bold=True)
        
        current_row += 3
        ws.cell(row=current_row, column=2, value="رئيس مجلس الإدارة: زاهر محمود صبيح").font = Font(name="Segoe UI", size=10, bold=True)
        ws.cell(row=current_row, column=5, value="مدير المشروع: ........................").font = Font(name="Segoe UI", size=10, bold=True)

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max(max_len + 3, 12)
        
    wb.save(output)
    return output.getvalue()

# 3. تهيئة قواعد البيانات المحلية
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = ""
if 'user_fullname' not in st.session_state: st.session_state.user_fullname = ""

if 'expenses' not in st.session_state: st.session_state.expenses = load_data('expenses.json')
if 'employees' not in st.session_state: st.session_state.employees = load_data('employees.json')
if 'inventory' not in st.session_state: st.session_state.inventory = load_data('inventory.json')
if 'transport_records' not in st.session_state: st.session_state.transport_records = load_data('transport_records.json')
if 'login_logs' not in st.session_state: st.session_state.login_logs = load_data('login_logs.json')

# 4. واجهة تسجيل الدخول الآمنة بالصلاحيات مع رصد حركات الدخول
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔒 نظام بوابة الحياة والأمل الإلكترونية</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔑 كلمة المرور", type="password")
        if st.button("🚪 دخول النظام"):
            if username in USERS and hash_password(password) == USERS[username]["password"]:
                st.session_state.logged_in = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.user_fullname = username
                
                # 📝 تعديل ذكي: رصد حركة الدخول بالوقت والتاريخ واليوم في حال كان المستخدم accountant أو storekeeper
                if username in ["accountant", "storekeeper"]:
                    new_log = {
                        "المستخدم": username,
                        "الصلاحية": USERS[username]["role"],
                        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
                        "الوقت": datetime.now().strftime("%I:%M:%S %p")
                    }
                    st.session_state.login_logs.append(new_log)
                    save_data('login_logs.json', st.session_state.login_logs)
                
                st.success(f"مرحباً بك بصلاحية: {st.session_state.user_role}")
                st.rerun()
            else:
                st.error("❌ خطأ في بيانات الدخول الممنوحة!")
else:
    # القائمة الجانبية بناءً على صلاحيات الحساب
    st.sidebar.markdown(f"""
    <div class="logo-container">
        <div class="logo-icon">🏢</div>
        <div class="logo-text">جمعية الحياة والأمل<br><small>👤 {st.session_state.user_fullname} ({st.session_state.user_role})</small></div>
    </div>
    """, unsafe_allow_html=True)
    
    available_pages = ["🏠 الشاشة الرئيسية"]
    
    if st.session_state.user_role in ["مدير عام", "محاسب مالي"]:
        available_pages.extend(["🚗 كشف المواصلات (ملفك المرفق)", "💰 المصروفات العامة"])
        
    if st.session_state.user_role in ["مدير عام", "أمين المخزن"]:
        available_pages.extend(["👥 شؤون الموظفين والعهد", "📦 جرد ومحتويات المخزن"])
        
    available_pages.append("🚪 خروج")
    
    menu = st.sidebar.radio("📂 تصفح أقسام النظام الحالية:", available_pages)
    
    if menu == "🚪 خروج":
        st.session_state.logged_in = False
        st.session_state.user_role = ""
        st.session_state.user_fullname = ""
        st.rerun()
        
    elif menu == "🏠 الشاشة الرئيسية":
        st.markdown("<div class='welcome-card'><h3>لوحة التحكم والتحليلات البيانية المتكاملة</h3></div>", unsafe_allow_html=True)
        st.write(f"📅 **التاريخ:** {datetime.now().strftime('%Y-%m-%d')} | ⏰ **الوقت:** {datetime.now().strftime('%I:%M %p')}")
        
        # 🚨 نظام مراقبة المستخدمين الخاص بالمدير العام فقط (aymanyaghi)
        if st.session_state.user_fullname == "aymanyaghi":
            st.markdown("### 🔔 نظام تنبيه ومراقبة دخول المستخدمين للمنظومة")
            
            # حساب إجمالي عدد المرات
            df_logs = pd.DataFrame(st.session_state.login_logs) if st.session_state.login_logs else pd.DataFrame()
            
            count_acc = len(df_logs[df_logs["المستخدم"] == "accountant"]) if not df_logs.empty else 0
            count_store = len(df_logs[df_logs["المستخدم"] == "storekeeper"]) if not df_logs.empty else 0
            
            # بطاقات إحصائية سريعة للمدير
            col_log1, col_log2 = st.columns(2)
            col_log1.metric("📊 مرات دخول المحاسب (accountant)", f"{count_acc} مرات")
            col_log2.metric("📊 مرات دخول أمين المخزن (storekeeper)", f"{count_store} مرات")
            
            # زر إظهار التقرير التفصيلي للوقت والتاريخ
            if st.checkbox("🔍 عرض سجل التواريخ والأوقات التفصيلي لحركات الدخول"):
                if not df_logs.empty:
                    st.dataframe(df_logs, use_container_width=True)
                else:
                    st.info("لم يقم أي مستخدم بالدخول بعد منذ تفعيل نظام الرصد.")
            st.markdown("---")

        # نظام التنبيه بنقص المخزون للكل
        low_stock_items = [item for item in st.session_state.inventory if item.get("الكمية", 0) <= item.get("الحد الأدنى", 0)]
        if low_stock_items:
            st.error("🚨 **تنبيه نقص المخزون السريع:** المواد التالية وصلت إلى حد الأمان أو أقل، يرجى تزويد المخزن:")
            for item in low_stock_items:
                st.write(f"⚠️ **{item['اسم المادة']}** -> المتوفر حالياً: `{item['الكمية']}` حبة فقط (حد الأمان المعتمد: {item['الحد الأدنى']})")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🚗 حركات المواصلات المؤرشفة", len(st.session_state.transport_records))
        c2.metric("👥 العهد الموثقة للموظفين", len(st.session_state.employees))
        c3.metric("💰 قيود الصرف المالي العام", len(st.session_state.expenses))
        
        if st.session_state.transport_records:
            st.markdown("### 📊 إجمالي حركات المواصلات حسب العملة المحددة")
            df = pd.DataFrame(st.session_state.transport_records)
            if "العملة" in df.columns and "المبلغ" in df.columns:
                currency_summary = df.groupby("العملة")["المبلغ"].sum().reset_index()
                st.dataframe(currency_summary, use_container_width=True)

    elif menu == "🚗 كشف المواصلات (ملفك المرفق)":
        st.title("🚗 نموذج كشف مواصلات الموظفين الفردي التابع للجمعية")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة حركة جديدة")
            emp = st.text_input("👤 اسم الموظف")
            job = st.text_input("💼 المسمى الوظيفي")
            day = st.selectbox("📆 اليوم", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
            dt = st.date_input("📅 التاريخ", datetime.now(), key="trans_date")
            fr = st.text_input("📍 من")
            to = st.text_input("🏁 إلى")
            amt = st.number_input("💰 المبلغ المحدد", min_value=0.0, step=0.5)
            curr = st.selectbox("💱 تحديد العملة", ["شيكل", "دولار أمريكي", "دينار أردني"], key="trans_curr")
            rsn = st.text_area("🔍 سبب الحركة والمشروع الممول")
            
            if st.button("💾 ترحيل القيد"):
                if emp and amt > 0:
                    st.session_state.transport_records.append({
                        "اسم الموظف": emp, "المسمى الوظيفي": job, "اليوم": day, 
                        "التاريخ": dt.strftime("%Y-%m-%d"), "من": fr, "إلى": to, 
                        "المبلغ": amt, "العملة": curr, "سبب الحركة": rsn
                    })
                    save_data('transport_records.json', st.session_state.transport_records)
                    st.success("✅ تم حفظ قيد المواصلات بنجاح")
                    st.rerun()
        with col2:
            st.subheader("🔍 الفلترة الفردية والتنزيل الملون المعتمد")
            if st.session_state.transport_records:
                df_t = pd.DataFrame(st.session_state.transport_records)
                sel_emp = st.selectbox("🎯 اختر اسم الموظف لعرض الكشف الفردي ملوّن:", df_t["اسم الموظف"].unique())
                df_res = df_t[df_t["اسم الموظف"] == sel_emp].copy()
                st.dataframe(df_res, use_container_width=True)
                
                excel_file = export_to_styled_excel(df_res, title_report=sel_emp, is_transport=True)
                st.download_button(
                    label=f"📥 تنزيل كشف الموظف {sel_emp} بصيغة Excel الملونة",
                    data=excel_file,
                    file_name=f"كشف_مواصلات_{sel_emp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("لا توجد بيانات مواصلات مسجلة حالياً.")

    elif menu == "💰 المصروفات العامة":
        st.title("💰 إدارة البنود المالية العمومية والمشاريع")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ تقييد مصروف عام")
            exp_date = st.date_input("📅 التاريخ", datetime.now(), key="exp_date")
            exp_item = st.text_input("🏷️ البند / السلعة المصروفة")
            exp_details = st.text_input("📑 تفاصيل وجهة الصرف")
            exp_price = st.number_input("💸 القيمة والشدة", min_value=0.0, step=1.0)
            exp_curr = st.selectbox("💱 العملة المالية", ["شيكل", "دولار أمريكي", "دينار أردني"], key="exp_curr")
            if st.button("💾 ترحيل للمصاريف العمومية"):
                if exp_item and exp_price > 0:
                    st.session_state.expenses.append({
                        "التاريخ": exp_date.strftime("%Y-%m-%d"), "نوع السلعة": exp_item, 
                        "التفاصيل": exp_details, "السعر": exp_price, "العملة": exp_curr
                    })
                    save_data('expenses.json', st.session_state.expenses)
                    st.success("✅ تم حفظ البند المالي داخل النظام")
                    st.rerun()
        with col2:
            st.subheader("📋 كشوفات المصروفات الحالية للجمعية")
            if st.session_state.expenses:
                df_e = pd.DataFrame(st.session_state.expenses)
                st.dataframe(df_e, use_container_width=True)
                excel_exp = export_to_styled_excel(df_e, title_report="المصروفات العامة", is_transport=False)
                st.download_button(
                    label="📥 تحميل كشف المصروفات الإجمالي (Excel)",
                    data=excel_exp,
                    file_name="المصروفات_العامة.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("سجل المصروفات العمومية فارغ.")
        
    elif menu == "👥 شؤون الموظفين والعهد":
        st.title("👥 إدارة سجلات العهد والأصول المتطورة")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ توثيق عهدة موظف تفصيلية")
            e_name = st.text_input("🤵 اسم الموظف الثلاثي")
            e_id = st.text_input("💳 رقم الهوية الشخصية")
            e_phone = st.text_input("📞 رقم الجوال للاتصال")
            e_contract = st.selectbox("📜 نوع عقد العمل للتوثيق", ["عقد محدد المدة", "يومي / بطالة", "تطوع مسجل"])
            e_asset = st.text_input("📦 طبيعة العهدة (جهاز، لابتوب، أثاث...)")
            e_curr = st.selectbox("💱 قيمة العهدة المقدرة بعملة", ["شيكل", "دولار أمريكي", "دينار أردني"])
            e_val = st.number_input("💰 القيمة المقدرة للعهدة", min_value=0.0)
            e_date_start = st.date_input("📅 تاريخ الاستلام الفعلي للعهدة", datetime.now())
            e_date_end = st.date_input("📅 تاريخ الإرجاع المتوقع أو إنهاء الخدمة", datetime.now())
            e_status = st.selectbox("🔄 الحالة الحالية للعهدة في السجل", ["مستلمة وفي عهدته", "تم استردادها بأمان"])
            
            if st.button("💾 ترحيل بيانات العهدة"):
                if e_name and e_id:
                    st.session_state.employees.append({
                        "اسم الموظف": e_name, "رقم الهوية": e_id, "رقم الجوال": e_phone, 
                        "نوع العقد": e_contract, "العهدة المستلمة": e_asset, "القيمة": e_val, 
                        "العملة": e_curr, "تاريخ الاستلام": e_date_start.strftime("%Y-%m-%d"), 
                        "تاريخ الإرجاع المتوقع": e_date_end.strftime("%Y-%m-%d"), "الحالة": e_status
                    })
                    save_data('employees.json', st.session_state.employees)
                    st.success("✅ تم حفظ وتأريخ بيانات العهدة في سجل الموظفين")
                    st.rerun()
        with col2:
            st.subheader("📋 كشف العهد والأصول والأمانات الحالية")
            if st.session_state.employees:
                df_emp = pd.DataFrame(st.session_state.employees)
                st.dataframe(df_emp, use_container_width=True)
                excel_emp = export_to_styled_excel(df_emp, title_report="سجلات العهد والأصول", is_transport=False)
                st.download_button(
                    label="📥 تحميل كشف سجلات العهد الكامل (Excel)",
                    data=excel_emp,
                    file_name="كشف_العهد_الرسمي.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("لا يوجد موظفين مقيدين في قائمة الأصول والعهد حالياً.")
        
    elif menu == "📦 جرد ومحتويات المخزن":
        st.title("📦 جرد مستودعات ومخازن الجمعية الذكي")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ توريد مادة جديدة للمخزن")
            i_name = st.text_input("📦 اسم المادة أو الصنف للتخزين")
            i_qty = st.number_input("🔢 الكمية الموردة الحالية", min_value=0, step=1)
            i_min = st.number_input("🚨 حد الأمان الأدنى (نظام التنبيه)", min_value=1, step=1)
            if st.button("💾 ترحيل صنف للجرد الفعلي"):
                if i_name:
                    st.session_state.inventory.append({
                        "اسم المادة": i_name, "الكمية": i_qty, "الحد الأدنى": i_min
                    })
                    save_data('inventory.json', st.session_state.inventory)
                    st.success("✅ تم تسجيل وتوريد الصنف بنجاح")
                    st.rerun()
        with col2:
            st.subheader("📋 جدول جرد الأصناف مع نظام مراقبة مستويات الأمان")
            if st.session_state.inventory:
                df_i = pd.DataFrame(st.session_state.inventory)
                st.dataframe(df_i, use_container_width=True)
                excel_inv = export_to_styled_excel(df_i, title_report="جرد وموجودات المخزن", is_transport=False)
                st.download_button(
                    label="📥 تحميل مستند الجرد النهائي (Excel)",
                    data=excel_inv,
                    file_name="جرد_المخزن_الفعلي.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("مستودع مخزن الجمعية فارغ بانتظار التوريد.")
