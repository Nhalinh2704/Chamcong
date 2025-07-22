
import sqlite3

DB_PATH = "chamcong.db"

def da_diem_danh(ma_nv, ngay):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chamcong WHERE ma_nv = ? AND ngay = ?", (ma_nv, ngay))
    result = cursor.fetchone()[0]
    conn.close()
    return result > 0

def ngay_diem_danh_dau(ma_nv):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(ngay) FROM chamcong WHERE ma_nv = ?", (ma_nv,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def luu_diem_danh(ma_nv, cong, ghi_chu, ngay):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chamcong (ma_nv, cong, ghi_chu, ngay) VALUES (?, ?, ?, ?)", (ma_nv, cong, ghi_chu, ngay))
    conn.commit()
    conn.close()

def lay_diem_danh_theo_ngay(ngay):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chamcong WHERE ngay = ?", (ngay,))
    rows = cursor.fetchall()
    conn.close()
    import pandas as pd
    return pd.DataFrame(rows, columns=["Mã nhân viên", "Công", "Ghi chú", "Ngày"])
import sqlite3

def xoa_diem_danh(ma_nv=None, tu_ngay=None, den_ngay=None):
    conn = sqlite3.connect("chamcong.db")
    cursor = conn.cursor()

    query = "DELETE FROM chamcong WHERE 1=1"
    params = []

    if ma_nv:
        query += " AND ma_nv = ?"
        params.append(ma_nv)

    if tu_ngay:
        query += " AND ngay >= ?"
        params.append(tu_ngay)

    if den_ngay:
        query += " AND ngay <= ?"
        params.append(den_ngay)

    cursor.execute(query, params)
    conn.commit()
    conn.close()
    print("✅ Đã xóa dữ liệu chấm công theo điều kiện.")
