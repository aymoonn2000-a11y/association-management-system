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
    page_title="نظام إدارة الجمعية المتكامل",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة تشفير كلمة المرور لحماية وأمن البيانات (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

CORRECT_USERNAME = "aymanyaghi"
CORRECT_PASSWORD_HASH = "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5" 

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
    font-size: 18px;
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

# دالة استخراج ملف Excel بتنسيق ملون وتصفية تلقائية ودوال رياضية وتواقيع
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
    
    if is_transport and "المبلغ بالشيكل" in dataframe.columns:
        amount_col_idx = dataframe.columns.get_loc("المبلغ بالشيكل") + 1
        current_row += 1
        ws.cell(row=current_row, column=amount_col_idx-1, value="المبلغ الإجمالي بالشيكل:").font = Font(name="Segoe UI", size=10, bold=True)
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
if 'expenses' not in st.session_state: st.session_state.expenses = load_data('expenses.json')
if 'employees' not in st.session_state: st.session_state.employees = load_data('employees.json')
if 'inventory' not in st.session_state: st.session_state.inventory = load_data('inventory.json')
if 'transport_records' not in st.session_state: st.session_state.transport_records = load_data('transport_records.json')

# 4. واجهة تسجيل الدخول الآمنة
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔒 نظام إدارة جمعية الحياة والأمل</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔑 كلمة المرور", type="password")
        if st.button("🚪 دخول النظام"):
            if username == CORRECT_USERNAME and hash_password(password) == CORRECT_PASSWORD_HASH:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ خطأ في صلاحيات الدخول الممنوحة!")
else:
    st.sidebar.markdown("""
    <div class="logo-container">
        <div class="logo-icon">🏢</div>
        <div class="logo-text">جمعية الحياة والأمل</div>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.sidebar.radio(
        "📂 تصفح أقسام النظام:",
        ["🏠 الشاشة الرئيسية", "🚗 كشف المواصلات (ملفك المرفق)", "💰 المصروفات العامة", "👥 شؤون الموظفين والعهد", "📦 جرد ومحتويات المخزن", "🚪 خروج"]
    )
    
    if menu == "🚪 خروج":
        st.session_state.logged_in = False
        st.rerun()
        
    elif menu == "🏠 الشاشة الرئيسية":
        st.markdown("<div class='welcome-card'><h3>لوحة التحكم والتحليلات البيانية المتكاملة</h3></div>", unsafe_allow_html=True)
        st.write(f"📅 **تاريخ اليوم:** {datetime.now().strftime('%Y-%m-%d')} | ⏰ **الوقت الحالي:** {datetime.now().strftime('%I:%M %p')}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🚗 حركات المواصلات", len(st.session_state.transport_records))
        c2.metric("👥 الموظفين المسجلين", len(st.session_state.employees))
        c3.metric("💰 قيود المصروفات العامة", len(st.session_state.expenses))
        
        if st.session_state.transport_records:
            st.markdown("### 📊 رسم بياني لمبالغ المواصلات لكل موظف")
            df = pd.DataFrame(st.session_state.transport_records)
            st.bar_chart(df.groupby("اسم الموظف")["المبلغ بالشيكل"].sum())

    elif menu == "🚗 كشف المواصلات (ملفك المرفق)":
        st.title("🚗 نموذج كشف مواصلات الموظفين الفردي")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة حقل جديد")
            emp = st.text_input("👤 اسم الموظف")
            job = st.text_input("💼 المسمى الوظيفي")
            day = st.selectbox("📆 اليوم", ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"])
            dt = st.date_input("📅 التاريخ", datetime.now(), key="trans_date")
            fr = st.text_input("📍 من")
            to = st.text_input("🏁 إلى")
            amt = st.number_input("💰 المبلغ بالشيكل", min_value=0.0, step=0.5)
            rsn = st.text_area("🔍 سبب الحركة")
            
            if st.button("💾 ترحيل الحركة"):
                if emp and amt > 0:
                    st.session_state.transport_records.append({
                        "اسم الموظف": emp, "المسمى الوظيفي": job,
                        "اليوم": day, "التاريخ": dt.strftime("%Y-%m-%d"), "من": fr, "إلى": to, "المبلغ بالشيكل": amt, "سبب الحركة": rsn
                    })
                    save_data('transport_records.json', st.session_state.transport_records)
                    st.success("✅ تم حفظ الحركة بنجاح")
                    st.rerun()
        with col2:
            st.subheader("🔍 استعراض الفلترة الفردية والتنزيل الملون")
            if st.session_state.transport_records:
                df_t = pd.DataFrame(st.session_state.transport_records)
                sel_emp = st.selectbox("🎯 اختر الموظف لفلترة وعرض كشفه:", df_t["اسم الموظف"].unique())
                df_res = df_t[df_t["اسم الموظف"] == sel_emp].copy()
                
                st.dataframe(df_res, use_container_width=True)
                st.metric("📊 إجمالي المستحق للشخص", f"{df_res['المبلغ بالشيكل'].sum()} شيكل")
                
                excel_file = export_to_styled_excel(df_res, title_report=sel_emp, is_transport=True)
                st.download_button(
                    label="📥 تنزيل الكشف بصيغة Excel (ملون ومفلتر وتلقائي)",
                    data=excel_file,
                    file_name=f"كشف_مواصلات_{sel_emp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("لا توجد بيانات مسجلة حالياً.")

    elif menu == "💰 المصروفات العامة":
        st.title("💰 إدارة البنود المالية العمومية")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة مصروف")
            exp_date = st.date_input("📅 التاريخ", datetime.now(), key="exp_date")
            exp_item = st.text_input("🏷️ البند / السلعة")
            exp_details = st.text_input("📑 التفاصيل")
            exp_price = st.number_input("💸 السعر بالشيكل", min_value=0.0, step=1.0)
            if st.button("💾 حفظ المصروف"):
                if exp_item and exp_price > 0:
                    st.session_state.expenses.append({
                        "التاريخ": exp_date.strftime("%Y-%m-%d"),
                        "نوع السلعة": exp_item, "التفاصيل": exp_details, "السعر (شيكل)": exp_price
                    })
                    save_data('expenses.json', st.session_state.expenses)
                    st.success("✅ تم حفظ البند المالي")
                    st.rerun()
        with col2:
            st.subheader("📋 كشف المصروفات والتحميل")
            if st.session_state.expenses:
                df_e = pd.DataFrame(st.session_state.expenses)
                st.dataframe(df_e, use_container_width=True)
                excel_exp = export_to_styled_excel(df_e, title_report="المصروفات العامة", is_transport=False)
                st.download_button(
                    label="📥 تحميل كشف المصروفات (Excel ملون)",
                    data=excel_exp,
                    file_name="المصروفات_العامة.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("لا توجد مصروفات مسجلة.")
        
    elif menu == "👥 شؤون الموظفين والعهد":
        st.title("👥 إدارة سجلات العهد والأصول للموظفين")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة موظف وعهدة")
            e_name = st.text_input("🤵 اسم الموظف")
            e_id = st.text_input("💳 رقم الهوية")
            e_asset = st.text_input("📦 العهدة المستلمة")
            e_status = st.selectbox("🔄 الحالة", ["مستلمة", "مرجعة"])
            if st.button("💾 حفظ الموظف"):
                if e_name and e_id:
                    st.session_state.employees.append({
                        "اسم الموظف": e_name, "رقم الهوية": e_id, "العهدة": e_asset, "الحالة": e_status
                    })
                    save_data('employees.json', st.session_state.employees)
                    st.success("✅ تم حفظ السجل بنجاح")
                    st.rerun()
        with col2:
            st.subheader("📋 قائمة العهد الحالية")
            if st.session_state.employees:
                df_emp = pd.DataFrame(st.session_state.employees)
                st.dataframe(df_emp, use_container_width=True)
                excel_emp = export_to_styled_excel(df_emp, title_report="سجلات العهد", is_transport=False)
                st.download_button(
                    label="📥 تحميل كشف العهد (Excel ملون)",
                    data=excel_emp,
                    file_name="كشف_العهد.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("لا يوجد موظفين مسجلين.")
        
    elif menu == "📦 جرد ومحتويات المخزن":
        st.title("📦 موجودات ومخازن الجمعية")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("➕ إضافة مادة للمخزن")
            i_name = st.text_input("📦 اسم المادة")
            i_qty = st.number_input("🔢 الكمية المتوفرة", min_value=0, step=1)
            if st.button("💾 حفظ في الجرد"):
                if i_name:
                    st.session_state.inventory.append({
                        "اسم المادة": i_name, "الكمية": i_qty
                    })
                    save_data('inventory.json', st.session_state.inventory)
                    st.success("✅ تم الإضافة للجرد")
                    st.rerun()
        with col2:
            st.subheader("📋 كشف الجرد الفعلي")
            if st.session_state.inventory:
                df_i = pd.DataFrame(st.session_state.inventory)
                st.dataframe(df_i, use_container_width=True)
                excel_inv = export_to_styled_excel(df_i, title_report="جرد المخزن", is_transport=False)
                st.download_button(
                    label="📥 تحميل كشف الجرد (Excel ملون)",
                    data=excel_inv,
                    file_name="جرد_المخزن.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else: st.info("المخزن فارغ حالياً.")
