import streamlit as st
from datetime import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫")

# 1. KHỞI TẠO DỮ LIỆU (Lưu tạm thời trong phiên làm việc)
if 'users' not in st.session_state:
    st.session_state.users = {"admin": {"password": "123", "name": "Ban Giám Khảo", "class": "BTC"}}
if 'page' not in st.session_state: st.session_state.page = "login"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# 2. GIAO DIỆN ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ TÀI KHOẢN")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        dob = st.date_input("Ngày tháng năm sinh:", min_value=datetime(2000, 1, 1))
        classes = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        lop = st.selectbox("Lớp:", classes)
        user_id = st.text_input("Tên tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if user_id and pwd and name:
                st.session_state.users[user_id] = {"password": pwd, "name": name, "class": lop}
                st.success("✅ Đăng ký thành công! Hãy quay lại đăng nhập.")
            else: st.error("Vui lòng điền đủ thông tin!")
    if st.button("Quay lại Đăng nhập"):
        st.session_state.page = "login"
        st.rerun()

# 3. GIAO DIỆN ĐĂNG NHẬP
def login_page():
    st.title("🏫 TRƯỜNG THPT MÙ CANG CHẢI")
    user_input = st.text_input("Tên tài khoản:")
    pwd_input = st.text_input("Mật khẩu:", type="password")
    if st.button("Đăng nhập", use_container_width=True):
        if user_input in st.session_state.users and st.session_state.users[user_input]["password"] == pwd_input:
            st.session_state.logged_in = True
            st.session_state.user_info = st.session_state.users[user_input]
            st.rerun()
        else: st.error("Sai tài khoản hoặc mật khẩu!")
    if st.button("Chưa có tài khoản? Đăng ký ngay", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()

# 4. GIAO DIỆN CHÍNH (DASHBOARD)
def main_dashboard():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    st.sidebar.write(f"🏫 Lớp: {user['class']}")
    if st.sidebar.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📍 HỆ THỐNG QUẢN LÝ")
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1: 
        if st.button("📍 Điểm danh", use_container_width=True): st.success("✅ Đã gửi điểm danh!")
    with col2: 
        if st.button("🍱 Báo ăn", use_container_width=True): st.session_state.sub = "an"
    with col3: 
        if st.button("📚 TKB", use_container_width=True): st.session_state.sub = "tkb"
    with col4: 
        if st.button("📝 Xin nghỉ", use_container_width=True): st.session_state.sub = "nghi"
    with col5: 
        if st.button("🤖 Trợ giúp", use_container_width=True): st.session_state.sub = "ai"

    if 'sub' in st.session_state:
        st.divider()
        if st.session_state.sub == "an":
            st.write("🍱 **Báo ăn bán trú**")
            st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            st.radio("Lựa chọn:", ["Đăng ký ăn", "Xin nghỉ ăn bữa này"])
            if st.button("Gửi báo cáo cơm"): st.success("✅ Đã báo cơm thành công!")
        elif st.session_state.sub == "tkb":
            st.write("📚 **Thời khóa biểu Sáng/Chiều**")
            st.table({"Buổi": ["Sáng", "Chiều"], "T1": ["Toán", "Sử"], "T2": ["Văn", "Địa"], "T3": ["Anh", "GDCD"], "T4": ["Lý", "CN"], "T5": ["Hóa", "SHL"]})
        elif st.session_state.sub == "nghi":
            st.write("📝 **Đơn xin nghỉ Online**")
            st.text_area("Lý do nghỉ:")
            if st.button("Gửi thầy chủ nhiệm"): st.warning("⏳ Chờ thầy giáo chủ nhiệm xác nhận...")
        elif st.session_state.sub == "ai":
            hoi = st.text_input("🤖 Hỏi AI bất cứ điều gì về trường:")
            if hoi: st.write("AI: Tôi đã ghi nhận câu hỏi và sẽ phản hồi sớm!")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_dashboard()
