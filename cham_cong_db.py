
import sqlite3
from datetime import datetime

DB_PATH = "chamcong.db"

def create_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cham_cong (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_nv TEXT,
                ho_ten TEXT,
                don_vi TEXT,
                nhom TEXT,
                sort INTEGER,
                ngay TEXT,
                cong TEXT,
                ghi_chu TEXT
            )
        """)
        conn.commit()

def da_diem_danh(ma_nv, ngay):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ngay FROM cham_cong WHERE ma_nv = ? AND ngay = ?", (ma_nv, ngay))
        return cursor.fetchone()

def ngay_diem_danh_dau(ma_nv):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ngay FROM cham_cong WHERE ma_nv = ? ORDER BY ngay LIMIT 1", (ma_nv,))
        result = cursor.fetchone()
        return result[0] if result else None

def luu_diem_danh(ma_nv, ho_ten, don_vi, nhom, sort, ngay, cong, ghi_chu):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cham_cong (ma_nv, ho_ten, don_vi, nhom, sort, ngay, cong, ghi_chu) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (ma_nv, ho_ten, don_vi, nhom, sort, ngay, cong, ghi_chu))
        conn.commit()

def lay_du_lieu_theo_ngay(ngay):
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM cham_cong WHERE ngay = ?", conn, params=(ngay,))
        return df



def lay_so_ngay_nghi_bu(ma_nv):
    import pandas as pd
    try:
        df_nghi_bu = pd.read_excel("nghi_bu.xlsx", dtype={'Mã nhân viên': str})
        nghi_bu_dict = dict(zip(df_nghi_bu['Mã nhân viên'], df_nghi_bu['Số ngày nghỉ bù']))
        return nghi_bu_dict.get(ma_nv, 0)
    except Exception as e:
        return 0

def xoa_diem_danh_voi_mk(ma_nv=None, tu_ngay=None, den_ngay=None, mat_khau=None):
    if mat_khau != "66702002":
        print("❌ Sai mật khẩu!")
        return False

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
    print("✅ Đã xóa dữ liệu chấm công.")
    return True
