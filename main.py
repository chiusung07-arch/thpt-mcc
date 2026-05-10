import streamlit as st

# --- CẤU HÌNH GIAO DIỆN CHUẨN APP ---
st.set_page_config(page_title="Hệ thống THPT Mù Cang Chải", layout="centered")

# CSS ĐỂ GIAO DIỆN "RA TRÒ" (Nút to, màu sắc đúng chuẩn, tràn màn hình)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 4em; 
        font-weight: bold; font-size: 16px; background-color: #d32f2f; color: white;
        border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input { border-radius: 10px; height: 3.5em; }
    .school-header {
        text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://vnecdn.net');
        background-size: cover; padding: 40px 20px; color: white; border-radius: 0 0 25px 25px; margin-bottom: 20px;
    }
    .robot-chat {
        position: fixed; bottom: 20px; right: 20px; text-align: center; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- QUẢN LÝ CHUYỂN TRANG ---
if 'page' not in st.session_state: st.session_state.page = 'login'
if 'user_name' not in st.session_state: st.session_state.user_name = ""

def switch_page(p):
    st.session_state.page = p
    st.rerun()

# --- 1. TRANG ĐĂNG NHẬP (TRANG ĐẦU TIÊN) ---
if st.session_state.page == 'login':
    st.markdown('<div class="school-header"><img src="https://wikimedia.org" width="60"><br><h1>Xin chào đến với Trường THPT Mù Cang Chải</h1></div>', unsafe_allow_html=True)
    
    u = st.text_input("1. Tên tài khoản", key="u1")
    p = st.text_input("2. Mật khẩu", type="password", key="p1")
    m = st.text_input("3. Mã học sinh", key="m1")
    
    if st.button("ĐĂNG NHẬP"):
        if u == 'BGH THPTMCC2025' and p == 'THPT1983@': switch_page('bgh')
        elif u == 'muahaquangdz' and p == 'Mrquang@123': switch_page('giaovien')
        elif u == 'Baocomngon' and p == 'ankhongvanan': switch_page('baocom_admin')
        else:
            st.session_state.user_name = u
            switch_page('home_hs')

    if st.button("4. Mục đăng ký tài khoản"): switch_page('register')

# --- 2. TRANG ĐĂNG KÝ ---
elif st.session_state.page == 'register':
    st.subheader("BẠN PHẢI LÀ HỌC SINH TRƯỜNG THPT MÙ CANG CHẢI")
    st.text_input("2. Tên tài khoản")
    st.text_input("3. Họ và tên học sinh")
    st.selectbox("4. Lớp", [f"10A{i}" for i in range(1,10)] + [f"11A{i}" for i in range(1,8)] + [f"12A{i}" for i in range(1,8)])
    st.text_input("5. Mật khẩu", type="password")
    st.text_input("6. Email (bắt buộc)")
    st.text_input("7. Số điện thoại")
    st.selectbox("8. Loại hình học sinh", ["Học sinh bán trú", "Học sinh ngoại trú"])
    
    if st.button("10. XÁC NHẬN ĐĂNG KÝ"):
        st.success("Đăng ký thành công!")
        time.sleep(1)
        switch_page('login')
    if st.button("Quay lại"): switch_page('login')

# --- 3. TRANG CHỦ HỌC SINH ---
elif st.session_state.page == 'home_hs':
    st.markdown(f"<h2 style='color:#d32f2f;'>Xin chào {st.session_state.user_name} và chúc bạn có một ngày vui vẻ</h2>", unsafe_allow_html=True)
    
    if st.button("1. Mục điểm danh"):
        st.warning("Yêu cầu chụp bất cứ chỗ nào xung quanh lớp học và gửi cho giáo viên")
    if st.button("2. Mục báo cơm"): switch_page('hs_com')
    if st.button("3. Mục xin nghỉ"): switch_page('hs_nghi')
    if st.button("4. Phản hồi ý kiến"): switch_page('hs_phanhoi')
    if st.button("5. Hòm thư"): switch_page('hs_homthu')
    if st.button("Thông tin tài khoản"): switch_page('hs_info')
    if st.button("Đăng xuất"): switch_page('login')

    # Trợ lý ảo Robot
    st.markdown('---')
    st.markdown('<div style="text-align:center;"><img src="https://flaticon.com" width="80"><br><b>Bạn cần tôi giúp gì không?</b></div>', unsafe_allow_html=True)
    chat = st.text_input("Nhập tin nhắn vào đây...")
    if chat: st.error("Ai chưa thể sử dụng chính thức")

# --- 4. TRANG BAN GIÁM HIỆU ---
elif st.session_state.page == 'bgh':
    st.header("Quản lý nhà trường và tiếp nhận phản ánh")
    st.info("1. Sĩ số báo lại: Mùa Hà Quang 12A3 47/47 đủ")
    st.text_area("2. Mục phê duyệt và trả lời phản ánh học sinh")
    if st.button("Gửi"): st.success("Đã gửi thành công")
    st.text_input("3. Sự kiện gửi thông báo đến hòm thư học sinh")
    if st.button("Đăng xuất"): switch_page('login')

# --- 5. TRANG GIÁO VIÊN ---
elif st.session_state.page == 'giaovien':
    st.header("Chào thầy Mr Quang một ngày tốt đẹp")
    st.write("1. Nhận điểm danh lớp 12A3 (VD: Sùng A Chiều đã đi học 6:30 9/4/2024)")
    st.text_area("2. Thông báo đến học sinh của lớp gửi tới hòm thư")
    if st.button("Gửi thông báo"): st.success("Đã gửi xong")
    if st.button("Đăng xuất"): switch_page('login')

# --- 6. TRANG BÁO CƠM ADMIN ---
elif st.session_state.page == 'baocom_admin':
    st.header("Hãy làm việc cẩn thận nhé bác sạch cơm ngon")
    st.write("1. Số lượng ăn hôm nay (Lớp 12A3 23 bạn báo làm 23 suất)")
    st.write("2. Thời gian ăn: Trưa (11:45-12:30) - Chiều (16:20-17:30)")
    if st.button("Đăng xuất"): switch_page('login')

# --- TRANG THÔNG TIN TÀI KHOẢN (CCCD) ---
elif st.session_state.page == 'hs_info':
    st.subheader("Thông tin tài khoản")
    st.write(f"Học sinh: {st.session_state.user_name}")
    st.text_input("Nhập CCCD (bắt buộc)")
    st.password_input("Mật khẩu hiện tại")
    st.password_input("Mật khẩu mới")
    if st.button("Xác nhận đổi mật khẩu"): st.success("Thành công")
    if st.button("Quay lại"): switch_page('home_hs')

# --- CÁC TRANG CON KHÁC ---
elif st.session_state.page == 'hs_com':
    st.subheader("Mục báo cơm")
    if st.button("Báo cơm cho tôi hôm nay"): st.success("Đã báo cơm")
    st.checkbox("Xin nghỉ bữa trưa")
    st.checkbox("Xin nghỉ bữa tối")
    if st.button("Quay lại"): switch_page('home_hs')

elif st.session_state.page == 'hs_nghi':
    st.subheader("Mục xin nghỉ")
    st.text_area("Lý do xin nghỉ (Phải chính đáng)")
    if st.button("Gửi đơn"): st.info("Đang chờ thầy giáo chủ nhiệm duyệt 5 phút có kết quả...")
    if st.button("Quay lại"): switch_page('home_hs')
