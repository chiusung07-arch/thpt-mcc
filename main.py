import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# Tự động tạo file dữ liệu nếu chưa có
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

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# --- GIAO DIỆN ---
def login_page():
    st.title("🏫 THPT MÙ CANG CHẢI")
    u = st.text_input("Tài khoản")
    p = st.text_input("Mật khẩu", type="password")
    if st.button("ĐĂNG NHẬP"):
        if u == "admin" and p == "123": # Admin mặc định
            st.session_state.logged_in = True
            st.session_state.user_info = {"name": "Ban Giám Hiệu", "role": "admin"}
            st.rerun()
        else:
            users = load_data("hoc-sinh.csv")
            user = next((x for x in users if str(x['username'])==u and str(x['password'])==p), None)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = user
                st.rerun()
            else: st.error("Sai tài khoản!")
    if st.button("Đăng ký học sinh mới"): st.session_state.page = "reg"; st.rerun()

def reg_page():
    st.title("📝 ĐĂNG KÝ")
    with st.form("f"):
        n = st.text_input("Họ tên")
        c = st.text_input("Lớp")
        u = st.text_input("Tên đăng nhập")
        p = st.text_input("Mật khẩu", type="password")
        if st.form_submit_button("Xác nhận"):
            save_data("hoc-sinh.csv", {"username":u, "password":p, "name":n, "class":c, "role":"student"})
            st.success("Xong! Quay lại đăng nhập"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

def main_app():
    user = st.session_state.user_info
    st.sidebar.write(f"Chào, {user['name']}")
    if st.sidebar.button("Thoát"): st.session_state.logged_in = False; st.rerun()

    if user['role'] == "student":
        st.title("HỌC SINH")
        if st.button("ĐIỂM DANH"):
            save_data("nhat-ky.csv", {"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Thời gian":datetime.now().strftime("%H:%M %d/%m")})
            st.success("Đã điểm danh!")
    else:
        st.title("BAN GIÁM HIỆU")
        data = load_data("nhat-ky.csv")
        if data: st.table(pd.DataFrame(data))
        else: st.write("Chưa có dữ liệu.")

if not st.session_state.logged_in:
    if st.session_state.page == "login": login_page()
    else: reg_page()
else: main_app()
