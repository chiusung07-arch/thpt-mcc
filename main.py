# Thêm phần khởi tạo bộ nhớ lưu trữ vào đầu code
if 'lich_su_gui' not in st.session_state:
    st.session_state.lich_su_gui = [] # Nơi lưu trữ tất cả báo cáo

# ... (Giữ nguyên các phần cũ) ...

# 4. TRONG MỤC DASHBOARD - PHẦN XỬ LÝ NÚT BẤM
def main_dashboard():
    user = st.session_state.user_info
    # ... (phần code hiện các nút) ...

    if st.session_state.sub == "an":
        st.write("🍱 **Báo ăn bán trú**")
        thu = st.selectbox("Chọn thứ:", ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"])
        chon = st.radio("Lựa chọn:", ["Đăng ký ăn", "Xin nghỉ ăn bữa này"])
        if st.button("Gửi báo cáo cơm"):
            # LƯU DỮ LIỆU VÀO LỊCH SỬ
            st.session_state.lich_su_gui.append({
                "Thời gian": datetime.now().strftime("%H:%M - %d/%m"),
                "Học sinh": user['name'],
                "Lớp": user['class'],
                "Nội dung": f"Báo ăn {thu}: {chon}"
            })
            st.success("✅ Đã báo cơm thành công! Thầy cô đã nhận được.")

# 5. MỤC DÀNH RIÊNG CHO GIÁO VIÊN (Kiểm tra xem ai đã gửi)
if st.session_state.logged_in and st.session_state.user_info['class'] == "BTC":
    st.divider()
    st.subheader("📊 DANH SÁCH BÁO CÁO NHẬN ĐƯỢC (Dành cho Giáo viên)")
    if st.session_state.lich_su_gui:
        st.table(st.session_state.lich_su_gui)
    else:
        st.write("Chưa có báo cáo nào được gửi đến.")
