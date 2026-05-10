import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f4f4f4; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .page { display: none; padding: 20px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .header-school { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net');
            background-size: cover; padding: 30px 20px; color: white; border-radius: 0 0 20px 20px;
        }
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .box-info { background: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid var(--primary); font-size: 13px; }
        
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .menu-item i { font-size: 20px; color: var(--primary); margin-bottom: 5px; }

        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 100; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .robot-img { width: 60px; animation: float 3s infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    </style>
</head>
<body>
<div class="container">

    <!-- 1. TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px; margin-bottom:5px">
            <h3 style="margin:0">Xin chào đến với <br> Trường THPT Mù Cang Chải</h3>
        </div>
        <div style="padding: 10px 0;">
            <input type="text" id="userIn" placeholder="1. Tên tài khoản">
            <input type="password" id="passIn" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="handleLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px; margin-top: 15px;">
                <span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Mục đăng ký tài khoản</span>
            </p>
        </div>
    </div>

    <!-- TRANG 1: BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info"><strong>1. Sĩ số báo lại:</strong><br><div id="bghData"><i>(Đang chờ báo cáo...)</i></div></div>
        <textarea placeholder="2. Trả lời thắc mắc..."></textarea>
        <button onclick="alert('Đã gửi phản hồi thành công!')">Ô gửi</button>
        <div class="box-info">3. Sự kiện:</div>
        <input type="text" placeholder="Ô ghi sự kiện...">
        <button onclick="alert('Đã gửi thông báo!')">Gửi</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- TRANG 2: GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">1. Nhận điểm danh lớp 12A3: Sùng A Chiều đã đi học (Hình ảnh) 6:30 9/4/2024</div>
        <p><strong>2. Thông báo cho lớp:</strong></p>
        <textarea placeholder="Ô nhập dữ liệu gửi..."></textarea>
        <button onclick="alert('Đã gửi xong!')">Gửi</button>
        <p><strong>Báo cáo sĩ số lên BGH:</strong></p>
        <input type="text" id="gvSiso" placeholder="Nhập: Mùa Hà Quang 12A3 47/47 đủ">
        <button onclick="gvGuiBGH()" style="background:green">GỬI SĨ SỐ</button>
        <button onclick="location.reload()" style="background:#666; margin-top:20px">Đăng xuất</button>
    </div>

    <!-- TRANG 3: QUẢN LÝ BÁO CƠM -->
    <div id="pageBC" class="page">
        <h3 style="color:#e67e22">HÃY LÀM VIỆC CẨN THẬN NHÉ BÁC SẠCH CƠM NGON</h3>
        <div class="box-info">1. Số lượng ăn hôm nay: Lớp 12A3 23 bạn đã báo làm 23 xuất</div>
        <p><strong>2. Thời gian ăn:</strong><br>Trưa: 11h45-12h30<br>Chiều: 16h20-17h30</p>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- TRANG CHỦ HỌC SINH -->
    <div id="homeHS" class="page">
        <h3 id="hiHS" style="color:var(--primary); margin:0">Xin chào!</h3>
        <p style="font-size:13px">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Chụp ảnh xung quanh lớp...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item"><i class="fa fa-file-alt"></i><br>3. Xin nghỉ</div>
            <div class="menu-item"><i class="fa fa-comment-dots"></i><br>4. Phản hồi</div>
            <div class="menu-item"><i class="fa fa-envelope"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('profHS')"><i class="fa fa-user-circle"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="grid-column: span 2; background:#eee"><i class="fa fa-sign-out-alt"></i> Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="talkAI()"><div class="robot-bubble">Bạn cần tôi giúp gì không?</div><img src="https://flaticon.com" class="robot-img"></div>
    </div>

    <!-- TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="text-align:center; color:var(--primary)">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regN" placeholder="3. Họ tên">
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <button onclick="handleReg()">XÁC NHẬN ĐĂNG KÝ</button>
        <button onclick="goPage('loginPage')" style="background:#666">Quay lại</button>
    </div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id==='pageBGH'){
            const d = localStorage.getItem('siso_tu_gv');
            if(d) document.getElementById('bghData').innerText = d;
        }
    }

    function handleLogin() {
        const u = document.getElementById('userIn').value;
        const p = document.getElementById('passIn').value;

        // KIỂM TRA CHÍNH XÁC 3 TÀI KHOẢN ADMIN NHƯ BẠN YÊU CẦU
        if(u === 'BGH THPTMCC2025' && p === 'THPT1983@') {
            goPage('pageBGH');
        } 
        else if(u === 'muahaquangdz' && p === 'Mrquang@123') {
            goPage('pageGV');
        } 
        else if(u === 'Baocomngon' && p === 'ankhongvanan') {
            goPage('pageBC');
        } 
        else {
            // Kiểm tra tài khoản học sinh đã đăng ký
            const stored = localStorage.getItem('user_'+u);
            if(stored && JSON.parse(stored).pass === p) {
                document.getElementById('hiHS').innerText = "Xin chào " + JSON.parse(stored).name + "!";
                goPage('homeHS');
            } else {
                alert('Sai tài khoản hoặc mật khẩu!');
            }
        }
    }

    function handleReg() {
        const u = document.getElementById('regU').value;
        const n = document.getElementById('regN').value;
        const p = document.getElementById('regP').value;
        if(u && p) {
            localStorage.setItem('user_'+u, JSON.stringify({pass: p, name: n}));
            alert('Đăng ký thành công!');
            goPage('loginPage');
        }
    }

    function gvGuiBGH() {
        localStorage.setItem('siso_tu_gv', document.getElementById('gvSiso').value);
        alert('Đã gửi báo cáo lên BGH!');
    }

    function talkAI() {
        const q = prompt("Bạn cần tôi giúp gì?");
        if(q) alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
