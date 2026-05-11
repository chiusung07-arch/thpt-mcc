import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- TỰ ĐỘNG KHỞI TẠO FILE DỮ LIỆU (Để không bị lỗi đỏ) ---
for f in ["hoc-sinh.csv", "nhat-ky.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=["username","password","name","class","role"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái"]).to_csv(f, index=False)

def load_data(file_name):
    try: return pd.read_csv(file_name).to_dict('records')
    except: return []

def save_data(file_name, new_entry):
    data = load_data(file_name)
    data.append(new_entry)
    pd.DataFrame(data).to_csv(file_name, index=False)

# KHỞI TẠO BIẾN SESSION
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = [f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)]
        lop = st.selectbox("Lớp học:", classes)
        user_id = st.text_input("Tên tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if user_id and pwd and name:
                save_data("hoc-sinh.csv", {"username": user_id, "password": pwd, "name": name, "class": lop, "role": "student"})
                st.success("✅ Đăng ký thành công! Hãy quay lại đăng nhập.")
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

# 2. TRANG ĐĂNG NHẬP
def login_page():
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TRƯỜNG THPT MÙ CANG CHẢI</h1>", unsafe_allow_html=True)
    u_in = st.text_input("Tên tài khoản:")
    p_in = st.text_input("Mật khẩu:", type="password")
    if st.button("ĐĂNG NHẬP", use_container_width=True):
        if u_in == "thptmcc_admin" and p_in == "giaovien2024":
            st.session_state.logged_in = True; st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin_gv"}
            st.rerun()
        elif u_in == "bantru_mcc" and p_in == "comngon2024":
            st.session_state.logged_in = True; st.session_state.user_info = {"name": "Quản lý Bán trú", "role": "admin_an"}
            st.rerun()
        else:
            users = load_data("hoc-sinh.csv")
            user_found = next((u for u in users if str(u['username']) == u_in and str(u['password']) == p_in), None)
            if user_found:
                st.session_state.logged_in = True; st.session_state.user_info = user_found; st.rerun()
            else: st.error("Sai thông tin!")
    if st.button("Đăng ký mới"): st.session_state.page = "register"; st.rerun()

# 3. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # --- HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG HỌC SINH")
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Báo cơm", "Xin nghỉ", "Phản ánh"])
        with t1:
            st.info("Chụp ảnh để điểm danh vào lớp")
            anh = st.camera_input("Camera")
            if anh and st.button("GỬI ĐIỂM DANH"):
                save_data("nhat-ky.csv", {"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Đã chụp ảnh", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Thành công"})
                st.success("✅ Đã điểm danh!")
        with t2:
            thu = st.selectbox("Ngày:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Lựa chọn:", ["Báo cơm cho tôi hôm nay", "Xin nghỉ ăn"])
            if st.button("Gửi báo cơm"):
                save_data("nhat-ky.csv", {"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã gửi"})
                st.success("🍱 Đã báo cơm!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            if st.button("Gửi đơn xin nghỉ"):
                save_data("nhat-ky.csv", {"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.success("✅ Đã gửi đơn!")
        with t4:
            yk = st.text_area("Ý kiến phản ánh:")
            if st.button("Gửi phản ánh"):
                save_data("nhat-ky.csv", {"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": yk, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã nhận"})
                st.success("📩 Đã gửi phản ánh!")

    # --- BAN GIÁM HIỆU ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        df = pd.DataFrame(nhat_ky)
        if not df.empty:
            st.metric("Tổng lượt hoạt động", len(df))
            st.subheader("Danh sách chi tiết")
            st.dataframe(df, use_container_width=True)
        else: st.info("Chưa có dữ liệu.")

    # --- BÁN TRÚ ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        nhat_ky = load_data("nhat-ky.csv")
        ds_an = [i for i in nhat_ky if i['Loại'] == "Báo ăn"]
        if ds_an:
            st.table(ds_an)
        else: st.info("Chưa có báo cơm nào.")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
