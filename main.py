import streamlit as st
from datetime import datetime
import pandas as pd
import os
import base64
import hashlib

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="THPT Mù Cang Chải",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CSS
# ==================================================

def set_style():

    st.markdown("""
    <style>

    .stApp{
        background-image:
        linear-gradient(rgba(255,255,255,0.88),
        rgba(255,255,255,0.88)),
        url("https://images.unsplash.com/photo-1509062522246-3755977927d7");

        background-size:cover;
        background-position:center;
        background-attachment:fixed;
    }

    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:#1565C0;
        margin-bottom:5px;
    }

    .sub-title{
        text-align:center;
        font-size:18px;
        color:#666;
        margin-bottom:25px;
    }

    div[data-testid="stMetric"]{
        background:white;
        padding:15px;
        border-radius:15px;
        box-shadow:0 4px 10px rgba(0,0,0,0.08);
    }

    </style>
    """, unsafe_allow_html=True)

# ==================================================
# FILE
# ==================================================

USER_FILE = "hoc-sinh.csv"
LOG_FILE = "nhat-ky.csv"

# ==================================================
# ADMIN ACCOUNT
# ==================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_ACCOUNTS = {
    "thptmcc_admin": {
        "password": hash_password("bangianhieu2026"),
        "name": "Ban Giám Hiệu",
        "role": "admin_gv"
    },

    "bantru_mcc": {
        "password": hash_password("comngon2026"),
        "name": "Quản lý Bán trú",
        "role": "admin_an"
    }
}

# ==================================================
# CREATE FILE
# ==================================================

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

# ==================================================
# LOAD DATA
# ==================================================

def load_data(file):

    try:

        df = pd.read_csv(file)

        if df.empty:
            return []

        return df.fillna("").to_dict("records")

    except:
        return []

# ==================================================
# SAVE DATA
# ==================================================

def save_data(file, data):

    pd.DataFrame(data).to_csv(file, index=False)

# ==================================================
# FILE TO BASE64
# ==================================================

def file_to_base64(file):

    if file is not None:

        try:
            return base64.b64encode(
                file.getvalue()
            ).decode()

        except:
            return ""

    return ""

# ==================================================
# SESSION
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = {}

# ==================================================
# LOGIN PAGE
# ==================================================

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

            password = st.text_input(
                "Mật khẩu",
                type="password"
            )

            if st.button(
                "ĐĂNG NHẬP",
                use_container_width=True
            ):

                hashed = hash_password(password)

                # ==================================
                # LOGIN ADMIN
                # ==================================

                if username in ADMIN_ACCOUNTS:

                    admin = ADMIN_ACCOUNTS[username]

                    if hashed == admin["password"]:

                        st.session_state.logged_in = True

                        st.session_state.user = {
                            "username": username,
                            "name": admin["name"],
                            "role": admin["role"]
                        }

                        st.success("Đăng nhập admin thành công!")

                        st.rerun()

                    else:
                        st.error("Sai mật khẩu admin")

                # ==================================
                # LOGIN STUDENT
                # ==================================

                else:

                    users = load_data(USER_FILE)

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

            if st.button(
                "📝 Tạo tài khoản học sinh",
                use_container_width=True
            ):

                st.session_state.page = "register"

                st.rerun()

# ==================================================
# REGISTER PAGE
# ==================================================

def register_page():

    set_style()

    st.markdown(
        '<div class="main-title">📝 ĐĂNG KÝ HỌC SINH</div>',
        unsafe_allow_html=True
    )

    users = load_data(USER_FILE)

    with st.form("register_form"):

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

                st.error("Mật khẩu không khớp")

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

