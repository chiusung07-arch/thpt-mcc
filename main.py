import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- TỰ ĐỘNG KHỞI TẠO FILE DỮ LIỆU ---
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

    # --- GIAO DIỆN HỌC SINH ---
    if user.get('role') == "student":
        st.title("📍 CỔNG HỌC SINH")
        
        # Thông báo từ BGH
        nhat_ky_all = load_data("nhat-ky.csv")
        thong_bao = [i for i in nhat_ky_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
        if thong_bao:
            for tb in thong_bao:
                st.success(f"📢 **Thông báo:** {tb['Trạng thái']}. Bạn hãy nghỉ ngơi theo yêu cầu!")

        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Báo cơm", "Xin nghỉ", "Phản ánh"])
        with t1:
            anh = st.camera_input("Chụp ảnh điểm danh")
            if anh and st.button("GỬI ĐIỂM DANH"):
                save_data("nhat-ky.csv", {"Loại": "Điểm danh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": "Đã chụp ảnh", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.success("✅ Đã gửi ảnh điểm danh!")
        with t2:
            thu = st.selectbox("Ngày báo cơm:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            buoi = st.multiselect("Chọn buổi ăn:", ["Bữa Trưa", "Bữa Chiều"], default=["Bữa Trưa"])
            chon = st.radio("Lựa chọn:", ["Đăng ký ăn", "Xin nghỉ ăn"])
            if st.button("Xác nhận báo cơm"):
                save_data("nhat-ky.csv", {"Loại": "Báo ăn", "Lớp": user['class'], "Tên": user['name'], "Nội dung": f"{thu} ({', '.join(buoi)}): {chon}", "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "Đã gửi"})
                st.success("🍱 Đã lưu thông tin báo cơm!")
        with t3:
            ly_do = st.text_area("Lý do xin nghỉ:")
            if st.button("Gửi đơn xin nghỉ"):
                save_data("nhat-ky.csv", {"Loại": "Xin nghỉ", "Lớp": user['class'], "Tên": user['name'], "Nội dung": ly_do, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Chờ duyệt"})
                st.success("✅ Đơn đã được gửi tới BGH!")
        with t4:
            yk = st.text_area("Ý kiến/Kiến nghị:")
            if st.button("Gửi phản ánh"):
                save_data("nhat-ky.csv", {"Loại": "Phản ánh", "Lớp": user['class'], "Tên": user['name'], "Nội dung": yk, "Thời gian": datetime.now().strftime("%H:%M %d/%m"), "Trạng thái": "⏳ Đã gửi"})
                st.success("📩 Cảm ơn bạn đã phản hồi!")

    # --- GIAO DIỆN BAN GIÁM HIỆU (PHÂN 3 MỤC) ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        
        tab_nghi, tab_danh, tab_phan_anh = st.tabs(["📑 Duyệt đơn xin nghỉ", "📸 Duyệt điểm danh", "💬 Trả lời phản ánh"])

        with tab_nghi:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Xin nghỉ":
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(f"**Lớp:** {item['Lớp']} | **Lý do:** {item['Nội dung']}")
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            if st.button(f"Duyệt ✅", key=f"n_d_{i}"):
                                nhat_ky[i]['Trạng thái'] = "✅ Đã duyệt"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        with c2:
                            if st.button(f"Từ chối ❌", key=f"n_tc_{i}"):
                                nhat_ky[i]['Trạng thái'] = "❌ Từ chối"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        with c3:
                            if st.button(f"Xóa 🗑️", key=f"n_del_{i}"):
                                nhat_ky.pop(i); pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()

        with tab_danh:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Điểm danh":
                    with st.expander(f"👤 {item['Tên']} - {item['Lớp']} ({item['Trạng thái']})"):
                        if st.button(f"Xác nhận có mặt ✅", key=f"d_d_{i}"):
                            nhat_ky[i]['Trạng thái'] = "✅ Đã duyệt"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        if st.button(f"Xóa 🗑️", key=f"d_del_{i}"):
                            nhat_ky.pop(i); pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()

        with tab_phan_anh:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Phản ánh":
                    with st.expander(f"📩 Từ {item['Tên']} ({item['Trạng thái']})"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        tra_loi = st.text_input("Nhập câu trả lời:", key=f"rep_{i}")
                        if st.button("Gửi phản hồi", key=f"rep_b_{i}"):
                            nhat_ky[i]['Trạng thái'] = f"✅ BGH trả lời: {tra_loi}"
                            pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        if st.button(f"Xóa 🗑️", key=f"p_del_{i}"):
                            nhat_ky.pop(i); pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()

    # --- GIAO DIỆN BÁN TRÚ ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        nhat_ky = load_data("nhat-ky.csv")
        ds_an = [i for i in nhat_ky if i['Loại'] == "Báo ăn"]
        if ds_an:
            st.table(pd.DataFrame(ds_an))
        else: st.info("Chưa có dữ liệu báo cơm.")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
