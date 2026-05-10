import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="THPT Mù Cang Chải - Kết nối 10/10", layout="centered")

html_perfect_final = """
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
        .page { display: none; padding: 20px; animation: fadeIn 0.4s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        /* Header & Background */
        .header-school { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net');
            background-size: cover; padding: 35px 20px; color: white; border-radius: 0 0 20px 20px;
        }
        
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; font-size: 13px; }
        .menu-item i { font-size: 22px; color: var(--primary); margin-bottom: 5px; }

        /* Robot Assistant */
        .robot-box { position: fixed; bottom: 20px; right: 15px; text-align: center; cursor: pointer; z-index: 100; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 11px; margin-bottom: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .robot-img { width: 65px; animation: float 3s infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

        .box-info { background: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid var(--primary); font-size: 13px; }
    </style>
</head>
<body>
<div class="container">

    <!-- TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px; margin-bottom:10px">
            <h2 style="margin:0">Xin chào đến với <br> Trường THPT Mù Cang Chải</h2>
        </div>
        <input type="text" id="u" placeholder="1. Tên tài khoản">
        <input type="password" id="p" placeholder="2. Mật khẩu">
        <input type="text" placeholder="3. Mã học sinh">
        <button onclick="handleLogin()">ĐĂNG NHẬP</button>
        <p style="text-align: center; font-size: 13px;"><span onclick="goPage('regPage')" style="color:blue; cursor:pointer">4. Đăng ký tài khoản</span></p>
    </div>

    <!-- TRANG ĐĂNG KÝ (10 MỤC) -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select id="regClass"><option>4. Chọn lớp...</option><script>for(let i=1;i<=9;i++) document.write(`<option>10A${i}</option>`); for(let i=1;i<=7;i++) document.write(`<option>11A${i}</option>`); for(let i=1;i<=7;i++) document.write(`<option>12A${i}</option>`);</script></select>
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <input type="email" placeholder="6. Email (bắc buộc)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <p style="font-size:12px; color:blue; cursor:pointer" onclick="goPage('forgotPage')">9. Quên mật khẩu</p>
        <button onclick="handleReg()">10. XÁC NHẬN ĐĂNG KÝ</button>
    </div>

    <!-- TRANG 1: BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info"><strong>1. Sĩ số báo lại:</strong><br><div id="bghDataDisplay"><i>(Đang chờ báo cáo từ giáo viên...)</i></div></div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Trả lời thắc mắc học sinh..."></textarea>
        <button onclick="alert('Đã gửi phản hồi thành công!')">Gửi trả lời</button>
        <div class="box-info">3. Sự kiện gửi thông báo:</div>
        <input type="text" placeholder="Ghi sự kiện...">
        <button onclick="alert('Đã gửi xong!')">Gửi</button>
        <button onclick="location.reload()" style="background:#666; margin-top:20px">Đăng xuất</button>
    </div>

    <!-- TRANG 2: GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">1. Nhận điểm danh lớp 12A3: Sùng A Chiều đã đi học (Hình ảnh) 6:30 9/4/2024</div>
        <p><strong>2. Gửi báo cáo sĩ số lên BGH:</strong></p>
        <input type="text" id="gvSisoInput" placeholder="Ví dụ: Mùa Hà Quang 12A3 47/47 đủ">
        <button onclick="gvGuiBGH()" style="background:green">GỬI LÊN BAN GIÁM HIỆU</button>
        <p><strong>3. Thông báo cho lớp:</strong></p>
        <textarea placeholder="Nhập dữ liệu thông báo gửi tới hòm thư..."></textarea>
        <button onclick="alert('Đã gửi thông báo tới lớp!')">Gửi thông báo</button>
        <button onclick="location.reload()" style="background:#666; margin-top:20px">Đăng xuất</button>
    </div>

    <!-- TRANG 3: QUẢN LÝ BÁO CƠM -->
    <div id="pageCom" class="page">
        <h3 style="color:#e67e22">HÃY LÀM VIỆC CẨN THẬN NHÉ BÁC SẠCH CƠM NGON</h3>
        <div class="box-info">1. Số lượng ăn hôm nay: Lớp 12A3 23 bạn đã báo làm 23 xuất</div>
        <p><strong>2. Thời gian ăn:</strong><br>Trưa: 11h45-12h30<br>Chiều: 16h20-17h30</p>
        <button onclick="location.reload()" style="background:#666; margin-top:20px">Đăng xuất</button>
    </div>

    <!-- TRANG CHỦ HỌC SINH -->
    <div id="homeHS" class="page">
        <h3 id="hiHS" style="color:var(--primary); margin:0">Xin chào!</h3>
        <p style="font-size:13px">Chúc bạn một ngày vui vẻ!</p>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Mở camera điểm danh lớp học...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealHS')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leaveHS')"><i class="fa fa-file-signature"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedHS')"><i class="fa fa-bullhorn"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('boxHS')"><i class="fa fa-envelope"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="goPage('profileHS')"><i class="fa fa-user-cog"></i><br>Tài khoản</div>
            <div class="menu-item" onclick="location.reload()" style="grid-column: span 2; background:#eee"><i class="fa fa-sign-out-alt"></i> Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="talkAI()"><div class="robot-bubble">Bạn cần tôi giúp gì không?</div><img src="https://flaticon.com" class="robot-img"></div>
    </div>

    <!-- TRANG QUÊN MẬT KHẨU -->
    <div id="forgotPage" class="page">
        <h3>QUÊN MẬT KHẨU</h3>
        <input type="text" placeholder="1. Email hoặc số điện thoại">
        <button onclick="alert('Đã gửi mã!')">3. Gửi cấp lại mật khẩu</button>
        <input type="text" placeholder="4. Nhập mã">
        <button onclick="alert('Xác nhận thành công!'); goPage('loginPage')">5. Xác nhận</button>
    </div>

    <!-- MỤC BÁO CƠM HỌC SINH -->
    <div id="mealHS" class="page">
        <h3>BÁO CƠM</h3>
        <button onclick="alert('Đã báo cơm cho bạn hôm nay!')">1. Báo cơm cho tôi hôm nay</button>
        <p><strong>2. Cho tôi xin nghỉ bữa:</strong></p>
        <label><input type="checkbox"> Trưa</label> <label style="margin-left:20px"><input type="checkbox"> Tối</label>
        <button onclick="goPage('homeHS')" style="margin-top:20px">Xác nhận</button>
    </div>

    <!-- TÀI KHOẢN HỌC SINH -->
    <div id="profileHS" class="page">
        <h3 id="profName">Tài khoản</h3>
        <button onclick="location.reload()">Đăng xuất</button>
        <hr>
        <input type="text" placeholder="Nhập CCCD (bắc buộc)">
        <p><strong>Đổi mật khẩu:</strong></p>
        <input type="password" placeholder="Mật khẩu hiện tại">
        <input type="password" placeholder="Mật khẩu mới">
        <button onclick="alert('Đã đổi thành công!')">Xác nhận đổi mật khẩu</button>
        <button onclick="goPage('homeHS')" style="background:#666; margin-top:20px">Quay lại</button>
    </div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id === 'pageBGH') {
            const data = localStorage.getItem('siso_tu_gv');
            if(data) document.getElementById('bghDataDisplay').innerText = data;
        }
    }

    function handleLogin() {
        const u = document.getElementById('u').value, p = document.getElementById('p').value;
        // Kiểm tra 3 tài khoản Admin
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else if(u==='Baocomngon' && p==='ankhongvanan') goPage('pageCom');
        else {
            const s = localStorage.getItem('user_'+u);
            if(s && JSON.parse(s).pass === p) {
                document.getElementById('hiHS').innerText = "Xin chào " + JSON.parse(s).name + "!";
                document.getElementById('profName').innerText = "Học sinh: " + JSON.parse(s).name;
                goPage('homeHS');
            } else alert('Tài khoản không đúng hoặc chưa đăng ký!');
        }
    }

    function handleReg() {
        const u = document.getElementById('regU').value, n = document.getElementById('regName').value, p = document.getElementById('regP').value;
        if(u && p) {
            localStorage.setItem('user_'+u, JSON.stringify({pass:p, name:n}));
            alert('Đăng ký thành công!'); goPage('loginPage');
        }
    }

    function gvGuiBGH() {
        const val = document.getElementById('gvSisoInput').value;
        if(val) {
            localStorage.setItem('siso_tu_gv', val);
            alert('Đã gửi sĩ số lên Ban Giám Hiệu thành công!');
        }
    }

    function talkAI() {
        const q = prompt("Bạn cần tôi giúp gì không?");
        if(q) alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_perfect_final, height=850, scrolling=True)
