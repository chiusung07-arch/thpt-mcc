import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import hashlib

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="THPT Mù Cang Chải",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CSS
# =========================================

def set_style():
    st.markdown("""
    <style>

    .stApp {
        background-image:
        linear-gradient(rgba(255,255,255,0.88),
        rgba(255,255,255,0.88)),
        url("https://images.unsplash.com/photo-1509062522246-3755977927d7");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:#1565C0;
        margin-bottom:10px;
    }

    .sub-title{
        text-align:center;
        color:#555;
        font-size:18px;
        margin-bottom:30px;
    }

    .card{
        padding:20px;
        border-radius:20px;
        background:white;
        box-shadow:0 4px 15px rgba(0,0,0,0.1);
    }

    div[data-testid="stMetric"]{
        background:white;
        padding:15px;
        border-radius:15px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }

    </style>
    """, unsafe_allow_html=True)

# =========================================
# HASH PASSWORD
# =========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================================
# FILE SYSTEM
# =========================================

USER_FILE = "hoc-sinh.csv"
LOG_FILE = "nhat-ky.csv"

# =========================================
# CREATE FILES
# =========================================

def create_files():

    if not os.path.exists(USER_FILE):

        cols = [
            "username",
            "password",
            "name",
            "class",
            "role",
            "type",
            "dob",
            "cccd",
            "phone",
            "email",
            "address",
            "diem_10",
            "diem_11",
            "diem_12",
            "file_diem"
        ]

        pd.DataFrame(columns=cols).to_csv(USER_FILE, index=False)

    if not os.path.exists(LOG_FILE):

        cols = [
            "Loại",
            "Lớp",
            "Tên",
            "Nội dung",
            "Thời gian",
            "Trạng thái"
        ]

        pd.DataFrame(columns=cols).to_csv(LOG_FILE, index=False)

# =========================================
# LOAD DATA
# =========================================

def load_data(file):

    try:
        df = pd.read_csv(file)

        if df.empty:
            return []

        return df.fillna("").to_dict("records")

    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
        return []

# =========================================
# SAVE DATA
# =========================================

def save_data(file, data):

    try:
        pd.DataFrame(data).to_csv(file, index=False)

    except Exception as e:
        st.error(f"Lỗi lưu dữ liệu: {e}")

# =========================================
# FILE TO BASE64
# =========================================

def file_to_base64(file):

    if file is None:
        return ""

    try:
        return base64.b64encode(file.getvalue()).decode()

    except Exception as e:
        st.error(f"Lỗi upload file: {e}")
        return ""

# =========================================
# INIT SESSION
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = {}

# =========================================
# LOGIN PAGE
# =========================================

