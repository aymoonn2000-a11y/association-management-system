import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Page Configuration with wide layout
st.set_page_config(page_title="Association Management Dashboard", layout="wide", page_icon="🏢")

# ====================== Modern CSS Styling ======================
st.markdown("""
    <style>
    /* Global Font and Text Alignment for English UI */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [data-testid="stWidgetFormSubmitButton"], .stMarkdown, .stSelectbox, .stTextInput, .stButton {
        font-family: 'Inter', sans-serif !important;
        direction: ltr;
        text-align: left;
    }
    
    /* Modern Dashboard Metric Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #1E3A8A; /* Professional Dark Blue */
        margin-bottom: 15px;
    }
    .metric-card.success { border-left-color: #10B981; } /* Green */
    .metric-card.warning { border-left-color: #F59E0B; } /* Orange */
    .metric-card.danger { border-left-color: #EF4444; } /* Red */
    
    .metric-title { font-size: 14px; color: #6B7280; font-weight: 500; margin-bottom: 5px; }
    .metric-value { font-size: 24px; color: #111827; font-weight: 700; }
    
    /* Input Elements and UI Refinements */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stExpander"] {
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# ====================== Database Initialization & Automation ======================
def init_db():
    with sqlite3.connect('association.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS project_employees 
                     (id INTEGER PRIMARY KEY, project_type TEXT, name TEXT, national_id TEXT, phone TEXT, job_title TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS suppliers 
                     (id INTEGER PRIMARY KEY, name TEXT, category TEXT, phone TEXT, email TEXT, address TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS invoices 
                     (id INTEGER PRIMARY KEY, supplier_id INTEGER, item_name TEXT, qty INTEGER, total_price REAL, status TEXT, details TEXT, date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS inventory 
                     (id INTEGER PRIMARY KEY, item_name TEXT, category TEXT, quantity INTEGER, status TEXT, last_updated TEXT)''')
        conn.commit()

init_db()

# Smart Automation Function to sync purchased items with the inventory
def autocomplete_inventory(item_name, qty):
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    with sqlite3.connect('association.db') as conn:
        c = conn.cursor()
        # Check if the item already exists in the inventory
        c.execute("SELECT id, quantity FROM inventory WHERE LOWER(item_name) = LOWER(?)", (item_name,))
        result = c.fetchone()
        
        if result:
            new_qty = result[1] + qty
            status = "In Stock / Good Condition" if new_qty >= 5 else "Low Stock (Reorder Urgent)"
            c.execute("UPDATE inventory SET quantity = ?, status = ?, last_updated = ? WHERE id = ?", (new_qty, status, update_time, result[0]))
        else:
            status = "In Stock / Good Condition" if qty >= 5 else "Low Stock (Reorder Urgent)"
            c.execute("INSERT INTO inventory (item_name, category, quantity, status, last_updated) VALUES (?, 'Stationery & Office Supplies', ?, ?, ?)", 
                      (item_name, qty, status, update_time))
        conn.commit()

# ====================== Main Dashboard Header ======================
st.markdown("<h1 style='color: #1E3A8A; font-size: 32px; font-weight: 700; margin-bottom: 5px;'>🏢 Association Cloud Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 16px; margin-bottom: 25px;'>Advanced Management Information System for Procurement, Inventory, and Field Operations</p>", unsafe_allow_html=True)
st.divider()

# Main Project Tabs
tab_projects, tab_suppliers, tab_inventory = st.tabs([
    "📁 Project Sectors & Staff", 
    "🧾 Suppliers & Smart Invoices", 
    "📦 Central Office Inventory"
])

# ================== 1. Project Sectors & Staff Tab ==================
with tab_projects:
    st.markdown("<h3 style='color: #1E3A8A;'>🛠️ Staff & Field Operations Management</h3>", unsafe_allow_html=True)
    
    proj_tabs = st.tabs(["🏠 Shelter Sector", "💳 CVA Sector", "📊 MEAL Sector"])
    project_details = [
        {"tab": proj_tabs[0], "name": "Shelter", "icon": "🏠"},
        {"tab": proj_tabs[1], "name": "CVA", "icon": "💳"},
        {"tab": proj_tabs[2], "name": "MEAL", "icon": "📊"}
    ]
    
    for idx, project in enumerate(project_details):
        with project["tab"]:
            st.markdown(f"<h4>{project['icon']} {project['name']} Project Team</h4>", unsafe_allow_html=True)
            
            # Expandable Registration Form
            with st.expander(f"➕ Register New Staff Member for {project['name']}", expanded=False):
                with st.form(f"form_emp_{project['name']}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        emp_name = st.text_input("Full Name")
                        emp_national_id = st.text_input("National ID / Passport Number")
                    with c2:
                        emp_phone = st.text_input("Phone Number")
                        emp_job_title = st.text_input("Job Title / Role")
                    
                    if st.form_submit_button("Save Staff Member"):
                        if emp_name and emp_national_id:
                            with sqlite3.connect('association.db') as conn:
                                conn.execute("INSERT INTO project_employees (project_type, name, national_id, phone, job_title) VALUES (?,?,?,?,?)", 
                                             (project['name'], emp_name, emp_national_id, emp_phone, emp_job_title))
                                conn.commit()
                            st.success("✅ Staff member registered successfully!")
                            st.rerun()
            
            # Fetch and Display Team Data
            with sqlite3.connect('association.db') as conn:
                df_emp = pd.read_sql_query("SELECT id, name, national_id, phone, job_title FROM project_employees WHERE project_type = ?", conn, params=(project['name'],))
            
            if not df_emp.empty:
                st.dataframe(df_emp, use_container_width=True, hide_index=True)
                
                # Modern CSV Export Options
                csv_emp = df_emp.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download Staff Roster (CSV)", data=csv_emp, file_name=f"employees_{project['name']}.csv", mime='text/csv')
            else:
                st.info(f"No active staff recorded in the {project['name']} sector yet.")

# ================== 2. Suppliers & Invoices Tab ==================
with tab_suppliers:
    st.markdown("<h3 style='color: #1E3A8A;'>🏪 Procurement & Vendor Management</h3>", unsafe_allow_html=True)
    sub_tab_supp, sub_tab_inv = st.tabs(["📋 Approved Vendor Directory", "🧾 Orders & Cost Invoices"])
    
    with sub_tab_supp:
        with st.form("supplier_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                s_name = st.text_input("Company / Vendor Name")
                s_category = st.selectbox("Category of Supply", ["Electronic Devices", "Stationery & Office Supplies", "Construction & Maintenance Material", "General Services"])
            with col2:
                s_phone = st.text_input("Contact Number")
                s_email = st.text_input("Email Address")
            with col3:
                s_address = st.text_input("Office Headquarters / Address")
            
            if st.form_submit_button("Approve & Add Vendor"):
                if s_name and s_phone:
                    with sqlite3.connect('association.db') as conn:
                        conn.execute("INSERT INTO suppliers (name, category, phone, email, address) VALUES (?, ?, ?, ?, ?)", (s_name, s_category, s_phone, s_email, s_address))
                        conn.commit()
                    st.success("✅ Vendor successfully listed in the directory!")
                    st.rerun()
        
        st.divider()
        with sqlite3.connect('association.db') as conn:
            df_suppliers = pd.read_sql_query("SELECT * FROM suppliers", conn)
        if not df_suppliers.empty:
            st.dataframe(df_suppliers, use_container_width=True, hide_index=True)

    with sub_tab_inv:
        with sqlite3.connect('association.db') as conn:
            suppliers_df = pd.read_sql_query("SELECT id, name FROM suppliers", conn)
            
        if suppliers_df.empty:
            st.warning("⚠️ No vendors found. Please add a vendor from the Approved Directory tab before registering invoices.")
        else:
            supplier_mapping = dict(zip(suppliers_df['name'], suppliers_df['id']))
            with st.form("invoice_form"):
                col1, col2 = st.columns(2)
                with col1:
                    chosen_supplier = st.selectbox("Select Vendor", suppliers_df['name'].tolist())
                    inv_item_name = st.text_input("Item / Service Description (e.g., Premium A4 Paper)")
                    inv_qty = st.number_input("Quantity Ordered", min_value=1, value=1)
                with col2:
                    inv_price = st.number_input("Total Invoice Amount (Tax Included)", min_value=0.0)
                    inv_status = st.selectbox("Financial & Delivery Status", ["Pending Processing/Order", "Paid in Full & Received into Inventory", "On Credit / Unpaid"])
                    inv_details = st.text_area("Additional Terms or Specifications")
                    
                if st.form_submit_button("Record Invoice & Log Cost"):
                    if inv_item_name and inv_price > 0:
                        s_id = supplier_mapping[chosen_supplier]
                        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                        with sqlite3.connect('association.db') as conn:
                            conn.execute("INSERT INTO invoices (supplier_id, item_name, qty, total_price, status, details, date) VALUES (?,?,?,?,?,?,?)",
                                         (s_id, inv_item_name, inv_qty, inv_price, inv_status, inv_details, current_date))
                            conn.commit()
                        
                        # Smart Automation Trigger
                        if inv_status == "Paid in Full & Received into Inventory":
                            autocomplete_inventory(inv_item_name, inv_qty)
                            st.info("🤖 System Automation: Quantities have been automatically pushed to the office inventory ledger!")
                            
                        st.success("✅ Financial invoice logged successfully!")
                        st.rerun()
        
        st.divider()
        with sqlite3.connect('association.db') as conn:
            df_invoices = pd.read_sql_query("""
                SELECT i.id, s.name as supplier_name, i.item_name, i.qty, i.total_price, i.status, i.date 
                FROM invoices i LEFT JOIN suppliers s ON i.supplier_id = s.id
            """, conn)
            
        if not df_invoices.empty:
            # Modern Analytic Metric Cards
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f'<div class="metric-card"><div class="metric-title">Total Logs Filed</div><div class="metric-value">{len(df_invoices)}</div></div>', unsafe_allow_html=True)
            with m_col2:
                st.markdown(f'<div class="metric-card success"><div class="metric-title">Total Financial Expenditure</div><div class="metric-value">${df_invoices["total_price"].sum():,.2f}</div></div>', unsafe_allow_html=True)
            with m_col3:
                pending_inv = len(df_invoices[df_invoices['status'] == 'Pending Processing/Order'])
                st.markdown(f'<div class="metric-card warning"><div class="metric-title">Pending Orders</div><div class="metric-value">{pending_inv}</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(df_invoices, use_container_width=True, hide_index=True)
            
            csv_inv = df_invoices.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Export Procurement Ledger (CSV)", data=csv_inv, file_name="invoice_report.csv", mime='text/csv')

# ================== 3. Central Office Inventory Tab ==================
with tab_inventory:
    st.markdown("<h3 style='color: #1E3A8A;'>📦 Office Stock Audit & Stationery Ledger</h3>", unsafe_allow_html=True)
    
    # Automatic Stock Threshold Alert System
    with sqlite3.connect('association.db') as conn:
        df_inventory = pd.read_sql_query("SELECT * FROM inventory", conn)
        
    if not df_inventory.empty:
        low_stock_items = df_inventory[df_inventory['quantity'] < 5]['item_name'].tolist()
        if low_stock_items:
            st.markdown(f"""
            <div style="background-color: #FEF2F2; color: #991B1B; padding: 15px; border-radius: 8px; border-left: 5px solid #EF4444; font-weight: 500; margin-bottom: 20px;">
                ⚠️ <b>Critical Stock Warning:</b> The following assets are running out (Quantity under 5 units): {', '.join(low_stock_items)}
            </div>
            """, unsafe_allow_html=True)
    
    with st.form("inventory_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            inv_name = st.text_input("Asset Name (e.g., HP Printer Ink 652)")
        with col2:
            inv_cat = st.selectbox("Stock Classification", ["Stationery & Office Supplies", "Ink & Printer Consumables", "Cleaning & Sanitizing Materials", "Office Hospitality & Snacks"])
        with col3:
            inv_quantity = st.number_input("Initial Available Stock", min_value=0, value=1)
            
        if st.form_submit_button("Manually Restock Shelf"):
            if inv_name:
                update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                status = "In Stock / Good Condition" if inv_quantity >= 5 else "Low Stock (Reorder Urgent)"
                with sqlite3.connect('association.db') as conn:
                    conn.execute("INSERT INTO inventory (item_name, category, quantity, status, last_updated) VALUES (?, ?, ?, ?, ?)",
                                 (inv_name, inv_cat, inv_quantity, status, update_time))
                    conn.commit()
                st.success("✅ Stock tracking metrics updated!")
                st.rerun()
                
    st.divider()
    if not df_inventory.empty:
        # Inventory Analytics
        i_col1, i_col2 = st.columns(2)
        with i_col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Unique SKUs Tracked</div><div class="metric-value">{len(df_inventory)}</div></div>', unsafe_allow_html=True)
        with i_col2:
            st.markdown(f'<div class="metric-card danger"><div class="metric-title">Items Requiring Reorder</div><div class="metric-value">{len(df_inventory[df_inventory["quantity"] < 5])}</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df_inventory, use_container_width=True, hide_index=True)
        
        csv_inv = df_inventory.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Full Stock Audit Sheet", data=csv_inv, file_name="inventory_status.csv", mime='text/csv')
    else:
        st.info("No corporate assets or stationery supplies currently recorded in the warehouse.")

# ================== Footer ==================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 15px; color: #9CA3AF; font-size: 14px;">
    <p>💼 Association Cloud Platform | Modernized English Layout & Secured Infrastructure © 2026</p>
</div>
""", unsafe_allow_html=True)
