import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import json

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# --- HÀM HỖ TRỢ KỸ THUẬT ---
def file_to_base64(file):
    if file is not None:
        try: return base64.b64encode(file.getvalue()).decode()
        except: return ""
    return ""

def load_data(file_name):
    try: 
        df = pd.read_csv(file_name)
        return df.where(pd.notnull(df), "").to_dict('records')
    except: return []

def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

# --- CSS GIAO DIỆN ---
def set_style():
    bg_img = "https://unsplash.com"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url("{bg_img}"); background-size: cover; }}
        .school-title {{ white-space: nowrap; text-align: center; color: #1E88E5; font-size: clamp(22px, 5vw, 45px); font-weight: bold; margin-bottom: 5px; }}
        .date-display {{ text-align: center; font-size: 18px; color: #555; margin-bottom: 25px; font-weight: 500; }}
        </style>
        """, unsafe_allow_html=True)

# --- KHỞI TẠO FILE ---
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            cols = ["username","password","name","class","role","type","dob","cccd","phone","email","address","diem_10","diem_11","diem_12","file_diem"]
            pd.DataFrame(columns=cols).to_csv(f, index=False)
        else: pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh","File"]).to_csv(f, index=False)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# --- TRANG ĐĂNG NHẬP & ĐĂNG KÝ ---
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
                    else: st.error("Sai tài khoản hoặc mật khẩu!")
            st.divider()
            if st.button("Tạo tài khoản cho học sinh", use_container_width=True): st.session_state.page = "register"; st.rerun()

def registration_page():
    st.markdown('<div class="school-title">TẠO TÀI KHOẢN HỌC SINH</div>', unsafe_allow_html=True)
    with st.form("reg"):
        n = st.text_input("Họ và tên học sinh:"); l = st.selectbox("Lớp:", [f"10A{i}" for i in range(1,10)] + [f"11A{i}" for i in range(1,8)] + [f"12A{i}" for i in range(1,8)]); t = st.radio("Loại hình:", ["Học sinh bán trú", "Học sinh ngoại trú"])
        u = st.text_input("Tài khoản:"); p = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("XÁC NHẬN"):
            all_u = load_data("hoc-sinh.csv")
            all_u.append({"username":u, "password":p, "name":n, "class":l, "role":"student", "type":t})
            save_all_data("hoc-sinh.csv", all_u); st.success("✅ Đăng ký thành công!"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

# --- MAIN APP ---
def main_app():
    set_style()
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    
    # Xử lý ngày tháng chuẩn (Sửa lỗi Thứ 2)
    now = datetime.now()
    weekday = now.isoweekday() # 1=Thứ 2, 7=Chủ Nhật
    days = ["", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    date_str = f"{days[weekday]}, ngày {now.strftime('%d/%m/%Y')}"

    # --- BAN GIÁM HIỆU ---
    if user.get('role') == "admin_gv":
        st.markdown('<div class="school-title">HỆ THỐNG QUẢN LÝ HỌC SINH</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="date-display">{date_str}</div>', unsafe_allow_html=True)
        
        tab_sk, tab_duyet, tab_users, tab_score, tab_file = st.tabs(["📢 Đăng bài", "📑 Phê duyệt", "👥 Tài khoản", "📈 Nhập điểm & File", "📁 Gửi File riêng"])
        
        with tab_score:
            st.subheader("Cập nhật Điểm & File học tập theo lớp")
            all_u = load_data("hoc-sinh.csv")
            classes = sorted(list(set([u['class'] for u in all_u if u['role'] == 'student'])))
            sel_class = st.selectbox("Chọn lớp:", classes)
            
            if sel_class:
                students_in_class = [u for u in all_u if u['class'] == sel_class]
                st.write(f"Danh sách học sinh lớp {sel_class}:")
                for s in students_in_class:
                    with st.expander(f"Học sinh: {s['name']}"):
                        with st.form(key=f"score_{s['username']}"):
                            d10 = st.text_input("Điểm lớp 10", value=s.get('diem_10', ""))
                            d11 = st.text_input("Điểm lớp 11", value=s.get('diem_11', ""))
                            d12 = st.text_input("Điểm lớp 12", value=s.get('diem_12', ""))
                            f_up = st.file_uploader("Cập nhật file điểm chi tiết (PDF/Excel)", type=['pdf','xlsx'], key=f"f_{s['username']}")
                            if st.form_submit_button("Lưu dữ liệu"):
                                idx = next(i for i, u in enumerate(all_u) if u['username'] == s['username'])
                                all_u[idx].update({"diem_10":d10, "diem_11":d11, "diem_12":d12, "file_diem": file_to_base64(f_up) if f_up else s.get('file_diem', "")})
                                save_all_data("hoc-sinh.csv", all_u); st.success(f"Đã cập nhật cho {s['name']}!"); st.rerun()

        # (Các tab Đăng bài, Phê duyệt, Tài khoản... giữ nguyên logic chuẩn đã trao đổi)

    # --- HỌC SINH ---
    else:
        st.markdown('<div class="school-title">🏠 TRANG CHỦ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="date-display">{date_str}</div>', unsafe_allow_html=True)
        
        menu = st.sidebar.radio("Danh mục", ["📣 Bảng tin", "📝 Hồ sơ cá nhân", "📊 Kết quả học kỳ", "🛠️ Gửi yêu cầu"])
        
        if menu == "📊 Kết quả học kỳ":
            st.subheader("Kết quả rèn luyện & Học tập")
            c1, c2, c3 = st.columns(3)
            c1.metric("Lớp 10", user.get('diem_10', "Trống"))
            c2.metric("Lớp 11", user.get('diem_11', "Trống"))
            c3.metric("Lớp 12", user.get('diem_12', "Trống"))
            
            if str(user.get('file_diem')) != "":
                st.divider()
                st.write("📂 **Tài liệu điểm chi tiết từ BGH:**")
                b64 = user['file_diem']
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="bang_diem_{user["name"]}.pdf" style="text-decoration:none; background:#28a745; color:white; padding:8px 20px; border-radius:5px;">📥 Tải bảng điểm chi tiết</a>'
                st.markdown(href, unsafe_allow_html=True)

        elif menu == "📝 Hồ sơ cá nhân":
            st.subheader("Cập nhật thông tin cá nhân")
            all_u = load_data("hoc-sinh.csv")
            idx = next(i for i, u in enumerate(all_u) if u['username'] == user['username'])
            with st.form("profile"):
                n = st.text_input("Họ và tên", value=all_u[idx]['name'])
                d = st.text_input("Ngày sinh", value=all_u[idx].get('dob', ""))
                c = st.text_input("Số CCCD", value=all_u[idx].get('cccd', ""))
                p = st.text_input("Số điện thoại", value=all_u[idx].get('phone', ""))
                e = st.text_input("Email", value=all_u[idx].get('email', ""))
                a = st.text_area("Địa chỉ thường trú", value=all_u[idx].get('address', ""))
                if st.form_submit_button("Lưu thay đổi"):
                    all_u[idx].update({"name":n, "dob":d, "cccd":c, "phone":p, "email":e, "address":a})
                    save_all_data("hoc-sinh.csv", all_u); st.success("✅ Đã cập nhật hồ sơ!"); st.rerun()

        elif menu == "🛠️ Gửi yêu cầu":
            t1, t2, t3, t4 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh"])
            with t4:
                st.subheader("Gửi phản ánh/kiến nghị")
                pa = st.text_area("Nội dung ý kiến:")
                if st.button("Gửi tới BGH"):
                    if pa:
                        save_all_data("nhat-ky.csv", load_data("nhat-ky.csv") + [{"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":pa,"Thời gian":now.strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Đã gửi"}])
                        st.success("📩 Cảm ơn bạn, phản ánh đã được gửi đi!")

    if st.sidebar.button("ĐĂNG XUẤT"): st.session_state.logged_in = False; st.rerun()

# ĐIỀU HƯỚNG
if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: registration_page()
else: main_app()