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
        return base64.b64encode(image_file.getvalue()).decode()
    return ""

# --- TỰ ĐỘNG KHỞI TẠO FILE ---
for f in ["hoc-sinh.csv", "nhat-ky.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=["username","password","name","class","role"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

def load_data(file_name):
    try: return pd.read_csv(file_name).to_dict('records')
    except: return []

def save_data(file_name, new_entry):
    data = load_data(file_name)
    data.append(new_entry)
    pd.DataFrame(data).to_csv(file_name, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG KÝ & ĐĂNG NHẬP
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
                save_data("hoc-sinh.csv", {"username": u_id, "password": pwd, "name": name, "class": lop, "role": "student"})
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
        # HIỂN THỊ THÔNG BÁO KIỂU FACEBOOK
        st.subheader("🔔 Thông báo mới")
        nhat_ky_all = load_data("nhat-ky.csv")
        thong_bao_fb = [i for i in nhat_ky_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
        
        if thong_bao_fb:
            for tb in reversed(thong_bao_fb[-3:]): # Hiện 3 thông báo mới nhất
                with st.container(border=True):
                    c_ic, c_txt = st.columns([0.1, 0.9])
                    c_ic.markdown("### 🔵")
                    c_txt.markdown(f"**Ban Giám Hiệu** đã phản hồi yêu cầu *{tb['Loại']}* của bạn.")
                    c_txt.caption(f"{tb['Trạng thái']} • {tb['Thời gian']}")
        else:
            st.info("Chưa có thông báo mới.")
        
        st.divider()
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh"])
        
        with t1:
            a_dd = st.camera_input("Chụp ảnh điểm danh")
            if a_dd and st.button("GỬI ĐIỂM DANH"):
                save_data("nhat-ky.csv", {"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)})
                st.success("✅ Đã gửi!")

        with t2:
            st.error("🚫 **Lưu ý:** Hủy bữa Trưa trước 09h00 | Hủy bữa Chiều trước 15h00.")
            thu = st.selectbox("Ngày báo hủy:", ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6"])
            buoi = st.multiselect("Buổi muốn hủy:", ["Bữa Trưa", "Bữa Chiều"], default=["Bữa Trưa"])
            xac_nhan = st.checkbox(f"Tôi xác nhận hủy ăn {thu}")
            gio_hien_tai = datetime.now().hour
            if st.button("Gửi yêu cầu hủy"):
                if xac_nhan:
                    loi = False
                    if "Bữa Trưa" in buoi and gio_hien_tai >= 9: st.error("Quá 9h! Không thể hủy trưa."); loi = True
                    if "Bữa Chiều" in buoi and gio_hien_tai >= 15: st.error("Quá 15h! Không thể hủy chiều."); loi = True
                    if not loi:
                        save_data("nhat-ky.csv", {"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY ĂN: {thu} ({', '.join(buoi)})","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                        st.success("❌ Đã gửi yêu cầu hủy!")
                else: st.warning("Vui lòng tích xác nhận.")

        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            a_nghi = st.camera_input("Minh chứng (Đơn thuốc/Chỗ đau)")
            if st.button("Gửi đơn"):
                save_data("nhat-ky.csv", {"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly_do,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_nghi)})
                st.success("✅ Đã gửi đơn!")

        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi"):
                save_data("nhat-ky.csv", {"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":yk,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})

    # --- BAN GIÁM HIỆU ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        t_nghi, t_dd, t_pa = st.tabs(["📑 Duyệt nghỉ", "📸 Duyệt điểm danh", "💬 Trả lời phản ánh"])
        
        def render_section(loai, msg):
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == loai:
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        
                        if loai == "Phản ánh":
                            rep = st.text_input("Trả lời:", key=f"r_{i}")
                            if st.button("Gửi", key=f"rb_{i}"):
                                nhat_ky[i]['Trạng thái'] = f"✅ BGH phản hồi: {rep}"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        else:
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                if st.button("Duyệt ✅", key=f"d_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = msg; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.balloons(); st.rerun()
                            with c2:
                                if st.button("Từ chối ❌", key=f"tc_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = "❌ Từ chối"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                            with c3:
                                if st.button("Xóa 🗑️", key=f"del_{loai}_{i}"):
                                    nhat_ky.pop(i); pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()

        with t_nghi: render_section("Xin nghỉ", "✅ Đã duyệt! Bạn hãy nghỉ ngơi theo yêu cầu nhé.")
        with t_dd: render_section("Điểm danh", "✅ BGH xác nhận điểm danh thành công.")
        with t_pa: render_section("Phản ánh", "")

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