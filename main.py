import streamlit as st
from datetime import datetime

# --- CẤU HÌNH ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫")

# 1. KHỞI TẠO DỮ LIỆU
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "123", "name": "Thầy Chủ Nhiệm", "role": "admin_gv"},
        "adminbaoan": {"password": "12345678", "name": "Quản lý Bán trú", "role": "admin_an"}
    }
if 'lich_su' not in st.session_state: st.session_state.lich_su = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# 2. TRANG ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ TÀI KHOẢN")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        lop = st.selectbox("Lớp:", classes)
        user_id = st.text_input("Tên tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if user_id and pwd and name:
                st.session_state.users[user_id] = {"password": pwd, "name": name, "class": lop, "role": "student"}
                st.success("✅ Đăng ký thành công! Hãy quay lại đăng nhập.")
            else: st.error("Điền thiếu thông tin!")
    if st.button("Quay lại Đăng nhập"): st.session_state.page = "login"; st.rerun()

# 3. TRANG ĐĂNG NHẬP
def login_page():
    st.title("🏫 THPT MÙ CANG CHẢI")
    user_input = st.text_input("Tên tài khoản:")
    pwd_input = st.text_input("Mật khẩu:", type="password")
    if st.button("Đăng nhập", use_container_width=True):
        if user_input in st.session_state.users and st.session_state.users[user_input]["password"] == pwd_input:
            st.session_state.logged_in = True
            st.session_state.user_info = st.session_state.users[user_input]
            st.rerun()
        else: st.error("Sai tài khoản hoặc mật khẩu!")
    if st.button("Đăng ký tài khoản mới", use_container_width=True): st.session_state.page = "register"; st.rerun()

# 4. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if 'class' in user: st.sidebar.write(f"Lớp: {user['class']}")
    if st.sidebar.button("Đăng xuất"): st.session_state.logged_in = False; st.rerun()

    # --- GIAO DIỆN HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG THÔNG TIN HỌC SINH")
        tab1, tab2, tab3, tab4 = st.tabs(["Điểm danh", "Báo ăn", "Xin nghỉ", "Phản ánh"])
        
        with tab1:
            if st.button("📍 XÁC NHẬN CÓ MẶT"):
                st.session_state.lich_su.append({"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Đã đi học", "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.success("✅ Đã điểm danh thành công!")
        
        with tab2:
            thu = st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Lựa chọn:", ["Đăng ký ăn", "Xin nghỉ ăn bữa này"])
            if st.button("Gửi báo cáo ăn"):
                st.session_state.lich_su.append({"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.success("🍱 Đã báo cơm thành công!")

        with tab3:
            ly_do = st.text_area("Nhập lý do xin nghỉ:")
            if st.button("Gửi đơn cho thầy cô"):
                st.session_state.lich_su.append({"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.info("⏳ Đã gửi đơn. Chờ thầy cô phê duyệt.")

        with tab4:
            thac_mac = st.text_area("Nhập thắc mắc hoặc phản ánh của bạn:")
            if st.button("Gửi hòm thư góp ý"):
                st.session_state.lich_su.append({"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": thac_mac, "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.success("📩 Đã gửi ý kiến đến nhà trường.")

    # --- GIAO DIỆN ADMIN GIÁO VIÊN ---
    elif user.get('role') == "admin_gv":
        st.title("📂 HÒM THƯ QUẢN LÝ GIÁO VIÊN")
        st.subheader("1. Danh sách học sinh đi học")
        chon_lop = st.selectbox("Xem theo lớp:", [f"{k}A{i}" for k in [10,11,12] for i in range(1,10)])
        ds_lop = [item for item in st.session_state.lich_su if item['Loại'] == "Điểm danh" and item['Lớp'] == chon_lop]
        st.table(ds_lop if ds_lop else "Chưa có dữ liệu lớp này")

        st.subheader("2. Hòm thư Xin nghỉ & Phản ánh")
        ds_don = [item for item in st.session_state.lich_su if item['Loại'] in ["Xin nghỉ", "Phản ánh"]]
        st.table(ds_don if ds_don else "Hòm thư đang trống")

    # --- GIAO DIỆN ADMIN BÁO ĂN ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        st.subheader("Danh sách học sinh Báo ăn / Nghỉ ăn")
        ds_an = [item for item in st.session_state.lich_su if item['Loại'] == "Báo ăn"]
        st.table(ds_an if ds_an else "Chưa có dữ liệu báo ăn")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if 'page' not in st.session_state or st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
