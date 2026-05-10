import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải - Pro", layout="centered")

html_perfect_pro = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f0f2f5; --accent: #ffd700; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 30px rgba(0,0,0,0.1); overflow: hidden; }
        
        /* Hiệu ứng chuyển trang mượt mà */
        .page { display: none; padding: 20px; animation: slideIn 0.4s ease-out; }
        .active { display: block; }
        @keyframes slideIn { from { transform: translateX(50px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

        /* Header phong cách vùng cao */
        .header-main { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://vnecdn.net');
            background-size: cover; padding: 40px 20px; color: white; border-radius: 0 0 25px 25px;
        }
        
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 10px; border: 1px solid #ddd; box-sizing: border-box; transition: 0.3s; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; box-shadow: 0 4px 6px rgba(211, 47, 47, 0.2); }
        button:active { transform: scale(0.98); }

        /* Menu Grid 8 mục */
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; }
        .menu-item { background: #fff; padding: 18px; border-radius: 15px; text-align: center; border: 1px solid #eee; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .menu-item i { font-size: 24px; color: var(--primary); margin-bottom: 8px; }
        .menu-item:hover { background: #fff5f5; border-color: var(--primary); }

        /* Robot Trợ Lý Bay Lơ Lửng */
        .robot-box { position: fixed; bottom: 25px; right: 20px; text-align: center; cursor: pointer; z-index: 1000; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 6px 12px; border-radius: 20px; font-size: 11px; margin-bottom: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); font-weight: bold; }
        .robot-img { width: 70px; animation: float 3s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }

        /* Camera Scan ảo */
        #cameraOverlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: none; align-items: center; justify-content: center; color: white; flex-direction: column; }
        .scan-line { width: 250px; height: 2px; background: #00ff00; position: absolute; animation: scan 2s linear infinite; box-shadow: 0 0 15px #00ff00; }
        @keyframes scan { 0% { top: 30%; } 100% { top: 70%; } }

        .box-info { background: #f8f9fa; padding: 12px; border-radius: 10px; margin: 10px 0; border-left: 5px solid var(--primary); font-size: 13px; line-height: 1.5; }
    </style>
</head>
<body>
<div class="container">

    <!-- CAMERA SCAN ẢO -->
    <div id="cameraOverlay" onclick="this.style.display='none'">
        <div style="border: 2px solid #00ff00; width: 250px; height: 350px; position: relative;">
            <div class="scan-line"></div>
        </div>
        <p style="margin-top:20px; font-weight:bold;">ĐANG QUÉT LỚP HỌC...</p>
        <p style="font-size:12px;">Bấm vào đây để hoàn tất</p>
    </div>

    <!-- 1. TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-main">
            <img src="https://wikimedia.org" style="width:45px; margin-bottom:10px; border: 1px solid white;">
            <h2 style="margin:0; letter-spacing: 1px;">XIN CHÀO ĐẾN VỚI <br> TRƯỜNG THPT MÙ CANG CHẢI</h2>
        </div>
        <div style="padding: 20px;">
            <input type="text" id="u" placeholder="1. Tên tài khoản">
            <input type="password" id="p" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="handleLogin()">ĐĂNG NHẬP HỆ THỐNG</button>
            <p style="text-align: center; font-size: 13px; margin-top: 15px;">
                Chưa có tài khoản? <span onclick="goPage('regPage')" style="color:var(--primary); cursor:pointer; font-weight:bold;">4. Đăng ký ngay</span>
            </p>
        </div>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ (10 MỤC) -->
    <div id="regPage" class="page">
        <h3 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h3>
        <input type="text" id="regU" placeholder="2 Tên tài khoản">
        <input type="text" id="regName" placeholder="3 Họ và tên học sinh">
        <select>
            <option>4 Chọn lớp...</option>
            <script>
                const blocks = ["10A", "11A", "12A"];
                blocks.forEach(b => { let max = (b === "10A") ? 9 : 7; for(let i=1; i<=max; i++) document.write(`<option>${b}${i}</option>`); });
            </script>
        </select>
        <input type="password" id="regP" placeholder="5 Mật khẩu">
        <input type="email" placeholder="6 Email (Bắc buộc khôi phục)">
        <input type="tel" placeholder="7 Số điện thoại">
        <select><option>8 Học sinh bán trú</option><option>8 Học sinh ngoại trú</option></select>
        <p style="color:gray; font-size:12px; cursor:pointer" onclick="goPage('forgotPage')">9 Ô quên mật khẩu</p>
        <button onclick="handleReg()">10 XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH (8 MỤC) -->
    <div id="homeHS" class="page">
        <div style="display:flex; justify-content: space-between; align-items: flex-start; background: #fff5f5; padding: 15px; border-radius: 15px;">
            <div>
                <h3 id="hiHS" style="color:var(--primary); margin:0">Xin chào!</h3>
                <p style="font-size:12px; margin:5px 0 0 0;">Chúc bạn một ngày vui vẻ!</p>
            </div>
            <div onclick="goPage('profilePage')" style="text-align:right; cursor:pointer">
                <i class="fa fa-user-circle" style="font-size:28px; color:var(--primary)"></i><br><small>Tài khoản</small>
            </div>
        </div>
        
        <div class="menu-grid">
            <div class="menu-item" onclick="document.getElementById('cameraOverlay').style.display='flex'"><i class="fa fa-camera"></i><br>1 Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealPage')"><i class="fa fa-utensils"></i><br>2 Báo cơm</div>
            <div class="menu-item" onclick="goPage('leavePage')"><i class="fa fa-notes-medical"></i><br>3 Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedPage')"><i class="fa fa-bullhorn"></i><br>4 Phản hồi</div>
            <div class="menu-item" onclick="goPage('boxPage')"><i class="fa fa-inbox"></i><br>5 Hòm thư</div>
            <div class="menu-item" onclick="alert('Mở Góc học tập...')"><i class="fa fa-book-reader"></i><br>6 Góc học tập</div>
            <div class="menu-item" style="grid-column: span 2; background:#333; color:white;" onclick="location.reload()"><i class="fa fa-sign-out-alt"></i> Đăng xuất</div>
        </div>

        <div class="robot-box" onclick="talkAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- CÁC TRANG QUẢN LÝ (Giữ nguyên logic của bạn) -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG</h3>
        <div class="box-info"><strong>1 Sĩ số báo lại:</strong><br><div id="bghData"><i>(Đang đợi giáo viên...)</i></div></div>
        <textarea placeholder="2 Trả lời thắc mắc..."></textarea>
        <button onclick="alert('Đã gửi!')">Gửi trả lời</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG</h3>
        <div class="box-info">1 Nhận điểm danh lớp 12A3: Sùng A Chiều...</div>
        <input type="text" id="gvIn" placeholder="Nhập sĩ số gửi BGH...">
        <button onclick="gvGui()">Gửi báo cáo</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <div id="pageBC" class="page">
        <h3 style="color:#e67e22">BÁC SẠCH CƠM NGON</h3>
        <div class="box-info">Lớp 12A3 23 bạn báo suất cơm.</div>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id==='pageBGH'){
            const d = localStorage.getItem('siso_live');
            if(d) document.getElementById('bghData').innerText = d;
        }
    }
    function handleLogin() {
        const u = document.getElementById('u').value;
        const p = document.getElementById('p').value;
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else if(u==='Baocomngon' && p==='ankhongvanan') goPage('pageBC');
        else {
            const s = localStorage.getItem('user_'+u);
            if(s && JSON.parse(s).pass === p) {
                document.getElementById('hiHS').innerText = "Xin chào " + JSON.parse(s).name + "!";
                goPage('homeHS');
            } else alert('Vui lòng Đăng ký trước!');
        }
    }
    function handleReg() {
        const u = document.getElementById('regU').value;
        const n = document.getElementById('regName').value;
        const p = document.getElementById('regP').value;
        if(u && p) {
            localStorage.setItem('user_'+u, JSON.stringify({pass:p, name:n}));
            alert('Đăng ký thành công!'); goPage('loginPage');
        }
    }
    function gvGui() {
        localStorage.setItem('siso_live', document.getElementById('gvIn').value);
        alert('Đã gửi!');
    }
    function talkAI() {
        const q = prompt("Bạn cần Robot giúp gì?");
        if(q) alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_perfect_pro, height=850, scrolling=True)
