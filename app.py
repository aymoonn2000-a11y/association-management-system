import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="نظام إدارة الجمعية الذكي",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

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
    --danger:#ef4444;
    --warning:#f59e0b;

    --danger-light:#fee2e2;
    --success-light:#ecfdf5;

    --shadow:0 4px 6px -1px rgba(0,0,0,.05),
              0 2px 4px -1px rgba(0,0,0,.02);
}

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Cairo,sans-serif;
}

body{
background:var(--bg-main);
padding:30px;
}

.container{
max-width:1200px;
margin:auto;
}

.card{
background:white;
padding:20px;
border-radius:16px;
box-shadow:var(--shadow);
margin-bottom:20px;
}

h1{
color:var(--primary);
margin-bottom:20px;
text-align:center;
}

h2{
margin-bottom:15px;
border-right:4px solid var(--primary);
padding-right:10px;
}

.form-control{
width:100%;
padding:12px;
margin-bottom:15px;
border:1px solid var(--border);
border-radius:10px;
}

button{
background:var(--primary);
color:white;
border:none;
padding:12px 20px;
border-radius:10px;
cursor:pointer;
width:100%;
font-size:16px;
}

button:hover{
background:var(--primary-hover);
}

table{
width:100%;
border-collapse:collapse;
margin-top:20px;
}

th,td{
padding:12px;
border-bottom:1px solid #ddd;
text-align:right;
}

th{
background:#f1f5f9;
}

</style>

</head>

<body>

<div class="container">

<h1>
نظام الإدارة الداخلي للجمعية
</h1>

<div class="card">

<h2>إدارة المخزون</h2>

<select class="form-control" id="item">
<option>شاي</option>
<option>قهوة</option>
<option>منظفات</option>
<option>قرطاسية</option>
</select>

<input
class="form-control"
type="number"
id="qty"
placeholder="أدخل الكمية">

<button onclick="addItem()">
إضافة للمخزون
</button>

<table>

<thead>

<tr>
<th>المادة</th>
<th>الكمية</th>
</tr>

</thead>

<tbody id="inventory">

</tbody>

</table>

</div>

</div>

<script>

let data=[];

function addItem(){

let item=
document.getElementById("item").value;

let qty=
document.getElementById("qty").value;

if(qty==""){
alert("أدخل الكمية");
return;
}

data.push({
item:item,
qty:qty
});

render();

document.getElementById(
"qty"
).value="";

}

function render(){

let tbody=
document.getElementById(
"inventory"
);

tbody.innerHTML="";

data.forEach(row=>{

tbody.innerHTML+=`

<tr>

<td>${row.item}</td>

<td>${row.qty}</td>

</tr>

`;

});

}

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=900,
    scrolling=True
)
