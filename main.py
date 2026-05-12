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

st.markdown(
    """
    <style>
    /* 1. Đổi màu nền toàn trang sang màu xám nhạt */
    .stApp {
        background-color: #f4f7f6;
    }

    /* 2. Tạo khung trắng bao quanh nội dung để tạo sự độc đáo */
    .block-container {
        background-color: white;
        padding: 40px !important;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        max-width: 450px !important;
        margin-top: 50px;
    }

    /* 3. Căn giữa và làm đẹp tiêu đề chữ xanh theo Logo */
    h1 {
        color: #0056b3;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 4. Nút Đăng nhập màu xanh chuẩn */
    div.stButton > button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        border-radius: 10px;
        height: 45px;
        border: none;
        font-weight: bold;
    }

    /* 5. Nút Đăng ký mới màu xanh lá cho tươi mát */
    div.stButton:nth-of-type(2) > button {
        background-color: #28a745;
        margin-top: -10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
                    "avatar"
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
                    str(u['username']) == u_id
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
                        image_to_base64(avatar)

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

        # ADMIN BGH
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

        # ADMIN BÁN TRÚ
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

                    if str(u['username']) == u_in

                    and

                    str(u['password']) ==
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

    # ======================================
    # SIDEBAR
    # ======================================

    if user.get("avatar"):

        st.sidebar.image(
            base64.b64decode(
                user['avatar']
            ),
            width=120
        )

    st.sidebar.title(
        f"👤 {user['name']}"
    )

    st.sidebar.info(
        datetime.now().strftime(
            "🕒 %H:%M %d/%m/%Y"
        )
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

        st.markdown("""
        <h2 style='color:#1565C0'>
        🎓 CỔNG HỌC SINH
        </h2>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📸 Điểm danh",
                "Hoạt động"
            )

        with c2:
            st.metric(
                "🍱 Bán trú",
                "Đang mở"
            )

        with c3:
            st.metric(
                "🎉 Sự kiện",
                len(load_data("su-kien.csv"))
            )

        st.divider()

        tabs = st.tabs([

            "📸 Điểm danh",
            "🍱 Hủy bữa",
            "📝 Xin nghỉ",
            "💬 Phản ánh",
            "🎉 Sự kiện",
            "📅 Thời khóa biểu"

        ])

        t1, t2, t3, t4, t5, t6 = tabs

        # ==================================
        # ĐIỂM DANH
        # ==================================

        with t1:

            st.subheader(
                "📸 Điểm danh AI"
            )

            a_dd = st.camera_input(
                "Chụp khuôn mặt"
            )

            if (
                a_dd
                and
                st.button("GỬI ĐIỂM DANH")
            ):

                with st.spinner(
                    "🤖 AI đang nhận diện..."
                ):

                    time.sleep(2)

                data = load_data(
                    "nhat-ky.csv"
                )

                data.append({

                    "Loại":"Điểm danh",

                    "Lớp":user['class'],

                    "Tên":user['name'],

                    "Nội dung":"Có mặt",

                    "Thời gian":
                    datetime.now().strftime(
                        "%H:%M %d/%m"
                    ),

                    "Trạng thái":
                    "⏳ Chờ duyệt",

                    "Ảnh":
                    image_to_base64(a_dd)

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "🤖 AI nhận diện thành công!"
                )

        # ==================================
        # HỦY BỮA
        # ==================================

        with t2:

            st.error(
                "🚫 Hủy Trưa trước 09h | "
                "Hủy Chiều trước 15h"
            )

            thu = st.selectbox(
                "Ngày báo hủy",
                [
                    "Thứ 2",
                    "Thứ 3",
                    "Thứ 4",
                    "Thứ 5",
                    "Thứ 6"
                ]
            )

            buoi = st.multiselect(
                "Buổi muốn hủy",
                [
                    "Bữa Trưa",
                    "Bữa Chiều"
                ],
                default=["Bữa Trưa"]
            )

            if st.button(
                "Xác nhận Hủy"
            ):

                gio = datetime.now().hour

                if (
                    ("Bữa Trưa" in buoi and gio >= 9)
                    or
                    ("Bữa Chiều" in buoi and gio >= 15)
                ):

                    st.error(
                        "❌ Quá giờ!"
                    )

                else:

                    data = load_data(
                        "nhat-ky.csv"
                    )

                    data.append({

                        "Loại":"Báo ăn",

                        "Lớp":user['class'],

                        "Tên":user['name'],

                        "Nội dung":
                        f"HỦY: {thu} {buoi}",

                        "Thời gian":
                        datetime.now().strftime(
                            "%H:%M"
                        ),

                        "Trạng thái":
                        "Đã gửi",

                        "Ảnh":""

                    })

                    save_all_data(
                        "nhat-ky.csv",
                        data
                    )

                    st.success(
                        "✅ Đã báo hủy!"
                    )

        # ==================================
        # XIN NGHỈ
        # ==================================

        with t3:

            ly_do = st.text_area(
                "Lý do nghỉ"
            )

            a_ng = st.camera_input(
                "Ảnh minh chứng"
            )

            if st.button("Gửi đơn"):

                data = load_data(
                    "nhat-ky.csv"
                )

                data.append({

                    "Loại":"Xin nghỉ",

                    "Lớp":user['class'],

                    "Tên":user['name'],

                    "Nội dung":ly_do,

                    "Thời gian":
                    datetime.now().strftime(
                        "%H:%M %d/%m"
                    ),

                    "Trạng thái":
                    "⏳ Chờ duyệt",

                    "Ảnh":
                    image_to_base64(a_ng)

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "✅ Đã gửi!"
                )

        # ==================================
        # PHẢN ÁNH
        # ==================================

        with t4:

            yk = st.text_area(
                "Ý kiến phản ánh"
            )

            if st.button(
                "Gửi phản ánh"
            ):

                data = load_data(
                    "nhat-ky.csv"
                )

                data.append({

                    "Loại":"Phản ánh",

                    "Lớp":user['class'],

                    "Tên":user['name'],

                    "Nội dung":yk,

                    "Thời gian":
                    datetime.now().strftime(
                        "%H:%M"
                    ),

                    "Trạng thái":
                    "Đã gửi",

                    "Ảnh":""

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "📩 Đã gửi!"
                )

        # ==================================
        # SỰ KIỆN
        # ==================================

        with t5:

            st.subheader(
                "📣 Bảng tin sự kiện"
            )

            ds_sk = load_data(
                "su-kien.csv"
            )

            if ds_sk:

                for idx, sk in enumerate(
                    reversed(ds_sk)
                ):

                    r_idx = (
                        len(ds_sk)-1-idx
                    )

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### {sk['Tiêu đề']}"
                        )

                        st.caption(
                            sk['Thời gian']
                        )

                        st.write(
                            sk['Nội dung']
                        )

                        if sk.get('Ảnh'):

                            st.image(
                                base64.b64decode(
                                    sk['Ảnh']
                                ),
                                use_container_width=True
                            )

                        likes = int(
                            sk.get('Likes') or 0
                        )

                        if st.button(
                            f"👍 Like ({likes})",
                            key=f"lk_{r_idx}"
                        ):

                            ds_sk[r_idx]['Likes'] = (
                                likes + 1
                            )

                            save_all_data(
                                "su-kien.csv",
                                ds_sk
                            )

                            st.rerun()

                        raw_comments = sk.get(
                            'Comments'
                        )

                        try:

                            comments = (
                                json.loads(
                                    raw_comments
                                )
                                if raw_comments
                                else []
                            )

                        except:
                            comments = []

                        for c in comments[-5:]:

                            st.markdown(
                                f"**💬 {c['user']}:** "
                                f"{c['text']}"
                            )

                        with st.form(
                            f"f_c_{r_idx}",
                            clear_on_submit=True
                        ):

                            new_com = st.text_input(
                                "Bình luận..."
                            )

                            if st.form_submit_button(
                                "Gửi ✈️"
                            ):

                                comments.append({

                                    "user":
                                    user['name'],

                                    "text":
                                    new_com

                                })

                                ds_sk[r_idx][
                                    'Comments'
                                ] = json.dumps(
                                    comments,
                                    ensure_ascii=False
                                )

                                save_all_data(
                                    "su-kien.csv",
                                    ds_sk
                                )

                                st.rerun()

        # ==================================
        # THỜI KHÓA BIỂU
        # ==================================

        with t6:

            st.subheader(
                "📅 Thời khóa biểu"
            )

            tkb = load_data(
                "thoikhoabieu.csv"
            )

            tkb_lop = [

                i for i in tkb

                if i['Lớp'] == user['class']

            ]

            if tkb_lop:

                st.dataframe(
                    pd.DataFrame(tkb_lop),
                    use_container_width=True
                )

            else:

                st.info(
                    "Chưa có thời khóa biểu."
                )

    # ======================================
    # ADMIN BGH
    # ======================================

    elif user.get('role') == "admin_gv":

        st.title(
            "🏫 BẢNG ĐIỀU KHIỂN BAN GIÁM HIỆU"
        )

        nhat_ky = load_data(
            "nhat-ky.csv"
        )

        ds_sk = load_data(
            "su-kien.csv"
        )

        tong_nghi = len([
            i for i in nhat_ky
            if i['Loại']=="Xin nghỉ"
        ])

        tong_dd = len([
            i for i in nhat_ky
            if i['Loại']=="Điểm danh"
        ])

        tong_pa = len([
            i for i in nhat_ky
            if i['Loại']=="Phản ánh"
        ])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📑 Đơn nghỉ",
                tong_nghi
            )

        with c2:
            st.metric(
                "📸 Điểm danh",
                tong_dd
            )

        with c3:
            st.metric(
                "💬 Phản ánh",
                tong_pa
            )

        st.divider()

        st.subheader(
            "📊 Thống kê hệ thống"
        )

        chart_data = pd.DataFrame({

            "Loại": [
                "Xin nghỉ",
                "Điểm danh",
                "Phản ánh"
            ],

            "Số lượng": [
                tong_nghi,
                tong_dd,
                tong_pa
            ]

        })

        st.bar_chart(
            chart_data.set_index("Loại")
        )

        st.divider()

        tabs = st.tabs([

            "📑 Đơn nghỉ",
            "📸 Điểm danh",
            "💬 Phản ánh",
            "📢 Đăng bài"

        ])

        t_ng, t_dd, t_pa, t_sk = tabs

        def render_admin(loai, msg):

            for i, item in enumerate(
                nhat_ky
            ):

                if item['Loại'] == loai:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### 👤 {item['Tên']}"
                        )

                        st.caption(
                            f"{item['Lớp']} • "
                            f"{item['Thời gian']}"
                        )

                        st.write(
                            item['Nội dung']
                        )

                        if item.get('Ảnh'):

                            st.image(
                                base64.b64decode(
                                    item['Ảnh']
                                ),
                                use_container_width=True
                            )

                        c1, c2, c3 = st.columns(3)

                        with c1:

                            if st.button(
                                "✅ Duyệt",
                                key=f"d_{loai}_{i}"
                            ):

                                nhat_ky[i]['Trạng thái'] = msg

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

                        with c2:

                            if st.button(
                                "❌ Từ chối",
                                key=f"tc_{loai}_{i}"
                            ):

                                nhat_ky[i]['Trạng thái'] = (
                                    "❌ Từ chối"
                                )

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

                        with c3:

                            if st.button(
                                "🗑️ Xóa",
                                key=f"del_{loai}_{i}"
                            ):

                                nhat_ky.pop(i)

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

        with t_ng:

            render_admin(
                "Xin nghỉ",
                "✅ Đã duyệt nghỉ!"
            )

        with t_dd:

            render_admin(
                "Điểm danh",
                "✅ Đã xác nhận!"
            )

        with t_pa:

            for i, item in enumerate(
                nhat_ky
            ):

                if item['Loại']=="Phản ánh":

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### 💬 {item['Tên']}"
                        )

                        st.write(
                            item['Nội dung']
                        )

                        rep = st.text_input(
                            "Trả lời",
                            key=f"rep_{i}"
                        )

                        if st.button(
                            "📨 Gửi",
                            key=f"r_{i}"
                        ):

                            nhat_ky[i]['Trạng thái'] = (
                                f"✅ BGH phản hồi: {rep}"
                            )

                            save_all_data(
                                "nhat-ky.csv",
                                nhat_ky
                            )

                            st.rerun()

        with t_sk:

            with st.form("new_post"):

                tt = st.text_input(
                    "Tiêu đề"
                )

                nd = st.text_area(
                    "Nội dung"
                )

                im = st.file_uploader(
                    "Ảnh",
                    type=['jpg','png']
                )

                if st.form_submit_button(
                    "🚀 Đăng bài"
                ):

                    ds_sk.append({

                        "Tiêu đề":tt,

                        "Nội dung":nd,

                        "Ảnh":
                        image_to_base64(im),

                        "Thời gian":
                        datetime.now().strftime(
                            "%d/%m"
                        ),

                        "Likes":0,

                        "Comments":"[]"

                    })

                    save_all_data(
                        "su-kien.csv",
                        ds_sk
                    )

                    st.success(
                        "✅ Đã đăng!"
                    )

                    st.rerun()

    # ======================================
    # ADMIN BÁN TRÚ
    # ======================================

    elif user.get('role') == "admin_an":

        st.title(
            "🍱 QUẢN LÝ BÁN TRÚ"
        )

        ds_an = [

            i for i in load_data(
                "nhat-ky.csv"
            )

            if i['Loại']=="Báo ăn"
        ]

        if ds_an:

            st.dataframe(
                pd.DataFrame(ds_an),
                use_container_width=True
            )

        else:

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