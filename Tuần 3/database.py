"""
database.py - Quản lý SQLite với đầy đủ bảng:
  users, doan_vien, doan_phi, hoat_dong, tham_gia_hd, xep_loai
"""

import sqlite3
import hashlib
from datetime import datetime


class Database:
    DB_PATH = "qldv.db"

    def __init__(self):
        self.db_path = self.DB_PATH

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            # ── Bảng users ──────────────────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                full_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

            # ── Bảng đoàn viên ───────────────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS doan_vien (
                ma_dv TEXT PRIMARY KEY,
                ho_ten TEXT NOT NULL,
                ngay_sinh TEXT,
                gioi_tinh TEXT DEFAULT 'Nam',
                lop TEXT,
                khoa TEXT,
                email TEXT,
                so_dien_thoai TEXT,
                ngay_vao_doan TEXT,
                trang_thai TEXT DEFAULT 'Đang sinh hoạt',
                ghi_chu TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

            # ── Bảng đoàn phí ────────────────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS doan_phi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_dv TEXT NOT NULL,
                hoc_ky TEXT NOT NULL,
                nam_hoc TEXT NOT NULL,
                so_tien REAL DEFAULT 0,
                da_nop INTEGER DEFAULT 0,
                ngay_nop TEXT,
                ghi_chu TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(ma_dv) REFERENCES doan_vien(ma_dv) ON DELETE CASCADE,
                UNIQUE(ma_dv, hoc_ky, nam_hoc))""")

            # ── Bảng hoạt động ───────────────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS hoat_dong (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ten_hd TEXT NOT NULL,
                mo_ta TEXT,
                loai_hd TEXT DEFAULT 'Tình nguyện',
                ngay_to_chuc TEXT,
                dia_diem TEXT,
                so_luong_toi_da INTEGER DEFAULT 100,
                diem_cong REAL DEFAULT 1.0,
                trang_thai TEXT DEFAULT 'Sắp diễn ra',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

            # ── Bảng tham gia hoạt động ──────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS tham_gia_hd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_dv TEXT NOT NULL,
                id_hd INTEGER NOT NULL,
                ngay_dang_ky TEXT DEFAULT CURRENT_TIMESTAMP,
                da_tham_gia INTEGER DEFAULT 0,
                vai_tro TEXT DEFAULT 'Thành viên',
                ghi_chu TEXT,
                FOREIGN KEY(ma_dv) REFERENCES doan_vien(ma_dv) ON DELETE CASCADE,
                FOREIGN KEY(id_hd) REFERENCES hoat_dong(id) ON DELETE CASCADE,
                UNIQUE(ma_dv, id_hd))""")

            # ── Bảng xếp loại đoàn viên ──────────────────────────────────────
            cur.execute("""CREATE TABLE IF NOT EXISTS xep_loai (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_dv TEXT NOT NULL,
                hoc_ky TEXT NOT NULL,
                nam_hoc TEXT NOT NULL,
                diem_rl REAL DEFAULT 0,
                xep_loai_rl TEXT DEFAULT 'Chưa xếp loại',
                diem_hk REAL DEFAULT 0,
                xep_loai_hk TEXT DEFAULT 'Chưa xếp loại',
                so_hd_tham_gia INTEGER DEFAULT 0,
                dong_doan_phi INTEGER DEFAULT 0,
                ket_qua TEXT DEFAULT 'Chưa xếp loại',
                ghi_chu TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(ma_dv) REFERENCES doan_vien(ma_dv) ON DELETE CASCADE,
                UNIQUE(ma_dv, hoc_ky, nam_hoc))""")

            conn.commit()
            self._seed_users(cur, conn)
            self._seed_doan_vien(cur, conn)
            self._seed_hoat_dong(cur, conn)
            self._seed_doan_phi(cur, conn)
            self._seed_tham_gia(cur, conn)
            self._seed_xep_loai(cur, conn)
        except Exception as e:
            print(f"DB init error: {e}")
            import traceback; traceback.print_exc()
        finally:
            conn.close()

    # ── Seed data ────────────────────────────────────────────────────────────

    def _seed_users(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            admin_pw = hashlib.sha256("admin123".encode()).hexdigest()
            user_pw  = hashlib.sha256("user123".encode()).hexdigest()
            cur.executemany(
                "INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                [("admin","admin123_hash","admin","Nguyễn Văn Quản Trị"),
                 ("biquyet", admin_pw, "admin", "Bí Thư Đoàn Trường"),
                 ("user",  user_pw,  "user",  "Người Dùng Thường")])
            # Fix: dùng đúng hash
            cur.execute("UPDATE users SET password=? WHERE username='admin'",
                        (hashlib.sha256("admin123".encode()).hexdigest(),))
            conn.commit()

    def _seed_doan_vien(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM doan_vien")
        if cur.fetchone()[0] > 0: return
        data = [
            ("DV001","Nguyễn Văn An","2002-05-15","Nam","CNTT01","Công nghệ thông tin","an.nv@email.com","0901234567","2020-09-01","Đang sinh hoạt",""),
            ("DV002","Trần Thị Bình","2002-08-20","Nữ","CNTT01","Công nghệ thông tin","binh.tt@email.com","0912345678","2020-09-01","Đang sinh hoạt",""),
            ("DV003","Lê Văn Cường","2001-03-10","Nam","KT02","Kinh tế","cuong.lv@email.com","0923456789","2019-09-01","Đang sinh hoạt",""),
            ("DV004","Phạm Thị Dung","2003-11-25","Nữ","KT02","Kinh tế","dung.pt@email.com","0934567890","2021-09-01","Đang sinh hoạt",""),
            ("DV005","Hoàng Văn Em","2002-07-14","Nam","XD03","Xây dựng","em.hv@email.com","0945678901","2020-09-01","Đã rời","Tốt nghiệp"),
            ("DV006","Nguyễn Thị Fương","2002-01-30","Nữ","CNTT02","Công nghệ thông tin","fuong.nt@email.com","0956789012","2020-09-01","Đang sinh hoạt",""),
            ("DV007","Vũ Văn Giang","2001-06-18","Nam","CK04","Cơ khí","giang.vv@email.com","0967890123","2019-09-01","Đang sinh hoạt",""),
            ("DV008","Đặng Thị Hoa","2003-04-22","Nữ","KT01","Kinh tế","hoa.dt@email.com","0978901234","2021-09-01","Đang sinh hoạt",""),
            ("DV009","Bùi Văn Inh","2002-09-05","Nam","CK04","Cơ khí","inh.bv@email.com","0989012345","2020-09-01","Đang sinh hoạt",""),
            ("DV010","Phan Thị Kim","2001-12-11","Nữ","XD03","Xây dựng","kim.pt@email.com","0990123456","2019-09-01","Đang sinh hoạt",""),
            ("DV011","Lý Văn Long","2003-02-28","Nam","CNTT02","Công nghệ thông tin","long.lv@email.com","0901234560","2021-09-01","Đang sinh hoạt",""),
            ("DV012","Tô Thị Mai","2002-10-17","Nữ","KT01","Kinh tế","mai.tt@email.com","0912345670","2020-09-01","Đã rời","Chuyển trường"),
            ("DV013","Đinh Văn Nam","2003-07-09","Nam","DD05","Điện - Điện tử","nam.dv@email.com","0923456780","2021-09-01","Đang sinh hoạt",""),
            ("DV014","Cao Thị Oanh","2002-03-14","Nữ","DD05","Điện - Điện tử","oanh.ct@email.com","0934567801","2020-09-01","Đang sinh hoạt",""),
            ("DV015","Trịnh Văn Phong","2001-11-02","Nam","CNTT01","Công nghệ thông tin","phong.tv@email.com","0945678902","2019-09-01","Đang sinh hoạt","Cán bộ lớp"),
        ]
        cur.executemany("""INSERT INTO doan_vien
            (ma_dv,ho_ten,ngay_sinh,gioi_tinh,lop,khoa,email,so_dien_thoai,
             ngay_vao_doan,trang_thai,ghi_chu) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", data)
        conn.commit()

    def _seed_hoat_dong(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM hoat_dong")
        if cur.fetchone()[0] > 0: return
        data = [
            ("Hiến máu tình nguyện HK1/2024","Chiến dịch hiến máu tình nguyện lần 1","Hiến máu","2024-10-15","Hội trường A",200,2.0,"Đã kết thúc"),
            ("Hỗ trợ trẻ em vùng cao","Tình nguyện mang sách vở & quần áo lên Tây Bắc","Tình nguyện","2024-11-20","Hà Giang",50,3.0,"Đã kết thúc"),
            ("Ngày hội thiện nguyện 2024","Quyên góp, hỗ trợ người nghèo dịp Tết","Thiện nguyện","2024-12-22","Sân trường",300,1.5,"Đã kết thúc"),
            ("Mùa hè xanh 2024","Tình nguyện xây dựng nhà tình thương","Mùa hè xanh","2024-06-10","Nghệ An",80,4.0,"Đã kết thúc"),
            ("Hiến máu tình nguyện HK2/2024","Chiến dịch hiến máu lần 2 trong năm","Hiến máu","2025-03-18","Hội trường B",200,2.0,"Đã kết thúc"),
            ("Dọn vệ sinh môi trường","Tổng vệ sinh khuôn viên trường và khu dân cư","Môi trường","2025-04-22","Trường & lân cận",500,1.0,"Đã kết thúc"),
            ("Hỗ trợ thi cử 2025","Tiếp sức mùa thi - hỗ trợ thí sinh","Tiếp sức mùa thi","2025-06-01","Hội đồng thi",100,1.5,"Sắp diễn ra"),
            ("Trại hè kỹ năng lãnh đạo","Rèn kỹ năng sống và lãnh đạo cho cán bộ Đoàn","Kỹ năng","2025-07-15","Nhà văn hóa",60,2.5,"Sắp diễn ra"),
        ]
        cur.executemany("""INSERT INTO hoat_dong
            (ten_hd,mo_ta,loai_hd,ngay_to_chuc,dia_diem,so_luong_toi_da,diem_cong,trang_thai)
            VALUES(?,?,?,?,?,?,?,?)""", data)
        conn.commit()

    def _seed_doan_phi(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM doan_phi")
        if cur.fetchone()[0] > 0: return
        import random
        hk_list = [("HK1","2023-2024"),("HK2","2023-2024"),("HK1","2024-2025")]
        cur.execute("SELECT ma_dv FROM doan_vien WHERE trang_thai='Đang sinh hoạt'")
        dvs = [r[0] for r in cur.fetchall()]
        rows = []
        for ma in dvs:
            for hk, nh in hk_list:
                da_nop = random.choice([0,1,1,1])
                ngay   = f"2024-0{random.randint(1,9)}-{random.randint(10,28)}" if da_nop else None
                rows.append((ma, hk, nh, 30000.0, da_nop, ngay, ""))
        cur.executemany("""INSERT OR IGNORE INTO doan_phi
            (ma_dv,hoc_ky,nam_hoc,so_tien,da_nop,ngay_nop,ghi_chu)
            VALUES(?,?,?,?,?,?,?)""", rows)
        conn.commit()

    def _seed_tham_gia(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM tham_gia_hd")
        if cur.fetchone()[0] > 0: return
        import random
        cur.execute("SELECT id FROM hoat_dong")
        hds = [r[0] for r in cur.fetchall()]
        cur.execute("SELECT ma_dv FROM doan_vien WHERE trang_thai='Đang sinh hoạt'")
        dvs = [r[0] for r in cur.fetchall()]
        rows = []
        for id_hd in hds:
            tham_gia = random.sample(dvs, min(random.randint(4,10), len(dvs)))
            for ma in tham_gia:
                rows.append((ma, id_hd, 1, "Thành viên", ""))
        cur.executemany("""INSERT OR IGNORE INTO tham_gia_hd
            (ma_dv,id_hd,da_tham_gia,vai_tro,ghi_chu) VALUES(?,?,?,?,?)""", rows)
        conn.commit()

    def _seed_xep_loai(self, cur, conn):
        cur.execute("SELECT COUNT(*) FROM xep_loai")
        if cur.fetchone()[0] > 0: return
        import random
        cur.execute("SELECT ma_dv FROM doan_vien WHERE trang_thai='Đang sinh hoạt'")
        dvs = [r[0] for r in cur.fetchall()]
        hk_list = [("HK1","2024-2025"),("HK2","2023-2024")]
        rows = []
        for ma in dvs:
            for hk, nh in hk_list:
                drl = round(random.uniform(55, 100), 1)
                dhk = round(random.uniform(2.0, 4.0), 2)
                so_hd = random.randint(1, 6)
                dp = random.choice([0,1,1])
                xrl = self._xep_loai_rl(drl)
                xhk = self._xep_loai_hk(dhk)
                kq  = self._ket_qua(drl, dhk, so_hd, dp)
                rows.append((ma, hk, nh, drl, xrl, dhk, xhk, so_hd, dp, kq, ""))
        cur.executemany("""INSERT OR IGNORE INTO xep_loai
            (ma_dv,hoc_ky,nam_hoc,diem_rl,xep_loai_rl,diem_hk,xep_loai_hk,
             so_hd_tham_gia,dong_doan_phi,ket_qua,ghi_chu)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""", rows)
        conn.commit()

    @staticmethod
    def _xep_loai_rl(d):
        if d >= 90: return "Xuất sắc"
        if d >= 75: return "Tốt"
        if d >= 60: return "Khá"
        if d >= 50: return "Trung bình"
        return "Yếu"

    @staticmethod
    def _xep_loai_hk(d):
        if d >= 3.6: return "Xuất sắc"
        if d >= 3.2: return "Giỏi"
        if d >= 2.5: return "Khá"
        if d >= 2.0: return "Trung bình"
        return "Yếu"

    @staticmethod
    def _ket_qua(drl, dhk, so_hd, dp):
        if drl >= 75 and dhk >= 2.5 and so_hd >= 2 and dp == 1:
            if drl >= 90 and dhk >= 3.6: return "Đoàn viên Xuất sắc"
            return "Đoàn viên Hoàn thành tốt"
        if drl >= 50 and dhk >= 2.0:
            return "Đoàn viên Hoàn thành"
        return "Đoàn viên Không hoàn thành"

    # ── CRUD Users ───────────────────────────────────────────────────────────

    def verify_login(self, username, password):
        pw = hashlib.sha256(password.encode()).hexdigest()
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, pw))
            r = cur.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def get_all_users(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id,username,role,full_name,created_at FROM users ORDER BY id")
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def add_user(self, username, password, role, full_name):
        pw = hashlib.sha256(password.encode()).hexdigest()
        conn = self.get_connection()
        try:
            conn.execute("INSERT INTO users(username,password,role,full_name) VALUES(?,?,?,?)",
                         (username, pw, role, full_name))
            conn.commit()
            return True, "Tạo tài khoản thành công!"
        except Exception as e:
            return False, f"Tên đăng nhập đã tồn tại!"
        finally:
            conn.close()

    def delete_user(self, uid):
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM users WHERE id=?", (uid,))
            conn.commit()
            return True
        finally:
            conn.close()

    # ── CRUD Đoàn viên ───────────────────────────────────────────────────────

    def get_all_dv(self, search="", field="ho_ten"):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            safe = field if field in ("ho_ten","ma_dv","lop","khoa") else "ho_ten"
            if search:
                cur.execute(f"SELECT * FROM doan_vien WHERE {safe} LIKE ? ORDER BY ma_dv",
                            (f"%{search}%",))
            else:
                cur.execute("SELECT * FROM doan_vien ORDER BY ma_dv")
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def get_dv_by_ma(self, ma):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM doan_vien WHERE ma_dv=?", (ma,))
            r = cur.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def add_dv(self, d):
        conn = self.get_connection()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("""INSERT INTO doan_vien
                (ma_dv,ho_ten,ngay_sinh,gioi_tinh,lop,khoa,email,
                 so_dien_thoai,ngay_vao_doan,trang_thai,ghi_chu,created_at,updated_at)
                VALUES(:ma_dv,:ho_ten,:ngay_sinh,:gioi_tinh,:lop,:khoa,:email,
                       :so_dien_thoai,:ngay_vao_doan,:trang_thai,:ghi_chu,:now,:now)""",
                {**d, "now": now})
            conn.commit()
            return True, "Thêm thành công!"
        except Exception as e:
            return False, f"Mã đã tồn tại: {e}"
        finally:
            conn.close()

    def update_dv(self, ma, d):
        conn = self.get_connection()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("""UPDATE doan_vien SET
                ho_ten=:ho_ten,ngay_sinh=:ngay_sinh,gioi_tinh=:gioi_tinh,
                lop=:lop,khoa=:khoa,email=:email,so_dien_thoai=:so_dien_thoai,
                ngay_vao_doan=:ngay_vao_doan,trang_thai=:trang_thai,
                ghi_chu=:ghi_chu,updated_at=:now WHERE ma_dv=:ma""",
                {**d, "ma": ma, "now": now})
            conn.commit()
            return True, "Cập nhật thành công!"
        finally:
            conn.close()

    def delete_dv(self, ma):
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM doan_vien WHERE ma_dv=?", (ma,))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_next_ma(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT ma_dv FROM doan_vien ORDER BY ma_dv DESC LIMIT 1")
            r = cur.fetchone()
            num = int(r[0][2:]) + 1 if r else 1
            return f"DV{num:03d}"
        finally:
            conn.close()

    def get_stats(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM doan_vien"); total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM doan_vien WHERE trang_thai='Đang sinh hoạt'"); active = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM doan_vien WHERE trang_thai='Đã rời'"); left = cur.fetchone()[0]
            cur.execute("SELECT COUNT(DISTINCT khoa) FROM doan_vien"); khoa = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM hoat_dong"); hd = cur.fetchone()[0]
            return {"total":total,"active":active,"left":left,"khoa":khoa,"hoat_dong":hd}
        finally:
            conn.close()

    def get_stats_by_khoa(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""SELECT khoa, COUNT(*) as sl FROM doan_vien
                WHERE trang_thai='Đang sinh hoạt' GROUP BY khoa ORDER BY sl DESC""")
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def get_stats_by_lop(self):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""SELECT lop, khoa, COUNT(*) as sl FROM doan_vien
                WHERE trang_thai='Đang sinh hoạt' GROUP BY lop ORDER BY khoa,lop""")
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    # ── Đoàn phí ─────────────────────────────────────────────────────────────

    def get_doan_phi(self, search="", hoc_ky="", nam_hoc=""):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            q = """SELECT dp.*, dv.ho_ten, dv.lop, dv.khoa
                   FROM doan_phi dp JOIN doan_vien dv ON dp.ma_dv=dv.ma_dv WHERE 1=1"""
            params = []
            if search:
                q += " AND (dv.ho_ten LIKE ? OR dp.ma_dv LIKE ?)"
                params += [f"%{search}%", f"%{search}%"]
            if hoc_ky and hoc_ky != "Tất cả":
                q += " AND dp.hoc_ky=?"; params.append(hoc_ky)
            if nam_hoc and nam_hoc != "Tất cả":
                q += " AND dp.nam_hoc=?"; params.append(nam_hoc)
            q += " ORDER BY dp.nam_hoc DESC, dp.hoc_ky, dv.lop, dv.ho_ten"
            cur.execute(q, params)
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def update_doan_phi(self, id_, da_nop, ngay_nop, ghi_chu):
        conn = self.get_connection()
        try:
            conn.execute("UPDATE doan_phi SET da_nop=?,ngay_nop=?,ghi_chu=? WHERE id=?",
                         (da_nop, ngay_nop, ghi_chu, id_))
            conn.commit()
            return True
        finally:
            conn.close()

    def add_doan_phi_bulk(self, hoc_ky, nam_hoc, so_tien):
        """Tự động tạo bản ghi đoàn phí cho tất cả đoàn viên đang sinh hoạt"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT ma_dv FROM doan_vien WHERE trang_thai='Đang sinh hoạt'")
            dvs = [r[0] for r in cur.fetchall()]
            for ma in dvs:
                try:
                    conn.execute("""INSERT OR IGNORE INTO doan_phi
                        (ma_dv,hoc_ky,nam_hoc,so_tien,da_nop) VALUES(?,?,?,?,0)""",
                        (ma, hoc_ky, nam_hoc, so_tien))
                except: pass
            conn.commit()
            return True, f"Đã tạo đoàn phí {hoc_ky}/{nam_hoc} cho {len(dvs)} đoàn viên"
        finally:
            conn.close()

    def get_doan_phi_stats(self, hoc_ky="", nam_hoc=""):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            q = "SELECT COUNT(*) as total, SUM(da_nop) as da_nop, SUM(so_tien*da_nop) as tong_thu FROM doan_phi WHERE 1=1"
            params = []
            if hoc_ky and hoc_ky != "Tất cả":
                q += " AND hoc_ky=?"; params.append(hoc_ky)
            if nam_hoc and nam_hoc != "Tất cả":
                q += " AND nam_hoc=?"; params.append(nam_hoc)
            cur.execute(q, params)
            return dict(cur.fetchone())
        finally:
            conn.close()

    # ── Hoạt động ─────────────────────────────────────────────────────────────

    def get_all_hoat_dong(self, search="", loai=""):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            q = """SELECT hd.*, 
                   (SELECT COUNT(*) FROM tham_gia_hd t WHERE t.id_hd=hd.id AND t.da_tham_gia=1) as so_tham_gia
                   FROM hoat_dong hd WHERE 1=1"""
            params = []
            if search:
                q += " AND hd.ten_hd LIKE ?"; params.append(f"%{search}%")
            if loai and loai != "Tất cả":
                q += " AND hd.loai_hd=?"; params.append(loai)
            q += " ORDER BY hd.ngay_to_chuc DESC"
            cur.execute(q, params)
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def get_hoat_dong_by_id(self, id_):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM hoat_dong WHERE id=?", (id_,))
            r = cur.fetchone()
            return dict(r) if r else None
        finally:
            conn.close()

    def add_hoat_dong(self, d):
        conn = self.get_connection()
        try:
            conn.execute("""INSERT INTO hoat_dong
                (ten_hd,mo_ta,loai_hd,ngay_to_chuc,dia_diem,so_luong_toi_da,diem_cong,trang_thai)
                VALUES(:ten_hd,:mo_ta,:loai_hd,:ngay_to_chuc,:dia_diem,:so_luong_toi_da,:diem_cong,:trang_thai)""", d)
            conn.commit()
            return True, "Thêm hoạt động thành công!"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def update_hoat_dong(self, id_, d):
        conn = self.get_connection()
        try:
            conn.execute("""UPDATE hoat_dong SET
                ten_hd=:ten_hd,mo_ta=:mo_ta,loai_hd=:loai_hd,ngay_to_chuc=:ngay_to_chuc,
                dia_diem=:dia_diem,so_luong_toi_da=:so_luong_toi_da,
                diem_cong=:diem_cong,trang_thai=:trang_thai WHERE id=:id""",
                {**d, "id": id_})
            conn.commit()
            return True, "Cập nhật thành công!"
        finally:
            conn.close()

    def delete_hoat_dong(self, id_):
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM hoat_dong WHERE id=?", (id_,))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_tham_gia(self, id_hd):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""SELECT t.*, dv.ho_ten, dv.lop, dv.khoa
                FROM tham_gia_hd t JOIN doan_vien dv ON t.ma_dv=dv.ma_dv
                WHERE t.id_hd=? ORDER BY dv.lop, dv.ho_ten""", (id_hd,))
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def dang_ky_tham_gia(self, ma_dv, id_hd, vai_tro="Thành viên"):
        conn = self.get_connection()
        try:
            conn.execute("""INSERT OR IGNORE INTO tham_gia_hd
                (ma_dv,id_hd,da_tham_gia,vai_tro) VALUES(?,?,1,?)""",
                (ma_dv, id_hd, vai_tro))
            conn.commit()
            return True
        except: return False
        finally:
            conn.close()

    def cap_nhat_tham_gia(self, id_, da_tham_gia, vai_tro, ghi_chu):
        conn = self.get_connection()
        try:
            conn.execute("UPDATE tham_gia_hd SET da_tham_gia=?,vai_tro=?,ghi_chu=? WHERE id=?",
                         (da_tham_gia, vai_tro, ghi_chu, id_))
            conn.commit()
            return True
        finally:
            conn.close()

    def xoa_tham_gia(self, id_):
        conn = self.get_connection()
        try:
            conn.execute("DELETE FROM tham_gia_hd WHERE id=?", (id_,))
            conn.commit()
        finally:
            conn.close()

    # ── Xếp loại ─────────────────────────────────────────────────────────────

    def get_xep_loai(self, hoc_ky="", nam_hoc="", ket_qua="", search=""):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            q = """SELECT xl.*, dv.ho_ten, dv.lop, dv.khoa FROM xep_loai xl
                   JOIN doan_vien dv ON xl.ma_dv=dv.ma_dv WHERE 1=1"""
            p = []
            if hoc_ky and hoc_ky != "Tất cả":
                q += " AND xl.hoc_ky=?"; p.append(hoc_ky)
            if nam_hoc and nam_hoc != "Tất cả":
                q += " AND xl.nam_hoc=?"; p.append(nam_hoc)
            if ket_qua and ket_qua != "Tất cả":
                q += " AND xl.ket_qua=?"; p.append(ket_qua)
            if search:
                q += " AND (dv.ho_ten LIKE ? OR xl.ma_dv LIKE ?)"; p += [f"%{search}%"]*2
            q += " ORDER BY xl.nam_hoc DESC, xl.hoc_ky, dv.lop, dv.ho_ten"
            cur.execute(q, p)
            return [dict(r) for r in cur.fetchall()]
        finally:
            conn.close()

    def save_xep_loai(self, d):
        conn = self.get_connection()
        try:
            xrl = Database._xep_loai_rl(d["diem_rl"])
            xhk = Database._xep_loai_hk(d["diem_hk"])
            kq  = Database._ket_qua(d["diem_rl"], d["diem_hk"], d["so_hd_tham_gia"], d["dong_doan_phi"])
            conn.execute("""INSERT INTO xep_loai
                (ma_dv,hoc_ky,nam_hoc,diem_rl,xep_loai_rl,diem_hk,xep_loai_hk,
                 so_hd_tham_gia,dong_doan_phi,ket_qua,ghi_chu)
                VALUES(:ma_dv,:hoc_ky,:nam_hoc,:drl,:xrl,:dhk,:xhk,:so_hd,:dp,:kq,:ghi_chu)
                ON CONFLICT(ma_dv,hoc_ky,nam_hoc) DO UPDATE SET
                diem_rl=:drl,xep_loai_rl=:xrl,diem_hk=:dhk,xep_loai_hk=:xhk,
                so_hd_tham_gia=:so_hd,dong_doan_phi=:dp,ket_qua=:kq,ghi_chu=:ghi_chu""",
                {**d, "drl":d["diem_rl"],"xrl":xrl,"dhk":d["diem_hk"],
                 "xhk":xhk,"so_hd":d["so_hd_tham_gia"],"dp":d["dong_doan_phi"],"kq":kq})
            conn.commit()
            return True, f"Lưu xếp loại thành công! Kết quả: {kq}"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def auto_xep_loai(self, hoc_ky, nam_hoc):
        """Tự động xếp loại toàn bộ đoàn viên theo học kỳ"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT ma_dv FROM doan_vien WHERE trang_thai='Đang sinh hoạt'")
            dvs = [r[0] for r in cur.fetchall()]
            count = 0
            for ma in dvs:
                # Lấy điểm rèn luyện (dùng random nếu chưa có)
                cur.execute("SELECT diem_rl FROM xep_loai WHERE ma_dv=? AND hoc_ky=? AND nam_hoc=?",
                            (ma, hoc_ky, nam_hoc))
                ex = cur.fetchone()
                import random
                drl = ex[0] if ex else round(random.uniform(60, 95), 1)
                dhk = round(random.uniform(2.2, 3.9), 2)
                # Đếm hoạt động tham gia
                cur.execute("""SELECT COUNT(*) FROM tham_gia_hd t
                    JOIN hoat_dong h ON t.id_hd=h.id
                    WHERE t.ma_dv=? AND t.da_tham_gia=1""", (ma,))
                so_hd = cur.fetchone()[0]
                # Kiểm tra đóng đoàn phí
                cur.execute("SELECT da_nop FROM doan_phi WHERE ma_dv=? AND hoc_ky=? AND nam_hoc=?",
                            (ma, hoc_ky, nam_hoc))
                dp_r = cur.fetchone()
                dp = dp_r[0] if dp_r else 0
                xrl = Database._xep_loai_rl(drl)
                xhk = Database._xep_loai_hk(dhk)
                kq  = Database._ket_qua(drl, dhk, so_hd, dp)
                conn.execute("""INSERT INTO xep_loai
                    (ma_dv,hoc_ky,nam_hoc,diem_rl,xep_loai_rl,diem_hk,xep_loai_hk,
                     so_hd_tham_gia,dong_doan_phi,ket_qua)
                    VALUES(?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(ma_dv,hoc_ky,nam_hoc) DO UPDATE SET
                    diem_rl=excluded.diem_rl,xep_loai_rl=excluded.xep_loai_rl,
                    diem_hk=excluded.diem_hk,xep_loai_hk=excluded.xep_loai_hk,
                    so_hd_tham_gia=excluded.so_hd_tham_gia,
                    dong_doan_phi=excluded.dong_doan_phi,ket_qua=excluded.ket_qua""",
                    (ma,hoc_ky,nam_hoc,drl,xrl,dhk,xhk,so_hd,dp,kq))
                count += 1
            conn.commit()
            return True, f"Đã xếp loại {count} đoàn viên cho {hoc_ky}/{nam_hoc}"
        finally:
            conn.close()
