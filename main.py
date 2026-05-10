import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

html_live_system = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        :root { --primary: #d32f2f; --bg: #f5f5f5; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); }
        .container { max-width: 450px; margin: auto; min-height: 100vh; background: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .page { display: none; padding: 20px; animation: fadeIn 0.3s; }
        .active { display: block; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .header-school { text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net'); background-size: cover; padding: 30px 20px; color: white; }
        input, textarea, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box; }
        button { background: var(--primary); color: white; font-weight: bold; border: none; cursor: pointer; }
        .admin-tag { background: #333; color: gold; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        .data-box { background: #f0f7ff; padding: 15px; border-radius: 10px; margin: 10px 0; font-size: 14px; border-left: 5px solid #2196f3; }
    </style>
</head>
<body>

<div class="container">
    <!-- 1. ĐĂNG NHẬP -->
    <div id="loginPage" class="page active">
        <div class="header-school">
            <img src="https://wikimedia.org" style="width:40px">
            <h3>THPT MÙ CANG CHẢI</h3>
        </div>
        <div style="padding: 20px;">
            <input type="text" id="user" placeholder="Tên tài khoản">
            <input type="password" id="pass" placeholder="Mật khẩu">
            <button onclick="checkLogin()">ĐĂNG NHẬP</button>
        </div>
    </div>

    <!-- 2. TRANG BGH -->
    <div id="pageBGH" class="page">
        <span class="admin-tag">QUẢN TRỊ VIÊN</span>
        <h3>QUẢN LÝ NHÀ TRƯỜNG</h3>
        <p><strong>1. Sĩ số báo cáo từ Giáo viên:</strong></p>
        <div id="bghViewData" class="data-box">
            <i>Đang chờ giáo viên gửi báo cáo...</i>
        </div>
        <p><strong>2. Phản hồi học sinh:</strong></p>
        <textarea placeholder="Nhập lời giải đáp..."></textarea>
        <button onclick="alert('Đã gửi phản hồi!')">GỬI TRẢ LỜI</button>
        <button style="background:#666" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>

    <!-- 3. TRANG GIÁO VIÊN (Mr Quang) -->
    <div id="pageGV" class="page">
        <span class="admin-tag">GIÁO VIÊN: MÙA HÀ QUANG</span>
        <h3>GỬI BÁO CÁO SĨ SỐ</h3>
        <input type="text" id="gvClass" value="12A3" readonly>
        <input type="text" id="gvSiso" placeholder="Nhập sĩ số (VD: 47/47 đủ)">
        <button onclick="gvGuiBaoCao()" style="background:#2e7d32">GỬI BÁO CÁO LÊN BGH</button>
        <hr>
        <button style="background:#666" onclick="location.reload()">ĐĂNG XUẤT</button>
    </div>
</div>

<script>
    function goPage(id) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        
        // Nếu vào trang BGH, cập nhật dữ liệu mới nhất từ bộ nhớ
        if(id === 'pageBGH') {
            const data = localStorage.getItem('siso_report');
            if(data) {
                document.getElementById('bghViewData').innerHTML = data;
            }
        }
    }

    function checkLogin() {
        const u = document.getElementById('user').value;
        const p = document.getElementById('pass').value;
        if(u === 'BGH THPTMCC2025' && p === 'THPT1983@') goPage('pageBGH');
        else if(u === 'muahaquangdz' && p === 'Mrquang@123') goPage('pageGV');
        else alert('Sai tài khoản hoặc mật khẩu!');
    }

    function gvGuiBaoCao() {
        const lop = document.getElementById('gvClass').value;
        const siso = document.getElementById('gvSiso').value;
        if(!siso) return alert('Vui lòng nhập sĩ số!');
        
        const report = `<strong>Lớp ${lop}:</strong> ${siso} <br><small>Gửi lúc: ${new Date().toLocaleTimeString()}</small>`;
        
        // Lưu vào bộ nhớ trình duyệt
        localStorage.setItem('siso_report', report);
        alert('Đã gửi báo cáo lên Ban Giám Hiệu thành công!');
    }
</script>
</body>
</html>
"""

components.html(html_live_system, height=800, scrolling=True)
