import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_full_system = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --success: #2e7d32; --bg: #f5f5f5; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .page { display: none; padding: 20px; animation: fadeIn 0.4s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        /* Header */
        .header-school { text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); background-size: cover; padding: 30px 20px; color: white; }
        .flag { width: 45px; margin-bottom: 5px; }

        input, select, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        .admin-tag { background: #333; color: gold; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-bottom: 10px; display: inline-block; }
        
        /* Menu Grid */
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .menu-item i { font-size: 22px; color: var(--primary); margin-bottom: 5px; }

        /* Robot */
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 99; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .robot-img { width: 60px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    </style>
</head>
<body>

<div class="container">
    <!-- TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" class="flag">
            <h3 style="margin:0">XIN CHÀO ĐẾN VỚI <br> TRƯỜNG THPT MÙ CANG CHẢI</h3>
        </div>
        <div style="padding: 20px 0;">
            <input type="text" id="user" placeholder="Tên tài khoản">
            <input type="password" id="pass" placeholder="Mật khẩu">
            <input type="text" placeholder="Mã học sinh (Nếu là HS)">
            <button onclick="checkLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px; color: #666; margin-top: 15px;">
                <span onclick="goPage('regPage')" style="color:var(--primary); cursor:pointer">Đăng ký tài khoản</span>
            </p>
        </div>
    </div>

    <!-- TRANG 1: BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <span class="admin-tag">QUẢN TRỊ VIÊN</span>
        <h3 style="margin-top:0">QUẢN LÝ NHÀ TRƯỜNG</h3>
        <div style="background:#f0f7ff; padding:15px; border-radius:10px; margin-bottom:15px; font-size:14px;">
            <strong>1. Sĩ số hôm nay:</strong><br>
            - Mùa Hà Quang 12A3: 47/47 (Đủ)<br>
            - Giàng A Páo 10A1: 44/45 (Vắng 1)
        </div>
        <p><strong>2. Trả lời phản ánh:</strong></p>
        <textarea placeholder="Nhập lời giải đáp..."></textarea>
        <button onclick="alert('Đã gửi phản hồi thành công!')">GỬI VÀ XÁC NHẬN</button>
        <button style="background:#666" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- TRANG 2: GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <span class="admin-tag">GIÁO VIÊN CHỦ NHIỆM</span>
        <h3 style="margin-top:0">Chào thầy Mr Quang, chúc ngày tốt đẹp!</h3>
        <div style="background:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:15px;">
            <strong>1. Nhận điểm danh lớp 12A3:</strong><br>
            <p style="font-size:13px; color:#555">- Sùng A Chiều: Đã đi học (Hình ảnh) <br> <small>Lúc 6:30 - 9/4/2024</small></p>
        </div>
        <p><strong>2. Thông báo đến lớp:</strong></p>
        <textarea placeholder="Nhập nội dung thông báo..."></textarea>
        <button onclick="alert('Đã gửi thông báo đến lớp!')">GỬI THÔNG BÁO</button>
        <button style="background:#666" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- TRANG 3: QUẢN LÝ BÁO CƠM -->
    <div id="pageCom" class="page">
        <span class="admin-tag">QUẢN LÝ BÁN TRÚ</span>
        <h3 style="margin-top:0">Làm việc cẩn thận - Bát sạch cơm ngon!</h3>
        <div style="background:#fffde7; padding:15px; border-radius:10px; margin-bottom:15px; border-left: 5px solid #fbc02d;">
            <strong>Số lượng ăn hôm nay:</strong><br>
            - Lớp 12A3: 23 bạn đã báo làm 23 suất.
        </div>
        <div style="font-size:14px; color:#d32f2f;">
            <i class="fa fa-clock"></i> <strong>Thời gian ăn:</strong><br>
            - Trưa: 11h45 - 12h30<br>
            - Chiều: 16h20 - 17h30
        </div>
        <button style="background:#666; margin-top:30px" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- TRANG HỌC SINH -->
    <div id="homeStudent" class="page">
        <h3 id="txtHello" style="color:var(--primary)">Xin chào!</h3>
        <p style="font-size:14px">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Camera yêu cầu chụp xung quanh lớp...')"><i class="fa fa-camera"></i><br>Điểm danh</div>
            <div class="menu-item"><i class="fa fa-utensils"></i><br>Báo cơm</div>
            <div class="menu-item"><i class="fa fa-file-contract"></i><br>Xin nghỉ</div>
            <div class="menu-item"><i class="fa fa-bullhorn"></i><br>Phản hồi</div>
            <div class="menu-item"><i class="fa fa-envelope"></i><br>Hòm thư</div>
            <div class="menu-item" onclick="location.reload()"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="askAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }

    function checkLogin() {
        const u = document.getElementById('user').value;
        const p = document.getElementById('pass').value;

        if(u === 'BGH THPTMCC2025' && p === 'THPT1983@') {
            goPage('pageBGH');
        } else if(u === 'muahaquangdz' && p === 'Mrquang@123') {
            goPage('pageGV');
        } else if(u === 'Baocomngon' && p === 'ankhongvanan') {
            goPage('pageCom');
        } else {
            document.getElementById('txtHello').innerText = "Xin chào " + (u || "Học sinh") + "!";
            goPage('homeStudent');
        }
    }

    function askAI() {
        prompt("Bạn cần trợ lý giúp gì?");
        alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_full_system, height=850, scrolling=True)
