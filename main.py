# --- HÀM MÃ HÓA ẢNH ---
def image_to_base64(image_file):
    if image_file is not None:
        return base64.b64encode(image_file.getvalue()).decode()
        try: return base64.b64encode(image_file.getvalue()).decode()
        except: return ""
    return ""

# --- TỰ ĐỘNG KHỞI TẠO FILE ---
for f in ["hoc-sinh.csv", "nhat-ky.csv"]:
for f in ["hoc-sinh.csv", "nhat-ky.csv", "su-kien.csv"]:
    if not os.path.exists(f):
        if f == "hoc-sinh.csv":
            pd.DataFrame(columns=["username","password","name","class","role"]).to_csv(f, index=False)
        elif f == "su-kien.csv":
            pd.DataFrame(columns=["Tiêu đề","Nội dung","Ảnh","Thời gian"]).to_csv(f, index=False)
        else:
            pd.DataFrame(columns=["Loại","Lớp","Tên","Nội dung","Thời gian","Trạng thái","Ảnh"]).to_csv(f, index=False)

def load_data(file_name):
    try: return pd.read_csv(file_name).to_dict('records')
    except: return []

def save_data(file_name, new_entry):
def save_all_data(file_name, data_list):
    pd.DataFrame(data_list).to_csv(file_name, index=False)

def save_single_data(file_name, new_entry):
    data = load_data(file_name)
    data.append(new_entry)
    pd.DataFrame(data).to_csv(file_name, index=False)
    save_all_data(file_name, data)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = "login"

# 1. TRANG ĐĂNG KÝ & ĐĂNG NHẬP
# 1. ĐĂNG KÝ & ĐĂNG NHẬP
def registration_page():
    st.title("📝 ĐĂNG KÝ HỌC SINH")
    with st.form("reg_form"):
@@ -44,7 +50,7 @@ def registration_page():
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.form_submit_button("Xác nhận đăng ký"):
            if u_id and pwd and name:
                save_data("hoc-sinh.csv", {"username": u_id, "password": pwd, "name": name, "class": lop, "role": "student"})
                save_single_data("hoc-sinh.csv", {"username": u_id, "password": pwd, "name": name, "class": lop, "role": "student"})
                st.success("✅ Đăng ký thành công!"); st.session_state.page = "login"
    if st.button("Quay lại"): st.session_state.page = "login"; st.rerun()

