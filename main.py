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

# --- CSS TÙY CHỈNH (Giao diện FB, Ngày tháng, Ảnh nền) ---
def set_style():
    bg_img = "https://unsplash.com"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("{bg_img}"); background-size: cover; }}
        .school-title {{ white-space: nowrap; text-align: center; color: #1E88E5; font-size: clamp(22px, 5vw, 45px); font-weight: bold; margin-bottom: 5px; }}
        .date-display {{ text-align: center; font-size: 18px; color: #555; margin-bottom: 25px; font-weight: 500; font-style: italic; }}
        .comment-box {{ background-color: #f0f2f5; padding: 10px; border-radius: 10px; margin-top: 5px; margin-bottom: 5px; font-size: 14px; border-left: 3px solid #1E88E5; }}
        </style>
        """, unsafe_allow_html=True)

# --- KHỞI TẠO FILE ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            cols = ["username","password","name","class","role","type","dob","cccd","phone","email","address","diem_10","diem_11","diem_12"]
            pd.DataFrame(columns=cols).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["Tiêu đề","Nội dung","Ảnh","Thời gian","Likes","Comments"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh","File"]).to_csv(f, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# --- LOGIN & REGISTRATION ---
def login_page():
    set_style()
    st.markdown('<div class="school-title">TRƯỜNG THPT MÙ CANG CHẢI</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c2:
        with st.container(border=True):
            u = st.text_input("Tài Khoản")
            p = st.text_input("Mật khẩu", type="password")
            if st.button("ĐĂNG NHẬP", use_container_width=True):
                if u == "thptmcc_admin" and p == "bangianhieu2026":
                    st.session_state.logged_in = True; st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin_gv"}; st.rerun()
                elif u == "bantru_mcc" and p == "comngon2026":
                    st.session_state.logged_in = True; st.session_state.user_info = {"name": "Quản lý Bán trú", "role": "admin_an"}; st.rerun()
                else:
                    users = load_data("hoc-sinh.csv")
                    user = next((x for x in users if str(x['username'])==u and str(x['password'])==p), None)
                    if user: st.session_state.logged_in = True; st.session_state.user_info = user; st.rerun()
                    else: st.error("Sai thông tin đăng nhập!")
            st.divider()
            if st.button("Tạo tài khoản cho học sinh", use_container_width=True): st.session_state.page = "register"; st.rerun()

def registration_page():
    st.markdown('<div class="school-title">TẠO TÀI KHOẢN HỌC SINH</div>', unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Họ và tên học sinh:"); l = st.selectbox("Lớp:", [f"10A{i}" for i in range(1,10)] + [f"11A{i}" for i in range(1,8)]); t = st.radio("Loại hình:", ["Học sinh bán trú", "Học sinh ngoại trú"])
        u = st.text_input("Tên tài khoản mới:"); p = st.text_input("Mật khẩu mới:", type="password")
        if st.form_submit_button("XÁC NHẬN ĐĂNG KÝ"):
            if n and u and p:
                all_u = load_data("hoc-sinh.csv")
                all_u.append({"username":u, "password":p, "name":n, "class":l, "role":"student", "type":t})
                save_all_data("hoc-sinh.csv", all_u); st.success("✅ Đăng ký thành công!"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

# --- MAIN APP ---
def main_app():
    set_style()
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

    # Lấy ngày hiện tại
    now = datetime.now()
    date_str = now.strftime("Thứ %u, ngày %d tháng %m năm %Y").replace("Thứ 1","Chủ Nhật").replace("Thứ 2","Thứ Hai").replace("Thứ 3","Thứ Ba").replace("Thứ 4","Thứ Tư").replace("Thứ 5","Thứ Năm").replace("Thứ 6","Thứ Sáu").replace("Thứ 7","Thứ Bảy")

    # --- GIAO DIỆN ADMIN (HỆ THỐNG QUẢN LÝ HỌC SINH) ---
    if user.get('role') == "admin_gv":
        st.markdown('<div class="school-title">HỆ THỐNG QUẢN LÝ HỌC SINH</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="date-display">{date_str}</div>', unsafe_allow_html=True)
        
        tab_post, tab_duyet, tab_users, tab_score, tab_file = st.tabs(["📢 Đăng bài", "📑 Phê duyệt", "👥 Quản lý tài khoản", "📈 Nhập điểm", "📁 Gửi File"])
        
        with tab_post:
            with st.form("p_f", clear_on_submit=True):
                tt = st.text_input("Tiêu đề bài viết"); nd = st.text_area("Nội dung bài viết"); im = st.file_uploader("Hình ảnh", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG BÀI LÊN BẢNG TIN"):
                    sk = load_data("su-kien.csv")
                    sk.append({"Tiêu đề":tt, "Nội dung":nd, "Ảnh":image_to_base64(im), "Thời gian":now.strftime("%H:%M %d/%m"), "Likes":0, "Comments":"[]"})
                    save_all_data("su-kien.csv", sk); st.success("🎉 Đã đăng bài!"); st.rerun()
            st.divider()
            ds_sk = load_data("su-kien.csv")
            for i, s in enumerate(ds_sk):
                c1, c2 = st.columns([0.85, 0.15])
                c1.write(f"📌 **{s['Tiêu đề']}**")
                if c2.button("Xóa 🗑️", key=f"d_sk_{i}"): ds_sk.pop(i); save_all_data("su-kien.csv", ds_sk); st.rerun()

        with tab_duyet:
            nk = load_data("nhat-ky.csv")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("**📑 Duyệt xin nghỉ**")
                for i, it in enumerate(nk):
                    if it['Loại'] == "Xin nghỉ" and "⏳" in str(it['Trạng thái']):
                        with st.expander(it['Tên']):
                            st.write(f"Lý do: {it['Nội dung']}")
                            if it.get('Ảnh'): st.image(base64.b64decode(it['Ảnh']), width=200)
                            if st.button("Duyệt ✅", key=f"dn_{i}"): nk[i]['Trạng thái'] = "✅ BGH đã duyệt và cho phép nghỉ!"; save_all_data("nhat-ky.csv", nk); st.rerun()
            with c2:
                st.write("**📸 Duyệt điểm danh**")
                for i, it in enumerate(nk):
                    if it['Loại'] == "Điểm danh" and "⏳" in str(it['Trạng thái']):
                        with st.expander(it['Tên']):
                            if it.get('Ảnh'): st.image(base64.b64decode(it['Ảnh']), width=200)
                            if st.button("Xác nhận ✅", key=f"dd_{i}"): nk[i]['Trạng thái'] = "✅ BGH xác nhận bạn đã có mặt"; save_all_data("nhat-ky.csv", nk); st.rerun()
            with c3:
                st.write("**💬 Phản ánh**")
                for i, it in enumerate(nk):
                    if it['Loại'] == "Phản ánh":
                        with st.expander(f"Từ {it['Tên']}"):
                            st.write(it['Nội dung']); r = st.text_input("Trả lời:", key=f"r_{i}")
                            if st.button("Gửi phản hồi ✈️", key=f"rb_{i}"): nk[i]['Trạng thái'] = f"✅ BGH trả lời: {r}"; save_all_data("nhat-ky.csv", nk); st.rerun()

        with tab_users:
            all_u = load_data("hoc-sinh.csv")
            for i, u in enumerate(all_u):
                if u['role'] == 'student':
                    with st.container(border=True):
                        col1, col2 = st.columns([0.8, 0.2])
                        col1.write(f"🎓 **{u['name']}** | Lớp: {u['class']} | {u['type']}")
                        if col2.button("Xóa tài khoản 🗑️", key=f"del_u_{i}"): all_u.pop(i); save_all_data("hoc-sinh.csv", all_u); st.rerun()

        with tab_file:
            st.subheader("Gửi tài liệu cho từng học sinh")
            all_u = load_data("hoc-sinh.csv")
            s_list = [u['name'] for u in all_u if u['role'] == 'student']
            target = st.selectbox("Chọn học sinh:", s_list)
            f_up = st.file_uploader("Chọn file (PDF, Ảnh...)", type=['pdf','png','jpg','docx'])
            if st.button("Gửi File 📁"):
                if f_up and target:
                    nk = load_data("nhat-ky.csv"); target_u = next(u for u in all_u if u['name'] == target)
                    nk.append({"Loại":"Tài liệu","Lớp":target_u['class'],"Tên":target,"Nội dung":f_up.name,"Thời gian":now.strftime("%H:%M %d/%m"),"Trạng thái":f"✅ BGH gửi file: {f_up.name}","File":base64.b64encode(f_up.getvalue()).decode()})
                    save_all_data("nhat-ky.csv", nk); st.success("Đã gửi file!")

    # --- QUẢN LÝ BÁN TRÚ ---
    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")
        ds_an = [i for i in load_data("nhat-ky.csv") if i['Loại'] == "Báo ăn"]
        if ds_an: st.table(pd.DataFrame(ds_an))
        else: st.info("Không có ai báo hủy cơm.")

    # --- HỌC SINH: TRANG CHỦ ---
    else:
        st.markdown('<div class="school-title">🏠 TRANG CHỦ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="date-display">{date_str}</div>', unsafe_allow_html=True)
        
        menu = st.sidebar.radio("Danh mục", ["📣 Bảng tin nhà trường", "📝 Hồ sơ cá nhân", "📊 Kết quả học kỳ", "🛠️ Gửi yêu cầu"])
        
        if menu == "📣 Bảng tin nhà trường":
            # Thông báo FB
            nk_all = load_data("nhat-ky.csv")
            tb_fb = [i for i in nk_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
            if tb_fb:
                st.subheader("🔔 Thông báo mới")
                for tb in reversed(tb_fb[-2:]):
                    with st.container(border=True):
                        st.markdown(f"🔵 {tb['Trạng thái']}")
                        if str(tb.get('File')) != "" and str(tb.get('File')) != "nan":
                            href = f'<a href="data:application/octet-stream;base64,{tb["File"]}" download="tai_lieu.pdf" style="text-decoration:none; background:#1E88E5; color:white; padding:5px 10px; border-radius:5px;">📥 Tải tài liệu</a>'
                            st.markdown(href, unsafe_allow_html=True)
            
            st.divider()
            ds_sk = load_data("su-kien.csv")
            for idx, sk in enumerate(reversed(ds_sk)):
                r_idx = len(ds_sk) - 1 - idx
                with st.container(border=True):
                    st.markdown(f"### {sk['Tiêu đề']}"); st.write(sk['Nội dung'])
                    if sk.get('Ảnh'): st.image(base64.b64decode(sk['Ảnh']), use_container_width=True)
                    col_l, col_c = st.columns([0.2, 0.8])
                    likes = int(sk.get('Likes', 0))
                    if col_l.button(f"👍 Thích ({likes})", key=f"lk_{r_idx}"):
                        ds_sk[r_idx]['Likes'] = likes + 1; save_all_data("su-kien.csv", ds_sk); st.rerun()
                    
                    # Bình luận FB
                    try:
                        coms = json.loads(sk['Comments'].replace("'", '"')) if sk.get('Comments') else []
                        for c in coms[-3:]: st.markdown(f"<div class='comment-box'><b>{c['user']}:</b> {c['text']}</div>", unsafe_allow_html=True)
                    except: pass
                    with st.form(f"fc_{r_idx}", clear_on_submit=True):
                        txt = st.text_input("Bình luận...", key=f"ic_{r_idx}")
                        if st.form_submit_button("Gửi ✈️"):
                            if txt:
                                try: coms = json.loads(sk['Comments'].replace("'", '"'))
                                except: coms = []
                                coms.append({"user":user['name'], "text":txt})
                                ds_sk[r_idx]['Comments'] = json.dumps(coms, ensure_ascii=False)
                                save_all_data("su-kien.csv", ds_sk); st.rerun()

        elif menu == "🛠️ Gửi yêu cầu":
            t1, t2, t3, t4 = st.tabs(["Điểm danh", "Hủy bữa ăn", "Xin nghỉ học", "Phản ánh"])
            with t1:
                st.info(f"📍 Điểm danh ngày: {now.strftime('%d/%m/%Y')}")
                a = st.camera_input("Chụp ảnh xác nhận")
                if a and st.button("GỬI 📸"):
                    save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":now.strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a)}]); st.success("Đã gửi!")
            with t2:
                if user.get('type') == "Học sinh ngoại trú": st.warning("Bạn là học sinh ngoại trú, không có suất ăn để hủy.")
                else:
                    st.error("🚫 Cảnh báo: Bữa Trưa hủy trước 09h00 | Bữa Chiều hủy trước 15h00.")
                    b = st.multiselect("Chọn buổi hủy:", ["Trưa", "Chiều"])
                    if st.button("Xác nhận hủy ăn"):
                        gio = now.hour
                        if ("Trưa" in b and gio >= 9) or ("Chiều" in b and gio >= 15): st.error("Đã quá giờ quy định!")
                        else:
                            save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY: {b}","Thời gian":now.strftime("%H:%M"),"Trạng thái":"Đã gửi"}]); st.success("Đã gửi yêu cầu hủy!")
            with t3:
                st.info(f"📑 Đơn xin nghỉ ngày: {now.strftime('%d/%m/%Y')}")
                ly = st.text_area("Lý do nghỉ học:"); a_ng = st.camera_input("Ảnh minh chứng (nếu có)")
                if st.button("Gửi đơn xin nghỉ"):
                    save_all_data("nhat-ky.csv", load_data("nhat-ky.csv")+[{"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly,"Thời gian":now.strftime("%H:%M"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_ng)}]); st.success("Đã gửi đơn!")

        elif menu == "📊 Kết quả học kỳ":
            st.subheader("Kết quả rèn luyện học tập")
            c1, c2, c3 = st.columns(3)
            c1.metric("Lớp 10", user.get('diem_10', "Trống"))
            c2.metric("Lớp 11", user.get('diem_11', "Trống"))
            c3.metric("Lớp 12", user.get('diem_12', "Trống"))

        elif menu == "📝 Thông tin cá nhân":
            all_u = load_data("hoc-sinh.csv"); idx = next(i for i, u in enumerate(all_u) if u['username'] == user['username'])
            with st.form("i"):
                f1 = st.text_input("Họ và tên", value=all_u[idx]['name']); f2 = st.text_input("Ngày sinh", value=all_u[idx].get('dob',"")); f3 = st.text_input("CCCD", value=all_u[idx].get('cccd',""))
                f4 = st.text_input("SĐT", value=all_u[idx].get('phone',"")); f5 = st.text_input("Email", value=all_u[idx].get('email',"")); f6 = st.text_area("Địa chỉ", value=all_u[idx].get('address',""))
                if st.form_submit_button("Cập nhật hồ sơ"):
                    all_u[idx].update({"name":f1,"dob":f2,"cccd":f3,"phone":f4,"email":f5,"address":f6}); save_all_data("hoc-sinh.csv", all_u); st.success("Đã lưu thành công!")

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()