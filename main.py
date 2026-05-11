import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import json

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- HÀM HỖ TRỢ KỸ THUẬT ---
def image_to_base64(image_file):
    if image_file is not None:
        try: return base64.b64encode(image_file.getvalue()).decode()
        except: return ""
    return ""

def safe_image_display(b64_string, width=300):
    try:
        if b64_string and str(b64_string) != "nan" and len(str(b64_string)) > 10:
            st.image(base64.b64decode(b64_string), width=width)
    except:
        st.caption("⚠️ Không thể hiển thị ảnh.")

def load_data(file_name):
    try: 
        df = pd.read_csv(file_name)
        return df.where(pd.notnull(df), "").to_dict('records')
    except: return []

def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

# --- CSS TÙY CHỈNH THEO Ý THẦY GIÁO ---
def set_style():
    bg_img = "https://unsplash.com"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("{bg_img}"); background-size: cover; }}
        .school-title {{ white-space: nowrap; text-align: center; color: #1E88E5; font-size: clamp(22px, 5vw, 45px); font-weight: bold; margin-bottom: 30px; }}
        </style>
        """, unsafe_allow_html=True)

# --- KHỞI TẠO HỆ THỐNG DỮ LIỆU ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            cols = ["username","password","name","class","role","type","dob","cccd","phone","email","address","diem_10","diem_11","diem_12"]
            pd.DataFrame(columns=cols).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["Tiêu đề","Nội dung","Ảnh","Thời gian","Likes","Comments"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG NHẬP & ĐĂNG KÝ
def login_page():
    set_style()
    st.markdown('<div class="school-title">TRƯỜNG THPT MÙ CANG CHẢI</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c2:
        with st.container(border=True):
            u_in = st.text_input("Tài Khoản")
            p_in = st.text_input("Mật khẩu", type="password")
            if st.button("ĐĂNG NHẬP", use_container_width=True):
                if u_in == "thptmcc_admin" and p_in == "bangianhieu2026":
                    st.session_state.logged_in = True; st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin_gv"}; st.rerun()
                elif u_in == "bantru_mcc" and p_in == "comngon2026":
                    st.session_state.logged_in = True; st.session_state.user_info = {"name": "Quản lý Bán trú", "role": "admin_an"}; st.rerun()
                else:
                    users = load_data("hoc-sinh.csv")
                    user = next((x for x in users if str(x['username'])==u_in and str(x['password'])==p_in), None)
                    if user: st.session_state.logged_in = True; st.session_state.user_info = user; st.rerun()
                    else: st.error("Tài khoản hoặc mật khẩu không chính xác!")
            st.divider()
            if st.button("Tạo tài khoản cho học sinh", use_container_width=True):
                st.session_state.page = "register"; st.rerun()

def registration_page():
    st.markdown('<div class="school-title">TẠO TÀI KHOẢN HỌC SINH</div>', unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Họ và tên học sinh:"); l = st.selectbox("Lớp học:", [f"10A{i}" for i in range(1,10)] + [f"11A{i}" for i in range(1,8)]); t = st.radio("Loại hình học sinh:", ["Học sinh bán trú", "Học sinh ngoại trú"])
        u = st.text_input("Tên tài khoản mới:"); p = st.text_input("Mật khẩu mới:", type="password")
        if st.form_submit_button("XÁC NHẬN ĐĂNG KÝ"):
            all_u = load_data("hoc-sinh.csv")
            all_u.append({"username":u, "password":p, "name":n, "class":l, "role":"student", "type":t})
            save_all_data("hoc-sinh.csv", all_u); st.success("🎉 Đăng ký thành công!"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

# 2. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # --- ADMIN: HỆ THỐNG QUẢN LÝ HỌC SINH ---
    if user.get('role') == "admin_gv":
        st.title("📂 HỆ THỐNG QUẢN LÝ HỌC SINH")
        tab_sk, tab_duyet, tab_u, tab_diem = st.tabs(["📢 Đăng bài & Sự kiện", "📑 Phê duyệt đơn", "👥 Quản lý tài khoản", "📈 Nhập điểm"])
        
        with tab_sk:
            with st.form("post", clear_on_submit=True):
                tt = st.text_input("Tiêu đề"); nd = st.text_area("Nội dung"); img = st.file_uploader("Ảnh bài viết", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG BÀI"):
                    sk_data = load_data("su-kien.csv")
                    sk_data.append({"Tiêu đề":tt, "Nội dung":nd, "Ảnh":image_to_base64(img), "Thời gian":datetime.now().strftime("%H:%M %d/%m"), "Likes":0, "Comments":"[]"})
                    save_all_data("su-kien.csv", sk_data); st.success("Đã đăng bài!"); st.rerun()
            st.divider()
            ds_sk = load_data("su-kien.csv")
            for i, s in enumerate(ds_sk):
                c1, c2 = st.columns([0.85, 0.15])
                c1.write(f"📌 **{s['Tiêu đề']}**")
                if c2.button("Xóa 🗑️", key=f"d_sk_{i}"):
                    ds_sk.pop(i); save_all_data("su-kien.csv", ds_sk); st.rerun()

        with tab_duyet:
            nhat_ky = load_data("nhat-ky.csv")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("📑 Duyệt nghỉ")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Xin nghỉ" and "⏳" in str(it['Trạng thái']):
                        with st.expander(f"{it['Tên']}"):
                            st.write(it['Nội dung'])
                            safe_image_display(it.get('Ảnh'))
                            if st.button("Duyệt ✅", key=f"dn_{i}"): nhat_ky[i]['Trạng thái'] = "✅ BGH đã duyệt nghỉ!"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
            with c2:
                st.subheader("📸 Điểm danh")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Điểm danh" and "⏳" in str(it['Trạng thái']):
                        with st.expander(f"{it['Tên']}"):
                            safe_image_display(it.get('Ảnh'))
                            if st.button("Xác nhận ✅", key=f"dd_{i}"): nhat_ky[i]['Trạng thái'] = "✅ Xác nhận có mặt"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
            with c3:
                st.subheader("💬 Phản ánh")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Phản ánh":
                        with st.expander(f"Từ {it['Tên']}"):
                            st.write(it['Nội dung']); r = st.text_input("Trả lời:", key=f"r_{i}")
                            if st.button("Gửi ✈️", key=f"rb_{i}"): nhat_ky[i]['Trạng thái'] = f"✅ Trả lời: {r}"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with tab_u:
            all_u = load_data("hoc-sinh.csv")
            for i, u in enumerate(all_u):
                if u['role'] == 'student':
                    col1, col2 = st.columns([0.8, 0.2])
                    col1.write(f"🎓 **{u['name']}** ({u['type']})")
                    if col2.button("Xóa 🗑️", key=f"del_u_{i}"): all_u.pop(i); save_all_data("hoc-sinh.csv", all_u); st.rerun()

    # --- QUẢN LÝ BÁN TRÚ ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        ds_an = [i for i in load_data("nhat-ky.csv") if i['Loại'] == "Báo ăn"]
        if ds_an: st.table(pd.DataFrame(ds_an))
        else: st.info("Không có ai báo hủy.")

    # --- HỌC SINH: TRANG CHỦ ---
    else:
        st.title("🏠 TRANG CHỦ")
        menu_hs = st.sidebar.radio("Menu", ["🏠 Bảng tin", "📝 Thông tin cá nhân", "📊 Kết quả học kỳ", "🛠️ Gửi yêu cầu"])
        
        if menu_hs == "🏠 Bảng tin":
            nk_all = load_data("nhat-ky.csv")
            tb_fb = [i for i in nk_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
            if tb_fb:
                for tb in reversed(tb_fb[-2:]): st.success(f"🔵 **Thông báo:** {tb['Trạng thái']}")
            
            ds_sk = load_data("su-kien.csv")
            for idx, sk in enumerate(reversed(ds_sk)):
                r_idx = len(ds_sk) - 1 - idx
                with st.container(border=True):
                    st.markdown(f"### {sk['Tiêu đề']}"); st.write(sk['Nội dung'])
                    safe_image_display(sk.get('Ảnh'), width=None)
                    likes = int(sk.get('Likes', 0))
                    if st.button(f"👍 Like ({likes})", key=f"lk_{r_idx}"):
                        ds_sk[r_idx]['Likes'] = likes + 1
                        save_all_data("su-kien.csv", ds_sk); st.rerun()

        elif menu_hs == "📝 Thông tin cá nhân":
            all_u = load_data("hoc-sinh.csv")
            idx = next(i for i, u in enumerate(all_u) if u['username'] == user['username'])
            with st.form("info"):
                f1 = st.text_input("1. Họ tên", value=all_u[idx]['name'])
                f2 = st.text_input("2. Ngày sinh", value=all_u[idx].get('dob',""))
                f3 = st.text_input("3. CCCD", value=all_u[idx].get('cccd',""))
                f4 = st.text_input("4. SĐT", value=all_u[idx].get('phone',""))
                f5 = st.text_input("5. Email", value=all_u[idx].get('email',""))
                f6 = st.text_area("6. Địa chỉ", value=all_u[idx].get('address',""))
                if st.form_submit_button("Lưu"):
                    all_u[idx].update({"name":f1,"dob":f2,"cccd":f3,"phone":f4,"email":f5,"address":f6})
                    save_all_data("hoc-sinh.csv", all_u); st.success("Đã lưu!")

        elif menu_hs == "📊 Kết quả học kỳ":
            c1, c2, c3 = st.columns(3)
            c1.metric("Lớp 10", user.get('diem_10', "Trống"))
            c2.metric("Lớp 11", user.get('diem_11', "Trống"))
            c3.metric("Lớp 12", user.get('diem_12', "Trống"))

        elif menu_hs == "🛠️ Gửi yêu cầu":
            t_dd, t_com, t_nghi = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ"])
            with t_dd:
                a = st.camera_input("Chụp ảnh"); 
                if a and st.button("Gửi"): save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a)}]); st.success("Xong!")
            with t_com:
                if user.get('type') == "Học sinh ngoại trú": st.warning("Bạn là học sinh ngoại trú.")
                else: 
                    b = st.multiselect("Bữa hủy:", ["Trưa", "Chiều"])
                    if st.button("Hủy bữa"): save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY: {b}","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""}]); st.success("Đã báo!")
            with t_nghi:
                l = st.text_area("Lý do"); anh = st.camera_input("Ảnh")
                if st.button("Gửi đơn"): save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":l,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(anh)}]); st.success("Đã gửi!")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()