def login_page():

    set_style()

    st.markdown(
        '<div class="main-title">🏫 TRƯỜNG THPT MÙ CANG CHẢI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Hệ thống quản lý học sinh thông minh</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1,1.2,1])

    with c2:

        with st.container(border=True):

            st.subheader("🔐 Đăng nhập")

            username = st.text_input("Tài khoản")
            password = st.text_input("Mật khẩu", type="password")

            if st.button("ĐĂNG NHẬP", use_container_width=True):

                users = load_data(USER_FILE)

                hashed = hash_password(password)

                user = next(
                    (
                        u for u in users
                        if str(u["username"]) == username
                        and str(u["password"]) == hashed
                    ),
                    None
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success("Đăng nhập thành công!")
                    st.rerun()

                else:
                    st.error("Sai tài khoản hoặc mật khẩu")

            st.divider()

            if st.button("📝 Tạo tài khoản"):
                st.session_state.page = "register"
                st.rerun()

# =========================================
# REGISTER PAGE
# =========================================

def register_page():

    set_style()

    st.markdown(
        '<div class="main-title">📝 ĐĂNG KÝ HỌC SINH</div>',
        unsafe_allow_html=True
    )

    users = load_data(USER_FILE)

    with st.form("register"):

        name = st.text_input("Họ và tên")

        lop = st.selectbox(
            "Lớp",
            [f"10A{i}" for i in range(1,10)] +
            [f"11A{i}" for i in range(1,8)] +
            [f"12A{i}" for i in range(1,8)]
        )

        loai = st.radio(
            "Loại hình",
            ["Học sinh bán trú", "Học sinh ngoại trú"]
        )

        username = st.text_input("Tài khoản")

        password = st.text_input(
            "Mật khẩu",
            type="password"
        )

        confirm = st.text_input(
            "Nhập lại mật khẩu",
            type="password"
        )

        submit = st.form_submit_button("XÁC NHẬN")

        if submit:

            if not all([name, username, password]):
                st.warning("Vui lòng nhập đầy đủ thông tin")

            elif password != confirm:
                st.error("Mật khẩu nhập lại không khớp")

            elif any(u["username"] == username for u in users):
                st.error("Tài khoản đã tồn tại")

            elif len(password) < 6:
                st.warning("Mật khẩu tối thiểu 6 ký tự")

            else:

                users.append({
                    "username": username,
                    "password": hash_password(password),
                    "name": name,
                    "class": lop,
                    "role": "student",
                    "type": loai
                })

                save_data(USER_FILE, users)

                st.success("✅ Đăng ký thành công!")

                st.balloons()

                st.session_state.page = "login"

    if st.button("⬅ Quay lại"):
        st.session_state.page = "login"
        st.rerun()

# =========================================
# MAIN APP
# =========================================

def main_app():

    set_style()

    user = st.session_state.user

    now = datetime.now()

    days = [
        "Thứ Hai",
        "Thứ Ba",
        "Thứ Tư",
        "Thứ Năm",
        "Thứ Sáu",
        "Thứ Bảy",
        "Chủ Nhật"
    ]

    date_text = f"""
    {days[now.weekday()]},
    {now.strftime('%d/%m/%Y')}
    """

    st.sidebar.title(f"👤 {user['name']}")

    st.sidebar.info(date_text)

    menu = st.sidebar.radio(
        "Chức năng",
        [
            "🏠 Trang chủ",
            "📊 Kết quả học tập",
            "📝 Hồ sơ",
            "📨 Gửi phản ánh"
        ]
    )

    # =====================================
    # HOME
    # =====================================

    if menu == "🏠 Trang chủ":

        st.markdown(
            '<div class="main-title">🏫 HỆ THỐNG HỌC SINH</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("Học lực", "Khá")
        c2.metric("Điểm danh", "98%")
        c3.metric("Hạnh kiểm", "Tốt")

        st.success("Chào mừng bạn đến với hệ thống")

    # =====================================
    # SCORE
    # =====================================

    elif menu == "📊 Kết quả học tập":

        st.subheader("📈 Kết quả học tập")

        c1, c2, c3 = st.columns(3)

        c1.metric("Lớp 10", user.get("diem_10", "Trống"))
        c2.metric("Lớp 11", user.get("diem_11", "Trống"))
        c3.metric("Lớp 12", user.get("diem_12", "Trống"))

    # =====================================
    # PROFILE
    # =====================================

    elif menu == "📝 Hồ sơ":

        st.subheader("Thông tin cá nhân")

        st.write(f"👤 Họ tên: {user['name']}")
        st.write(f"🏫 Lớp: {user['class']}")
        st.write(f"📚 Loại hình: {user['type']}")

    # =====================================
    # FEEDBACK
    # =====================================

    elif menu == "📨 Gửi phản ánh":

        st.subheader("Gửi phản ánh")

        text = st.text_area("Nhập nội dung")

        if st.button("Gửi"):

            if text:

                logs = load_data(LOG_FILE)

                logs.append({
                    "Loại": "Phản ánh",
                    "Lớp": user["class"],
                    "Tên": user["name"],
                    "Nội dung": text,
                    "Thời gian": now.strftime("%H:%M %d/%m/%Y"),
                    "Trạng thái": "Đã gửi"
                })

                save_data(LOG_FILE, logs)

                st.success("📩 Đã gửi phản ánh")

            else:
                st.warning("Bạn chưa nhập nội dung")

    # =====================================
    # LOGOUT
    # =====================================

    if st.sidebar.button("🚪 Đăng xuất"):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.rerun()

# =========================================
# START
# =========================================

create_files()

if not st.session_state.logged_in:

    if st.session_state.page == "login":
        login_page()

    else:
        register_page()

else:
    main_app()