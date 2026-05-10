import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải", layout="centered")

html_final_perfect = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f4f4f4; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        .page { display: none; padding: 15px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Header */
        .header-main { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net');
            background-size: cover; padding: 30px 20px; color: white; border-radius: 0 0 20px 20px;
        }
        
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 100; }
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

    <!-- 2. TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select id="regClass">
            <option value="">4. Chọn lớp...</option>
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

    <!-- 10. TRANG BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info">
            <strong>1. Sĩ số báo lại:</strong><br>
            <div id="bghDataDisplay"><i>Chưa có giáo viên nào báo cáo...</i></div>
        </div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Trả lời thắc mắc..."></textarea>
        <button onclick="alert('Đã gửi thành công!')">Gửi trả lời</button>
        <div class="box-info">3. Sự kiện gửi thông báo:</div>
        <input type="text" placeholder="Ghi sự kiện...">
        <button onclick="alert('Đã gửi thông báo!')">Gửi sự kiện</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 11. TRANG GIÁO VIÊN -->
    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">
            <strong>1. Nhận điểm danh lớp 12A3:</strong><br>
            - Sùng A Chiều đã đi học (Hình ảnh) 6:30 9/4/2024
        </div>
        <p><strong>2. Thông báo & Gửi sĩ số:</strong></p>
        <input type="text" id="gvSisoInput" placeholder="Nhập sĩ số (VD: Mùa Hà Quang 12A3 47/47 đủ)">
        <button onclick="gvGuiBaoCao()">Gửi báo cáo lên BGH</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- Các trang khác (Học sinh, Báo cơm...) giữ nguyên như kịch bản cũ -->
    <div id="homeHS" class="page">
        <h3 id="hiHS">Xin chào!</h3>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Chụp ảnh điểm danh...')">Điểm danh</div>
            <div class="menu-item" onclick="goPage('loginPage')">Đăng xuất</div>
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
            const data = localStorage.getItem('live_siso');
            if(data) document.getElementById('bghDataDisplay').innerHTML = data;
        }
    }

    function gvGuiBaoCao() {
        const val = document.getElementById('gvSisoInput').value;
        if(!val) return alert('Vui lòng nhập dữ liệu!');
        localStorage.setItem('live_siso', val);
        alert('Đã gửi thành công lên BGH!');
    }

    function handleLogin() {
        const user = document.getElementById('u').value;
        const pass = document.getElementById('p').value;
        if(user==='BGH THPTMCC2025' && pass==='THPT1983@') return goPage('pageBGH');
        if(user==='muahaquangdz' && pass==='Mrquang@123') return goPage('pageGV');
        // ... Logic đăng nhập học sinh ...
        goPage('homeHS');
    }

    function handleReg() { alert('Đăng ký thành công!'); goPage('loginPage'); }
    function talkAI() { prompt("Bạn cần gì?"); alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_final_perfect, height=850, scrolling=True)
