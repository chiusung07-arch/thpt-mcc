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

def load_data(file_name):
    try: 
        df = pd.read_csv(file_name)
        return df.where(pd.notnull(df), "").to_dict('records')
    except: return []

def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

# --- CSS TÙY CHỈNH THEO Ý THẦY ---
def set_style():
    bg_img = "https://unsplash.com"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("{bg_img}"); background-size: cover; }}
        .school-title {{ white-space: nowrap; text-align: center; color: #1E88E5; font-size: clamp(22px, 5vw, 45px); font-weight: bold; margin-bottom: 30px; text-shadow: 1px 1px 2px #fff; }}
        [data-testid="stMetricValue"] {{ font-size: 25px; color: #1E88E5; }}
        </style>
        """, unsafe_allow_html=True)

# --- KHỞI TẠO HỆ THỐNG DỮ LIỆU ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            cols = ["username","password","name","class","role","type","dob","cccd","phone","email","address","diem_10","diem_11","diem_12"]
            pd.DataFrame(columns=cols).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["ID","Tiêu đề","Nội dung","Ảnh","Thời gian","Likes","Comments"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG NHẬP & ĐĂNG KÝ
def login_page():
    set_style()
    st.markdown('<div class="school-title">TRƯỜNG THPT MÙ CANG CHẢI</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            u = st.text_input("Tài Khoản")
            p = st.text_input("Mật khẩu", type="password")
            if st.button("ĐĂNG NHẬP", use_container_width=True):
                if u == "admin" and p == "123":
                    st.session_state.logged_in = True; st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin_gv"}
                    st.rerun()
                else:
                    users = load_data("hoc-sinh.csv")
                    user = next((x for x in users if str(x['username'])==u and str(x['password'])==p), None)
                    if user: st.session_state.logged_in = True; st.session_state.user_info = user; st.rerun()
                    else: st.error("Tài khoản hoặc mật khẩu không chính xác!")
            st.divider()
            if st.button("Tạo tài khoản cho học sinh", use_container_width=True):
                st.session_state.page = "register"; st.rerun()

def registration_page():
    st.markdown('<div class="school-title">ĐĂNG KÝ TÀI KHOẢN HỌC SINH</div>', unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Họ và tên học sinh:")
        l = st.selectbox("Lớp học:", [f"10A{i}" for i in range(1,10)] + [f"11A{i}" for i in range(1,8)] + [f"12A{i}" for i in range(1,8)])
        t = st.radio("Loại hình học sinh:", ["Học sinh bán trú", "Học sinh ngoại trú"])
        u = st.text_input("Tên đăng nhập (Tài khoản):")
        p = st.text_input("Mật khẩu mới:", type="password")
        if st.form_submit_button("XÁC NHẬN ĐĂNG KÝ"):
            if n and u and p:
                all_u = load_data("hoc-sinh.csv")
                all_u.append({"username":u, "password":p, "name":n, "class":l, "role":"student", "type":t})
                save_all_data("hoc-sinh.csv", all_u)
                st.success("🎉 Đăng ký thành công! Hãy đăng nhập."); st.session_state.page = "login"
    if st.button("Quay lại đăng nhập"): st.session_state.page = "login"; st.rerun()

# 2. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    
    # --- GIAO DIỆN ADMIN: HỆ THỐNG QUẢN LÝ HỌC SINH ---
    if user.get('role') == "admin_gv":
        st.title("📂 HỆ THỐNG QUẢN LÝ HỌC SINH")
        t_post, t_check, t_mng, t_diem = st.tabs(["📢 Đăng bài & Sự kiện", "📑 Phê duyệt Đơn", "👥 Quản lý Tài khoản", "📈 Nhập điểm số"])
        
        with t_post:
            with st.form("p", clear_on_submit=True):
                tt = st.text_input("Tiêu đề bài viết")
                nd = st.text_area("Nội dung")
                im = st.file_uploader("Ảnh bài viết", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG BÀI LÊN BẢNG TIN"):
                    sk = load_data("su-kien.csv")
                    sk.append({"Tiêu đề":tt, "Nội dung":nd, "Ảnh":image_to_base64(im), "Thời gian":datetime.now().strftime("%H:%M %d/%m"), "Likes":0, "Comments":"[]"})
                    save_all_data("su-kien.csv", sk); st.success("Đã đăng!"); st.rerun()
            st.divider()
            ds_sk = load_data("su-kien.csv")
            for i, s in enumerate(ds_sk):
                c1, c2 = st.columns([0.85, 0.15])
                c1.write(f"📌 **{s['Tiêu đề']}** ({s['Thời gian']})")
                if c2.button("Xóa 🗑️", key=f"d_sk_{i}"):
                    ds_sk.pop(i); save_all_data("su-kien.csv", ds_sk); st.rerun()

        with t_check:
            nhat_ky = load_data("nhat-ky.csv")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("📑 Đơn xin nghỉ")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Xin nghỉ" and "⏳" in str(it['Trạng thái']):
                        with st.expander(f"{it['Tên']} - {it['Lớp']}"):
                            st.write(it['Nội dung'])
                            if it.get('Ảnh'): st.image(base64.b64decode(it['Ảnh']), width=200)
                            if st.button("Duyệt ✅", key=f"dn_{i}"):
                                nhat_ky[i]['Trạng thái'] = "✅ BGH đã duyệt và cho phép nghỉ!"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
            with col2:
                st.subheader("📸 Điểm danh")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Điểm danh" and "⏳" in str(it['Trạng thái']):
                        with st.expander(f"{it['Tên']} - {it['Lớp']}"):
                            if it.get('Ảnh'): st.image(base64.b64decode(it['Ảnh']), width=200)
                            if st.button("Xác nhận ✅", key=f"dd_{i}"):
                                nhat_ky[i]['Trạng thái'] = "✅ BGH xác nhận điểm danh thành công"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
            with col3:
                st.subheader("💬 Phản ánh")
                for i, it in enumerate(nhat_ky):
                    if it['Loại'] == "Phản ánh":
                        with st.expander(f"Từ: {it['Tên']}"):
                            st.write(it['Nội dung'])
                            rep = st.text_input("Trả lời:", key=f"rp_{i}")
                            if st.button("Gửi ✈️", key=f"rb_{i}"):
                                nhat_ky[i]['Trạng thái'] = f"✅ BGH trả lời: {rep}"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with t_mng:
            st.subheader("Danh sách học sinh toàn trường")
            all_u = load_data("hoc-sinh.csv")
            for i, u in enumerate(all_u):
                if u['role'] == 'student':
                    with st.container(border=True):
                        c1, c2 = st.columns([0.8, 0.2])
                        c1.write(f"🎓 **{u['name']}** | Lớp: {u['class']} | Loại: {u['type']}")
                        if c2.button("Xóa tài khoản 🗑️", key=f"del_u_{i}"):
                            all_u.pop(i); save_all_data("hoc-sinh.csv", all_u); st.rerun()

        with t_diem:
            st.subheader("Cập nhật kết quả học tập")
            all_u = load_data("hoc-sinh.csv")
            s_list = [u['name'] for u in all_u if u['role'] == 'student']
            target = st.selectbox("Chọn học sinh:", s_list)
            if target:
                idx = next(i for i, u in enumerate(all_u) if u['name'] == target)
                with st.form("diem"):
                    d10 = st.text_input("Lớp 10", value=all_u[idx].get('diem_10', ""))
                    d11 = st.text_input("Lớp 11", value=all_u[idx].get('diem_11', ""))
                    d12 = st.text_input("Lớp 12", value=all_u[idx].get('diem_12', ""))
                    if st.form_submit_button("Lưu kết quả"):
                        all_u[idx].update({"diem_10":d10, "diem_11":d11, "diem_12":d12})
                        save_all_data("hoc-sinh.csv", all_u); st.success("Đã cập nhật!")

    # --- GIAO DIỆN HỌC SINH: TRANG CHỦ ---
    else:
        st.title("🏠 TRANG CHỦ")
        
        # Sidebar menu cho học sinh
        menu_hs = st.sidebar.radio("Chức năng", ["🏠 Bảng tin nhà trường", "📝 Thông tin cá nhân", "📊 Kết quả học tập", "🛠️ Gửi yêu cầu"])
        
        if menu_hs == "🏠 Bảng tin nhà trường":
            # Thông báo FB
            nk_all = load_data("nhat-ky.csv")
            tb_fb = [i for i in nk_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
            if tb_fb:
                st.subheader("🔔 Thông báo mới")
                for tb in reversed(tb_fb[-2:]):
                    with st.container(border=True):
                        st.markdown(f"🔵 **Phản hồi từ BGH:** {tb['Trạng thái']}")
            
            st.subheader("📣 Tin tức mới nhất")
            ds_sk = load_data("su-kien.csv")
            if not ds_sk: st.info("Hôm nay chưa có tin mới.")
            for idx, sk in enumerate(reversed(ds_sk)):
                r_idx = len(ds_sk) - 1 - idx
                with st.container(border=True):
                    st.markdown(f"### {sk['Tiêu đề']}")
                    st.caption(f"📅 Đăng lúc: {sk['Thời gian']}")
                    st.write(sk['Nội dung'])
                    if sk.get('Ảnh'): st.image(base64.b64decode(sk['Ảnh']), use_container_width=True)
                    
                    c1, c2 = st.columns([0.2, 0.8])
                    likes = int(sk.get('Likes', 0))
                    if c1.button(f"👍 Like ({likes})", key=f"lk_{r_idx}"):
                        ds_sk[r_idx]['Likes'] = likes + 1
                        save_all_data("su-kien.csv", ds_sk); st.rerun()
                    
                    new_c = st.text_input("Bình luận...", key=f"in_c_{r_idx}")
                    if st.button("Gửi ✈️", key=f"bt_c_{r_idx}"):
                        try: coms = json.loads(sk['Comments'].replace("'", '"'))
                        except: coms = []
                        coms.append({"user":user['name'], "text":new_c})
                        ds_sk[r_idx]['Comments'] = json.dumps(coms, ensure_ascii=False)
                        save_all_data("su-kien.csv", ds_sk); st.rerun()
                    
                    # Hiện bình luận
                    try: 
                        curr_coms = json.loads(sk['Comments'].replace("'", '"'))
                        for c in curr_coms[-3:]: st.markdown(f"**💬 {c['user']}:** {c['text']}")
                    except: pass

        elif menu_hs == "📝 Thông tin cá nhân":
            st.subheader("Hồ sơ học sinh")
            all_u = load_data("hoc-sinh.csv")
            idx = next(i for i, u in enumerate(all_u) if u['username'] == user['username'])
            with st.form("info"):
                f1 = st.text_input("Họ và tên", value=all_u[idx]['name'])
                f2 = st.text_input("Ngày sinh", value=all_u[idx].get('dob', ""))
                f3 = st.text_input("Số CCCD", value=all_u[idx].get('cccd', ""))
                f4 = st.text_input("Số điện thoại", value=all_u[idx].get('phone', ""))
                f5 = st.text_input("Email", value=all_u[idx].get('email', ""))
                f6 = st.text_area("Địa chỉ thường trú", value=all_u[idx].get('address', ""))
                if st.form_submit_button("Lưu thay đổi"):
                    all_u[idx].update({"name":f1,"dob":f2,"cccd":f3,"phone":f4,"email":f5,"address":f6})
                    save_all_data("hoc-sinh.csv", all_u); st.success("✅ Đã lưu!")

        elif menu_hs == "📊 Kết quả học tập":
            st.subheader("Kết quả học tập qua các năm")
            c1, c2, c3 = st.columns(3)
            c1.metric("Điểm Lớp 10", user.get('diem_10', "Trống"))
            c2.metric("Điểm Lớp 11", user.get('diem_11', "Trống"))
            c3.metric("Điểm Lớp 12", user.get('diem_12', "Trống"))

        elif menu_hs == "🛠️ Gửi yêu cầu":
            t_dd, t_com, t_nghi, t_pa = st.tabs(["📸 Điểm danh", "🍱 Hủy bữa", "📑 Xin nghỉ", "💬 Phản ánh"])
            with t_dd:
                a_dd = st.camera_input("Chụp ảnh điểm danh")
                if a_dd and st.button("GỬI 📸"):
                    save_all_data("nhat-ky.csv", load_data("nhat-ky.csv") + [{"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)}])
                    st.success("Đã gửi!")
            with t_com:
                if user.get('type') == "Học sinh ngoại trú":
                    st.warning("Bạn là học sinh ngoại trú, không có chế độ suất ăn để hủy.")
                else:
                    st.error("🚫 Hủy Trưa trước 09h | Hủy Chiều trước 15h.")
                    b = st.multiselect("Chọn buổi muốn hủy:", ["Trưa", "Chiều"], default=["Trưa"])
                    if st.button("Xác nhận hủy suất ăn"):
                        gio = datetime.now().hour
                        if ("Trưa" in b and gio >= 9) or ("Chiều" in b and gio >= 15): st.error("Đã quá giờ quy định!")
                        else:
                            save_all_data("nhat-ky.csv", load_data("nhat-ky.csv") + [{"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY: {b}","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""}])
                            st.success("❌ Đã báo hủy!")
            with t_nghi:
                ly = st.text_area("Lý do xin nghỉ:")
                anh = st.camera_input("Ảnh minh chứng (nếu có)")
                if st.button("Gửi đơn xin nghỉ"):
                    save_all_data("nhat-ky.csv", load_data("nhat-ky.csv") + [{"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(anh)}])
                    st.success("✅ Đã gửi đơn!")
            with t_pa:
                pa = st.text_area("Nội dung phản ánh:")
                if st.button("Gửi ý kiến"):
                    save_all_data("nhat-ky.csv", load_data("nhat-ky.csv") + [{"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":pa,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""}])
                    st.success("📩 Đã nhận!")

    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

# ĐIỀU HƯỚNG CHÍNH
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()