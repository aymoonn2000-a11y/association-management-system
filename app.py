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

    --shadow:
        0 4px 6px -1px rgba(0,0,0,.05),
        0 2px 4px -1px rgba(0,0,0,.02);
}

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
    font-size:2rem;
    margin-bottom:.5rem;
}

header p{
    color:var(--text-muted);
}

/* Tabs */

.tabs{
    display:flex;
    gap:1rem;
    margin-bottom:2rem;
    border-bottom:2px solid var(--border);
    overflow-x:auto;
}

.tab-btn{
    border:none;
    background:none;
    padding:1rem;
    cursor:pointer;
    color:var(--text-muted);
    font-weight:600;
    transition:.3s;
}

.tab-btn:hover{
    color:var(--primary);
}

.tab-btn.active{
    color:var(--primary);
    border-bottom:3px solid var(--primary);
}

/* Grid */

.grid{
    display:grid;
    grid-template-columns:1fr 2fr;
    gap:2rem;
}

@media(max-width:992px){
    .grid{
        grid-template-columns:1fr;
    }
}

/* Cards */

.card{
    background:var(--bg-card);
    border-radius:16px;
    padding:1.5rem;
    box-shadow:var(--shadow);
    border:1px solid var(--border);
}

.card h2{
    margin-bottom:1rem;
    border-right:4px solid var(--primary);
    padding-right:10px;
}

/* Forms */

.form-group{
    margin-bottom:1rem;
}

.form-group label{
    display:block;
    margin-bottom:.5rem;
    font-weight:600;
}

.form-control{
    width:100%;
    padding:.8rem;
    border:1px solid var(--border);
    border-radius:8px;
    background:#f1f5f9;
    transition:.3s;
}

.form-control:focus{
    outline:none;
    border-color:var(--primary);
    background:white;
    box-shadow:0 0 0 3px rgba(37,99,235,.15);
}

.form-control.error{
    border-color:var(--danger);
}

/* Buttons */

.btn{
    width:100%;
    border:none;
    background:var(--primary);
    color:white;
    padding:.9rem;
    border-radius:8px;
    cursor:pointer;
    transition:.3s;
    font-weight:600;
}

.btn:hover{
    background:var(--primary-hover);
}

.btn-small{
    width:auto;
    padding:.5rem .8rem;
}

.btn-secondary{
    background:var(--text-muted);
}

/* Tables */

.table-container{
    overflow:auto;
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

tr:hover{
    background:#f8fafc;
}

/* Badges */

.badge{
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

/* Responsive */

@media(max-width:768px){

body{
    padding:1rem;
}

header h1{
    font-size:1.6rem;
}

.card{
    padding:1rem;
}

table{
    font-size:.85rem;
}

th,
td{
    padding:.7rem;
}

.btn{
    font-size:.9rem;
}

}

</style>
