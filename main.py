import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải", layout="centered")

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
        .page { display: none; padding: 15px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Giao diện Trang đầu */
        .header-main { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net');
            background-size: cover; padding: 40px 20px; color: white; border-radius: 0 0 20px 20px;
        }
        .flag-box { width: 50px; margin-bottom: 10px; }
        
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; font-size: 14px; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; }
        .menu-item i { font-size: 20px; color: var(--primary); margin-bottom: 5px; }
        
        /* Robot trợ lý */
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 100; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
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
            <img src="https://wikimedia.org" class="flag-box">
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
        <h4 style="color:var(--primary); text-align:center">1. BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
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

    <!-- 3. TRANG QUÊN MẬT KHẨU -->
    <div id="forgotPage" class="page">
        <h3>9. QUÊN MẬT KHẨU</h3>
        <input type="text" placeholder="1. Email hoặc số điện thoại">
        <button onclick="alert('Đã gửi mã!')">3. Gửi cấp lại mật khẩu</button>
        <input type="text" placeholder="4. Nhập mã">
        <button onclick="alert('Xác nhận thành công!'); goPage('loginPage')">5. Xác nhận</button>
    </div>

    <!-- 4. TRANG CHỦ HỌC SINH -->
    <div id="homeHS" class="page">
        <div style="display:flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h3 id="hiHS" style="color:var(--primary); margin-bottom:0">Xin chào!</h3>
                <p style="font-size:13px">Chúc bạn một ngày vui vẻ!</p>
            </div>
            <div onclick="goPage('profilePage')" style="text-align:right; cursor:pointer">
                <i class="fa fa-user-circle" style="font-size:25px"></i><br><small>Tài khoản</small>
            </div>
        </div>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Yêu cầu chụp bất cứ chỗ nào xung quanh lớp...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealPage')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leavePage')"><i class="fa fa-notes-medical"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedPage')"><i class="fa fa-bullhorn"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('boxPage')"><i class="fa fa-envelope-open"></i><br>5. Hòm thư</div>
        </div>
        <!-- Trợ lý Robot -->
        <div class="robot-box" onclick="talkAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- 5. TRANG BÁO CƠM -->
    <div id="mealPage" class="page">
        <h3>2. MỤC BÁO CƠM</h3>
        <button onclick="alert('Đã báo cơm hôm nay!')">1. Báo cơm cho tôi hôm nay</button>
        <p><strong>2. Cho tôi xin nghỉ bữa này:</strong></p>
        <label><input type="checkbox"> Bữa trưa</label>
        <label><input type="checkbox"> Bữa tối</label>
        <button onclick="goPage('homeHS')">Gửi yêu cầu</button>
    </div>

    <!-- 6. TRANG XIN NGHỈ -->
    <div id="leavePage" class="page">
        <h3>3. XIN NGHỈ (Việc gấp mới cần thiết)</h3>
        <textarea id="reason" placeholder="Nhập lý do chính đáng..."></textarea>
        <button onclick="guiXinNghi()">Gửi xin nghỉ</button>
        <div id="waitMsg" style="display:none" class="box-info">Đang chờ thầy giáo chủ nhiệm duyệt... (5 phút)</div>
    </div>

    <!-- 7. TRANG PHẢN HỒI -->
    <div id="feedPage" class="page">
        <h3>4. PHẢN HỒI Ý KIẾN</h3>
        <textarea placeholder="Nhập thắc mắc của bạn..."></textarea>
        <button onclick="alert('Đã gửi cho BGH!'); goPage('homeHS')">Gửi cho Ban giám hiệu</button>
        <div class="box-info">Đang chờ Ban giám hiệu phản hồi (24-48h)</div>
    </div>

    <!-- 8. HÒM THƯ -->
    <div id="boxPage" class="page">
        <h3>5. HÒM THƯ</h3>
        <div class="box-info">Nhận phản hồi từ BGH/Thầy cô tại đây.</div>
        <button onclick="alert('Đã xác nhận đã đọc')">Xác nhận đã đọc</button>
    </div>

    <!-- 9. THÔNG TIN TÀI KHOẢN -->
    <div id="profilePage" class="page">
        <h3 style="text-align:left">TÀI KHOẢN</h3>
        <div class="box-info">1. Học sinh: <span id="profName">...</span></div>
        <button onclick="location.reload()" style="background:#666">2. Đăng xuất</button>
        <hr>
        <p><strong>3. Nhập thông tin:</strong></p>
        <input type="text" placeholder="Nhập CCCD (Bắt buộc)">
        <button onclick="alert('Đã cập nhật CCCD')">Lưu thông tin</button>
        <hr>
        <p><strong>4. Đặt lại mật khẩu:</strong></p>
        <input type="password" placeholder="1. Mật khẩu hiện tại">
        <input type="password" placeholder="2. Mật khẩu mới">
        <input type="password" placeholder="3. Xác nhận mật khẩu mới">
        <button onclick="alert('Đã đổi mật khẩu thành công!')">Xác nhận đổi mật khẩu</button>
    </div>

    <!-- 10. TRANG BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info">
            <strong>1. Sĩ số báo lại:</strong><br>
            - Mùa Hà Quang 12A3 47/47 đủ
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
        <p><strong>2. Thông báo đến học sinh cho lớp:</strong></p>
        <textarea placeholder="Nhập dữ liệu thông báo..."></textarea>
        <button onclick="alert('Đã gửi xong!')">Gửi</button>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

    <!-- 12. TRANG BÁO CƠM -->
    <div id="pageBC" class="page">
        <h3 style="color:#e67e22">HÃY LÀM VIỆC CẨN THẬN NHÉ BÁC SẠCH CƠM NGON</h3>
        <div class="box-info">1. Số lượng ăn hôm nay: Lớp 12A3 23 bạn báo làm 23 xuất</div>
        <p><strong>2. Thời gian ăn:</strong><br>- Trưa: 11h45-12h30<br>- Chiều: 16h20-17h30</p>
        <button onclick="location.reload()" style="background:#666">Đăng xuất</button>
    </div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }

    function handleReg() {
        const u = document.getElementById('regU').value;
        const n = document.getElementById('regName').value;
        const p = document.getElementById('regP').value;
        if(!u || !p) return alert('Thiếu thông tin!');
        localStorage.setItem('u_'+u, JSON.stringify({pass:p, name:n}));
        alert('Đăng ký thành công!');
        goPage('loginPage');
    }

    function handleLogin() {
        const user = document.getElementById('u').value;
        const pass = document.getElementById('p').value;
        
        if(user==='BGH THPTMCC2025' && pass==='THPT1983@') return goPage('pageBGH');
        if(user==='muahaquangdz' && pass==='Mrquang@123') return goPage('pageGV');
        if(user==='Baocomngon' && pass==='ankhongvanan') return goPage('pageBC');
        
        const stored = localStorage.getItem('u_'+user);
        if(stored) {
            const d = JSON.parse(stored);
            if(d.pass === pass) {
                document.getElementById('hiHS').innerText = "Xin chào " + d.name;
                document.getElementById('profName').innerText = d.name;
                return goPage('homeHS');
            }
        }
        alert('Sai tài khoản hoặc hãy đăng ký!');
    }

    function guiXinNghi() {
        if(!document.getElementById('reason').value) return alert('Phải có lý do!');
        document.getElementById('waitMsg').style.display = 'block';
        setTimeout(() => {
            alert('Bạn được nghỉ theo quy định sau thời gian quay lại trường học bài');
            goPage('homeHS');
        }, 3000);
    }

    function talkAI() {
        const ask = prompt("Bạn cần tôi giúp gì không?");
        if(ask) alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
