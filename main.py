import streamlit as st
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="THPT Mù Cang Chải", page_icon="🏫")

# 1. Dữ liệu học sinh
danh_sach_hs = {"DH3564H": "Sùng A Chiu", "HUE567B": "Lờ A Cáng", "UHU789B": "Giàng A Sinh"}

# 2. Đăng nhập
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔑 ĐĂNG NHẬP HỆ THỐNG")
    ma_input = st.text_input("Nhập mã học sinh của bạn:").upper().strip()
    if st.button("Đăng nhập"):
        if ma_input in danh_sach_hs:
            st.session_state.logged_in = True
            st.session_state.user_name = danh_sach_hs[ma_input]
            st.rerun()
        else:
            st.error("Sai mã rồi bạn ơi!")
else:
    # 3. Giao diện Dashboard khi đã đăng nhập
    st.sidebar.button("Đăng xuất", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title(f"🏫 THPT MÙ CANG CHẢI")
    st.write(f"Chào mừng: **{st.session_state.user_name}** | Ngày: {datetime.now().strftime('%d/%m/%Y')}")

    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    with col1:
        if st.button("📍 Điểm danh", use_container_width=True):
            st.success("✅ Đã gửi điểm danh cho thầy giáo!")
    with col2:
        if st.button("🍱 Báo ăn", use_container_width=True):
            st.session_state.tab = "bao_an"
    with col3:
        if st.button("📚 TKB", use_container_width=True):
            st.session_state.tab = "tkb"
    with col4:
        if st.button("📝 Xin nghỉ", use_container_width=True):
            st.session_state.tab = "xin_nghi"
    with col5:
        if st.button("🤖 Trợ giúp AI", use_container_width=True):
            st.session_state.tab = "ai"

    # Hiển thị nội dung chi tiết
    if 'tab' in st.session_state:
        st.divider()
        if st.session_state.tab == "bao_an":
            thu = st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
            chon = st.radio("Trạng thái:", ["Đăng ký ăn", "Xin nghỉ ăn"])
            if st.button("Gửi báo cáo cơm"): st.info("✅ Đã báo cơm thành công!")
        
        elif st.session_state.tab == "tkb":
            st.table({"Buổi": ["Sáng", "Chiều"], "Tiết 1": ["Toán", "Sử"], "Tiết 2": ["Văn", "Địa"]}) # Bạn điền thêm nhé
            
        elif st.session_state.tab == "xin_nghi":
            ly_do = st.text_area("Lý do nghỉ:")
            if st.button("Gửi thầy chủ nhiệm"): st.warning("⏳ Chờ thầy giáo chủ nhiệm xác nhận...")

        elif st.session_state.tab == "ai":
            hoi = st.text_input("Bạn muốn hỏi gì về trường?")
            if hoi: st.write("🤖 AI: Tôi đã nhận được câu hỏi và sẽ phản hồi sớm!")