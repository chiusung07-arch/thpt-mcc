import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import json

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- HÀM HỖ TRỢ ---
def image_to_base64(image_file):
    if image_file is not None:
        try: return base64.b64encode(image_file.getvalue()).decode()
        except: return ""
    return ""

# --- KHỞI TẠO FILE DỮ LIỆU ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=["username","password","name","class","role"]).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["Tiêu đề","Nội dung","Ảnh","Thời gian","Likes","Comments"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

def load_data(file_name):
    try: return pd.read_csv(file_name).to_dict('records')
    except: return []

def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG KÝ & ĐĂNG NHẬP
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH")
    with st.form("reg_form"):
        name = st.text_input("Họ và tên học sinh:")
        classes = [f"10A{i}" for i in range(1, 10)] + [f"11A{i}" for i in range(1, 8)] + [f"12A{i}" for i in range(1, 8)]
        lop = st.selectbox("Lớp học:", classes)
        u_id = st.text_input("Tài khoản:")
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if u_id and pwd and name:
                pd.DataFrame(load_data("hoc-sinh.csv") + [{"username": u_id, "password": pwd, "name": name, "class": lop, "role": "student"}]).to_csv("hoc-sinh.csv", index=False)
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
            user = next((u for u in users if str(u['username']) == u_in and str(u['password']) == p_in), None)
            if user: st.session_state.logged_in = True; st.session_state.user_info = user; st.rerun()
            else: st.error("Sai thông tin!")
    if st.button("Đăng ký mới"): st.session_state.page = "register"; st.rerun()

# 2. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # --- CỔNG HỌC SINH ---
    if user.get('role') == "student":
        st.subheader("🔔 Thông báo")
        nhat_ky_all = load_data("nhat-ky.csv")
        thong_bao = [i for i in nhat_ky_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
        if thong_bao:
            for tb in reversed(thong_bao[-3:]):
                with st.container(border=True):
                    st.markdown(f"🔵 **BGH phản hồi:** {tb['Trạng thái']} • {tb['Thời gian']}")

        t1, t2, t3, t4, t5 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh", "🎉 Sự kiện"])
        
        with t1:
            a_dd = st.camera_input("Chụp ảnh điểm danh")
            if a_dd and st.button("GỬI ĐIỂM DANH"):
                pd.DataFrame(load_data("nhat-ky.csv") + [{"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)}]).to_csv("nhat-ky.csv", index=False)
                st.success("✅ Đã gửi!")
        with t2:
            st.error("🚫 Hủy Trưa trước 09h | Hủy Chiều trước 15h.")
            thu = st.selectbox("Ngày báo hủy:", ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6"])
            buoi = st.multiselect("Buổi muốn hủy:", ["Bữa Trưa", "Bữa Chiều"], default=["Bữa Trưa"])
            if st.button("Xác nhận Hủy"):
                gio = datetime.now().hour
                if ("Bữa Trưa" in buoi and gio >= 9) or ("Bữa Chiều" in buoi and gio >= 15):
                    st.error("Quá giờ quy định!")
                else:
                    pd.DataFrame(load_data("nhat-ky.csv") + [{"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY: {thu} {buoi}","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""}]).to_csv("nhat-ky.csv", index=False)
                    st.success("❌ Đã báo hủy!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            a_ng = st.camera_input("Ảnh minh chứng")
            if st.button("Gửi đơn"):
                pd.DataFrame(load_data("nhat-ky.csv") + [{"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly_do,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_ng)}]).to_csv("nhat-ky.csv", index=False)
                st.success("✅ Đã gửi!")
        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi phản ánh"):
                pd.DataFrame(load_data("nhat-ky.csv") + [{"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":yk,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""}]).to_csv("nhat-ky.csv", index=False)
                st.success("📩 Đã nhận!")
        with t5:
            st.subheader("📣 Bảng tin Sự kiện")
            ds_sk = load_data("su-kien.csv")
            if ds_sk:
                for idx, sk in enumerate(reversed(ds_sk)):
                    r_idx = len(ds_sk) - 1 - idx
                    with st.container(border=True):
                        st.markdown(f"### {sk['Tiêu đề']}")
                        st.caption(f"📅 {sk['Thời gian']}")
                        st.write(sk['Nội dung'])
                        if str(sk.get('Ảnh')) != "nan" and sk.get('Ảnh'):
                            st.image(base64.b64decode(sk['Ảnh']), use_container_width=True)
                        # Like & Comment
                        col_l, col_c = st.columns([0.2, 0.8])
                        if col_l.button(f"👍 Like ({int(sk.get('Likes',0))})", key=f"lk_{r_idx}"):
                            ds_sk[r_idx]['Likes'] = int(sk.get('Likes',0)) + 1
                            save_all_data("su-kien.csv", ds_sk); st.rerun()
                        new_com = st.text_input("Bình luận...", key=f"ic_{r_idx}")
                        if st.button("Gửi ✈️", key=f"bc_{r_idx}"):
                            coms = json.loads(sk['Comments'].replace("'", '"')) if str(sk.get('Comments')) != "nan" else []
                            coms.append({"user": user['name'], "text": new_com})
                            ds_sk[r_idx]['Comments'] = json.dumps(coms, ensure_ascii=False)
                            save_all_data("su-kien.csv", ds_sk); st.rerun()

    # --- CỔNG BAN GIÁM HIỆU (ĐÃ KHÔI PHỤC NÚT DUYỆT) ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        t_ng, t_dd, t_pa, t_sk = st.tabs(["📑 Duyệt nghỉ", "📸 Điểm danh", "💬 Phản ánh", "📢 Đăng bài"])
        
        def render_admin(loai, msg):
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == loai:
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        
                        if loai == "Phản ánh":
                            rep = st.text_input("Trả lời:", key=f"rep_{i}")
                            if st.button("Gửi phản hồi", key=f"r_b_{i}"):
                                nhat_ky[i]['Trạng thái'] = f"✅ Trả lời: {rep}"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
                        else:
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                if st.button("Duyệt ✅", key=f"d_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = msg; save_all_data("nhat-ky.csv", nhat_ky); st.balloons(); st.rerun()
                            with c2:
                                if st.button("Từ chối ❌", key=f"tc_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = "❌ Từ chối"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
                            with c3:
                                if st.button("Xóa 🗑️", key=f"del_{loai}_{i}"):
                                    nhat_ky.pop(i); save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with t_ng: render_admin("Xin nghỉ", "✅ BGH đã duyệt cho phép nghỉ!")
        with t_dd: render_admin("Điểm danh", "✅ BGH xác nhận điểm danh.")
        with t_pa: render_admin("Phản ánh", "")
        with t_sk:
            st.subheader("Đăng bài mới")
            with st.form("new_post"):
                tt = st.text_input("Tiêu đề"); nd = st.text_area("Nội dung"); im = st.file_uploader("Ảnh", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG"):
                    save_single_data("su-kien.csv", {"Tiêu đề":tt,"Nội dung":nd,"Ảnh":image_to_base64(im),"Thời gian":datetime.now().strftime("%d/%m"),"Likes":0,"Comments":"[]"})
                    st.success("Đã đăng!"); st.rerun()

    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        ds_an = [i for i in load_data("nhat-ky.csv") if i['Loại'] == "Báo ăn"]
        if ds_an: st.table(pd.DataFrame(ds_an))
        else: st.info("Chưa có ai báo hủy cơm.")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
