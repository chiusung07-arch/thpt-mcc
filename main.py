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

# ==========================================
# CONFIG
# ==========================================

st.set_page_config("THPT Mù Cang Chải", "🏫", layout="wide")

# ==========================================
# FUNCTION
# ==========================================

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def img64(f):
    return base64.b64encode(f.getvalue()).decode() if f else ""

def load(f):
    try:
        return pd.read_csv(f).fillna("").to_dict("records")
    except:
        return []

def save(f, d):
    pd.DataFrame(d).to_csv(f, index=False)

# ==========================================
# FILE INIT
# ==========================================

files = ["users.csv", "log.csv", "event.csv", "notice.csv"]

for f in files:
    if not os.path.exists(f):
        if f == "users.csv":
            pd.DataFrame(columns=["username","password","name","class","role","avatar","type"]).to_csv(f,index=False)
        elif f == "notice.csv":
            pd.DataFrame(columns=["title","content","time"]).to_csv(f,index=False)
        elif f == "event.csv":
            pd.DataFrame(columns=["title","content","img","time","like","cmt"]).to_csv(f,index=False)
        else:
            pd.DataFrame(columns=["type","class","name","content","time","status","img"]).to_csv(f,index=False)

# ==========================================
# SESSION
# ==========================================

if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ==========================================
# REGISTER
# ==========================================

def register():
    st.title("📝 Đăng ký")

    with st.form("r"):
        name = st.text_input("Tên")
        cls = st.text_input("Lớp")

        utype = st.selectbox("Loại", ["Bán trú", "Ngoại trú"])

        u = st.text_input("User")
        p = st.text_input("Pass", type="password")
        av = st.file_uploader("Avatar")

        if st.form_submit_button("OK"):
            users = load("users.csv")

            if any(x["username"] == u for x in users):
                st.error("Tồn tại")
            else:
                users.append({
                    "username":u,
                    "password":hash_pw(p),
                    "name":name,
                    "class":cls,
                    "role":"student",
                    "avatar":img64(av),
                    "type":utype
                })
                save("users.csv", users)
                st.success("OK")
                st.session_state.page="login"

# ==========================================
# LOGIN
# ==========================================

def login():
    st.title("🏫 LOGIN")

    u = st.text_input("User")
    p = st.text_input("Pass", type="password")

    if st.button("Login"):

        users = load("users.csv")

        user = next((x for x in users if x["username"]==u and x["password"]==hash_pw(p)), None)

        if user:
            st.session_state.login=True
            st.session_state.user=user
            st.rerun()
        else:
            st.error("Sai")

    if st.button("Register"):
        st.session_state.page="register"
        st.rerun()

# ==========================================
# MAIN
# ==========================================

def app():

    u = st.session_state.user

    st.sidebar.title(u["name"])
    st.sidebar.write(u["class"])
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

    # ======================================
    # STUDENT
    # ======================================

    if u["role"]=="student":

        tabs = [

            "🔔 Thông báo",
            "📸 Điểm danh",
            "📝 Xin nghỉ",
            "💬 Phản ánh",
            "🎉 Sự kiện"
        ]

        if u["type"]=="Bán trú":
            tabs.insert(2,"🍱 Hủy bữa")

        t = st.tabs(tabs)

        idx = 0

        # ---------------- THÔNG BÁO ----------------
        with t[idx]:
            st.subheader("🔔 Thông báo")

            for x in reversed(load("notice.csv")):
                st.info(f"{x['title']}\n{x['content']}\n{x['time']}")

        idx+=1

        # ---------------- ĐIỂM DANH ----------------
        with t[idx]:
            img = st.camera_input("Cam")

            if st.button("Gửi"):
                data = load("log.csv")
                data.append({
                    "type":"Điểm danh",
                    "class":u["class"],
                    "name":u["name"],
                    "content":"Có mặt",
                    "time":str(datetime.now()),
                    "status":"pending",
                    "img":img64(img)
                })
                save("log.csv",data)
                st.success("OK")

        idx+=1

        # ---------------- HỦY BỮA (CHỈ BÁN TRÚ) ----------------
        if u["type"]=="Bán trú":

            with t[idx]:
                day = st.selectbox("Ngày",["T2","T3","T4","T5","T6"])
                meal = st.multiselect("Bữa",["Trưa","Chiều"])

                if st.button("Gửi"):
                    data = load("log.csv")
                    data.append({
                        "type":"Báo ăn",
                        "class":u["class"],
                        "name":u["name"],
                        "content":f"Hủy {day} {meal}",
                        "time":str(datetime.now()),
                        "status":"sent",
                        "img":""
                    })
                    save("log.csv",data)
                    st.success("OK")

            idx+=1

        # ---------------- XIN NGHỈ ----------------
        with t[idx]:
            txt = st.text_area("Lý do")
            img = st.file_uploader("Ảnh")

            if st.button("Gửi"):
                data = load("log.csv")
                data.append({
                    "type":"Xin nghỉ",
                    "class":u["class"],
                    "name":u["name"],
                    "content":txt,
                    "time":str(datetime.now()),
                    "status":"pending",
                    "img":img64(img)
                })
                save("log.csv",data)

        idx+=1

        # ---------------- PHẢN ÁNH ----------------
        with t[idx]:
            txt = st.text_area("Ý kiến")

            if st.button("Gửi"):
                data = load("log.csv")
                data.append({
                    "type":"Phản ánh",
                    "class":u["class"],
                    "name":u["name"],
                    "content":txt,
                    "time":str(datetime.now()),
                    "status":"sent",
                    "img":""
                })
                save("log.csv",data)

        idx+=1

        # ---------------- SỰ KIỆN ----------------
        with t[idx]:
            for x in reversed(load("event.csv")):
                st.subheader(x["title"])
                st.write(x["content"])

# ==========================================
# RUN
# ==========================================

if not st.session_state.login:

    if st.session_state.page=="login":
        login()
    else:
        register()

else:
    app()