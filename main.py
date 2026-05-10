import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f5f5f5; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        .page { display: none; padding: 15px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .header-main { text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); background-size: cover; padding: 30px 20px; color: white; border-radius: 0 0 20px 20px; }
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; }
        .robot-img { width: 60px; }
        .box-info { background: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid var(--primary); font-size: 13px; }
    </style>
</head>
<body>
<div class="container">

    <!-- 1. TRANG ĐẦU TIÊN -->
    <div id="loginPage" class="page active">
        <div class="header-main">
            <img src="https://wikimedia.org" style="width:40px; margin-bottom:10px">
            <h2 style="margin:0">Xin chào đến với <br> Trường THPT Mù Cang Chải</h2>
        </div>
        <div style="padding: 20px 0;">
            <input type="text" id="u" placeholder="1. Tên tài khoản">
            <input type="password" id="p" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="handleLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px;">
                <span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Đăng ký tài khoản</span> | 
                <span onclick="goPage('forgotPage')" style="color:gray; cursor:pointer">9. Quên mật khẩu</span>
            </p>
        </div>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ (Đầy đủ 10 mục) -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select>
            <option>4. Chọn lớp...</option>
            <script>
                for(let i=1;i<=9;i++) document.write(`<option>10A${i}</option>`);
                for(let i=1;i<=7;i++) document.write(`<option>11A${i}</option>`);
                for(let i=1;i<=7;i++) document.write(`<option>12A${i}</option>`);
            </script>
        </select>
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (Bắt buộc khôi phục)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <button onclick="handleReg()">10. XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- 3. TRANG BGH -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info">
            <strong>1. Sĩ số báo lại:</strong><br>
            <div id="bghDataDisplay"><i>(Đang chờ giáo viên báo cáo sĩ số...)</i></div>
        </div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Trả lời thắc mắc..."></textarea>
        <button onclick="alert('Đã gửi thành công!')">Gửi trả lời</button>
        <div class="box-info">3. Sự kiện gửi thông báo:</div>
        <input type="text" placeholder="Ghi sự kiện...">
        <button onclick="alert('Đã gửi thông báo!')">Gửi sự kiện</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 4. TRANG GIÁO VIÊN -->
    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">1. Nhận điểm danh lớp 12A3: Sùng A Chiều đã đi học (Hình ảnh) 6:30 9/4/2024</div>
        <p><strong>2. Gửi báo cáo sĩ số lên BGH:</strong></p>
        <input type="text" id="gvSiso" placeholder="Nhập: Mùa Hà Quang 12A3 47/47 đủ">
        <button onclick="gvGui()">Gửi báo cáo</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 5. TRANG HỌC SINH -->
    <div id="homeHS" class="page">
        <h3 id="hiHS">Xin chào!</h3>
        <p>Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Chụp ảnh điểm danh...')">1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealHS')">2. Báo cơm</div>
            <div class="menu-item">3. Xin nghỉ</div>
            <div class="menu-item">4. Phản hồi</div>
            <div class="menu-item">5. Hòm thư</div>
            <div class="menu-item" onclick="location.reload()">Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="talkAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id === 'pageBGH') {
            const d = localStorage.getItem('siso_live');
            if(d) document.getElementById('bghDataDisplay').innerText = d;
        }
    }
    function gvGui() {
        const val = document.getElementById('gvSiso').value;
        if(val) { localStorage.setItem('siso_live', val); alert('Đã gửi!'); }
    }
    function handleLogin() {
        const u = document.getElementById('u').value;
        const p = document.getElementById('p').value;
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else { document.getElementById('hiHS').innerText = "Xin chào " + (u||"Bạn"); goPage('homeHS'); }
    }
    function handleReg() { alert('Đăng ký thành công!'); goPage('loginPage'); }
    function talkAI() { prompt("Bạn cần gì?"); alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
