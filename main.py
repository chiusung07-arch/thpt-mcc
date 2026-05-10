import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hệ thống Quản lý THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# 1. XỬ LÝ DỮ LIỆU TÀI KHOẢN (Lưu vĩnh viễn vào file CSV)
def load_users():
    if os.path.exists("hoc-sinh.csv"):
        try:
            return pd.read_csv("hoc-sinh.csv").to_dict('records')
        except:
            return []
    return []

def save_user_to_csv(new_user):
    users = load_users()
    users.append(new_user)
    pd.DataFrame(users).to_csv("hoc-sinh.csv", index=False)

# 2. KHỞI TẠO BIẾN HỆ THỐNG
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"
if 'lich_su' not in st.session_state: st.session_state.lich_su = []

# 3. GIAO DIỆN ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH MỚI")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        # Tạo danh sách lớp từ 10A1-12A7
        classes = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        lop = st.selectbox("Lớp học:", classes)
        user_id = st.text_input("Tên tài khoản (Mã HS):")
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
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TRƯỜNG THPT MÙ CANG CHẢI</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
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
        if st.button("Chưa có tài khoản? Đăng ký ngay", use_container_width=True):
            st.session_state.page = "register"; st.rerun()

# 5. GIAO DIỆN CHÍNH (DASHBOARD)
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if 'class' in user: st.sidebar.info(f"Lớp: {user['class']}")
    if st.sidebar.button("ĐĂNG XUẤT", use_container_width=True):
        st.session_state.logged_in = False; st.rerun()

    # --- GIAO DIỆN DÀNH CHO HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG THÔNG TIN HỌC SINH")
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Báo cơm", "Xin nghỉ", "Phản ánh"])
        
        with t1:
            st.subheader("📍 Điểm danh kèm ảnh chụp")
            anh = st.camera_input("Chụp ảnh để xác nhận có mặt")
            if anh:
                if st.button("GỬI ẢNH XÁC NHẬN"):
                    st.session_state.lich_su.append({
                        "Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], 
                        "Nội dung": "Đã chụp ảnh có mặt", "Ảnh": anh,
                        "Thời gian": datetime.now().strftime("%H:%M %d/%m")
                    })
                    st.success("✅ Đã gửi điểm danh kèm ảnh!")

        with t2:
            st.subheader("🍱 Báo cơm bán trú")
            thu = st.selectbox("Chọn ngày:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Lựa chọn:", ["Báo cơm cho tôi hôm nay", "Xin nghỉ ăn bữa này"])
            if st.button("Gửi báo cáo cơm"):
                st.session_state.lich_su.append({
                    "Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], 
                    "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m")
                })
                st.success("🍱 Đã ghi nhận thông tin báo cơm thành công!")

        with t3:
            st.subheader("📝 Đơn xin nghỉ Online")
            ly_do = st.text_area("Nhập lý do xin nghỉ:")
            if st.button("Gửi đơn"):
                if ly_do.strip():
                    st.session_state.lich_su.append({
                        "Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], 
                        "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), 
                        "Trạng thái": "⏳ Chờ phê duyệt"
                    })
                    st.success("✅ Đã gửi. Chờ phê duyệt!")
                else: st.error("Vui lòng nhập lý do!")

        with t4:
            yk = st.text_area("Hòm thư phản ánh & thắc mắc:")
            if st.button("Gửi phản ánh"):
                st.session_state.lich_su.append({
                    "Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], 
                    "Nội dung": yk, "Thời gian": datetime.now().strftime("%H:%M %d/%m")
                })
                st.success("📩 Nhà trường đã nhận được ý kiến của bạn!")

    # --- GIAO DIỆN ADMIN GIÁO VIÊN (Tài khoản: thptmcc_admin) ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ CỦA GIÁO VIÊN")
        classes_list = ([f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)])
        chon_lop = st.selectbox("Lọc danh sách đi học theo lớp:", classes_list)
        
        st.subheader(f"Danh sách học sinh lớp {chon_lop}")
        ds = [i for i in st.session_state.lich_su if i['Loại'] == "Điểm danh" and i['Lớp'] == chon_lop]
        if ds:
            for r in ds:
                c1, c2 = st.columns([1,3])
                with c1: st.image(r['Ảnh'], width=150)
                with c2: st.write(f"👤 **{r['Tên']}**\n\n⏰ Thời gian: {r['Thời gian']}")
        else: st.info(f"Lớp {chon_lop} chưa có dữ liệu điểm danh.")
        
        st.write("---")
        st.subheader("📩 Hòm thư Đơn xin nghỉ & Phản ánh")
        ds_don = [i for i in st.session_state.lich_su if i['Loại'] in ["Xin nghỉ", "Phản ánh"]]
        if ds_don: st.table(ds_don)
        else: st.info("Hòm thư hiện tại đang trống.")

    # --- GIAO DIỆN ADMIN BÁN TRÚ (Tài khoản: bantru_mcc) ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ SUẤT ĂN BÁN TRÚ")
        ds_an = [i for i in st.session_state.lich_su if i['Loại'] == "Báo ăn"]
        if ds_an:
            st.table(ds_an)
            tong = sum(1 for x in ds_an if "Báo cơm cho tôi hôm nay" in x['Nội dung'])
            st.metric("Tổng suất cơm cần chuẩn bị", f"{tong} suất")
        else: st.info("Chưa có dữ liệu báo cơm hôm nay.")

# --- ĐIỀU HƯỚNG CHÍNH ---
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()