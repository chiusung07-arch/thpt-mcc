import streamlit as st
import time

# --- CẤU HÌNH GIAO DIỆN HIỆN ĐẠI ---
st.set_page_config(page_title="MCC Smart School", page_icon="🏮", layout="wide")

# CSS tạo hiệu ứng chuyên nghiệp
st.markdown("""
    <style>
    .stApp { background: #fdfdfd; }
    .main-header {
        background: linear-gradient(135deg, #d32f2f 0%, #ff5252 100%);
        padding: 60px; text-align: center; color: white; border-radius: 0 0 50px 50px;
        box-shadow: 0 10px 30px rgba(211, 47, 47, 0.3);
    }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 3.5em; font-weight: bold;
        transition: 0.3s; border: none; background: white; color: #d32f2f;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        background: #d32f2f; color: white; transform: translateY(-3px);
    }
    .card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if 'step' not in st.session_state: st.session_state.step = 'login'

def navigate(s):
    st.session_state.step = s
    st.rerun()

# --- GIAO DIỆN THEO Ý TƯỞNG MỚI ---
if st.session_state.step == 'login':
    st.markdown('<div class="main-header"><h1>🏫 THPT MÙ CANG CHẢI</h1><p>Hệ thống quản lý thông minh thế hệ mới</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            u = st.text_input("👤 Tên tài khoản", placeholder="Nhập username...")
            p = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập password...")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 BẮT ĐẦU TRẢI NGHIỆM"):
                if u == 'BGH THPTMCC2025' and p == 'THPT1983@': navigate('admin')
                else: navigate('dashboard')
            
            st.markdown("<p style='text-align:center; font-size:14px; color:#888;'>Chưa có tài khoản? <b style='color:#d32f2f;'>Đăng ký ngay</b></p>", unsafe_allow_html=True)

elif st.session_state.step == 'dashboard':
    st.markdown("<h2 style='text-align:left; color:#333;'>Xin chào Học sinh! 👋</h2>", unsafe_allow_html=True)
    st.write("Hôm nay bạn muốn thực hiện công việc gì?")
    
    # Grid Menu hiện đại
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.button("📸 Điểm danh"): st.toast("Đang bật Camera nhận diện...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="margin-top:20px;">', unsafe_allow_html=True)
        if st.button("🍱 Báo cơm"): navigate('com')
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.button("📝 Xin nghỉ"): navigate('nghi')
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="margin-top:20px;">', unsafe_allow_html=True)
        if st.button("📩 Hòm thư"): st.toast("Bạn có 2 tin nhắn mới")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.button("💡 Phản hồi"): st.info("Gửi thắc mắc đến BGH")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="margin-top:20px;">', unsafe_allow_html=True)
        if st.button("⚙️ Cài đặt"): navigate('profile')
        st.markdown('</div>', unsafe_allow_html=True)

    # Robot Trợ Lý thông minh hơn
    st.sidebar.markdown("### 🤖 Trợ lý MCC-Bot")
    st.sidebar.info("Xin chào! Tôi có thể giúp bạn báo cơm hoặc làm đơn xin nghỉ nhanh chóng.")
    chat = st.sidebar.text_input("Hỏi tôi bất cứ điều gì...")
    if chat: st.sidebar.error("Xin lỗi, tính năng AI đang được bảo trì!")

    if st.button("❌ Đăng xuất", key="logout"): navigate('login')

# --- TRANG QUẢN TRỊ (ADMIN) ---
elif st.session_state.step == 'admin':
    st.title("📊 Bảng điều khiển Ban Giám Hiệu")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sĩ số hôm nay", "47/47", "Đủ (12A3)")
    with col2:
        st.metric("Số suất ăn bán trú", "125 suất", "+12%")
    
    st.text_area("Phản hồi nhanh cho học sinh")
    if st.button("Gửi thông báo toàn trường"): st.success("Đã phát tin!")
    if st.button("Quay lại"): navigate('login')

# --- TRANG CON ---
else:
    st.write(f"Tính năng **{st.session_state.step}** đang được tối ưu hóa.")
    if st.button("Quay lại trang chủ"): navigate('dashboard')
