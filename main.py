import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CẤU HÌNH ---
st.set_page_config(page_title="Hệ thống Quản lý THPT Mù Cang Chải", page_icon="🏫", layout="wide")

# 1. DỮ LIỆU & HÀM HỖ TRỢ
def load_users():
    if os.path.exists("hoc-sinh.csv"):
        try: return pd.read_csv("hoc-sinh.csv").to_dict('records')
        except: return []
    return []

def save_user_to_csv(new_user):
    users = load_users()
    users.append(new_user)
    pd.DataFrame(users).to_csv("hoc-sinh.csv", index=False)

if 'lich_su' not in st.session_state: st.session_state.lich_su = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 2. GIAO DIỆN ĐĂNG KÝ/ĐĂNG NHẬP (Giữ nguyên phần bạn đã làm)
# ... (Phần này bạn đã có, mình tập trung vào phần ghi điểm nhé) ...

# 3. GIAO DIỆN CHÍNH
def main_app():
    user = st.session_state.user_info
    st.sidebar.title(f"👤 {user['name']}")
    if st.sidebar.button("ĐĂNG XUẤT"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN BAN GIÁM HIỆU (PHẦN ĂN ĐIỂM 10) ---
    if user.get('role') == "admin_gv":
        st.title("📂 HÒM THƯ QUẢN LÝ CỦA BAN GIÁM HIỆU")
        
        # Thống kê nhanh (Điểm 10 ở đây)
        tong_hs = len([i for i in st.session_state.lich_su if i['Loại'] == "Điểm danh"])
        st.metric("Tổng số học sinh đã có mặt hôm nay", f"{tong_hs} bạn")
        
        st.write("---")
        # Duyệt đơn xin nghỉ có nút bấm và hiệu ứng
        ds_don = [i for i in st.session_state.lich_su if i['Loại'] in ["Xin nghỉ", "Phản ánh"]]
        if ds_don:
            for i, item in enumerate(st.session_state.lich_su):
                if item['Loại'] in ["Xin nghỉ", "Phản ánh"]:
                    with st.expander(f"✉️ {item['Loại']} - {item['Tên']} ({item['Trạng thái']})"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(f"✅ Duyệt ngay", key=f"d_{i}"):
                                item['Trạng thái'] = "✅ Đã đồng ý"
                                st.balloons() # PHÁO HOA ĂN ĐIỂM 10
                                st.rerun()
                        with c2:
                            if st.button(f"❌ Từ chối", key=f"tc_{i}"):
                                item['Trạng thái'] = "❌ Không đồng ý"
                                st.rerun()
        else: st.info("Hòm thư hiện tại đang trống.")

    # --- CÁC PHẦN KHÁC (Học sinh & Bán trú giữ nguyên code cũ của bạn) ---
    # ...