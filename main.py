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
# CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: #eef2f7;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCTIONS
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
# CREATE FILES
# ==========================================

for f in [
    "hoc-sinh.csv",
    "giao-vien.csv",
    "thoi-khoa-bieu.csv",
    "nhat-ky.csv",
    "su-kien.csv",
    "thong-bao.csv"
]:

    if not os.path.exists(f):

        if f == "hoc-sinh.csv":

            pd.DataFrame(columns=[

                "username",
                "password",
                "name",
                "class",
                "role",
                "avatar",
                "loai_hs"

            ]).to_csv(f, index=False)

        elif f == "su-kien.csv":

            pd.DataFrame(columns=[

                "Tiêu đề",
                "Nội dung",
                "Ảnh",
                "Thời gian",
                "Likes",
                "Comments"

            ]).to_csv(f, index=False)
        elif f == "thong-bao.csv":

            pd.DataFrame(columns=[

                "Tiêu đề",
                "Nội dung",
                "Thời gian"

            ]).to_csv(f, index=False)

        else:

            pd.DataFrame(columns=[

                "Loại",
                "Lớp",
                "Tên",
                "Nội dung",
                "Thời gian",
                "Trạng thái",
                "Ảnh"

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

    st.title("📝 ĐĂNG KÝ HỌC SINH")

    with st.form("register"):

        name = st.text_input(
            "Họ và tên"
        )

        classes = (
            [f"10A{i}" for i in range(1,10)] +
            [f"11A{i}" for i in range(1,8)] +
            [f"12A{i}" for i in range(1,7)]
        )

        lop = st.selectbox(
            "Lớp",
            classes
        )

        loai_hs = st.selectbox(
            "Loại học sinh",
            [
                "Bán trú",
                "Ngoại trú"
            ]
        )

        avatar = st.file_uploader(
            "Ảnh đại diện",
            type=['jpg','png','jpeg']
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

            users = load_data(
                "hoc-sinh.csv"
            )

            if any(
                str(u.get('username',"")) == u_id
                for u in users
            ):

                st.error(
                    "⚠️ Tài khoản đã tồn tại!"
                )

            else:

                users.append({

                    "username": u_id,

                    "password":
                    hash_password(pwd),

                    "name": name,

                    "class": lop,

                    "role": "student",

                    "avatar":
                    image_to_base64(avatar),

                    "loai_hs":
                    loai_hs

                })

                save_all_data(
                    "hoc-sinh.csv",
                    users
                )

                st.success(
                    "✅ Đăng ký thành công!"
                )

                st.session_state.page = "login"

    if st.button("Quay lại"):

        st.session_state.page = "login"

        st.rerun()

# ==========================================
# LOGIN
# ==========================================

def login_page():

    st.markdown("""
    <h1 style='text-align:center;color:#1565C0;'>
    🏫 THPT MÙ CANG CHẢI
    </h1>
    """, unsafe_allow_html=True)

    u_in = st.text_input(
        "Tên tài khoản"
    )

    p_in = st.text_input(
        "Mật khẩu",
        type="password"
    )

    if st.button("ĐĂNG NHẬP"):

        # ADMIN BGH
        if (
            u_in == "thptmcc_admin"
            and
            p_in == "giaovien2024"
        ):

            st.session_state.logged_in = True

            st.session_state.user_info = {

                "name":"Ban Giám Hiệu",
                "role":"admin_gv"

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

                "name":"Quản lý bán trú",
                "role":"admin_an"

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

    if st.button("Đăng ký mới"):

        st.session_state.page = "register"

        st.rerun()

# ==========================================
# MAIN APP
# ==========================================

def main_app():

    user = st.session_state.user_info

    # ======================================
    # SIDEBAR
    # ======================================

    if user.get("avatar"):

        try:

            st.sidebar.image(
                base64.b64decode(
                    user['avatar']
                ),
                width=120
            )

        except:
            pass

    st.sidebar.title(
        f"👤 {user['name']}"
    )

    st.sidebar.info(
        f"🏫 {user.get('class','')}"
    )

    if st.sidebar.button(
        "ĐĂNG XUẤT"
    ):

        for k in list(st.session_state.keys()):
            del st.session_state[k]

        st.rerun()

    # ======================================
    # STUDENT
    # ======================================

    if user.get('role') == "student":

        st.title(
            "🎓 CỔNG HỌC SINH"
        )

        tabs = [

            "📸 Điểm danh",

            "📝 Xin nghỉ",

            "💬 Phản ánh",

            "🎉 Sự kiện"

        ]

        # chỉ bán trú mới có hủy bữa
        if user.get("loai_hs") == "Bán trú":

            tabs.insert(
                1,
                "🍱 Hủy bữa"
            )

        tbs = st.tabs(tabs)

        index = 0

        # ==================================
        # ĐIỂM DANH
        # ==================================

        with tbs[index]:

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
                    "📨 Đã gửi",

                    "Ảnh":
                    image_to_base64(a_dd)

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "✅ Đã gửi điểm danh!"
                )

        index += 1

        # ==================================
        # HỦY BỮA
        # ==================================

        if user.get("loai_hs") == "Bán trú":

            with tbs[index]:

                st.subheader(
                    "🍱 Hủy bữa"
                )

                thu = st.selectbox(
                    "Ngày",
                    [
                        "Thứ 2",
                        "Thứ 3",
                        "Thứ 4",
                        "Thứ 5",
                        "Thứ 6"
                    ]
                )

                buoi = st.multiselect(
                    "Buổi",
                    [
                        "Bữa Trưa",
                        "Bữa Chiều"
                    ]
                )

                if st.button(
                    "Xác nhận hủy"
                ):

                    data = load_data(
                        "nhat-ky.csv"
                    )

                    data.append({

                        "Loại":"Báo ăn",

                        "Lớp":user['class'],

                        "Tên":user['name'],

                        "Nội dung":
                        f"Hủy {thu} {buoi}",

                        "Thời gian":
                        datetime.now().strftime(
                            "%H:%M"
                        ),

                        "Trạng thái":
                        "📨 Đã gửi",

                        "Ảnh":""

                    })

                    save_all_data(
                        "nhat-ky.csv",
                        data
                    )

                    st.success(
                        "✅ Đã gửi!"
                    )

            index += 1

        # ==================================
        # XIN NGHỈ
        # ==================================

        with tbs[index]:

            ly_do = st.text_area(
                "Lý do nghỉ"
            )

            a_ng = st.camera_input(
                "Ảnh minh chứng"
            )

            if st.button(
                "Gửi đơn"
            ):

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
                    "📨 Đã gửi",

                    "Ảnh":
                    image_to_base64(a_ng)

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "✅ Đã gửi đơn!")
                    
            # ================================
            #LỊCH SỬ ĐƠN XIN NGHỈ
            #================================
            st.divider()
            st.subheader("📌 Lịch sử đơn xin nghỉ")

            logs = load_data("nhat-ky.csv")
            my_requests = [i for i in logs if i.get("Tên") == user['name']]
            if my_requests:
                for r in reversed(my_requests):
                    st.info(f"📄 Nội dung: {r.get('Nội dung')}\n📌 Trạng thái: {r.get('Trạng thái')}\n🕒 {r.get('Thời gian','')}")
            else:
                st.warning("📌 Lịch sử đơn xin nghỉ.")
            index += 1
    
                # ==================================
                # PHẢN ÁNH
                # ==================================
        with tbs[index]:
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
                    "📨 Đã gửi",

                    "Ảnh":""

                })

                save_all_data(
                    "nhat-ky.csv",
                    data
                )

                st.success(
                    "✅ Đã gửi phản ánh!"
                )

            # hiện phản hồi
            st.divider()

            logs = load_data(
                "nhat-ky.csv"
            )

            replies = [

                i for i in logs

                if i['Tên'] == user['name']

                and

                "BGH phản hồi" in
                str(i['Trạng thái'])

            ]

            for r in replies:

                st.info(
                    r['Trạng thái']
                )

        index += 1

