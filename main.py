import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải", layout="centered")

# ĐÂY LÀ TOÀN BỘ Ý TƯỞNG CỦA BẠN ĐÃ ĐƯỢC CODE HÓA
html_all_in_one = """
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
        
        /* Header với máy trường và lá cờ */
        .header-school { 
            text-align: center; 
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); 
            background-size: cover; padding: 40px 20px; color: white; 
        }
        .flag { width: 50px; margin-bottom: 10px; border: 1px solid white; }
        
        .page { display: none; padding: 20px; animation: fadeIn 0.4s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        input, select, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 15px; }
        button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 16px; }
        
        /* Menu trang chủ học sinh */
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .menu-item i { font-size: 24px; color: var(--primary); margin-bottom: 8px; }
        
        /* Robot AI */
        .robot-box { position: fixed; bottom: 30px; right: 20px; text-align: center; cursor: pointer; z-index: 999; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 12px; margin-bottom: 8px; box-shadow: 2px 4px 10px rgba(0,0,0,0.2); font-weight: bold; }
        .robot-img { width: 70px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    </style>
</head>
<body>

<div class="container">
    <!-- 1. TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" class="flag">
            <h2 style="margin:0; font-size: 1.2rem;">XIN CHÀO ĐẾN VỚI <br> TRƯỜNG THPT MÙ CANG CHẢI</h2>
        </div>
        <div style="margin-top: 20px;">
            <input type="text" id="user" placeholder="1. Tên tài khoản">
            <input type="password" id="pass" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="checkLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 14px; margin-top: 20px;">
                <span style="color:blue; cursor:pointer" onclick="goPage('regPage')">4. Đăng ký tài khoản</span> | 
                <span style="color:gray; cursor:pointer" onclick="goPage('forgotPage')">9. Quên mật khẩu</span>
            </p>
        </div>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h3 style="color:var(--primary); text-align:center;">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h3>
        <input type="text" placeholder="2. Tên tài khoản">
        <input type="text" placeholder="3. Họ và tên học sinh">
        <select>
            <option>4. Chọn lớp...</option>
            <optgroup label="Khối 12">
                <script>for(let i=1; i<=7; i++) document.write(`<option>12A${i}</option>`)</script>
            </optgroup>
            <!-- Thêm tiếp các khối khác tương tự -->
        </select>
        <input type="password" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (Bắt buộc khôi phục)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <button onclick="alert('Đăng ký thành công!'); goPage('loginPage')">10. XÁC NHẬN ĐĂNG KÝ</button>
        <button style="background:#666" onclick="goPage('loginPage')">Quay lại</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH -->
    <div id="homeStudent" class="page">
        <div style="display:flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <h3 id="txtHello" style="margin:0; color: var(--primary);">Xin chào học sinh!</h3>
            <div onclick="goPage('profilePage')" style="font-size: 13px; text-align:right; cursor:pointer">
                <i class="fa fa-user-circle" style="font-size: 20px;"></i><br>Tài khoản
            </div>
        </div>
        <p>Chúc bạn một ngày vui vẻ!</p>
        
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Yêu cầu chụp ảnh lớp học...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealPage')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leavePage')"><i class="fa fa-file-signature"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedPage')"><i class="fa fa-bullhorn"></i><br>4. Phản hồi BGH</div>
            <div class="menu-item" onclick="goPage('boxPage')"><i class="fa fa-envelope-open-text"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('loginPage')"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>

        <!-- Trợ lý ảo Robot -->
        <div class="robot-box" onclick="talkAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>
    
    <!-- 4. TRANG BGH -->
    <div id="pageBGH" class="page">
        <h3 style="color:var(--primary)">QUẢN LÝ NHÀ TRƯỜNG</h3>
        <div style="background:#f9f9f9; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
            <strong>1. Sĩ số lớp (Ví dụ):</strong><br>
            - Mùa Hà Quang 12A3: 47/47 (Đủ)
        </div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Nhập câu trả lời cho học sinh..."></textarea>
        <button onclick="alert('Đã gửi phản hồi thành công!')">GỬI TRẢ LỜI</button>
        <button style="background:#666; margin-top:20px" onclick="goPage('loginPage')">ĐĂNG XUẤT</button>
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
            alert('Chào thầy Mr Quang một ngày tốt đẹp!');
            goPage('homeStudent'); // Ở đây có thể tạo trang GV riêng
        } else {
            document.getElementById('txtHello').innerText = "Xin chào " + (u || "Học sinh") + "!";
            goPage('homeStudent');
        }
    }

    function talkAI() {
        prompt("Robot: Bạn cần hỗ trợ gì?");
        alert("Thông báo: Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

# Hiển thị lên Streamlit
components.html(html_all_in_one, height=850, scrolling=True)
