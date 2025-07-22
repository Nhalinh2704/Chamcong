
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
