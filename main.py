import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# 1. HÀM XỬ LÝ DỮ LIỆU (Lưu vĩnh viễn vào CSV)
def load_users():
    if os.path.exists("hoc_sinh.csv"):
        return pd.read_csv("hoc_sinh.csv").to_dict('records')
    return []

def save_user_to_csv(new_user):
    users = load_users()
    users.append(new_user)
    pd.DataFrame(users).to_csv("hoc_sinh.csv", index=False)

# 2. KHỞI TẠO BIẾN TẠM
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"
if 'lich_su' not in st.session_state: st.session_state.lich_su = []

# 3. GIAO DIỆN ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH MỚI")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        lop = st.selectbox("Lớp học:", classes)
        user_id = st.text_input("Tên tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if user_id and pwd and name:
                save_user_to_csv({"username": user_id, "password": pwd, "name": name, "class": lop, "role": "student"})
                st.success("✅ Đăng ký thành công! Hãy quay lại đăng nhập.")
            else: st.error("Vui lòng điền đủ thông tin!")
    if st.button("Quay lại Đăng nhập"):
        st.session_state.page = "login"; st.rerun()

# 4. GIAO DIỆN ĐĂNG NHẬP
def login_page():
    st.title("🏫 TRƯỜNG THPT MÙ CANG CHẢI")
    u_in = st.text_input("Tên tài khoản:")
    p_in = st.text_input("Mật khẩu:", type="password")
    if st.button("ĐĂNG NHẬP", use_container_width=True):
        users = load_users()
        user_found = next((u for u in users if str(u['username']) == u_in and str(u['password']) == p_in), None)
        if user_found:
            st.session_state.logged_in = True
            st.session_state.user_info = user_found
            st.rerun()
        else: st.error("Sai tài khoản hoặc mật khẩu!")
    if st.button("Chưa có tài khoản? Đăng ký ngay"):
        st.session_state.page = "register"; st.rerun()

# 5. GIAO DIỆN CHÍNH (DASHBOARD)
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if 'class' in user: st.sidebar.info(f"Lớp: {user['class']}")
    if st.sidebar.button("ĐĂNG XUẤT"):
        st.session_state.logged_in = False; st.rerun()

    if user.get('role') == "student":
        st.title("📍 CỔNG THÔNG TIN HỌC SINH")
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Báo ăn", "Xin nghỉ", "Phản ánh"])
        with t1:
            if st.button("XÁC NHẬN CÓ MẶT"):
                st.session_state.lich_su.append({"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Có mặt", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Thành công"})
                st.success("✅ Đã điểm danh!")
        with t2:
            thu = st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Chọn:", ["Đăng ký ăn", "Xin nghỉ ăn"])
            if st.button("Gửi báo cơm"):
                st.session_state.lich_su.append({"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã báo"})
                st.success("🍱 Đã gửi!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            if st.button("Gửi đơn"):
                st.session_state.lich_su.append({"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.info("📩 Đơn đã gửi!")
        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi phản ánh"):
                st.session_state.lich_su.append({"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": yk, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã gửi"})
                st.success("📩 Đã ghi nhận!")

    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ GIÁO VIÊN")
        classes_list = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        chon_lop = st.selectbox("Lọc lớp:", classes_list)
        ds = [i for i in st.session_state.lich_su if i['Loại'] == "Điểm danh" and i['Lớp'] == chon_lop]
        st.table(ds if ds else [])
        st.subheader("Hòm thư đơn từ")
        st.table([i for i in st.session_state.lich_su if i['Loại'] in ["Xin nghỉ", "Phản ánh"]])

    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        st.table([i for i in st.session_state.lich_su if i['Loại'] == "Báo ăn"])

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
