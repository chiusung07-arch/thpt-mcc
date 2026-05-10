import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_final = """
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
        .data-box { background: #f0f7ff; padding: 10px; border-radius: 8px; border-left: 4px solid #2196f3; font-size: 13px; }
    </style>
</head>
<body>
<div class="container">
    <!-- 1. TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px">
            <h3>XIN CHÀO ĐẾN VỚI <br> TRƯỜNG THPT MÙ CANG CHẢI</h3>
        </div>
        <div style="padding: 10px 0;">
            <input type="text" id="u" placeholder="1. Tên tài khoản">
            <input type="password" id="p" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="checkLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px;">
                <span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Đăng ký tài khoản</span> | 
                <span onclick="goPage('forgotPage')" style="color:gray; cursor:pointer">9. Quên mật khẩu</span>
            </p>
        </div>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" placeholder="2. Tên tài khoản">
        <input type="text" placeholder="3. Họ và tên học sinh">
        <select>
            <option>4. Chọn lớp...</option>
            <script>
                for(let i=1;i<=9;i++) document.write(`<option>10A${i}</option>`);
                for(let i=1;i<=7;i++) document.write(`<option>11A${i}</option>`);
                for(let i=1;i<=7;i++) document.write(`<option>12A${i}</option>`);
            </script>
        </select>
        <input type="password" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (Bắt buộc khôi phục)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <button onclick="alert('Đăng ký thành công!'); goPage('loginPage')">10. XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH -->
    <div id="homeStudent" class="page">
        <h3 id="hiName" style="color:var(--primary); margin-bottom:0">Xin chào!</h3>
        <p style="font-size:13px; color:#666">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Mở Camera chụp lớp học...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealPage')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leavePage')"><i class="fa fa-paper-plane"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedbackPage')"><i class="fa fa-comment-dots"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('mailboxPage')"><i class="fa fa-envelope"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('profilePage')"><i class="fa fa-user-cog"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="background:#eee"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="askAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- 4. TRANG BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <h3 style="color:var(--primary)">QUẢN LÝ NHÀ TRƯỜNG</h3>
        <p><strong>1. Sĩ số báo cáo:</strong></p>
        <div id="bghData" class="data-box"><i>Chưa có báo cáo mới...</i></div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Trả lời thắc mắc học sinh..."></textarea>
        <button onclick="alert('Đã gửi phản hồi!')">GỬI VÀ XÁC NHẬN</button>
        <button style="background:#666; margin-top:20px" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- 5. TRANG GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <h3>Chào thầy Mr Quang một ngày tốt đẹp!</h3>
        <p><strong>1. Nhận điểm danh lớp 12A3:</strong></p>
        <div class="data-box" style="background:#f9f9f9">Sùng A Chiều - Đã đi học (Hình ảnh) lúc 6:30 9/4/2024</div>
        <p><strong>2. Gửi báo cáo sĩ số lên BGH:</strong></p>
        <input type="text" id="sisoInput" placeholder="Ví dụ: Mùa Hà Quang 12A3 47/47 đủ">
        <button onclick="gvGuiBGH()" style="background:#2e7d32">GỬI BÁO CÁO</button>
        <button style="background:#666; margin-top:20px" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- 6. TRANG BÁO CƠM -->
    <div id="pageCom" class="page">
        <h3 style="color:#e67e22">Hãy làm việc cẩn thận nhé bác sạch cơm ngon!</h3>
        <div class="data-box"><strong>1. Số lượng ăn:</strong> Lớp 12A3 23 bạn đã báo làm 23 xuất</div>
        <p><strong>2. Thời gian ăn:</strong><br>- Trưa: 11h45-12h30<br>- Chiều: 16h20-17h30</p>
        <button style="background:#666; margin-top:20px" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id === 'pageBGH') {
            const d = localStorage.getItem('siso_live');
            if(d) document.getElementById('bghData').innerHTML = d;
        }
    }
    function checkLogin() {
        const user = document.getElementById('u').value;
        const pass = document.getElementById('p').value;
        if(user==='BGH THPTMCC2025' && pass==='THPT1983@') goPage('pageBGH');
        else if(user==='muahaquangdz' && pass==='Mrquang@123') goPage('pageGV');
        else if(user==='Baocomngon' && pass==='ankhongvanan') goPage('pageCom');
        else { document.getElementById('hiName').innerText = "Xin chào " + (user||"Học sinh") + "!"; goPage('homeStudent'); }
    }
    function gvGuiBGH() {
        const val = document.getElementById('sisoInput').value;
        if(!val) return alert('Vui lòng nhập sĩ số!');
        localStorage.setItem('siso_live', val + " <br><small>Cập nhật: " + new Date().toLocaleTimeString() + "</small>");
        alert('Đã gửi báo cáo thành công!');
    }
    function askAI() { prompt("Bạn cần trợ lý giúp gì?"); alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_final, height=850, scrolling=True)
