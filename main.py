import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_full_original = """
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
        .box-info { background: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid var(--primary); font-size: 13px; }
    </style>
</head>
<body>
<div class="container">
    <!-- 1. TRANG ĐẦU TIÊN -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px">
            <h3>Xin chào đến với <br> Trường THPT Mù Cang Chải</h3>
        </div>
        <input type="text" id="u" placeholder="1. Tên tài khoản">
        <input type="password" id="p" placeholder="2. Mật khẩu">
        <input type="text" placeholder="3. Mã học sinh">
        <button onclick="handleLogin()">ĐĂNG NHẬP</button>
        <p style="text-align: center; font-size: 13px;">
            <span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Đăng ký tài khoản</span> | 
            <span onclick="goPage('forgotPage')" style="color:gray; cursor:pointer">9. Quên mật khẩu</span>
        </p>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select>
            <option>4. Chọn lớp...</option>
            <script>
                const blocks = ["10A", "11A", "12A"];
                blocks.forEach(b => {
                    let max = (b === "10A") ? 9 : 7;
                    for(let i=1; i<=max; i++) document.write(`<option>${b}${i}</option>`);
                });
            </script>
        </select>
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (bắc buộc)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <button onclick="handleReg()">10. XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH -->
    <div id="homeStudent" class="page">
        <h3 id="hiName" style="color:var(--primary)">Xin chào!</h3>
        <p>Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Chụp ảnh xung quanh lớp...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealHS')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leaveHS')"><i class="fa fa-file-alt"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedHS')"><i class="fa fa-comment-dots"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('boxHS')"><i class="fa fa-inbox"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('profileHS')"><i class="fa fa-user-circle"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="background:#eee"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="askAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- 4. TRANG BGH -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info"><strong>1. Sĩ số báo lại:</strong><br><div id="bghSiso"><i>Chờ báo cáo...</i></div></div>
        <textarea placeholder="2. Trả lời thắc mắc..."></textarea>
        <button onclick="alert('Gửi thành công!')">Gửi trả lời</button>
        <div class="box-info">3. Sự kiện:</div>
        <input type="text" placeholder="Ghi sự kiện...">
        <button onclick="alert('Đã gửi thông báo!')">Gửi</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 5. TRANG GIÁO VIÊN -->
    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">1. Nhận điểm danh lớp 12A3: Sùng A Chiều đã đi học (Hình ảnh) 6:30 9/4/2024</div>
        <p><strong>2. Thông báo cho lớp:</strong></p>
        <textarea placeholder="Nhập dữ liệu thông báo..."></textarea>
        <button onclick="alert('Đã gửi xong!')">Gửi thông báo</button>
        <input type="text" id="gvSisoInput" placeholder="Nhập sĩ số gửi BGH (VD: 12A3 47/47 đủ)">
        <button onclick="gvGuiBGH()" style="background:green">Gửi sĩ số lên BGH</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 6. TRANG BÁO CƠM ADMIN -->
    <div id="pageCom" class="page">
        <h3 style="color:#e67e22">HÃY LÀM VIỆC CẨN THẬN NHÉ BÁC SẠCH CƠM NGON</h3>
        <div class="box-info">1. Số lượng ăn hôm nay: Lớp 12A3 23 bạn báo làm 23 xuất</div>
        <p><strong>2. Thời gian ăn:</strong><br>Trưa: 11h45-12h30<br>Chiều: 16h20-17h30</p>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id === 'pageBGH') {
            const data = localStorage.getItem('siso_live');
            if(data) document.getElementById('bghSiso').innerText = data;
        }
    }
    function handleLogin() {
        const u = document.getElementById('u').value;
        const p = document.getElementById('p').value;
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else if(u==='Baocomngon' && p==='ankhongvanan') goPage('pageCom');
        else { 
            const stored = localStorage.getItem('u_'+u);
            if(stored && JSON.parse(stored).pass === p) {
                document.getElementById('hiName').innerText = "Xin chào " + JSON.parse(stored).name + "!";
                goPage('homeStudent');
            } else alert('Tài khoản không tồn tại!');
        }
    }
    function handleReg() {
        const u = document.getElementById('regU').value;
        const p = document.getElementById('regP').value;
        const n = document.getElementById('regName').value;
        localStorage.setItem('u_'+u, JSON.stringify({pass:p, name:n}));
        alert('Đăng ký thành công!'); goPage('loginPage');
    }
    function gvGuiBGH() {
        const val = document.getElementById('gvSisoInput').value;
        localStorage.setItem('siso_live', val);
        alert('Đã gửi!');
    }
    function askAI() { prompt("Bạn cần tôi giúp gì?"); alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_full_original, height=850, scrolling=True)
