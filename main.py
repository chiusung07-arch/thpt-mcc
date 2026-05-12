# ==========================================
# THPT MÙ CANG CHẢI - SMART SCHOOL SYSTEM
# ==========================================

import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import json
import hashlib
import time

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="THPT Mù Cang Chải",
    page_icon="🏫",
    layout="wide"
)

# ==========================================
# FUNCTIONS
# ==========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def image_to_base64(image_file):
    if image_file:
        try:
            return base64.b64encode(image_file.getvalue()).decode()
        except:
            return ""
    return ""

def load_data(file_name):
    try:
        df = pd.read_csv(file_name)
        return df.where(pd.notnull(df), None).to_dict("records")
    except:
        return []

def save_all_data(file_name, data):
    pd.DataFrame(data).to_csv(file_name, index=False)

# ==========================================
# CREATE FILES
# ==========================================

for f in [
    "hoc-sinh.csv",
    "nhat-ky.csv",
    "su-kien.csv",
    "thong-bao.csv"
]:

    if not os.path.exists(f):

        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=[
                "username","password","name","class","role","avatar","loai_hs"
            ]).to_csv(f, index=False)

        elif f == "su-kien.csv":
            pd.DataFrame(columns=[
                "Tiêu đề","Nội dung","Ảnh","Thời gian","Likes","Comments"
            ]).to_csv(f, index=False)

        elif f == "thong-bao.csv":
            pd.DataFrame(columns=[
                "Tiêu đề","Nội dung","Thời gian"
            ]).to_csv(f, index=False)

        else:
            pd.DataFrame(columns=[
                "Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"
            ]).to_csv(f, index=False)

# ==========================================
# SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ==========================================
# REGISTER
# ==========================================

def registration_page():

    st.title("📝 ĐĂNG KÝ")

    with st.form("reg"):

        name = st.text_input("Họ tên")

        lop = st.selectbox("Lớp", [f"10A{i}" for i in range(1,10)])

        loai_hs = st.selectbox("Loại học sinh", ["Bán trú","Ngoại trú"])

        u_id = st.text_input("Tài khoản")
        pwd = st.text_input("Mật khẩu", type="password")

        avatar = st.file_uploader("Avatar", type=["jpg","png"])

        if st.form_submit_button("Đăng ký"):

            users = load_data("hoc-sinh.csv")

            if any(u.get("username")==u_id for u in users):
                st.error("Tài khoản tồn tại")
            else:
                users.append({
                    "username": u_id,
                    "password": hash_password(pwd),
                    "name": name,
                    "class": lop,
                    "role": "student",
                    "avatar": image_to_base64(avatar),
                    "loai_hs": loai_hs
                })

                save_all_data("hoc-sinh.csv", users)
                st.success("OK")
                st.session_state.page = "login"

# ==========================================
# LOGIN
# ==========================================

def login_page():

    u = st.text_input("User")
    p = st.text_input("Pass", type="password")

    if st.button("Login"):

        users = load_data("hoc-sinh.csv")

        user = next((x for x in users if x["username"]==u and x["password"]==hash_password(p)), None)

        if user:
            st.session_state.logged_in = True
            st.session_state.user_info = user
            st.rerun()

        else:
            st.error("Sai")

# ==========================================
# MAIN
# ==========================================

def main_app():

    user = st.session_state.user_info

    st.sidebar.title(user["name"])

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # ======================================
    # STUDENT
    # ======================================

    if user["role"] == "student":

        st.title("🎓 HỌC SINH")

        tabs = [
            "🔔 Thông báo",
            "📸 Điểm danh",
            "📝 Xin nghỉ",
            "💬 Phản ánh",
            "🎉 Sự kiện"
        ]

        if user["loai_hs"] == "Bán trú":
            tabs.insert(2, "🍱 Hủy bữa")

        tbs = st.tabs(tabs)

        i = 0

        # THÔNG BÁO
        with tbs[i]:
            st.subheader("🔔 Thông báo")

            tb = load_data("thong-bao.csv")

            for t in reversed(tb):
                st.info(f"{t['Tiêu đề']} - {t['Nội dung']}")

        i += 1

        # ĐIỂM DANH
        with tbs[i]:
            st.write("Điểm danh")

        i += 1

        # HỦY BỮA (nếu có)
        if user["loai_hs"] == "Bán trú":
            with tbs[i]:
                st.write("Hủy bữa")
            i += 1

        # XIN NGHỈ
        with tbs[i]:
            st.write("Xin nghỉ")

        i += 1

        # PHẢN ÁNH
        with tbs[i]:
            st.write("Phản ánh")

        i += 1

        # SỰ KIỆN
        with tbs[i]:
            st.write("Sự kiện")

    # ======================================
    # ADMIN
    # ======================================

    elif user["role"] == "admin_gv":

        st.title("🏫 BAN GIÁM HIỆU")

        tabs = st.tabs([
            "Đơn nghỉ",
            "Điểm danh",
            "Phản ánh",
            "Đăng bài",
            "Thông báo"
        ])

        t_ng, t_dd, t_pa, t_post, t_tb = tabs

        # THÔNG BÁO
        with t_tb:

            st.subheader("Gửi thông báo")

            ds = load_data("thong-bao.csv")

            with st.form("tb"):

                t = st.text_input("Tiêu đề")
                n = st.text_area("Nội dung")

                if st.form_submit_button("Gửi"):

                    ds.append({
                        "Tiêu đề": t,
                        "Nội dung": n,
                        "Thời gian": str(datetime.now())
                    })

                    save_all_data("thong-bao.csv", ds)

                    st.success("OK")

# ==========================================
# RUN
# ==========================================

if not st.session_state.logged_in:

    if st.session_state.page == "login":
        login_page()
    else:
        registration_page()

else:
    main_app()