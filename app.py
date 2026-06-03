import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="نظام إدارة الجمعية الذكي",
    page_icon="🏢",
    layout="wide"
)

# ===================================
# CSS احترافي
# ===================================

st.markdown("""
<style>

.main{
    background:#f5f7fb;
}

.title{
    text-align:center;
    padding:20px;
    color:#2563eb;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 10px rgba(0,0,0,.1);
}

.metric-card{
    background:white;
    border-radius:15px;
    padding:20px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.1);
}

.metric-number{
    font-size:32px;
    color:#2563eb;
    font-weight:bold;
}

</style>
""",unsafe_allow_html=True)


# ===================================
# تخزين البيانات
# ===================================

if "employees" not in st.session_state:
    st.session_state.employees=[]

if "inventory" not in st.session_state:
    st.session_state.inventory=[
        {"المادة":"شاي","المتوفر":50,"الصادر":12},
        {"المادة":"قهوة","المتوفر":40,"الصادر":15},
        {"المادة":"منظفات","المتوفر":100,"الصادر":30},
    ]


# ===================================
# عنوان
# ===================================

st.markdown("""
<div class='title'>
<h1>🏢 نظام الإدارة الداخلي للجمعية</h1>
<p>إدارة الموظفين - المخزون - العهد الميدانية</p>
</div>
""",unsafe_allow_html=True)


# ===================================
# بطاقات الإحصائيات
# ===================================

c1,c2,c3=st.columns(3)

with c1:
    st.markdown(f"""
    <div class='metric-card'>
    <div>عدد الموظفين</div>
    <div class='metric-number'>
    {len(st.session_state.employees)}
    </div>
    </div>
    """,unsafe_allow_html=True)

with c2:
    total_inventory=sum(x["المتوفر"] for x in st.session_state.inventory)

    st.markdown(f"""
    <div class='metric-card'>
    <div>إجمالي المخزون</div>
    <div class='metric-number'>
    {total_inventory}
    </div>
    </div>
    """,unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='metric-card'>
    <div>العهد النشطة</div>
    <div class='metric-number'>
    12
    </div>
    </div>
    """,unsafe_allow_html=True)


st.write("")
tab1,tab2=st.tabs([
    "📦 إدارة المخزون",
    "👥 الموظفين والعهد"
])


# ===================================
# المخزون
# ===================================

with tab1:

    st.subheader("إضافة حركة مخزون")

    col1,col2,col3=st.columns(3)

    with col1:
        item=st.selectbox(
            "المادة",
            ["شاي","قهوة","منظفات","قرطاسية"]
        )

    with col2:
        available=st.number_input(
            "الكمية الداخلة",
            min_value=0
        )

    with col3:
        issued=st.number_input(
            "الكمية الصادرة",
            min_value=0
        )

    if st.button("تحديث المخزون"):

        found=False

        for i in st.session_state.inventory:

            if i["المادة"]==item:
                i["المتوفر"]+=available
                i["الصادر"]+=issued
                found=True

        if not found:
            st.session_state.inventory.append({
                "المادة":item,
                "المتوفر":available,
                "الصادر":issued
            })

        st.success("تم تحديث المخزون بنجاح")

    st.write("")
    st.dataframe(
        pd.DataFrame(
            st.session_state.inventory
        ),
        use_container_width=True
    )


# ===================================
# الموظفين
# ===================================

with tab2:

    st.subheader("إضافة موظف")

    name=st.text_input(
        "اسم الموظف"
    )

    title=st.text_input(
        "المسمى الوظيفي"
    )

    program=st.selectbox(
        "البرنامج",
        [
            "CVA",
            "MEAL",
            "WASH",
            "Shelter"
        ]
    )

    custody=st.multiselect(
        "العهدة",
        [
            "لاب توب",
            "آيباد",
            "قرطاسية",
            "تيشيرت"
        ]
    )

    notes=st.text_area(
        "ملاحظات"
    )

    if st.button("حفظ الموظف"):

        st.session_state.employees.append({

            "الاسم":name,
            "المسمى":title,
            "البرنامج":program,
            "العهدة":",".join(custody),
            "ملاحظات":notes
        })

        st.success(
            "تم حفظ الموظف بنجاح"
        )

    st.write("")

    search=st.text_input(
        "🔍 بحث عن موظف"
    )

    df=pd.DataFrame(
        st.session_state.employees
    )

    if not df.empty:

        if search:
            df=df[
                df["الاسم"]
                .str.contains(
                    search,
                    case=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

        csv=df.to_csv(
            index=False
        ).encode('utf-8-sig')

        st.download_button(
            "⬇ تصدير CSV",
            csv,
            "employees.csv",
            "text/csv"
        )
