
import streamlit as st
import pandas as pd
import datetime
from cham_cong_db import create_db, da_diem_danh, ngay_diem_danh_dau, luu_diem_danh
import os

create_db()

# Load danh sách nhân viên
df_nv = pd.read_excel("nhanvien.xlsx", dtype={'Mã nhân viên': str})
df_nghi_bu = pd.read_excel("nghi_bu.xlsx", dtype={'Mã nhân viên': str})

st.title("📝 Công cụ điểm danh chấm công hằng ngày")

ma_nv = st.text_input("Nhập mã nhân viên (6 chữ số):")
if ma_nv and len(ma_nv) != 6:
    st.warning("⚠️ Mã nhân viên phải đủ 6 chữ số.")

loai_cong = st.selectbox("Chọn loại công", [
    "X:8", "X:8 (local)", "X:4,P:4", "P:4,X:4", "NB:8", "X:4,NB:4",
    "NB:4,X:4", "P:8", "CT:8", "DL:8", "TS:8", "Rv:8"
])

ghi_chu = st.text_input("Ghi chú (không bắt buộc):")

today = datetime.date.today()
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Từ ngày", today)
with col2:
    end_date = st.date_input("Đến ngày", today)

if start_date < today:
    st.error("❌ Không được chọn ngày trước ngày hôm nay.")

submit = st.button("💾 Điểm danh")

if submit:
    if not ma_nv or len(ma_nv) != 6:
        st.error("❌ Vui lòng nhập mã nhân viên hợp lệ.")
    elif start_date > end_date:
        st.error("❌ Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc.")
    else:
        nv_info = df_nv[df_nv["Mã nhân viên"] == ma_nv]
        if nv_info.empty:
            st.error("❌ Mã nhân viên không tồn tại trong danh sách.")
        else:
            ho_ten = nv_info.iloc[0]["Họ tên"]
            don_vi = nv_info.iloc[0]["Đơn vị"]
            nhom = nv_info.iloc[0]["Nhóm"]
            sort = nv_info.iloc[0]["SORT"]
            nghi_bu_row = df_nghi_bu[df_nghi_bu["Mã nhân viên"] == ma_nv]
            so_ngay_nghi_bu = nghi_bu_row.iloc[0]["Số ngày nghỉ bù"] if not nghi_bu_row.empty else 0

            da_co_trong_ngay = False
            for i in range((end_date - start_date).days + 1):
                ngay = start_date + datetime.timedelta(days=i)
                ngay_str = ngay.strftime("%Y-%m-%d")
                if da_diem_danh(ma_nv, ngay_str):
                    if not da_co_trong_ngay:
                        ngay_dau = ngay_diem_danh_dau(ma_nv)
                        st.warning(f"⚠️ Bạn đã điểm danh ngày hôm nay vào ngày {ngay_dau}.")
                        da_co_trong_ngay = True
                    continue

                luu_diem_danh(ma_nv, ho_ten, don_vi, nhom, sort, ngay_str, loai_cong, ghi_chu)

            if not da_co_trong_ngay:
                st.success(f"✅ Bạn đã điểm danh thành công cho các ngày từ {start_date} đến {end_date}.")
