import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# 1. XỬ LÝ DỮ LIỆU TÀI KHOẢN
def load_users():
    if os.path.exists("hoc-sinh.csv"):
        try: return pd.read_csv("hoc-sinh.csv").to_dict('records')
        except: return []
    return []

def save_user_to_csv(new_user):
    users = load_users()
    users.append(new_user)
    pd.DataFrame(users).to_csv("hoc-sinh.csv", index=False)

# KHỞI TẠO BIẾN
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"
if 'lich_su' not in st.session_state: st.session_state.lich_su = []

# 2. TRANG ĐĂNG KÝ
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH")
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
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

# 3. TRANG ĐĂNG NHẬP
def login_page():
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TRƯỜNG THPT MÙ CANG CHẢI</h1>", unsafe_allow_html=True)
    u_in = st.text_input("Tên tài khoản:")
    p_in = st.text_input("Mật khẩu:", type="password")
    if st.button("ĐĂNG NHẬP", use_container_width=True):
        if u_in == "thptmcc_admin" and p_in == "giaovien2024":
            st.session_state.logged_in = True
            st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin_gv"}
            st.rerun()
        elif u_in == "bantru_mcc" and p_in == "comngon2024":
            st.session_state.logged_in = True
            st.session_state.user_info = {"name": "Quản lý Bán trú", "role": "admin_an"}
            st.rerun()
        else:
            users = load_users()
            user_found = next((u for u in users if str(u['username']) == u_in and str(u['password']) == p_in), None)
            if user_found:
                st.session_state.logged_in = True; st.session_state.user_info = user_found; st.rerun()
            else: st.error("Sai thông tin!")
    if st.button("Đăng ký mới"): st.session_state.page = "register"; st.rerun()

# 4. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # --- HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG HỌC SINH")
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Báo cơm", "Xin nghỉ", "Phản ánh"])
        with t1:
            anh = st.camera_input("Chụp ảnh điểm danh")
            if anh and st.button("GỬI ẢNH"):
                st.session_state.lich_su.append({"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Đã chụp ảnh", "Ảnh": anh, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Thành công"})
                st.success("✅ Đã điểm danh!")
        with t2:
            thu = st.selectbox("Ngày:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Lựa chọn:", ["Báo cơm cho tôi hôm nay", "Xin nghỉ ăn"])
            if st.button("Gửi báo cơm"):
                st.session_state.lich_su.append({"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu}: {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.success("🍱 Đã báo cơm!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            if st.button("Gửi đơn"):
                st.session_state.lich_su.append({"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.success("✅ Đã gửi. Chờ Ban Giám Hiệu phê duyệt!")
        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi"):
                st.session_state.lich_su.append({"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": yk, "Thời gian": datetime.now().strftime("%H:%M %d/%m")})
                st.success("📩 Đã nhận phản ánh!")

    # --- BAN GIÁM HIỆU (PHÁO HOA) ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        tong_hs = len([i for i in st.session_state.lich_su if i['Loại'] == "Điểm danh"])
        st.metric("Sĩ số có mặt hôm nay", f"{tong_hs} học sinh")
        
        st.subheader("Duyệt đơn & Phản ánh")
        if st.session_state.lich_su:
            for i, item in enumerate(st.session_state.lich_su):
                if item['Loại'] in ["Xin nghỉ", "Phản ánh"]:
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(item['Nội dung'])
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(f"Duyệt", key=f"d_{i}"):
                                item['Trạng thái'] = "✅ Đã duyệt"; st.balloons(); st.rerun()
                        with c2:
                            if st.button(f"Từ chối", key=f"tc_{i}"):
                                item['Trạng thái'] = "❌ Từ chối"; st.rerun()
        
        st.write("---")
        st.subheader("Ảnh điểm danh")
        ds_anh = [i for i in st.session_state.lich_su if i['Loại'] == "Điểm danh"]
        for r in ds_anh:
            col_a, col_b = st.columns([1,3])
            col_a.image(r['Ảnh'], width=100)
            col_b.write(f"👤 {r['Tên']} - {r['Lớp']}")

    # --- BÁN TRÚ ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        ds_an = [i for i in st.session_state.lich_su if i['Loại'] == "Báo ăn"]
        if ds_an:
            st.table(ds_an)
            tong = sum(1 for x in ds_an if "Báo cơm" in x['Nội dung'])
            st.metric("Tổng suất cơm", f"{tong} suất")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()