# ==================================
# SỰ KIỆN
# ==================================

        with tbs[index]:

            st.subheader(
                "🎉 Bảng tin sự kiện"
            )

            ds_sk = load_data(
                "su-kien.csv"
            )

            for idx, sk in enumerate(
                reversed(ds_sk)
            ):

                real_index = (
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

                        try:

                            st.image(
                                base64.b64decode(
                                    sk['Ảnh']
                                ),
                                use_container_width=True
                            )

                        except:
                            pass

                    likes = int(
                        sk.get('Likes') or 0
                    )

                    if st.button(
                        f"👍 Like ({likes})",
                        key=f"lk_{real_index}"
                    ):

                        ds_sk[real_index][
                            'Likes'
                        ] = likes + 1

                        save_all_data(
                            "su-kien.csv",
                            ds_sk
                        )

                        st.rerun()

                    # comments
                    try:

                        comments = json.loads(
                            sk.get(
                                'Comments',
                                "[]"
                            )
                        )

                    except:
                        comments = []

                    for c in comments:

                        st.markdown(
                            f"💬 "
                            f"**{c['user']}**:"
                            f" {c['text']}"
                        )

                    with st.form(
                        f"cmt_{real_index}",
                        clear_on_submit=True
                    ):

                        txt = st.text_input(
                            "Bình luận"
                        )

                        if st.form_submit_button(
                            "Gửi"
                        ):

                            comments.append({

                                "user":
                                user['name'],

                                "text":
                                txt

                            })

                            ds_sk[real_index][
                                'Comments'
                            ] = json.dumps(
                                comments,
                                ensure_ascii=False
                            )

                            save_all_data(
                                "su-kien.csv",
                                ds_sk
                            )

                            st.success(
                                "✅ Đã gửi bình luận!"
                            )

                            st.rerun()

    # ======================================
    # ADMIN BGH
    # ======================================

    elif user.get('role') == "admin_gv":

        st.markdown("""
        <h2 style='color:#1565C0;'>
        🏫 Ban Giám Hiệu
        </h2>
        """, unsafe_allow_html=True)

        nhat_ky = load_data(
            "nhat-ky.csv"
        )

        tabs = st.tabs([
            "📑 Đơn nghỉ",
            "📸 Điểm danh",
            "💬 Phản ánh",
            "📢 Đăng bài",
            "🔔 Thông báo"
        ])

        t_ng, t_dd, t_pa, t_sk = tabs

        def render_admin(loai, msg):
            nhat_ky = load_data("nhat-ky.csv")

            for i, item in enumerate(nhat_ky):

                if item['Loại'] == loai and item['Trạng thái'] == "📨 Đã gửi":

                   title = f"👤 {item['Tên']} | 🕒 {item['Thời gian']} | 📌 {item['Lớp']}"

                   with st.expander(title):

                       st.write("📄 Nội dung:")
                       st.write(item['Nội dung'])

                       st.info(f"📌 Trạng thái: {item['Trạng thái']}")

                       if item.get('Ảnh'):
                           try:
                               st.image(
                                   base64.b64decode(item['Ảnh']),
                                   use_container_width=True
                               )
                           except:
                               pass

                       c1, c2 = st.columns(2)

                       with c1:
                          if st.button("✅ Duyệt", key=f"d_{loai}_{i}"):

                              nhat_ky[i]['Trạng thái'] = msg
                              save_all_data("nhat-ky.csv", nhat_ky)
                              st.success("Đã duyệt")
                              st.rerun()

                       with c2:
                           if st.button("❌ Không duyệt", key=f"tc_{loai}_{i}"):

                               nhat_ky[i]['Trạng thái'] = "❌ Không duyệt"
                               save_all_data("nhat-ky.csv", nhat_ky)
                               st.error("Đã từ chối")
                               st.rerun()
        with t_ng:

            render_admin(
                "Xin nghỉ",
                "✅ Đã duyệt nghỉ!"
            )

        with t_dd:

            render_admin(
                "Điểm danh",
                "✅ Đã xác nhận điểm danh!"
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

                        st.info(
                            item['Trạng thái']
                        )

                        rep = st.text_input(
                            "Trả lời",
                            key=f"rep_{i}"
                        )

                        c1, c2 = st.columns(2)

                        with c1:

                            if st.button(
                                "📨 Gửi",
                                key=f"r_{i}"
                            ):

                                nhat_ky[i][
                                    'Trạng thái'
                                ] = (
                                    f"✅ BGH phản hồi:"
                                    f" {rep}"
                                )

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.success(
                                    "✅ Đã gửi!"
                                )

                                st.rerun()

                        with c2:

                            if st.button(
                                "🗑️ Xóa",
                                key=f"del_{i}"
                            ):

                                nhat_ky.pop(i)

                                save_all_data(
                                    "nhat-ky.csv",
                                    nhat_ky
                                )

                                st.rerun()

        with t_sk:

            ds_sk = load_data(
                "su-kien.csv"
            )

            with st.form("new_post"):

                tt = st.text_input(
                    "Tiêu đề"
                )

                nd = st.text_area(
                    "Nội dung"
                )

                im = st.file_uploader(
                    "Ảnh",
                    type=['jpg','png','jpeg']
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
                            "%H:%M %d/%m"
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

            st.divider()

            st.subheader(
                "📰 Lịch sử bài đăng"
            )

            for idx, sk in enumerate(
                reversed(ds_sk)
            ):

                real_index = (
                    len(ds_sk)-1-idx
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {sk['Tiêu đề']}"
                    )

                    st.write(
                        sk['Nội dung']
                    )

                    if sk.get('Ảnh'):

                        try:

                            st.image(
                                base64.b64decode(
                                    sk['Ảnh']
                                ),
                                use_container_width=True
                            )

                        except:
                            pass

                    if st.button(
                        "🗑️ Xóa bài đăng",
                        key=f"del_post_{real_index}"
                    ):

                        ds_sk.pop(
                            real_index
                        )

                        save_all_data(
                            "su-kien.csv",
                            ds_sk
                        )

                        st.success(
                            "✅ Đã xóa bài!"
                        )

                        st.rerun()

    # ======================================
    # ADMIN BÁN TRÚ
    # ======================================

    elif user.get('role') == "admin_an":

        st.title(
            "🍱 QUẢN LÝ BÁN TRÚ"
        )

        ds = [

            i for i in load_data(
                "nhat-ky.csv"
            )

            if i['Loại']=="Báo ăn"

        ]

        if ds:

            st.dataframe(
                pd.DataFrame(ds),
                use_container_width=True
            )

        else:

            st.info(
                "Chưa có dữ liệu."
            )

# ==========================================
# NAVIGATION
# ==========================================

if not st.session_state.logged_in:

    if st.session_state.page == "login":

        login_page()

    else:

        registration_page()

else:

    main_app()