@@ -74,91 +80,114 @@ def main_app():

    # --- HỌC SINH ---
    if user.get('role') == "student":
        # HIỂN THỊ THÔNG BÁO KIỂU FACEBOOK
        st.subheader("🔔 Thông báo mới")
        nhat_ky_all = load_data("nhat-ky.csv")
        thong_bao_fb = [i for i in nhat_ky_all if i['Tên'] == user['name'] and "✅" in str(i['Trạng thái'])]
        
        if thong_bao_fb:
            for tb in reversed(thong_bao_fb[-3:]): # Hiện 3 thông báo mới nhất
            for tb in reversed(thong_bao_fb[-3:]):
                with st.container(border=True):
                    c_ic, c_txt = st.columns([0.1, 0.9])
                    c_ic.markdown("### 🔵")
                    c_txt.markdown(f"**Ban Giám Hiệu** đã phản hồi yêu cầu *{tb['Loại']}* của bạn.")
                    c_txt.markdown(f"**Ban Giám Hiệu** đã phản hồi yêu cầu *{tb['Loại']}*.")
                    c_txt.caption(f"{tb['Trạng thái']} • {tb['Thời gian']}")
        else:
            st.info("Chưa có thông báo mới.")
        else: st.info("Chưa có thông báo mới.")

        st.divider()
        t1, t2, t3, t4 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh"])
        t1, t2, t3, t4, t5 = st.tabs(["Điểm danh", "Hủy bữa", "Xin nghỉ", "Phản ánh", "🎉 Sự kiện"])

        with t1:
            a_dd = st.camera_input("Chụp ảnh điểm danh")
            if a_dd and st.button("GỬI ĐIỂM DANH"):
                save_data("nhat-ky.csv", {"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)})
                save_single_data("nhat-ky.csv", {"Loại":"Điểm danh","Lớp":user['class'],"Tên":user['name'],"Nội dung":"Có mặt","Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_dd)})
                st.success("✅ Đã gửi!")

        with t2:
            st.error("🚫 **Lưu ý:** Hủy bữa Trưa trước 09h00 | Hủy bữa Chiều trước 15h00.")
            st.error("🚫 Hủy Trưa trước 09h | Hủy Chiều trước 15h.")
            thu = st.selectbox("Ngày báo hủy:", ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6"])
            buoi = st.multiselect("Buổi muốn hủy:", ["Bữa Trưa", "Bữa Chiều"], default=["Bữa Trưa"])
            xac_nhan = st.checkbox(f"Tôi xác nhận hủy ăn {thu}")
            gio_hien_tai = datetime.now().hour
            if st.button("Gửi yêu cầu hủy"):
                if xac_nhan:
                    loi = False
                    if "Bữa Trưa" in buoi and gio_hien_tai >= 9: st.error("Quá 9h! Không thể hủy trưa."); loi = True
                    if "Bữa Chiều" in buoi and gio_hien_tai >= 15: st.error("Quá 15h! Không thể hủy chiều."); loi = True
                    if not loi:
                        save_data("nhat-ky.csv", {"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY ĂN: {thu} ({', '.join(buoi)})","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                        st.success("❌ Đã gửi yêu cầu hủy!")
                else: st.warning("Vui lòng tích xác nhận.")

                save_single_data("nhat-ky.csv", {"Loại":"Báo ăn","Lớp":user['class'],"Tên":user['name'],"Nội dung":f"HỦY ĂN: {thu} ({', '.join(buoi)})","Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                st.success("❌ Đã báo hủy!")
        with t3:
            ly_do = st.text_area("Lý do nghỉ:")
            a_nghi = st.camera_input("Minh chứng (Đơn thuốc/Chỗ đau)")
            a_nghi = st.camera_input("Minh chứng (Đơn thuốc/Vết thương)")
            if st.button("Gửi đơn"):
                save_data("nhat-ky.csv", {"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly_do,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_nghi)})
                save_single_data("nhat-ky.csv", {"Loại":"Xin nghỉ","Lớp":user['class'],"Tên":user['name'],"Nội dung":ly_do,"Thời gian":datetime.now().strftime("%H:%M %d/%m"),"Trạng thái":"⏳ Chờ duyệt","Ảnh":image_to_base64(a_nghi)})
                st.success("✅ Đã gửi đơn!")

        with t4:
            yk = st.text_area("Ý kiến:")
            if st.button("Gửi"):
                save_data("nhat-ky.csv", {"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":yk,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
            if st.button("Gửi phản ánh"):
                save_single_data("nhat-ky.csv", {"Loại":"Phản ánh","Lớp":user['class'],"Tên":user['name'],"Nội dung":yk,"Thời gian":datetime.now().strftime("%H:%M"),"Trạng thái":"Đã gửi","Ảnh":""})
                st.success("📩 Đã nhận!")
        with t5:
            st.subheader("📣 Bản tin nhà trường")
            ds_sk = load_data("su-kien.csv")
            if ds_sk:
                for sk in reversed(ds_sk):
                    with st.container(border=True):
                        st.markdown(f"### {sk['Tiêu đề']}")
                        st.caption(f"📅 Đăng lúc: {sk['Thời gian']}")
                        st.write(sk['Nội dung'])
                        if str(sk.get('Ảnh')) != "nan" and sk.get('Ảnh'):
                            st.image(base64.b64decode(sk['Ảnh']), use_container_width=True)
            else: st.info("Chưa có sự kiện nào.")

    # --- BAN GIÁM HIỆU ---
    elif user.get('role') == "admin_gv":
        st.title("📂 QUẢN LÝ BAN GIÁM HIỆU")
        nhat_ky = load_data("nhat-ky.csv")
        t_nghi, t_dd, t_pa = st.tabs(["📑 Duyệt nghỉ", "📸 Duyệt điểm danh", "💬 Trả lời phản ánh"])
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Duyệt nghỉ", "📸 Duyệt điểm danh", "💬 Phản ánh", "📢 Quản lý Sự kiện"])

        def render_section(loai, msg):
        with tab1:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == loai:
                if item['Loại'] == "Xin nghỉ":
                    with st.expander(f"✉️ {item['Tên']} - {item['Trạng thái']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        
                        if loai == "Phản ánh":
                            rep = st.text_input("Trả lời:", key=f"r_{i}")
                            if st.button("Gửi", key=f"rb_{i}"):
                                nhat_ky[i]['Trạng thái'] = f"✅ BGH phản hồi: {rep}"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                        else:
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                if st.button("Duyệt ✅", key=f"d_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = msg; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.balloons(); st.rerun()
                            with c2:
                                if st.button("Từ chối ❌", key=f"tc_{loai}_{i}"):
                                    nhat_ky[i]['Trạng thái'] = "❌ Từ chối"; pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()
                            with c3:
                                if st.button("Xóa 🗑️", key=f"del_{loai}_{i}"):
                                    nhat_ky.pop(i); pd.DataFrame(nhat_ky).to_csv("nhat-ky.csv", index=False); st.rerun()

        with t_nghi: render_section("Xin nghỉ", "✅ Đã duyệt! Bạn hãy nghỉ ngơi theo yêu cầu nhé.")
        with t_dd: render_section("Điểm danh", "✅ BGH xác nhận điểm danh thành công.")
        with t_pa: render_section("Phản ánh", "")
                        if st.button(f"Duyệt ✅", key=f"d_n_{i}"):
                            nhat_ky[i]['Trạng thái'] = "✅ Đã duyệt và cho phép nghỉ!"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()
        
        with tab2:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Điểm danh":
                    with st.expander(f"👤 {item['Tên']} - {item['Lớp']}"):
                        if str(item.get('Ảnh')) != "nan" and item.get('Ảnh'):
                            st.image(base64.b64decode(item['Ảnh']), width=300)
                        if st.button(f"Xác nhận ✅", key=f"d_d_{i}"):
                            nhat_ky[i]['Trạng thái'] = "✅ BGH xác nhận điểm danh"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with tab3:
            for i, item in enumerate(nhat_ky):
                if item['Loại'] == "Phản ánh":
                    with st.expander(f"📩 Từ {item['Tên']}"):
                        st.write(f"**Nội dung:** {item['Nội dung']}")
                        rep = st.text_input("Trả lời:", key=f"rep_{i}")
                        if st.button("Gửi phản hồi", key=f"r_b_{i}"):
                            nhat_ky[i]['Trạng thái'] = f"✅ BGH phản hồi: {rep}"; save_all_data("nhat-ky.csv", nhat_ky); st.rerun()

        with tab4:
            st.subheader("Tạo sự kiện mới")
            with st.form("new_event"):
                t = st.text_input("Tiêu đề:")
                c = st.text_area("Nội dung:")
                img = st.file_uploader("Ảnh đính kèm", type=['jpg','png'])
                if st.form_submit_button("ĐĂNG BÀI"):
                    if t and c:
                        save_single_data("su-kien.csv", {"Tiêu đề":t, "Nội dung":c, "Ảnh":image_to_base64(img), "Thời gian":datetime.now().strftime("%H:%M %d/%m")})
                        st.success("Đã đăng!"); st.rerun()
            
            st.divider()
            st.subheader("Quản lý bài đã đăng")
            ds_sk = load_data("su-kien.csv")
            if ds_sk:
                for idx, sk in enumerate(ds_sk):
                    col1, col2 = st.columns([0.8, 0.2])
                    col1.write(f"📌 **{sk['Tiêu đề']}** ({sk['Thời gian']})")
                    if col2.button("Xóa bài 🗑️", key=f"del_sk_{idx}"):
                        ds_sk.pop(idx)
                        save_all_data("su-kien.csv", ds_sk)
                        st.rerun()
            else: st.info("Không có bài đăng nào.")

    elif user.get('role') == "admin_an":
        st.title("🍱 QUẢN LÝ BÁN TRÚ")