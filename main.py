# ==========================================
# THPT MÙ CANG CHẢI - SMART SCHOOL SYSTEM
# BẢN ĐÃ THÊM:
# ✅ BÁN TRÚ / NGOẠI TRÚ
# ✅ NGOẠI TRÚ KHÔNG CÓ TAB HỦY BỮA
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
# CẤU HÌNH
# ==========================================

st.set_page_config(
    page_title="THPT Mù Cang Chải",
    page_icon="🏫",
    layout="wide"
)

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    font-size: 15px;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}

[data-testid="stSidebar"] {
    background-color: #eef2f7;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HÀM
# ==========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def image_to_base64(image_file):

    if image_file is not None:

        try:
            return base64.b64encode(
                image_file.getvalue()
            ).decode()

        except:
            return ""

    return ""

@st.cache_data(ttl=2)
def load_data(file_name):

    try:

        df = pd.read_csv(file_name)

        return df.where(
            pd.notnull(df),
            None
        ).to_dict('records')

    except:
        return []

def save_all_data(file_name, data_list):

    pd.DataFrame(data_list).to_csv(
        file_name,
        index=False
    )

# ==========================================
# KHỞI TẠO FILE
# ==========================================

for f in [
    "hoc-sinh.csv",
    "nhat-ky.csv",
    "su-kien.csv",
    "thoikhoabieu.csv"
]:

    if not os.path.exists(f):

        if f == "hoc-sinh.csv":

            pd.DataFrame(
                columns=[
                    "username",
                    "password",
                    "name",
                    "class",
                    "role",
                    "avatar",
                    "student_type"
                ]
            ).to_csv(f, index=False)

        elif f == "su-kien.csv":

            pd.DataFrame(
                columns=[
                    "Tiêu đề",
                    "Nội dung",
                    "Ảnh",
                    "Thời gian",
                    "Likes",
                    "Comments"
                ]
            ).to_csv(f, index=False)

        elif f == "thoikhoabieu.csv":

            pd.DataFrame(
                columns=[
                    "Lớp",
                    "Thứ",
                    "Tiết 1",
                    "Tiết 2",
                    "Tiết 3",
                    "Tiết 4",
                    "Tiết 5"
                ]
            ).to_csv(f, index=False)

        else:

            pd.DataFrame(
                columns=[
                    "Loại",
                    "Lớp",
                    "Tên",
                    "Nội dung",
                    "Thời gian",
                    "Trạng thái",
                    "Ảnh"
                ]
            ).to_csv(f, index=False)

# ==========================================
# SESSION
# ==========================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "login"

# ==========================================
# ĐĂNG KÝ
# ==========================================

def registration_page():

    st.title("📝 ĐĂNG KÝ HỌC SINH")

    with st.form("reg_form"):

        name = st.text_input(
            "Họ và tên học sinh"
        )

        classes = (
            [f"10A{i}" for i in range(1,10)] +
            [f"11A{i}" for i in range(1,8)] +
            [f"12A{i}" for i in range(1,8)]
        )

        lop = st.selectbox(
            "Lớp học",
            classes
        )

        # ==========================
        # BÁN TRÚ / NGOẠI TRÚ
        # ==========================

        student_type = st.selectbox(
            "Loại học sinh",
            [
                "Bán trú",
                "Ngoại trú"
            ]
        )

        avatar = st.file_uploader(
            "Ảnh đại diện",
            type=['jpg','png']
        )

        u_id = st.text_input(
            "Tài khoản"
        )

        pwd = st.text_input(
            "Mật khẩu",
            type="password"
        )

        if st.form_submit_button(
            "Xác nhận đăng ký"
        ):

            if not name or not u_id or not pwd:

                st.warning(
                    "⚠️ Nhập đầy đủ thông tin!"
                )

            else:

                data = load_data(
                    "hoc-sinh.csv"
                )

                if any(
                    str(u.get('username', '')) == u_id
                    for u in data
                ):

                    st.error(
                        "⚠️ Tài khoản đã tồn tại!"
                    )

                else:

                    data.append({

                        "username": u_id,

                        "password":
                        hash_password(pwd),

                        "name": name,

                        "class": lop,

                        "role": "student",

                        "avatar":
                        image_to_base64(avatar),

                        "student_type":
                        student_type

                    })

                    save_all_data(
                        "hoc-sinh.csv",
                        data
                    )

                    st.success(
                        "✅ Đăng ký thành công!"
                    )

                    st.session_state.page = "login"

    if st.button("Quay lại"):

        st.session_state.page = "login"

        st.rerun()

# ==========================================
# ĐĂNG NHẬP
# ==========================================

def login_page():

    st.markdown("""
    <h1 style='text-align:center;color:#1565C0;'>
    🏫 THPT MÙ CANG CHẢI
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    u_in = st.text_input(
        "Tên tài khoản"
    )

    p_in = st.text_input(
        "Mật khẩu",
        type="password"
    )

    if st.button(
        "ĐĂNG NHẬP"
    ):

        if (
            u_in == "thptmcc_admin"
            and
            p_in == "giaovien2024"
        ):

            st.session_state.logged_in = True

            st.session_state.user_info = {

                "name": "Ban Giám Hiệu",
                "role": "admin_gv"

            }

            st.rerun()

        elif (
            u_in == "bantru_mcc"
            and
            p_in == "comngon2024"
        ):

            st.session_state.logged_in = True

            st.session_state.user_info = {

                "name": "Quản lý bán trú",
                "role": "admin_an"

            }

            st.rerun()

        else:

            users = load_data(
                "hoc-sinh.csv"
            )

            user = next(

                (
                    u for u in users

                    if str(u.get('username', '')) == u_in

                    and

                    str(u.get('password', '')) ==
                    hash_password(p_in)

                ),

                None
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.user_info = user

                st.rerun()

            else:

                st.error(
                    "❌ Sai thông tin!"
                )

    if st.button(
        "Đăng ký mới"
    ):

        st.session_state.page = "register"

        st.rerun()

# ==========================================
# APP CHÍNH
# ==========================================

def main_app():

    user = st.session_state.user_info

    st.sidebar.title(
        f"👤 {user['name']}"
    )

    st.sidebar.write(
        f"🎓 {user.get('student_type', '')}"
    )

    if st.sidebar.button(
        "ĐĂNG XUẤT"
    ):

        st.session_state.clear()

        st.rerun()

    # ======================================
    # HỌC SINH
    # ======================================

    if user.get('role') == "student":

        st.title("🎓 CỔNG HỌC SINH")

        # ==========================
        # TABS
        # ==========================

        if user.get("student_type") == "Bán trú":

            tabs = st.tabs([

                "📸 Điểm danh",
                "🍱 Hủy bữa",
                "📝 Xin nghỉ",
                "💬 Phản ánh",
                "🎉 Sự kiện",
                "📅 Thời khóa biểu"

            ])

            t1, t2, t3, t4, t5, t6 = tabs

        else:

            tabs = st.tabs([

                "📸 Điểm danh",
                "📝 Xin nghỉ",
                "💬 Phản ánh",
                "🎉 Sự kiện",
                "📅 Thời khóa biểu"

            ])

            t1, t3, t4, t5, t6 = tabs

        # ==========================
        # ĐIỂM DANH
        # ==========================

        with t1:

            st.subheader("📸 Điểm danh")

            a_dd = st.camera_input(
                "Chụp khuôn mặt"
            )

            if a_dd and st.button(
                "GỬI ĐIỂM DANH"
            ):

                with st.spinner(
                    "🤖 AI đang nhận diện..."
                ):

                    time.sleep(2)

                st.success(
                    "✅ Điểm danh thành công!"
                )

        # ==========================
        # HỦY BỮA
        # ==========================

        if user.get("student_type") == "Bán trú":

            with t2:

                st.subheader(
                    "🍱 Hủy bữa"
                )

                st.info(
                    "Chỉ học sinh bán trú mới có mục này."
                )

        # ==========================
        # XIN NGHỈ
        # ==========================

        with t3:

            st.subheader(
                "📝 Xin nghỉ"
            )

            st.text_area(
                "Lý do nghỉ"
            )

        # ==========================
        # PHẢN ÁNH
        # ==========================

        with t4:

            st.subheader(
                "💬 Phản ánh"
            )

            st.text_area(
                "Ý kiến phản ánh"
            )

        # ==========================
        # SỰ KIỆN
        # ==========================

        with t5:

            st.subheader(
                "🎉 Sự kiện"
            )

            st.info(
                "Chưa có sự kiện."
            )

        # ==========================
        # TKB
        # ==========================

        with t6:

            st.subheader(
                "📅 Thời khóa biểu"
            )

            st.info(
                "Chưa có dữ liệu."
            )

# ==========================================
# ĐIỀU HƯỚNG
# ==========================================

if not st.session_state.logged_in:

    if st.session_state.page == "login":

        login_page()

    else:

        registration_page()

else:

    main_app()