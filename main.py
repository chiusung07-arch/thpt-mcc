import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- HÀM MÃ HÓA ẢNH ---
def image_to_base64(image_file):
    if image_file is not None:
        try: return base64.b64encode(image_file.getvalue()).decode()
        except: return ""
    return ""

# --- TỰ ĐỘNG KHỞI TẠO FILE ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=["username","password","name","class","role"]).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["Tiêu đề","Nội dung","Ảnh","Thời gian"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

def load_data(file_name):
    try: return pd.read_csv(file_name).to_dict('records')
    except: return []

def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

def save_single_data(file_name, new_entry):
    data = load_data(file_name)
    data.append(new_entry)
    save_all_data(file_name, data)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. ĐĂNG KÝ & ĐĂNG NHẬP
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = [f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)]
        lop = st.selectbox("Lớp học:", classes)
        u_id = st.text_input("Tên tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if u_id and pwd and name:
                save_single_data("hoc-sinh.csv", {"username": u_id, "password": pwd, "name": name, "class": lop, "role": "student"})
                st.success("✅ Đăng ký thành công!"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

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
            if user_found: st.session_state.logged_in = True; st.session_state.user_info = user_found; st.rerun()
            else: st.error("Sai thông tin!")
    if st.button("Đăng ký mới"): st.session_state.page = "register"; st.rerun()

# 2. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # --- HỌC SINH ---
    if user.get('role') == "student":
        st.subheader("🔔 Thông báo mới")
        nhat_ky_all = load_data("nhat-ky.csv")
        thong_bao_fb = [i for i in nhat_ky_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
        if thong_bao_fb:
            for tb in reversed(thong_bao_fb[-3:]):
                with st.container(border=True):
                    c_ic, c_txt = st.columns([0.1, 0.9])
                    c_ic.markdown("### 🔵")
                    c_txt.markdown(f"**Ban Giám Hiệu** đã phản hồi yêu cầu *{tb['Loại']}*.")
                    c_txt.caption(f"{tb['Trạng thái']} • {tb['Thời gian']}")
        else: st.info("Chưa có thông báo mới.")
        
        st.divider()
        t1, t2, t3, t4, t5 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh", "🎉 Sự kiện"])
        
        with t1:
            a_dd = st.camera_input("Chụp ảnh điểm danh")
            if a_dd and st.button("GỬI ĐIỂM DANH"):
                save_single_data("nhat-ky.csv", {"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)})
                st.success("✅ Đã gửi!")
        with t2:
            st.error("🚫 Hủy Trưa trước 09h | Hủy Chiều trước 15h.")
            thu = st.selectbox("Ngày báo hủy:", ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6"])
            buoi = st.multiselect("Buổi muốn hủy:", ["Bữa Trưa", "Bữa Chiều"], default=["Bữa Trưa"])
            if st.button("Gửi yêu cầu hủy"):
                save_single_data("nhat-ky.csv", {"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY ĂN: {thu} ({', '.join(buoi)})","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                st.success("❌ Đã báo hủy!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            a_nghi = st.camera_input("Minh chứng (Đơn thuốc/Vết thương)")
            if st.button("Gửi đơn"):
                save_single_data("nhat-ky.csv", {"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly_do,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_nghi)})
                st.success("✅ Đã gửi đơn!")
        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi phản ánh"):
                save_single_data("nhat-ky.csv", {"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":yk,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                st.success("📩 Đã nhận!")
        with t5:
            st.subheader("📣 Bản tin nhà trường")
            ds_sk = load_data("su-kien.csv")
            if ds_sk:
                for sk in reversed(ds_sk):
                    with st.container(border=True):
                        st.markdown(f"### {sk['Tiêu đề']}")
                        st.caption(f"📅 Đăng lúc: {sk['Thời gian']}")
                        st.write(sk['Nội dung'])
                        if str(sk.get('Ảnh')) != "nan" and sk.get('Ảnh'):
                            st.image(base64.b64decode(sk['Ảnh']), use_container_width=True)
            else: st.info("Chưa có sự kiện nào.")

    # --- BAN GIÁM HIỆU ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Duyệt nghỉ", "📸 Duyệt điểm danh", "💬 Phản ánh", "📢 Quản lý Sự kiện"])
        
        with tab1:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Xin nghỉ":
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        if st.button(f"Duyệt ✅", key=f"d_n_{i}"):
                            nhat_ky[i]['Trạng thái'] = "✅ Đã duyệt và cho phép nghỉ!"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
        
        with tab2:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Điểm danh":
                    with st.expander(f"👤 {item['Tên']} - {item['Lớp']}"):
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        if st.button(f"Xác nhận ✅", key=f"d_d_{i}"):
                            nhat_ky[i]['Trạng thái'] = "✅ BGH xác nhận điểm danh"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with tab3:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Phản ánh":
                    with st.expander(f"📩 Từ {item['Tên']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        rep = st.text_input("Trả lời:", key=f"rep_{i}")
                        if st.button("Gửi phản hồi", key=f"r_b_{i}"):
                            nhat_ky[i]['Trạng thái'] = f"✅ BGH phản hồi: {rep}"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with tab4:
            st.subheader("Tạo sự kiện mới")
            with st.form("new_event"):
                t = st.text_input("Tiêu đề:")
                c = st.text_area("Nội dung:")
                img = st.file_uploader("Ảnh đính kèm", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG BÀI"):
                    if t and c:
                        save_single_data("su-kien.csv", {"Tiêu đề":t, "Nội dung":c, "Ảnh":image_to_base64(img), "Thời gian":datetime.now().strftime("%H:%M %d/%m")})
                        st.success("Đã đăng!"); st.rerun()
            
            st.divider()
            st.subheader("Quản lý bài đã đăng")
            ds_sk = load_data("su-kien.csv")
            if ds_sk:
                for idx, sk in enumerate(ds_sk):
                    col1, col2 = st.columns([0.8, 0.2])
                    col1.write(f"📌 **{sk['Tiêu đề']}** ({sk['Thời gian']})")
                    if col2.button("Xóa bài 🗑️", key=f"del_sk_{idx}"):
                        ds_sk.pop(idx)
                        save_all_data("su-kien.csv", ds_sk)
                        st.rerun()
            else: st.info("Không có bài đăng nào.")

    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        ds_an = [i for i in load_data("nhat-ky.csv") if i['Loại'] == "Báo ăn"]
        if ds_an: st.table(pd.DataFrame(ds_an))
        else: st.info("Chưa có ai báo hủy bữa.")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()