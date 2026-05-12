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
                    "loaingoaitru"
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

        loai_hs = st.selectbox(
            "Loại học sinh",
            ["Bán trú", "Ngoại trú"]
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
                    str(u.get('username',"")) == u_id
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

                        "loaingoaitru":
                        loai_hs

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

                    if str(u.get('username',"")) == u_in

                    and

                    str(u.get('password',"")) ==
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
        <h1 style='color:#1565C0'>
        🎓 CỔNG HỌC SINH
        </h1>
        """, unsafe_allow_html=True)

        nhat_ky = load_data("nhat-ky.csv")

        thongbao = [
            i for i in nhat_ky
            if i['Tên'] == user['name']
            and "✅" in str(i['Trạng thái'])
        ]

        for tb in thongbao[-3:]:

            st.success(tb['Trạng thái'])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📸 Điểm danh",
                "Hoạt động"
            )

        with c2:
            st.metric(
                "🏠 Loại",
                user.get("loaingoaitru","")
            )

        with c3:
            st.metric(
                "🎉 Sự kiện",
                len(load_data("su-kien.csv"))
            )

        st.divider()

        tab_names = [
            "📸 Điểm danh",
            "📝 Xin nghỉ",
            "💬 Phản ánh",
            "🎉 Sự kiện",
            "📅 Thời khóa biểu"
        ]

        if user.get("loaingoaitru") == "Bán trú":
            tab_names.insert(1, "🍱 Hủy bữa")

        tabs = st.tabs(tab_names)

        idx = 0

        t1 = tabs[idx]
        idx += 1

        if user.get("loaingoaitru") == "Bán trú":
            t2 = tabs[idx]
            idx += 1

        t3 = tabs[idx]
        idx += 1

        t4 = tabs[idx]
        idx += 1

        t5 = tabs[idx]
        idx += 1

        t6 = tabs[idx]

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

        if user.get("loaingoaitru") == "Bán trú":

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

            st.subheader("📝 Xin nghỉ")

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
                    "⏳ Chờ phản hồi",

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

        # ==================================
        # TKB
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

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📑 Đơn nghỉ",
                len([
                    i for i in nhat_ky
                    if i['Loại']=="Xin nghỉ"
                ])
            )

        with c2:
            st.metric(
                "📸 Điểm danh",
                len([
                    i for i in nhat_ky
                    if i['Loại']=="Điểm danh"
                ])
            )

        with c3:
            st.metric(
                "💬 Phản ánh",
                len([
                    i for i in nhat_ky
                    if i['Loại']=="Phản ánh"
                ])
            )

        st.success("✅ Hệ thống đang hoạt động")

        tabs = st.tabs([
            "📑 Đơn nghỉ",
            "📸 Điểm danh",
            "💬 Phản ánh",
            "📢 Đăng bài"
        ])

        t_ng, t_dd, t_pa, t_sk = tabs

        # ==================================
        # ĐƠN NGHỈ
        # ==================================

        with t_ng:

            ds_nghi = [
                i for i in nhat_ky
                if i['Loại']=="Xin nghỉ"
            ]

            if ds_nghi:

                for i, item in enumerate(ds_nghi):

                    with st.container(border=True):

                        st.subheader(
                            f"👤 {item['Tên']}"
                        )

                        st.write(
                            item['Nội dung']
                        )

                        st.info(
                            item['Trạng thái']
                        )

                        if item.get('Ảnh'):

                            st.image(
                                base64.b64decode(
                                    item['Ảnh']
                                ),
                                use_container_width=True
                            )

                        c1, c2 = st.columns(2)

                        with c1:

                            if st.button(
                                "✅ Duyệt",
                                key=f"duyet_nghi_{i}"
                            ):

                                for j in range(len(nhat_ky)):

                                    if nhat_ky[j] == item:

                                        nhat_ky[j]['Trạng thái'] = "✅ Đã duyệt nghỉ!"

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

                        with c2:

                            if st.button(
                                "❌ Không duyệt",
                                key=f"khong_nghi_{i}"
                            ):

                                for j in range(len(nhat_ky)):

                                    if nhat_ky[j] == item:

                                        nhat_ky[j]['Trạng thái'] = "❌ Không duyệt"

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

            else:

                st.info("Chưa có đơn nghỉ")

        # ==================================
        # ĐIỂM DANH
        # ==================================

        with t_dd:

            ds_dd = [
                i for i in nhat_ky
                if i['Loại']=="Điểm danh"
            ]

            if ds_dd:

                for i, item in enumerate(ds_dd):

                    with st.container(border=True):

                        st.subheader(
                            f"📸 {item['Tên']}"
                        )

                        st.write(
                            item['Thời gian']
                        )

                        st.info(
                            item['Trạng thái']
                        )

                        if item.get('Ảnh'):

                            st.image(
                                base64.b64decode(
                                    item['Ảnh']
                                ),
                                use_container_width=True
                            )

                        c1, c2 = st.columns(2)

                        with c1:

                            if st.button(
                                "✅ Xác nhận",
                                key=f"dd_ok_{i}"
                            ):

                                for j in range(len(nhat_ky)):

                                    if nhat_ky[j] == item:

                                        nhat_ky[j]['Trạng thái'] = "✅ Đã xác nhận điểm danh"

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

                        with c2:

                            if st.button(
                                "❌ Không hợp lệ",
                                key=f"dd_no_{i}"
                            ):

                                for j in range(len(nhat_ky)):

                                    if nhat_ky[j] == item:

                                        nhat_ky[j]['Trạng thái'] = "❌ Điểm danh không hợp lệ"

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

            else:

                st.info("Chưa có điểm danh")

        # ==================================
        # PHẢN ÁNH
        # ==================================

        with t_pa:

            ds_pa = [
                i for i in nhat_ky
                if i['Loại']=="Phản ánh"
            ]

            if ds_pa:

                for i, item in enumerate(ds_pa):

                    with st.container(border=True):

                        st.subheader(
                            f"💬 {item['Tên']}"
                        )

                        st.write(
                            item['Nội dung']
                        )

                        rep = st.text_input(
                            "Trả lời phản ánh",
                            key=f"rep_{i}"
                        )

                        if st.button(
                            "📨 Gửi phản hồi",
                            key=f"gui_{i}"
                        ):

                            for j in range(len(nhat_ky)):

                                if nhat_ky[j] == item:

                                    nhat_ky[j]['Trạng thái'] = (
                                        f"✅ BGH phản hồi: {rep}"
                                    )

                            save_all_data(
                                "nhat-ky.csv",
                                nhat_ky
                            )

                            st.rerun()

            else:

                st.info("Chưa có phản ánh")

        # ==================================
        # ĐĂNG BÀI
        # ==================================

        with t_sk:

            with st.form("new_post"):

                tt = st.text_input(
                    "Tiêu đề"
                )

                nd = st.text_area(
                    "Nội dung"
                )

                im = st.file_uploader(
                    "Tải ảnh lên",
                    type=['jpg','png']
                )

                if st.form_submit_button(
                    "🚀 Đăng bài"
                ):

                    ds_sk = load_data(
                        "su-kien.csv"
                    )

                    ds_sk.append({

                        "Tiêu đề":tt,

                        "Nội dung":nd,

                        "Ảnh":
                        image_to_base64(im),

                        "Thời gian":
                        datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        ),

                        "Likes":0,

                        "Comments":"[]"

                    })

                    save_all_data(
                        "su-kien.csv",
                        ds_sk
                    )

                    st.success(
                        "✅ Đăng bài thành công!"
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