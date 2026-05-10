<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống THPT Mù Cang Chải</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --secondary: #f44336; --bg: #f5f5f5; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 500px; margin: auto; min-height: 100vh; background: white; position: relative; overflow-x: hidden; }
        
        /* Giao diện Đăng nhập & Trường học */
        .page { display: none; padding: 20px; animation: fadeIn 0.5s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        .header-school { text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://vnecdn.net'); background-size: cover; padding: 40px 20px; color: white; border-radius: 0 0 20px 20px; }
        .flag { width: 60px; margin-bottom: 10px; }
        
        input, select, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        
        /* Dashboard học sinh */
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
        .menu-item { background: #fff5f5; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #ffebee; cursor: pointer; transition: 0.3s; }
        .menu-item i { font-size: 24px; color: var(--primary); margin-bottom: 8px; }
        
        /* Robot trợ lý */
        .robot-box { position: fixed; bottom: 20px; right: 20px; text-align: center; cursor: pointer; z-index: 100; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-bottom: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .robot-img { width: 60px; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2)); }
    </style>
</head>
<body>

<div class="container">
    <!-- TRANG ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" class="flag">
            <h2>XIN CHÀO ĐẾN VỚI TRƯỜNG THPT MÙ CANG CHẢI</h2>
        </div>
        <div style="padding-top: 20px;">
            <input type="text" id="user" placeholder="Tên tài khoản">
            <input type="password" id="pass" placeholder="Mật khẩu">
            <input type="text" placeholder="Mã học sinh">
            <button onclick="handleLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 14px;">
                <a href="#" onclick="showPage('registerPage')">Đăng ký tài khoản</a> | 
                <a href="#" onclick="showPage('forgotPassPage')">Quên mật khẩu</a>
            </p>
        </div>
    </div>

    <!-- TRANG ĐĂNG KÝ -->
    <div id="registerPage" class="page">
        <h3 style="color: var(--primary); text-align: center;">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h3>
        <input type="text" placeholder="Tên tài khoản">
        <input type="text" placeholder="Họ và tên học sinh">
        <select id="lop">
            <script>
                for(let i=1; i<=9; i++) document.write(`<option>Lớp 10A${i}</option>`);
                for(let i=1; i<=7; i++) document.write(`<option>Lớp 11A${i}</option>`);
                for(let i=1; i<=7; i++) document.write(`<option>Lớp 12A${i}</option>`);
            </script>
        </select>
        <input type="password" placeholder="Mật khẩu">
        <input type="email" placeholder="Email (Bắt buộc khôi phục)">
        <input type="tel" placeholder="Số điện thoại">
        <select><option>Học sinh bán trú</option><option>Học sinh ngoại trú</option></select>
        <button onclick="alert('Đăng ký thành công!'); showPage('loginPage')">XÁC NHẬN ĐĂNG KÝ</button>
        <button style="background: #666;" onclick="showPage('loginPage')">QUAY LẠI</button>
    </div>

    <!-- TRANG CHỦ HỌC SINH -->
    <div id="homeStudent" class="page">
        <div style="display:flex; justify-content: space-between; align-items: center;">
            <h3 id="welcomeName">Xin chào!</h3>
            <span onclick="showPage('profilePage')" style="cursor:pointer"><i class="fa fa-user-circle"></i> Tài khoản</span>
        </div>
        <p style="color: #666;">Chúc bạn một ngày vui vẻ!</p>
        
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Mở Camera điểm danh...')"><i class="fa fa-camera"></i><br>Điểm danh</div>
            <div class="menu-item" onclick="showPage('mealPage')"><i class="fa fa-utensils"></i><br>Báo cơm</div>
            <div class="menu-item" onclick="showPage('leavePage')"><i class="fa fa-envelope-open-text"></i><br>Xin nghỉ</div>
            <div class="menu-item" onclick="showPage('feedbackPage')"><i class="fa fa-comment-dots"></i><br>Phản hồi BGH</div>
            <div class="menu-item" onclick="showPage('mailboxPage')"><i class="fa fa-inbox"></i><br>Hòm thư</div>
            <div class="menu-item" onclick="showPage('loginPage')"><i class="fa fa-sign-out-alt"></i><br>Đăng xuất</div>
        </div>
    </div>

    <!-- TRANG CHỦ BAN GIÁM HIỆU -->
    <div id="homeBGH" class="page">
        <h3>QUẢN LÝ NHÀ TRƯỜNG & TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="menu-item" style="text-align: left; margin-bottom: 10px;">
            <strong>Sĩ số hôm nay:</strong><br>
            - 12A3: 47/47 (Đủ)<br>
            - 12A1: 45/46 (Vắng 1)
        </div>
        <textarea placeholder="Trả lời thắc mắc học sinh..."></textarea>
        <button onclick="alert('Đã gửi phản hồi!')">GỬI PHẢN HỒI</button>
        <button style="background: #666;" onclick="showPage('loginPage')">ĐĂNG XUẤT</button>
    </div>

    <!-- TRỢ LÝ ROBOT -->
    <div class="robot-box" id="robotAI" style="display:none;">
        <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
        <img src="https://flaticon.com" class="robot-img" onclick="askAI()">
    </div>
</div>

<script>
    function showPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        // Chỉ hiện robot ở trang chủ học sinh
        document.getElementById('robotAI').style.display = (id === 'homeStudent') ? 'block' : 'none';
    }

    function handleLogin() {
        const u = document.getElementById('user').value;
        const p = document.getElementById('pass').value;

        if(u === 'BGH THPTMCC2025' && p === 'THPT1983@') {
            showPage('homeBGH');
        } else if(u === 'muahaquangdz' && p === 'Mrquang@123') {
            alert('Chào thầy Mr Quang!');
            showPage('homeStudent'); // Bạn có thể tạo thêm trang riêng cho GV
        } else {
            document.getElementById('welcomeName').innerText = "Xin chào " + (u || "Học sinh") + "!";
            showPage('homeStudent');
        }
    }

    function askAI() {
        prompt("Tôi có thể giúp gì cho bạn?");
        alert("Ai chưa thể sử dụng chính thức");
    }
</script>

</body>
</html>
