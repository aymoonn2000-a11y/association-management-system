import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الأساسية لتطبيق Streamlit
st.set_page_config(
    page_title="نظام إدارة الجمعية الذكي",
    layout="wide"
)

# كود الواجهة البرمجية الكامل (HTML, CSS, JavaScript)
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="نظام إدارة ذكي للجمعيات - إدارة المخزون والموظفين والعهد">
    <title>نظام إدارة الجمعية الذكي</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --primary-light: rgba(37, 99, 235, 0.1);
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --danger-light: #fee2e2;
            --success-light: #ecfdf5;
            --info-light: #e0f2fe;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Cairo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            padding: 2rem 1rem;
            line-height: 1.6;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
        }

        /* Header */
        header {
            margin-bottom: 2.5rem;
            text-align: center;
        }

        header h1 {
            color: var(--primary);
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        header p {
            color: var(--text-muted);
            font-size: 1rem;
        }

        /* Navigation Tabs */
        .tabs {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0;
            overflow-x: auto;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: none;
            border: none;
            padding: 1rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 0.5rem 0.5rem 0 0;
            position: relative;
            white-space: nowrap;
        }

        .tab-btn:hover {
            color: var(--primary);
            background-color: var(--primary-light);
        }

        .tab-btn.active {
            color: var(--primary);
            background-color: var(--primary-light);
            border-bottom: 3px solid var(--primary);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Grid Layout */
        .grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .grid {
                grid-template-columns: 1fr;
            }
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }

        .card h2 {
            font-size: 1.3rem;
            margin-bottom: 1.5rem;
            color: var(--text-main);
            border-right: 4px solid var(--primary);
            padding-right: 0.75rem;
        }

        /* Form Groups */
        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-main);
        }

        .form-group.required label::after {
            content: " *";
            color: var(--danger);
            font-weight: 700;
        }

        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            font-size: 0.95rem;
            background-color: #f1f5f9;
            transition: all 0.3s ease;
            font-family: inherit;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            background-color: var(--bg-card);
            box-shadow: 0 0 0 3px var(--primary-light);
        }

        .form-control:disabled {
            background-color: #e2e8f0;
            cursor: not-allowed;
            opacity: 0.6;
        }

        .form-control.error {
            border-color: var(--danger);
            background-color: var(--danger-light);
        }

        .form-control.error:focus {
            box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
        }

        /* Error Messages */
        .error-message {
            color: var(--danger);
            font-size: 0.85rem;
            margin-top: 0.25rem;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        /* Checkboxes Group */
        .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            background: #f1f5f9;
            padding: 1rem;
            border-radius: 0.5rem;
            border: none;
        }

        .checkbox-group label {
            display: flex;
            align-items: center;
            font-weight: normal;
            margin-bottom: 0;
            cursor: pointer;
        }

        .checkbox-group input[type="checkbox"] {
            width: 1.25rem;
            height: 1.25rem;
            margin-left: 0.5rem;
            cursor: pointer;
            accent-color: var(--primary);
        }

        /* Buttons */
        .btn {
            background-color: var(--primary);
            color: #fff;
            border: none;
            padding: 0.875rem 1.5rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95rem;
            width: 100%;
            transition: all 0.3s ease;
            font-family: inherit;
        }

        .btn:hover:not(:disabled) {
            background-color: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }

        .btn:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-secondary {
            background-color: var(--text-muted);
        }

        .btn-secondary:hover:not(:disabled) {
            background-color: var(--text-main);
        }

        .btn-success {
            background-color: var(--success);
        }

        .btn-success:hover:not(:disabled) {
            background-color: #059669;
        }

        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
            width: auto;
        }

        /* Tables */
        .table-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: right;
            font-size: 0.95rem;
        }

        th {
            background-color: #f1f5f9;
            color: var(--text-main);
            padding: 1rem;
            font-weight: 600;
            border-bottom: 2px solid var(--border);
            text-align: right;
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
            color: var(--text-muted);
        }

        tr:hover td {
            background-color: #f8fafc;
            color: var(--text-main);
        }

        tbody tr:focus-within {
            outline: 2px solid var(--primary);
            outline-offset: -1px;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .badge-program {
            background-color: var(--info-light);
            color: #0369a1;
        }

        .badge-qty {
            background-color: var(--success-light);
            color: #065f46;
        }

        .badge-out {
            background-color: var(--danger-light);
            color: #991b1b;
        }

        .badge-warning {
            background-color: #fef3c7;
            color: #92400e;
        }

        /* Lists */
        .custody-list {
            font-size: 0.85rem;
            list-style: square;
            padding-right: 1.5rem;
            margin: 0;
        }

        .custody-list li {
            margin-bottom: 0.25rem;
        }

        /* Alert Messages */
        .alert {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .alert.show {
            display: block;
        }

        .alert-success {
            background-color: var(--success-light);
            border-left: 4px solid var(--success);
            color: #065f46;
        }

        .alert-error {
            background-color: var(--danger-light);
            border-left: 4px solid var(--danger);
            color: #991b1b;
        }

        .alert-info {
            background-color: var(--info-light);
            border-left: 4px solid #0369a1;
            color: #082f49;
        }

        /* Responsive */
        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            header h1 {
                font-size: 1.75rem;
            }

            .card {
                padding: 1rem;
            }

            .tabs {
                gap: 0.5rem;
            }

            .tab-btn {
                padding: 0.75rem 1rem;
                font-size: 0.9rem;
            }

            table {
                font-size: 0.85rem;
            }

            th, td {
                padding: 0.75rem 0.5rem;
            }

            .btn {
                padding: 0.75rem 1rem;
                font-size: 0.9rem;
            }
        }

        /* Accessibility */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }

        /* Focus Visible */
        .tab-btn:focus-visible,
        .form-control:focus-visible,
        .btn:focus-visible,
        .custody-list li:focus-visible {
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }

        /* Print Styles */
        @media print {
            body {
                background: white;
                padding: 0;
            }

            .card {
                page-break-inside: avoid;
                box-shadow: none;
                border: 1px solid #ccc;
            }

            .tabs,
            .form-group,
            .btn {
                display: none;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <header role="banner">
        <h1>نظام الإدارة الداخلي للجمعية</h1>
        <p>إدارة المخزون المستودعي، بيانات الموظفين، والعهد الميدانية الذكية</p>
    </header>

    <nav class="tabs" role="tablist" aria-label="قائمة التنقل الرئيسية">
        <button class="tab-btn active" role="tab" aria-selected="true" aria-controls="inventory" onclick="switchTab(event, 'inventory')">
            📦 إدارة المخزون
        </button>
        <button class="tab-btn" role="tab" aria-selected="false" aria-controls="staff" onclick="switchTab(event, 'staff')">
            👥 إدارة الموظفين والعهد
        </button>
    </nav>

    <div id="alertContainer" role="status" aria-live="polite" aria-atomic="true"></div>

    <section id="inventory" class="tab-content active" role="tabpanel">
        <div class="grid">
            <div class="card">
                <h2>تحديث حركة مخزن</h2>
                <form id="inventoryForm" novalidate>
                    <div class="form-group required">
                        <label for="itemCategory">صنف المادة</label>
                        <select class="form-control" id="itemCategory" required aria-required="true">
                            <option value="">-- اختر صنفاً --</option>
                            <option value="شاي">شاي</option>
                            <option value="قهوة">قهوة</option>
                            <option value="منظفات">منظفات</option>
                            <option value="قرطاسية (أوراق)">قرطاسية (أوراق)</option>
                            <option value="قرطاسية (أقلام)">قرطاسية (أقلام)</option>
                            <option value="قرطاسية (فايلات نايلون)">قرطاسية (فايلات نايلون)</option>
                        </select>
                        <div class="error-message" id="itemCategoryError" role="alert">يرجى اختيار صنف المادة</div>
                    </div>

                    <div class="form-group required">
                        <label for="itemAvailable">الكمية المتواجدة (الداخلة للمستودع)</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            id="itemAvailable" 
                            min="0" 
                            value="0" 
                            required 
                            aria-required="true"
                            placeholder="أدخل الكمية"
                        >
                        <div class="error-message" id="itemAvailableError" role="alert">يرجى إدخال كمية صحيحة (رقم موجب)</div>
                    </div>

                    <div class="form-group required">
                        <label for="itemIssued">الكمية الصادرة (المنصرفة)</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            id="itemIssued" 
                            min="0" 
                            value="0" 
                            required 
                            aria-required="true"
                            placeholder="أدخل الكمية"
                        >
                        <div class="error-message" id="itemIssuedError" role="alert">يرجى إدخال كمية صحيحة (رقم موجب)</div>
                    </div>

                    <button type="submit" class="btn">✓ تحديث المخزون</button>
                </form>
            </div>

            <div class="card">
                <h2>حالة المخزن الحالية</h2>
                <div class="table-container">
                    <table role="region" aria-label="جدول حالة المخزن الحالية">
                        <thead>
                            <tr>
                                <th scope="col">المادة</th>
                                <th scope="col">الكمية المتواجدة</th>
                                <th scope="col">الكمية الصادرة</th>
                                <th scope="col">الرصيد المتبقي</th>
                            </tr>
                        </thead>
                        <tbody id="inventoryTableBody">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <section id="staff" class="tab-content" role="tabpanel">
        <div class="grid">
            <div class="card">
                <h2>إضافة موظف وعهدة جديدة</h2>
                <form id="staffForm" novalidate>
                    <div class="form-group required">
                        <label for="staffName">اسم الموظف الثلاثي</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="staffName" 
                            placeholder="محمد علي أحمد" 
                            required 
                            aria-required="true"
                            minlength="3"
                            maxlength="100"
                        >
                        <div class="error-message" id="staffNameError" role="alert">يرجى إدخال اسم الموظف (3-100 أحرف)</div>
                    </div>

                    <div class="form-group required">
                        <label for="staffTitle">المسمى الوظيفي</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="staffTitle" 
                            placeholder="منسق ميداني" 
                            required 
                            aria-required="true"
                            minlength="2"
                            maxlength="50"
                        >
                        <div class="error-message" id="staffTitleError" role="alert">يرجى إدخال المسمى الوظيفي</div>
                    </div>

                    <div class="form-group required">
                        <label for="staffIdCard">رقم هوية الموظف</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="staffIdCard" 
                            placeholder="ID-100234" 
                            required 
                            aria-required="true"
                            pattern="^[A-Za-z0-9\-]{3,20}$"
                            minlength="3"
                            maxlength="20"
                        >
                        <div class="error-message" id="staffIdCardError" role="alert">يرجى إدخال رقم الهوية بشكل صحيح (حروف وأرقام وشرطات)</div>
                    </div>

                    <div class="form-group required">
                        <label for="staffProgram">البرنامج التابع له</label>
                        <select class="form-control" id="staffProgram" required aria-required="true">
                            <option value="">-- اختر برنامجاً --</option>
                            <option value="CVA Field Mentor">CVA Field Mentor</option>
                            <option value="MEAL Field Assistant">MEAL Field Assistant</option>
                            <option value="Shelter Field Engineer">Shelter Field Engineer</option>
                            <option value="WASH Field Engineer">WASH Field Engineer</option>
                            <option value="WASH Field Assistant">WASH Field Assistant</option>
                        </select>
                        <div class="error-message" id="staffProgramError" role="alert">يرجى اختيار البرنامج</div>
                    </div>

                    <div class="form-group">
                        <label>العهدة المستلمة (اختر ما ينطبق)</label>
                        <fieldset class="checkbox-group" aria-label="قائمة العهد المستلمة">
                            <legend class="sr-only">اختر العهد المستلمة</legend>
                            <label><input type="checkbox" value="لاب توب" class="custody-check"> لاب توب</label>
                            <label><input type="checkbox" value="آي باد" class="custody-check"> آي باد</label>
                            <label><input type="checkbox" value="تيشيرت باسم الجمعية" class="custody-check"> تيشيرت باسم الجمعية</label>
                            <label><input type="checkbox" value="حزمة قرطاسية متكاملة" class="custody-check"> قرطاسية</label>
                        </fieldset>
                    </div>

                    <div class="form-group required">
                        <label for="custodyDate">تاريخ استلام العهدة</label>
                        <input 
                            type="date" 
                            class="form-control" 
                            id="custodyDate" 
                            required 
                            aria-required="true"
                        >
                        <div class="error-message" id="custodyDateError" role="alert">يرجى اختيار تاريخ استلام العهدة</div>
                    </div>

                    <div class="form-group">
                        <label for="staffNotes">ملاحظات إضافية</label>
                        <textarea 
                            class="form-control" 
                            id="staffNotes" 
                            rows="3" 
                            placeholder="أي تفاصيل أخرى حول حالة العهدة..."
                            maxlength="500"
                        ></textarea>
                        <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">
                            <span id="charCount">0</span>/500 أحرف
                        </small>
                    </div>

                    <button type="submit" class="btn">✓ حفظ الموظف والعهدة</button>
                </form>
            </div>

            <div class="card">
                <h2>سجل الموظفين والعهد</h2>
                <div class="table-container">
                    <table role="region" aria-label="جدول سجل الموظفين والعهد">
                        <thead>
                            <tr>
                                <th scope="col">الموظف / الهوية</th>
                                <th scope="col">المسمى / البرنامج</th>
                                <th scope="col">العهدة المستلمة</th>
                                <th scope="col">تاريخ الاستلام</th>
                                <th scope="col">ملاحظات</th>
                                <th scope="col">الإجراءات</th>
                            </tr>
                        </thead>
                        <tbody id="staffTableBody">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>
</div>

<script>
    // ============================================
    // 1. UTILITY FUNCTIONS
    // ============================================

    function switchTab(event, tabId) {
        const tabBtns = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabBtns.forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        });

        tabContents.forEach(content => {
            content.classList.remove('active');
        });

        event.target.classList.add('active');
        event.target.setAttribute('aria-selected', 'true');
        document.getElementById(tabId).classList.add('active');
    }

    function showAlert(message, type = 'info', duration = 4000) {
        const container = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-\${type} show`;
        alert.setAttribute('role', 'status');
        alert.setAttribute('aria-live', 'polite');
        
        const icon = {
            success: '✓',
            error: '✗',
            info: 'ℹ'
        }[type] || 'ℹ';

        alert.innerHTML = `\${icon} \${message}`;
        container.appendChild(alert);

        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
        }, duration);
    }

    function formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('ar-EG', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // عدّاد الحروف للملاحظات
    document.getElementById('staffNotes').addEventListener('input', function() {
        document.getElementById('charCount').textContent = this.value.length;
    });

    // ============================================
    // 2. INVENTORY MANAGEMENT
    // ============================================

    const initialInventory = JSON.parse(localStorage.getItem('ngo_inventory')) || {
        "شاي": { available: 50, issued: 12 },
        "قهوة": { available: 40, issued: 15 },
        "منظفات": { available: 100, issued: 35 },
        "قرطاسية (أوراق)": { available: 200, issued: 80 },
        "قرطاسية (أقلام)": { available: 500, issued: 150 },
        "قرطاسية (فايلات نايلون)": { available: 300, issued: 45 }
    };

    function renderInventory() {
        const tbody = document.getElementById('inventoryTableBody');
        tbody.innerHTML = '';

        Object.entries(initialInventory).forEach(([item, data]) => {
            const remaining = data.available - data.issued;
            const statusBadge = remaining < 10 
                ? `<span class="badge badge-warning">منخفض</span>`
                : remaining < 50
                ? `<span class="badge">متوسط</span>`
                : `<span class="badge badge-qty">كافي</span>`;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>\${item}</strong></td>
                <td><span class="badge badge-qty">\${data.available}</span></td>
                <td><span class="badge badge-out">\${data.issued}</span></td>
                <td>
                    <strong style="color: \${remaining < 10 ? 'var(--danger)' : 'var(--text-main)'}">
                        \${remaining}
                    </strong> 
                    \${statusBadge}
                </td>
            `;
            tbody.appendChild(row);
        });
        
        localStorage.setItem('ngo_inventory', JSON.stringify(initialInventory));
    }

    function validateInventoryForm() {
        const category = document.getElementById('itemCategory');
        const available = document.getElementById('itemAvailable');
        const issued = document.getElementById('itemIssued');
        let isValid = true;

        document.querySelectorAll('#inventoryForm .error-message').forEach(el => el.classList.remove('show'));
        document.querySelectorAll('#inventoryForm .form-control').forEach(el => el.classList.remove('error'));

        if (!category.value.trim()) {
            document.getElementById('itemCategoryError').classList.add('show');
            category.classList.add('error');
            isValid = false;
        }

        if (available.value === '' || parseInt(available.value) < 0) {
            document.getElementById('itemAvailableError').classList.add('show');
            available.classList.add('error');
            isValid = false;
        }

        if (issued.value === '' || parseInt(issued.value) < 0) {
            document.getElementById('itemIssuedError').classList.add('show');
            issued.classList.add('error');
            isValid = false;
        }

        return isValid;
    }

    document.getElementById('inventoryForm').addEventListener('submit', function(e) {
        e.preventDefault();

        if (!validateInventoryForm()) {
            showAlert('يرجى تصحيح الأخطاء أعلاه', 'error');
            return;
        }

        const category = document.getElementById('itemCategory').value;
        const av = parseInt(document.getElementById('itemAvailable').value) || 0;
        const is = parseInt(document.getElementById('itemIssued').value) || 0;

        initialInventory[category].available += av;
        initialInventory[category].issued += is;

        renderInventory();
        this.reset();
        showAlert('تم تحديث المخزون بنجاح ✓', 'success');
    });

    // ============================================
    // 3. STAFF MANAGEMENT
    // ============================================

    let staffList = JSON.parse(localStorage.getItem('ngo_staff')) || [
        {
            id: 1710000000000,
            name: "حسن فضل أحمد طافش",
            idCard: "Emp-4022",
            title: "مهندس إيواء",
            program: "Shelter Field Engineer",
            custody: ["لاب توب", "تيشيرت باسم الجمعية"],
            date: "2026-02-15",
            notes: "اللاب توب بحالة ممتازة"
        }
    ];

    function renderStaff() {
        const tbody = document.getElementById('staffTableBody');
        tbody.innerHTML = '';

        if (staffList.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 2rem;">
                        لا توجد بيانات موظفين حالياً
                    </td>
                </tr>
            `;
            localStorage.setItem('ngo_staff', JSON.stringify(staffList));
            return;
        }

        staffList.forEach(staff => {
            const custodyItems = staff.custody && staff.custody.length > 0
                ? `<ul class="custody-list">\${staff.custody.map(item => `<li>\${item}</li>`).join('')}</ul>`
                : '<small style="color: var(--text-muted);">-</small>';

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <strong>\${staff.name}</strong><br>
                    <small style="color: var(--text-muted);">\${staff.idCard}</small>
                </td>
                <td>
                    <strong>\${staff.title}</strong><br>
                    <span class="badge badge-program">\${staff.program}</span>
                </td>
                <td>\${custodyItems}</td>
                <td><time datetime="\${staff.date}">\${formatDate(staff.date)}</time></td>
                <td><small>\${staff.notes || '-'}</small></td>
                <td>
                    <button class="btn btn-secondary btn-small" onclick="deleteStaff(\${staff.id})" aria-label="حذف سجل الموظف">
                        🗑️ حذف
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

        localStorage.setItem('ngo_staff', JSON.stringify(staffList));
    }

    function deleteStaff(id) {
        if (confirm('هل أنت متأكد من رغبتك في حذف هذا الموظف وسجل عهدته بالكامل؟')) {
            staffList = staffList.filter(staff => staff.id !== id);
            renderStaff();
            showAlert('تم حذف سجل الموظف بنجاح', 'success');
        }
    }

    function validateStaffForm() {
        const name = document.getElementById('staffName');
        const title = document.getElementById('staffTitle');
        const idCard = document.getElementById('staffIdCard');
        const program = document.getElementById('staffProgram');
        const date = document.getElementById('custodyDate');
        let isValid = true;

        document.querySelectorAll('#staffForm .error-message').forEach(el => el.classList.remove('show'));
        document.querySelectorAll('#staffForm .form-control').forEach(el => el.classList.remove('error'));

        if (!name.value.trim() || name.value.trim().length < 3) {
            document.getElementById('staffNameError').classList.add('show');
            name.classList.add('error');
            isValid = false;
        }

        if (!title.value.trim() || title.value.trim().length < 2) {
            document.getElementById('staffTitleError').classList.add('show');
            title.classList.add('error');
            isValid = false;
        }

        if (!idCard.value.trim() || idCard.value.trim().length < 3) {
            document.getElementById('staffIdCardError').classList.add('show');
            idCard.classList.add('error');
            isValid = false;
        }

        if (!program.value.trim()) {
            document.getElementById('staffProgramError').classList.add('show');
            program.classList.add('error');
            isValid = false;
        }

        if (!date.value) {
            document.getElementById('custodyDateError').classList.add('show');
            date.classList.add('error');
            isValid = false;
        }

        return isValid;
    }

    document.getElementById('staffForm').addEventListener('submit', function(e) {
        e.preventDefault();

        if (!validateStaffForm()) {
            showAlert('يرجى تعبئة كافة الحقول المطلوبة بشكل صحيح', 'error');
            return;
        }

        const checkedCustodies = [];
        document.querySelectorAll('.custody-check:checked').forEach(cb => {
            checkedCustodies.push(cb.value);
        });

        const newStaff = {
            id: Date.now(),
            name: document.getElementById('staffName').value.trim(),
            idCard: document.getElementById('staffIdCard').value.trim(),
            title: document.getElementById('staffTitle').value.trim(),
            program: document.getElementById('staffProgram').value.trim(),
            custody: checkedCustodies,
            date: document.getElementById('custodyDate').value,
            notes: document.getElementById('staffNotes').value.trim()
        };

        staffList.push(newStaff);
        renderStaff();
        this.reset();
        document.getElementById('charCount').textContent = '0';
        showAlert('تم حفظ الموظف والعهدة الميدانية بنجاح ✓', 'success');
    });

    // تشغيل العرض الأولي عند تحميل الصفحة أول مرة
    window.addEventListener('DOMContentLoaded', () => {
        renderInventory();
        renderStaff();
    });
</script>
</body>
</html>
"""

# عرض المكون داخل واجهة Streamlit بأبعاد مناسبة للتصفح والدقة العالية
components.html(
    html_code,
    height=1200,
    scrolling=True
)
