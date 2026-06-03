<style>
:root{
    --primary:#2563eb;
    --primary-hover:#1d4ed8;
    --primary-light:rgba(37,99,235,.1);

    --bg-main:#f8fafc;
    --bg-card:#ffffff;

    --text-main:#0f172a;
    --text-muted:#64748b;

    --border:#e2e8f0;

    --success:#10b981;
    --warning:#f59e0b;
    --danger:#ef4444;

    --danger-light:#fee2e2;
    --success-light:#ecfdf5;
    --info-light:#e0f2fe;

    --shadow:0 4px 6px -1px rgba(0,0,0,.05),
              0 2px 4px -1px rgba(0,0,0,.02);
}

/* Reset */

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Cairo',sans-serif;
}

html{
    scroll-behavior:smooth;
}

body{
    background:var(--bg-main);
    color:var(--text-main);
    line-height:1.6;
    padding:2rem 1rem;
}

.container{
    max-width:1300px;
    margin:auto;
}

/* Header */

header{
    text-align:center;
    margin-bottom:2rem;
}

header h1{
    color:var(--primary);
    font-size:2.2rem;
    margin-bottom:.5rem;
}

header p{
    color:var(--text-muted);
}

/* Tabs */

.tabs{
    display:flex;
    gap:1rem;
    flex-wrap:wrap;
    margin-bottom:2rem;
    border-bottom:2px solid var(--border);
}

.tab-btn{
    border:none;
    background:none;
    cursor:pointer;
    padding:1rem 1.5rem;
    font-size:1rem;
    color:var(--text-muted);
    border-radius:10px 10px 0 0;
    transition:.3s;
}

.tab-btn:hover{
    background:var(--primary-light);
    color:var(--primary);
}

.tab-btn.active{
    background:var(--primary-light);
    color:var(--primary);
    border-bottom:3px solid var(--primary);
}

/* Grid */

.grid{
    display:grid;
    grid-template-columns:1fr 2fr;
    gap:2rem;
}

@media(max-width:1024px){

.grid{
    grid-template-columns:1fr;
}

}

/* Cards */

.card{
    background:var(--bg-card);
    border-radius:16px;
    padding:1.5rem;
    border:1px solid var(--border);
    box-shadow:var(--shadow);
}

.card h2{
    margin-bottom:1.5rem;
    border-right:4px solid var(--primary);
    padding-right:.7rem;
}

/* Forms */

.form-group{
    margin-bottom:1.2rem;
}

.form-group label{
    display:block;
    margin-bottom:.5rem;
    font-weight:600;
}

.form-control{
    width:100%;
    padding:.8rem;
    border-radius:8px;
    border:1px solid var(--border);
    background:#f1f5f9;
    transition:.3s;
}

.form-control:focus{
    outline:none;
    border-color:var(--primary);
    background:white;
    box-shadow:0 0 0 3px var(--primary-light);
}

.form-control.error{
    border-color:var(--danger);
    background:var(--danger-light);
}

/* Checkbox */

.checkbox-group{
    display:flex;
    flex-direction:column;
    gap:.5rem;
    padding:1rem;
    border-radius:8px;
    background:#f1f5f9;
}

.checkbox-group label{
    display:flex;
    align-items:center;
    gap:.5rem;
}

/* Buttons */

.btn{
    width:100%;
    border:none;
    border-radius:8px;
    padding:.9rem;
    cursor:pointer;
    background:var(--primary);
    color:white;
    font-size:.95rem;
    font-weight:600;
    transition:.3s;
}

.btn:hover{
    background:var(--primary-hover);
    transform:translateY(-2px);
}

.btn-small{
    width:auto;
    padding:.5rem 1rem;
}

.btn-secondary{
    background:var(--text-muted);
}

.btn-success{
    background:var(--success);
}

/* Tables */

.table-container{
    overflow-x:auto;
}

table{
    width:100%;
    border-collapse:collapse;
}

th{
    background:#f1f5f9;
    padding:1rem;
    text-align:right;
}

td{
    padding:1rem;
    border-bottom:1px solid var(--border);
}

tr:hover td{
    background:#f8fafc;
}

/* Badges */

.badge{
    display:inline-block;
    padding:.3rem .7rem;
    border-radius:20px;
    font-size:.8rem;
}

.badge-program{
    background:var(--info-light);
}

.badge-qty{
    background:var(--success-light);
}

.badge-out{
    background:var(--danger-light);
}

.badge-warning{
    background:#fef3c7;
}

/* Alerts */

.alert{
    padding:1rem;
    border-radius:8px;
    margin-bottom:1rem;
}

.alert-success{
    background:var(--success-light);
}

.alert-error{
    background:var(--danger-light);
}

.alert-info{
    background:var(--info-light);
}

/* Mobile */

@media(max-width:768px){

body{
    padding:1rem;
}

header h1{
    font-size:1.7rem;
}

.card{
    padding:1rem;
}

.tab-btn{
    width:100%;
}

}

</style>
