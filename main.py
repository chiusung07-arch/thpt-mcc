import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải - Full", layout="centered")

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
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 15px rgba(0,0,0,0.2); }
        .page { display: none; padding: 20px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .header-main { text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); background-size: cover; padding: 30px 20px; color: white; border-radius: 0 0 20px 20px; }
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 100; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .robot-img { width: 60px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
        .box-info { background: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid var(--primary); font-size: 13px; }
    </style>
</head>
<body>
<div class="container">

    <!-- 1. TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-main">
            <img src="https://wikimedia.org" style="width:40px; margin-bottom:5px">
            <h3 style="margin:0">Xin chào đến với <br> Trường THPT Mù Cang Chải</h3>
        </div>
        <input type="text" id="u" placeholder="1. Tên tài khoản">
        <input type="password" id="p" placeholder="2. Mật khẩu">
        <input type="text" placeholder="3. Mã học sinh">
        <button onclick="handleLogin()">ĐĂNG NHẬP</button>
        <p style="text-align: center; font-size: 13px;"><span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Đăng ký tài khoản</span></p>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select><option>4. Chọn lớp...</option><script>for(let i=1;i<=9;i++) document.write(`<option>10A${i}</option>`);</script></select>
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (bắc buộc)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <button onclick="handleReg()">10. XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH -->
    <div id="homeHS" class="page">
        <h3 id="hiHS" style="color:var(--primary); margin:0">Xin chào!</h3>
        <p style="font-size:13px">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Mở camera chụp ảnh lớp...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('pageMeal')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('pageLeave')"><i class="fa fa-file-medical"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('pageFeed')"><i class="fa fa-comment-dots"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('pageBox')"><i class="fa fa-envelope"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('pageProfile')"><i class="fa fa-user-cog"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="background:#eee"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="talkAI()"><div class="robot-bubble">Bạn cần tôi giúp gì không?</div><img src="https://flaticon.com" class="robot-img"></div>
    </div>

    <!-- CÁC TRANG CHỨC NĂNG CON CỦA HỌC SINH -->
    <div id="pageMeal" class="page">
        <h3>2. MỤC BÁO CƠM</h3>
        <button onclick="alert('Đã báo cơm hôm nay!')">1. Báo cơm cho tôi hôm nay</button>
        <p><strong>2. Xin nghỉ bữa:</strong></p>
        <label><input type="checkbox"> Trưa</label> <label><input type="checkbox"> Tối</label>
        <button onclick="goPage('homeHS')">Gửi</button>
    </div>

    <div id="pageLeave" class="page">
        <h3>3. XIN NGHỈ</h3>
        <textarea id="reason" placeholder="Lý do chính đáng..."></textarea>
        <button onclick="handleLeave()">Gửi đơn</button>
        <div id="wait" style="display:none" class="box-info">Đang chờ thầy giáo duyệt (5 phút)...</div>
    </div>

    <div id="pageFeed" class="page">
        <h3>4. PHẢN HỒI BGH</h3>
        <textarea placeholder="Nhập thắc mắc..."></textarea>
        <button onclick="alert('Đã gửi phản hồi!'); goPage('homeHS')">Gửi cho ban giám hiệu</button>
    </div>

    <div id="pageBox" class="page">
        <h3>5. HÒM THƯ</h3>
        <div class="box-info">Bạn chưa có thông báo mới từ thầy cô.</div>
        <button onclick="goPage('homeHS')">Quay lại</button>
    </div>

    <div id="pageProfile" class="page">
        <h3>THÔNG TIN TÀI KHOẢN</h3>
        <input type="text" placeholder="Nhập CCCD (bắc buộc)">
        <button onclick="alert('Đã lưu CCCD')">Xác nhận</button>
        <p><strong>Đổi mật khẩu:</strong></p>
        <input type="password" placeholder="Mật khẩu cũ">
        <input type="password" placeholder="Mật khẩu mới">
        <button onclick="alert('Đã đổi mật khẩu')">Đổi mật khẩu</button>
        <button onclick="goPage('homeHS')" style="background:#666">Quay lại</button>
    </div>

    <!-- TRANG ADMINS -->
    <div id="pageBGH" class="page"><h3>BGH - QUẢN LÝ</h3><div id="bghData" class="box-info">Chờ báo cáo...</div><button onclick="location.reload()">Đăng xuất</button></div>
    <div id="pageGV" class="page"><h3>Chào thầy Quang!</h3><input type="text" id="gvIn" placeholder="Gửi sĩ số..."><button onclick="gvGui()">Gửi BGH</button><button onclick="location.reload()">Đăng xuất</button></div>
    <div id="pageBC" class="page"><h3>Bác sạch cơm ngon!</h3><div class="box-info">12A3: 23 bạn ăn</div><button onclick="location.reload()">Đăng xuất</button></div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id==='pageBGH'){ const d=localStorage.getItem('ss'); if(d) document.getElementById('bghData').innerText=d; }
    }
    function handleLogin() {
        const u=document.getElementById('u').value, p=document.getElementById('p').value;
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else if(u==='Baocomngon' && p==='ankhongvanan') goPage('pageBC');
        else { document.getElementById('hiHS').innerText="Xin chào "+(u||"Bạn"); goPage('homeHS'); }
    }
    function handleReg() { alert('Đăng ký thành công!'); goPage('loginPage'); }
    function gvGui() { localStorage.setItem('ss', document.getElementById('gvIn').value); alert('Đã gửi!'); }
    function handleLeave() { document.getElementById('wait').style.display='block'; setTimeout(()=>{alert('Bạn được nghỉ!'); goPage('homeHS');}, 2000); }
    function talkAI() { const a=prompt("Bạn cần gì?"); if(a) alert("Ai chưa thể sử dụng chính thức"); }
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
