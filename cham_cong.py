
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import io
from cham_cong_db import da_diem_danh, luu_diem_danh, ngay_diem_danh_dau, lay_diem_danh_theo_ngay

st.set_page_config(page_title="Chấm công", layout="wide")
st.title("📝 Chấm công P.TKTU")

# Đọc danh sách nhân viên và nghỉ bù
df_nv = pd.read_excel("nhanvien.xlsx", dtype={'Mã nhân viên': str})
df_nghi_bu = pd.read_excel("nghi_bu.xlsx", dtype={'Mã nhân viên': str})
nghi_bu_dict = dict(zip(df_nghi_bu['Mã nhân viên'], df_nghi_bu['Số ngày nghỉ bù']))

cong_options = [
    "X:8", "X:8 (local)", "X:4,P:4", "P:4,X:4", "NB:8", "X:4,NB:4", "NB:4,X:4",
    "P:8", "CT:8", "DL:8", "TS:8", "Rv:8"
]

with st.form("cham_cong_form"):
    ma_nv = st.text_input("Nhập mã nhân viên (6 chữ số):")
    loai_cong = st.selectbox("Chọn loại công", cong_options)
    ghi_chu = st.text_input("Ghi chú (nếu có)", value="")
    col1, col2 = st.columns(2)
    with col1:
        tu_ngay = st.date_input("Từ ngày", value=datetime.today())
    with col2:
        den_ngay = st.date_input("Đến ngày", value=datetime.today())

    submit = st.form_submit_button("✅ Điểm danh")

    if submit:
        if not ma_nv.isdigit() or len(ma_nv) != 6:
            st.error("Mã nhân viên phải gồm đúng 6 chữ số.")
        elif tu_ngay < datetime.today().date():
            st.error("Không thể chọn ngày chấm công trong quá khứ.")
        elif tu_ngay > den_ngay:
            st.error("Khoảng ngày không hợp lệ.")
        elif ma_nv not in df_nv["Mã nhân viên"].astype(str).values:
            st.error("Mã nhân viên không tồn tại trong danh sách.")
        else:
            ngay = tu_ngay
            da_luu = False
            while ngay <= den_ngay:
                if ngay < datetime.today().date():
                    st.warning(f'❌ Không thể điểm danh ngày quá khứ: {ngay.strftime("%d/%m/%Y")}')
                    ngay += timedelta(days=1)
                    continue
                if da_diem_danh(ma_nv, ngay.strftime("%Y-%m-%d")):
                    if not da_luu:
                        ngay_dau = ngay_diem_danh_dau(ma_nv)
                        st.warning(f"❌ Bạn đã điểm danh ngày hôm nay vào ngày {ngay_dau}.")
                        da_luu = True
                else:
                    luu_diem_danh(ma_nv, loai_cong, ghi_chu, ngay.strftime("%Y-%m-%d"))
                    st.success(f"✅ Đã điểm danh thành công ngày {ngay.strftime('%d/%m/%Y')}")
                ngay += timedelta(days=1)

# ----- Tải báo cáo theo ngày -----
st.markdown("---")
st.subheader("📤 Tải báo cáo chấm công theo ngày")

col1, col2 = st.columns([1, 2])
with col1:
    ngay_xuat = st.date_input("Chọn ngày cần xuất", value=datetime.today())

with col2:
    mk = st.text_input("Nhập mật khẩu để tải báo cáo", type="password")

if mk == "66702002":
    if st.button("📥 Xuất file Excel"):
        df_diemdanh = lay_diem_danh_theo_ngay(ngay_xuat.strftime("%Y-%m-%d"))
        df_diemdanh["Mã nhân viên"] = df_diemdanh["Mã nhân viên"].astype(str)

        # Mapping thông tin nhân viên
        df_out = pd.merge(df_nv, df_diemdanh[["Mã nhân viên", "Công", "Ghi chú"]], on="Mã nhân viên", how="left")
        df_out["Công"] = df_out["Công"].fillna("")
        df_out["Ghi chú"] = df_out["Ghi chú"].fillna("")

        # Gán công mặc định cho người chưa có công
        def fill_mac_dinh(row):
            if row["Công"]:
                return row["Công"]
            return "X:8 (local)" if "local" in row["Nhóm"].lower() else "X:8"

        df_out["Công"] = df_out.apply(fill_mac_dinh, axis=1)

        # Thêm STT
        df_out.insert(0, "STT", range(1, len(df_out) + 1))
        df_out = df_out[["STT", "Mã nhân viên", "Họ tên", "Đơn vị", "Công", "Ghi chú", "Nhóm"]]

        # Xuất Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_out.to_excel(writer, sheet_name="ChamCong", index=False)
        st.download_button("📥 Tải file Excel", output.getvalue(), file_name=f"ChamCong_{ngay_xuat}.xlsx")
else:
    if mk != "":
        st.warning("Sai mật khẩu!")