# ==================================================
# MAIN APP
# ==================================================

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
    ngày {now.strftime('%d/%m/%Y')}
    """

    st.sidebar.title(f"👤 {user['name']}")

    st.sidebar.info(date_text)

    # ==================================================
    # ADMIN GIÁO VIÊN
    # ==================================================

    if user.get("role") == "admin_gv":

        st.markdown(
            '<div class="main-title">📚 QUẢN TRỊ BAN GIÁM HIỆU</div>',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs([
            "👥 Học sinh",
            "📊 Điểm số",
            "📨 Phản ánh"
        ])

        # ==============================================
        # TAB HỌC SINH
        # ==============================================

        with tab1:

            users = load_data(USER_FILE)

            students = [
                u for u in users
                if u.get("role") == "student"
            ]

            st.dataframe(students, use_container_width=True)

        # ==============================================
        # TAB ĐIỂM
        # ==============================================

        with tab2:

            users = load_data(USER_FILE)

            students = [
                u for u in users
                if u.get("role") == "student"
            ]

            classes = sorted(
                list(set([u["class"] for u in students]))
            )

            selected_class = st.selectbox(
                "Chọn lớp",
                classes
            )

            students_class = [
                u for u in students
                if u["class"] == selected_class
            ]

            for s in students_class:

                with st.expander(f"👤 {s['name']}"):

                    with st.form(f"score_{s['username']}"):

                        d10 = st.text_input(
                            "Điểm lớp 10",
                            value=s.get("diem_10", "")
                        )

                        d11 = st.text_input(
                            "Điểm lớp 11",
                            value=s.get("diem_11", "")
                        )

                        d12 = st.text_input(
                            "Điểm lớp 12",
                            value=s.get("diem_12", "")
                        )

                        file_upload = st.file_uploader(
                            "Upload bảng điểm",
                            type=["pdf", "xlsx"],
                            key=s["username"]
                        )

                        submit = st.form_submit_button(
                            "💾 Lưu"
                        )

                        if submit:

                            index = next(
                                i for i, u in enumerate(users)
                                if u["username"] == s["username"]
                            )

                            users[index].update({
                                "diem_10": d10,
                                "diem_11": d11,
                                "diem_12": d12,
                                "file_diem":
                                file_to_base64(file_upload)
                                if file_upload
                                else s.get("file_diem", "")
                            })

                            save_data(USER_FILE, users)

                            st.success(
                                f"Đã cập nhật cho {s['name']}"
                            )

                            st.rerun()

        # ==============================================
        # TAB PHẢN ÁNH
        # ==============================================

        with tab3:

            logs = load_data(LOG_FILE)

            st.dataframe(logs, use_container_width=True)

    # ==================================================
    # ADMIN BÁN TRÚ
    # ==================================================

    elif user.get("role") == "admin_an":

        st.markdown(
            '<div class="main-title">🍱 QUẢN LÝ BÁN TRÚ</div>',
            unsafe_allow_html=True
        )

        st.info("Chức năng bán trú đang phát triển")

    # ==================================================
    # STUDENT
    # ==================================================

    else:

        st.markdown(
            '<div class="main-title">🏠 TRANG HỌC SINH</div>',
            unsafe_allow_html=True
        )

        menu = st.sidebar.radio(
            "Danh mục",
            [
                "📊 Kết quả học tập",
                "📝 Hồ sơ cá nhân",
                "📨 Gửi phản ánh"
            ]
        )

        # ==============================================
        # KẾT QUẢ
        # ==============================================

        if menu == "📊 Kết quả học tập":

            st.subheader("📈 Kết quả học tập")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Lớp 10",
                user.get("diem_10", "Trống")
            )

            c2.metric(
                "Lớp 11",
                user.get("diem_11", "Trống")
            )

            c3.metric(
                "Lớp 12",
                user.get("diem_12", "Trống")
            )

            if str(user.get("file_diem")) != "":

                st.divider()

                st.write("📂 File bảng điểm:")

                b64 = user["file_diem"]

                href = f'''
                <a href="data:application/octet-stream;base64,{b64}"
                download="bang_diem.pdf"
                style="
                text-decoration:none;
                background:#28a745;
                color:white;
                padding:10px 20px;
                border-radius:10px;
                ">
                📥 Tải bảng điểm
                </a>
                '''

                st.markdown(href, unsafe_allow_html=True)

        # ==============================================
        # HỒ SƠ
        # ==============================================

        elif menu == "📝 Hồ sơ cá nhân":

            users = load_data(USER_FILE)

            index = next(
                i for i, u in enumerate(users)
                if u["username"] == user["username"]
            )

            with st.form("profile_form"):

                name = st.text_input(
                    "Họ và tên",
                    value=users[index].get("name", "")
                )

                dob = st.text_input(
                    "Ngày sinh",
                    value=users[index].get("dob", "")
                )

                phone = st.text_input(
                    "Số điện thoại",
                    value=users[index].get("phone", "")
                )

                email = st.text_input(
                    "Email",
                    value=users[index].get("email", "")
                )

                address = st.text_area(
                    "Địa chỉ",
                    value=users[index].get("address", "")
                )

                submit = st.form_submit_button(
                    "💾 Lưu"
                )

                if submit:

                    users[index].update({
                        "name": name,
                        "dob": dob,
                        "phone": phone,
                        "email": email,
                        "address": address
                    })

                    save_data(USER_FILE, users)

                    st.success("✅ Đã cập nhật")

                    st.rerun()

        # ==============================================
        # PHẢN ÁNH
        # ==============================================

        elif menu == "📨 Gửi phản ánh":

            text = st.text_area(
                "Nội dung phản ánh"
            )

            if st.button("📤 Gửi"):

                if text:

                    logs = load_data(LOG_FILE)

                    logs.append({
                        "Loại": "Phản ánh",
                        "Lớp": user["class"],
                        "Tên": user["name"],
                        "Nội dung": text,
                        "Thời gian":
                        now.strftime("%H:%M %d/%m/%Y"),
                        "Trạng thái": "⏳ Đã gửi"
                    })

                    save_data(LOG_FILE, logs)

                    st.success("Đã gửi phản ánh")

                else:

                    st.warning("Bạn chưa nhập nội dung")

    # ==================================================
    # LOGOUT
    # ==================================================

    if st.sidebar.button("🚪 Đăng xuất"):

        st.session_state.logged_in = False

        st.session_state.user = {}

        st.rerun()

# ==================================================
# START
# ==================================================

create_files()

if not st.session_state.logged_in:

    if st.session_state.page == "login":

        login_page()

    else:

        register_page()

else:

    main_app()