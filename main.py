import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải - Perfect 10/10", layout="centered")

html_10_score = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f5f5f5; --accent: #2e7d32; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); color: #333; }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; position: relative; box-shadow: 0 0 30px rgba(0,0,0,0.1); }
        .page { display: none; padding: 20px; animation: fadeIn 0.4s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Giao diện Trang đầu */
        .header-main { 
            text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://vnecdn.net');
            background-size: cover; padding: 40px 20px; color: white; border-radius: 0 0 25px 25px;
        }
        
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 10px; border: 1px solid #ddd; box-sizing: border-box; font-size: 14px; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; transition: 0.3s; }
        button:hover { opacity: 0.9; transform: scale(0.99); }
        .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 15px; }
        .menu-item { background: #fff5f5; padding: 18px; border-radius: 15px; text-align: center; border: 1px solid #ffebee; cursor: pointer; transition: 0.3s; }
        .menu-item i { font-size: 22px; color: var(--primary); margin-bottom: 8px; }
        .menu-item:hover { border-color: var(--primary); background: white; }

        /* Robot Trợ Lý */
        .robot-box { position: fixed; bottom: 25px; right: 20px; text-align: center; cursor: pointer; z-index: 1000; }
        .robot-bubble { background: white; border: 2px solid var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 11px; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); font-weight: bold; }
        .robot-img { width: 65px; animation: float 3s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

        .box-info { background: #f9f9f9; padding: 12px; border-radius: 10px; margin: 10px 0; border-left: 5px solid var(--primary); font-size: 13px; line-height: 1.6; }
        .status-tag { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: bold; margin-bottom: 10px; }
    </style>
</head>
<body>
<div class="container">

    <!-- 1. TRANG ĐẦU TIÊN -->
    <div id="loginPage" class="page active">
        <div class="header-main">
            <img src="https://wikimedia.org" style="width:45px; margin-bottom:10px; border:1px solid #fff;">
            <h2 style="margin:0">Xin chào đến với <br> Trường THPT Mù Cang Chải</h2>
        </div>
        <div style="padding: 15px;">
            <input type="text" id="u" placeholder="1. Tên tài khoản">
            <input type="password" id="p" placeholder="2. Mật khẩu">
            <input type="text" placeholder="3. Mã học sinh">
            <button onclick="handleLogin()">ĐĂNG NHẬP</button>
            <p style="text-align: center; font-size: 13px; margin-top: 15px;">
                <span onclick="goPage('regPage')" style="color:blue; cursor:pointer; font-weight:bold;">4. Mục đăng ký tài khoản</span>
            </p>
        </div>
    </div>

    <!-- 2. TRANG ĐĂNG KÝ (10 Mục chi tiết) -->
    <div id="regPage" class="page">
        <h4 style="color:var(--primary); text-align:center">BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI</h4>
        <input type="text" id="regU" placeholder="2. Tên tài khoản">
        <input type="text" id="regName" placeholder="3. Họ và tên học sinh">
        <select id="regClass">
            <option value="">4. Lớp...</option>
            <script>
                const classes = ["10A", "11A", "12A"];
                classes.forEach(c => {
                    let m = c==="10A"?9:7;
                    for(let i=1;i<=m;i++) document.write(`<option>${c}${i}</option>`);
                });
            </script>
        </select>
        <input type="password" id="regP" placeholder="5. Mật khẩu">
        <input type="email" id="regEmail" placeholder="6. Email (bắc buộc để khôi phục)">
        <input type="tel" placeholder="7. Số điện thoại">
        <select><option>8. Học sinh bán trú</option><option>8. Học sinh ngoại trú</option></select>
        <p style="color:blue; font-size:12px; cursor:pointer" onclick="goPage('forgotPage')">9. Ô quên mật khẩu</p>
        <button onclick="handleReg()">10. XÁC NHẬN ĐĂNG KÝ</button>
        <button onclick="goPage('loginPage')" style="background:#666">Quay lại</button>
    </div>

    <!-- QUÊN MẬT KHẨU -->
    <div id="forgotPage" class="page">
        <h3>QUÊN MẬT KHẨU</h3>
        <input type="text" placeholder="1. Email hoặc số điện thoại">
        <button onclick="alert('Đã gửi mã!')">3. Gửi cấp lại mật khẩu</button>
        <input type="text" placeholder="4. Nhập mã">
        <button onclick="alert('Xác nhận!'); goPage('loginPage')">5. Xác nhận</button>
    </div>

    <!-- 3. TRANG CHỦ HỌC SINH (7 Mục + Robot) -->
    <div id="homeHS" class="page">
        <div style="display:flex; justify-content: space-between; align-items: flex-start; background: #fff5f5; padding: 15px; border-radius: 15px;">
            <div>
                <h3 id="hiHS" style="color:var(--primary); margin:0">Xin chào!</h3>
                <p style="font-size:12px; margin:5px 0 0 0;">Chúc bạn một ngày vui vẻ!</p>
            </div>
            <div onclick="goPage('profilePage')" style="text-align:right; cursor:pointer">
                <i class="fa fa-user-circle" style="font-size:30px; color:var(--primary)"></i><br><small>Tài khoản</small>
            </div>
        </div>
        <div class="menu-grid">
            <div class="menu-item" onclick="alert('Hãy chụp bất cứ chỗ nào xung quanh lớp học và gửi cho giáo viên...')"><i class="fa fa-camera"></i><br>1. Điểm danh</div>
            <div class="menu-item" onclick="goPage('mealPage')"><i class="fa fa-utensils"></i><br>2. Báo cơm</div>
            <div class="menu-item" onclick="goPage('leavePage')"><i class="fa fa-notes-medical"></i><br>3. Xin nghỉ</div>
            <div class="menu-item" onclick="goPage('feedPage')"><i class="fa fa-bullhorn"></i><br>4. Phản hồi</div>
            <div class="menu-item" onclick="goPage('boxPage')"><i class="fa fa-envelope-open"></i><br>5. Hòm thư</div>
            <div class="menu-item" onclick="location.reload()" style="grid-column: span 2; background:#333; color:white;"><i class="fa fa-sign-out-alt"></i> Đăng xuất</div>
        </div>
        <div class="robot-box" onclick="askAI()">
            <div class="robot-bubble">Bạn cần tôi giúp gì không?</div>
            <img src="https://flaticon.com" class="robot-img">
        </div>
    </div>

    <!-- CHI TIẾT CÁC MỤC HỌC SINH -->
    <div id="mealPage" class="page">
        <h3>2. MỤC BÁO CƠM (Dành cho bán trú)</h3>
        <button onclick="alert('Đã báo cơm cho bạn hôm nay!')">1. Báo cơm cho tôi hôm nay</button>
        <p><strong>2. Cho tôi xin nghỉ bữa này:</strong></p>
        <label><input type="checkbox"> Trưa</label> <label style="margin-left:20px"><input type="checkbox"> Tối</label>
        <button onclick="goPage('homeHS')" style="margin-top:20px">Xác nhận gửi</button>
    </div>

    <div id="leavePage" class="page">
        <h3>3. XIN NGHỈ (Việc gấp mới cần thiết)</h3>
        <p style="font-size:12px; color:red">Lý do phải chính đáng</p>
        <textarea id="leaveReason" placeholder="Ghi lý do xin nghỉ tại đây..."></textarea>
        <button onclick="guiXinNghi()">Gửi lý do</button>
        <div id="leaveStatus" style="display:none" class="box-info">Đang chờ thầy giáo chủ nhiệm duyệt... (5 phút)</div>
    </div>

    <div id="feedPage" class="page">
        <h3>4. PHẢN HỒI Ý KIẾN NHÀ TRƯỜNG</h3>
        <textarea placeholder="Nhập thắc mắc của bạn gửi cho Ban Giám Hiệu..."></textarea>
        <button onclick="alert('Đã gửi phản hồi!'); goPage('homeHS')">Gửi cho Ban Giám Hiệu</button>
        <div class="box-info">Trạng thái: Đang chờ ban giám hiệu phản hồi (Chờ ít nhất 24-48h sau ngày làm việc)</div>
    </div>

    <div id="boxPage" class="page">
        <h3>5. HÒM THƯ</h3>
        <div class="box-info">Chào bạn! Bạn sẽ nhận phản hồi từ BGH và thầy giáo tại đây.</div>
        <button onclick="alert('Đã xác nhận đã đọc!'); goPage('homeHS')">Xác nhận đã đọc</button>
    </div>

    <div id="profilePage" class="page">
        <h3 id="pName">Học sinh: ...</h3>
        <button onclick="location.reload()" style="background:#666">2. Đăng xuất</button>
        <hr>
        <p><strong>3. Nhập thông tin:</strong></p>
        <input type="text" id="cccd" placeholder="Nhập CCCD (là bắc buộc)">
        <button onclick="alert('Đã lưu CCCD!')">Lưu</button>
        <hr>
        <p><strong>4. Đặt lại mật khẩu:</strong></p>
        <input type="password" placeholder="1. Mật khẩu hiện tại">
        <input type="password" placeholder="2. Mật khẩu mới">
        <input type="password" placeholder="3. Xác nhận mật khẩu mới">
        <button onclick="alert('Đã đổi mật khẩu thành công!')">Ô xác nhận đổi mật khẩu</button>
        <button onclick="goPage('homeHS')" style="background:#666; margin-top:20px">Quay lại</button>
    </div>

    <!-- TRANG 1: BAN GIÁM HIỆU -->
    <div id="pageBGH" class="page">
        <div class="status-tag" style="background:#000; color:#fff">ADMIN: BGH</div>
        <h3>QUẢN LÝ NHÀ TRƯỜNG VÀ TIẾP NHẬN PHẢN ÁNH</h3>
        <div class="box-info"><strong>1. Sĩ số báo lại:</strong><br><div id="bghView"><i>(Đang chờ báo cáo sĩ số từ các thầy cô...)</i></div></div>
        <p><strong>2. Phê duyệt & Trả lời:</strong></p>
        <textarea placeholder="Trả lời thắc mắc của học sinh..."></textarea>
        <button onclick="alert('Gửi và đã gửi thành công!')">Ô GỬI</button>
        <p><strong>3. Sự kiện:</strong></p>
        <input type="text" placeholder="Ghi sự kiện gửi thông báo...">
        <button onclick="alert('Đã gửi thông báo đến hòm thư học sinh!')">GỬI THÔNG BÁO</button>
        <button onclick="location.reload()" style="background:#666; margin-top:30px">Đăng xuất</button>
    </div>

    <!-- TRANG 2: GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <div class="status-tag" style="background:green; color:#fff">GIÁO VIÊN CHỦ NHIỆM</div>
        <h3>CHÀO THẦY MR QUANG MỘT NGÀY TỐT ĐẸP</h3>
        <div class="box-info">
            <strong>1. Nhận điểm danh lớp 12A3:</strong><br>
            - Sùng A Chiều: Đã đi học (Hình ảnh) lúc 6:30 9/4/2024
        </div>
        <p><strong>2. Gửi báo cáo sĩ số lên BGH:</strong></p>
        <input type="text" id="gvSiso" placeholder="Ví dụ: Mùa Hà Quang 12A3 47/47 đủ">
        <button onclick="gvGui()" style="background:green">GỬI LÊN BGH</button>
        <hr>
        <p><strong>3. Thông báo cho lớp:</strong></p>
        <textarea placeholder="Nhập dữ liệu gửi tới hòm thư học sinh của lớp..."></textarea>
        <button onclick="alert('Đã gửi xong!')">GỬI THÔNG BÁO</button>
        <button onclick="location.reload()" style="background:#666; margin-top:20px">Đăng xuất</button>
    </div>

    <!-- TRANG 3: BÁO CƠM (Quản lý) -->
    <div id="pageCom" class="page">
        <div class="status-tag" style="background:#e67e22; color:#fff">QUẢN LÝ BÁO CƠM</div>
        <h3>HÃY LÀM VIỆC CẨN THẬN NHÉ BÁC SẠCH CƠM NGON</h3>
        <div class="box-info"><strong>1. Số lượng ăn hôm nay:</strong><br>Lớp 12A3 23 bạn đã báo làm 23 xuất</div>
        <div class="box-info">
            <strong>2. Thời gian ăn:</strong><br>
            - Trưa: 11h45 - 12h30<br>
            - Chiều: 16h20 - 17h30
        </div>
        <button onclick="location.reload()" style="background:#666; margin-top:30px">Đăng xuất</button>
    </div>

</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if(id==='pageBGH'){
            const d = localStorage.getItem('siso_live');
            if(d) document.getElementById('bghView').innerHTML = d;
        }
    }

    function handleLogin() {
        const u = document.getElementById('u').value, p = document.getElementById('p').value;
        if(u==='BGH THPTMCC2025' && p==='THPT1983@') goPage('pageBGH');
        else if(u==='muahaquangdz' && p==='Mrquang@123') goPage('pageGV');
        else if(u==='Baocomngon' && p==='ankhongvanan') goPage('pageCom');
        else {
            const s = localStorage.getItem('u_'+u);
            if(s && JSON.parse(s).pass === p) {
                document.getElementById('hiHS').innerText = "Xin chào " + JSON.parse(s).name + "!";
                document.getElementById('pName').innerText = "1. Học sinh: " + JSON.parse(s).name;
                goPage('homeHS');
            } else alert('Sai thông tin hoặc chưa đăng ký!');
        }
    }

    function handleReg() {
        const u = document.getElementById('regU').value, n = document.getElementById('regName').value, p = document.getElementById('regP').value;
        if(!u || !p || !n) return alert('Hãy điền đủ thông tin!');
        localStorage.setItem('u_'+u, JSON.stringify({pass:p, name:n}));
        alert('Đăng ký thành công! Hãy đăng nhập.');
        goPage('loginPage');
    }

    function gvGui() {
        const val = document.getElementById('gvSiso').value;
        if(!val) return alert('Hãy nhập sĩ số!');
        localStorage.setItem('siso_live', '<strong>Báo cáo từ thầy Quang:</strong> ' + val);
        alert('Đã gửi lên Ban Giám Hiệu!');
    }

    function guiXinNghi() {
        if(!document.getElementById('leaveReason').value) return alert('Phải có lý do!');
        document.getElementById('leaveStatus').style.display = 'block';
        setTimeout(() => {
            alert('BẠN ĐƯỢC NGHỈ THEO QUY ĐỊNH SAU THỜI GIAN QUAY LẠI TRƯỜNG HỌC BÀI');
            goPage('homeHS');
        }, 3000);
    }

    function talkAI() {
        const a = prompt("Bạn cần tôi giúp gì không?");
        if(a) alert("Ai chưa thể sử dụng chính thức");
    }
</script>
</body>
</html>
"""

components.html(html_10_score, height=850, scrolling=True)
