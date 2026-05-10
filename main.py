import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_final_auth = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f5f5f5; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); color: #333; }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .page { display: none; padding: 20px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .header-school { text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); background-size: cover; padding: 30px 20px; color: white; }
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; font-size: 14px; }
        .menu-item i { font-size: 20px; color: var(--primary); margin-bottom: 5px; }
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 99; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; }
        .robot-img { width: 60px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    </style>
</head>
<body>
<div class="container">
    <!-- TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px">
            <h3>XIN CHÀO ĐẾN VỚI <br> TRƯỜNG THPT MÙ CANG CHẢI</h3>
        </div>
        <div style="padding: 20px 0;">
            <input type="text" id="loginUser" placeholder="Tên tài khoản">
            <input type="password" id="loginPass" placeholder="Mật khẩu">
            <button onclick="handleLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px; margin-top:15px;">
                Chưa có tài khoản? <span onclick="goPage('regPage')" style="color:blue; cursor:pointer; font-weight:bold;">Đăng ký ngay</span>
            </p>
        </div>
    </div>

    <!-- TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">ĐĂNG KÝ TÀI KHOẢN MỚI</h4>
        <p style="font-size:12px; text-align:center;">Bạn phải là học sinh trường THPT Mù Cang Chải</p>
        <input type="text" id="regUser" placeholder="Tên tài khoản (để đăng nhập)">
        <input type="text" id="regFullName" placeholder="Họ và tên học sinh">
        <select id="regClass">
            <option value="">Chọn lớp học...</option>
            <script>
                const blocks = ["10A", "11A", "12A"];
                blocks.forEach(b => {
                    let max = (b === "10A") ? 9 : 7;
                    for(let i=1; i<=max; i++) document.write(`<option>${b}${i}</option>`);
                });
            </script>
        </select>
        <input type="password" id="regPass" placeholder="Mật khẩu">
        <input type="email" id="regEmail" placeholder="Email (Bắt buộc khôi phục)">
        <input type="tel" placeholder="Số điện thoại">
        <select><option>Học sinh bán trú</option><option>Học sinh ngoại trú</option></select>
        <button onclick="handleRegister()">XÁC NHẬN ĐĂNG KÝ</button>
        <button style="background:#666" onclick="goPage('loginPage')">Quay lại</button>
    </div>

    <!-- TRANG CHỦ HỌC SINH -->
    <div id="homeStudent" class="page">
        <h3 id="hiName" style="color:var(--primary); margin-bottom:0">Xin chào!</h3>
        <p style="font-size:13px; color:#666">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Mở Camera điểm danh...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item"><i class="fa fa-paper-plane"></i><br>3. Xin nghỉ</div>
            <div class="menu-item"><i class="fa fa-comment-dots"></i><br>4. Phản hồi</div>
            <div class="menu-item"><i class="fa fa-envelope"></i><br>5. Hòm thư</div>
            <div class="menu-item"><i class="fa fa-user-cog"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="grid-column: span 2; background:#eee"><i class="fa fa-sign-out-alt"></i> Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="askAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- CÁC TRANG ADMIN GIỮ NGUYÊN NHƯ Ý TƯỞNG CŨ -->
    <div id="pageBGH" class="page"><h3>BGH - QUẢN LÝ NHÀ TRƯỜNG</h3><button onclick="location.reload()">Đăng xuất</button></div>
    <div id="pageGV" class="page"><h3>Chào thầy Mr Quang!</h3><button onclick="location.reload()">Đăng xuất</button></div>
    <div id="pageCom" class="page"><h3>Bác sạch cơm ngon!</h3><button onclick="location.reload()">Đăng xuất</button></div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }

    // XỬ LÝ ĐĂNG KÝ
    function handleRegister() {
        const user = document.getElementById('regUser').value;
        const name = document.getElementById('regFullName').value;
        const pass = document.getElementById('regPass').value;
        const mail = document.getElementById('regEmail').value;

        if(!user || !pass || !name || !mail) return alert('Vui lòng nhập đầy đủ thông tin bắt buộc!');

        // Lưu thông tin vào localStorage (giả lập database)
        const userData = { username: user, password: pass, fullName: name };
        localStorage.setItem('user_' + user, JSON.stringify(userData));

        alert('Đăng ký thành công! Hãy dùng tài khoản này để đăng nhập.');
        goPage('loginPage');
    }

    // XỬ LÝ ĐĂNG NHẬP
    function handleLogin() {
        const user = document.getElementById('loginUser').value;
        const pass = document.getElementById('loginPass').value;

        // 1. Kiểm tra 3 tài khoản Admin cố định
        if(user==='BGH THPTMCC2025' && pass==='THPT1983@') return goPage('pageBGH');
        if(user==='muahaquangdz' && pass==='Mrquang@123') return goPage('pageGV');
        if(user==='Baocomngon' && pass==='ankhongvanan') return goPage('pageCom');

        // 2. Kiểm tra tài khoản học sinh đã đăng ký
        const storedUser = localStorage.getItem('user_' + user);
        if(storedUser) {
            const data = JSON.parse(storedUser);
            if(data.password === pass) {
                document.getElementById('hiName').innerText = "Xin chào " + data.fullName + "!";
                return goPage('homeStudent');
            }
        }

        alert('Tài khoản hoặc mật khẩu không chính xác. Vui lòng đăng ký nếu chưa có tài khoản!');
    }

    function askAI() { prompt("Bạn cần trợ lý giúp gì?"); alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_final_auth, height=850, scrolling=True)
