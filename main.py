import streamlit as st
from datetime import datetime
import pandas as pd

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ thống Quản lý THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# 1. KHỞI TẠO DỮ LIỆU (CẬP NHẬT TÀI KHOẢN ADMIN)
if 'users' not in st.session_state:
    st.session_state.users = {
        "thptmcc_admin": {"password": "giaovien2024", "name": "Ban Giám Hiệu - THPT Mù Cang Chải", "role": "admin_gv"},
        "bantru_mcc": {"password": "comngon2024", "name": "Phòng Quản Lý Bán Trú", "role": "admin_an"}
    }

if 'lich_su' not in st.session_state: st.session_state.lich_su = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 2. TRANG ĐĂNG KÝ
def registration_page():
    st.markdown("<h2 style='text-align: center;'>📝 ĐĂNG KÝ HỌC SINH MỚI</h2>", unsafe_allow_html=True)
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        lop = st.selectbox("Lớp học:", classes)
        user_id = st.text_input("Tên tài khoản mong muốn:")
        pwd = st.text_input("Mật khẩu tự chọn:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if user_id and pwd and name:
                st.session_state.users[user_id] = {"password": pwd, "name": name, "class": lop, "role": "student"}
                st.success("✅ Đăng ký thành công! Hãy quay lại trang Đăng nhập.")
            else: st.error("Bạn vui lòng điền đầy đủ các thông tin!")
    if st.button("Quay lại Đăng nhập"):
        st.session_state.page = "login"
        st.rerun()

# 3. TRANG ĐĂNG NHẬP (CẬP NHẬT GIAO DIỆN TRÊN)
def login_page():
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TRƯỜNG THPT MÙ CANG CHẢI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hệ thống quản lý học sinh và hỗ trợ bán trú trực tuyến</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_input = st.text_input("Tài khoản (Mã HS hoặc Admin):")
        pwd_input = st.text_input("Mật khẩu:", type="password")
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if user_input in st.session_state.users and st.session_state.users[user_input]["password"] == pwd_input:
                st.session_state.logged_in = True
                st.session_state.user_info = st.session_state.users[user_input]
                st.rerun()
            else: st.error("Thông tin đăng nhập không chính xác!")
        
        st.write("---")
        if st.button("BẠN LÀ HỌC SINH MỚI? ĐĂNG KÝ TẠI ĐÂY", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

# 4. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if 'class' in user: st.sidebar.info(f"Lớp: {user['class']}")
    
    if st.sidebar.button("ĐĂNG XUẤT", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- GIAO DIỆN HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG THÔNG TIN HỌC SINH")
        t1, t2, t3, t4 = st.tabs(["📍 Điểm danh", "🍱 Báo ăn", "📝 Xin nghỉ", "📩 Phản ánh"])
        
        with t1:
            if st.button("BẤM ĐỂ ĐIỂM DANH CÓ MẶT"):
                st.session_state.lich_su.append({"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Đã đi học", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Thành công"})
                st.success(f"✅ Chào {user['name']}, bạn đã điểm danh thành công!")
        
        with t2:
            thu = st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Lựa chọn:", ["Đăng ký ăn", "Xin nghỉ ăn bữa này"])
            if st.button("Gửi báo cáo cơm"):
                st.session_state.lich_su.append({"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã báo"})
                st.success("🍱 Thông tin báo ăn đã được gửi!")

        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            if st.button("Gửi đơn thầy chủ nhiệm"):
                st.session_state.lich_su.append({"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.info("📩 Đơn đã gửi. Hãy chờ thầy cô xác nhận nhé.")

        with t4:
            thac_mac = st.text_area("Nội dung phản ánh:")
            if st.button("Gửi hòm thư"):
                st.session_state.lich_su.append({"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": thac_mac, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã nhận"})
                st.success("📩 Ý kiến của bạn đã được chuyển tới nhà trường.")

    # --- GIAO DIỆN ADMIN GIÁO VIÊN ---
    elif user.get('role') == "admin_gv":
        st.title("📂 HÒM THƯ QUẢN LÝ GIÁO VIÊN")
        st.subheader("1. Kiểm tra sĩ số lớp")
        classes_list = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        chon_lop = st.selectbox("Lọc lớp:", classes_list)
        ds_lop = [item for item in st.session_state.lich_su if item['Loại'] == "Điểm danh" and item['Lớp'] == chon_lop]
        if ds_lop: st.table(ds_lop)
        else: st.write("Lớp này chưa có ai điểm danh.")

        st.subheader("2. Duyệt đơn xin nghỉ & Phản ánh")
        ds_don = [item for item in st.session_state.lich_su if item['Loại'] in ["Xin nghỉ", "Phản ánh"]]
        if ds_don:
            st.dataframe(ds_don)
            if st.button("PHÊ DUYỆT TẤT CẢ ĐƠN"):
                for item in st.session_state.lich_su:
                    if item['Loại'] == "Xin nghỉ": item['Trạng thái'] = "✅ Đã duyệt"
                st.success("Đã duyệt toàn bộ đơn nghỉ.")
        else: st.write("Không có đơn thư nào.")

    # --- GIAO DIỆN ADMIN BÁO ĂN ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ SUẤT ĂN BÁN TRÚ")
        ds_an = [item for item in st.session_state.lich_su if item['Loại'] == "Báo ăn"]
        if ds_an:
            st.table(ds_an)
            tong_an = sum(1 for x in ds_an if "Đăng ký ăn" in x['Nội dung'])
            st.metric("Tổng suất ăn cần chuẩn bị", f"{tong_an} suất")
        else: st.write("Hôm nay chưa có học sinh nào báo cơm.")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
