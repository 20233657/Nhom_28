"""views/main_window.py - Cửa sổ chính, sidebar sạch không border thừa"""
import math
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen, QPolygon
from styles import COLORS


class SidebarBtn(QPushButton):
    def __init__(self, icon, label, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f" {icon}  {label}")
        self._style(False)

    def _style(self, active):
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(198,40,40,0.85);
                    color: white;
                    border: none;
                    border-left: 3px solid {COLORS['accent']};
                    text-align: left;
                    padding-left: 18px;
                    font-size: 9.5pt;
                    font-weight: 700;
                    border-radius: 0;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: rgba(200, 210, 230, 0.80);
                    border: none;
                    border-left: 3px solid transparent;
                    text-align: left;
                    padding-left: 18px;
                    font-size: 9.5pt;
                    border-radius: 0;
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,0.06);
                    color: white;
                    border-left: 3px solid {COLORS['primary_light']};
                }}
            """)

    def set_active(self, v):
        self._style(v)


class _StarMini(QWidget):
    """Logo ngôi sao nhỏ cho sidebar header"""
    def __init__(self, size=40, parent=None):
        super().__init__(parent)
        self.sz = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        sz = self.sz
        cx, cy = sz // 2, sz // 2
        r = sz // 2 - 1

        # Viền vàng
        p.setBrush(QBrush(QColor(COLORS['accent'])))
        p.setPen(Qt.NoPen)
        p.drawEllipse(0, 0, sz, sz)

        # Nền đỏ
        g = QLinearGradient(0, 0, sz, sz)
        g.setColorAt(0, QColor(COLORS['primary_light']))
        g.setColorAt(1, QColor(COLORS['primary_dark']))
        p.setBrush(QBrush(g))
        p.setPen(Qt.NoPen)
        p.drawEllipse(3, 3, sz - 6, sz - 6)

        # Sao vàng
        p.setBrush(QBrush(QColor(COLORS['accent'])))
        p.setPen(Qt.NoPen)
        outer = r * 0.58
        inner = r * 0.25
        pts = []
        for i in range(10):
            angle = math.radians(-90 + i * 36)
            rr = outer if i % 2 == 0 else inner
            pts.append(QPoint(int(cx + rr * math.cos(angle)), int(cy + rr * math.sin(angle))))
        p.drawPolygon(QPolygon(pts))
        p.end()


class MainWindow(QMainWindow):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        role_txt = "QUẢN TRỊ VIÊN" if user['role'] == 'admin' else "NGƯỜI DÙNG"
        self.setWindowTitle(f"Quản lý Đoàn viên  ─  {user['full_name']}  [{role_txt}]")
        self.setMinimumSize(1280, 780)
        self.resize(1440, 860)
        self._build()
        self._center()
        self._switch(0)

    def _center(self):
        from PyQt5.QtWidgets import QDesktopWidget
        sc = QDesktopWidget().screenGeometry()
        self.move((sc.width() - self.width()) // 2, (sc.height() - self.height()) // 2)

    def _build(self):
        from styles import MAIN_STYLE
        self.setStyleSheet(MAIN_STYLE)
        cw = QWidget()
        self.setCentralWidget(cw)
        root = QHBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── SIDEBAR ────────────────────────────────────────────────────────
        sb = QWidget()
        sb.setFixedWidth(268)
        sb.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1C1C2E, stop:1 #13131F);
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        sl = QVBoxLayout(sb)
        sl.setContentsMargins(0, 0, 0, 0)
        sl.setSpacing(0)

        # Header sidebar: logo + tên app
        hdr = QWidget()
        hdr.setFixedHeight(84)
        hdr.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {COLORS['primary_dark']}, stop:0.5 {COLORS['primary']}, stop:1 #6A0000);
                border-bottom: 2px solid {COLORS['accent']};
            }}
            QLabel {{ background: transparent; border: none; }}
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(14, 0, 14, 0)
        hl.setSpacing(12)

        star = _StarMini(42)
        hl.addWidget(star)

        ntx = QVBoxLayout()
        ntx.setSpacing(1)
        n1 = QLabel("QUẢN LÝ")
        n1.setFont(QFont("Segoe UI", 9, QFont.Bold))
        n1.setStyleSheet("color: rgba(255,255,255,0.8); background: transparent; border: none; letter-spacing: 2px;")
        n2 = QLabel("ĐOÀN VIÊN")
        n2.setFont(QFont("Segoe UI", 13, QFont.Bold))
        n2.setStyleSheet(f"color: {COLORS['accent']}; background: transparent; border: none; letter-spacing: 1px;")
        ntx.addWidget(n1)
        ntx.addWidget(n2)
        hl.addLayout(ntx)
        hl.addStretch()
        sl.addWidget(hdr)

        # Thông tin user
        uf = QWidget()
        uf.setFixedHeight(64)
        uf.setStyleSheet("""
            QWidget { background: rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.08); }
            QLabel  { background: transparent; border: none; }
        """)
        ul = QHBoxLayout(uf)
        ul.setContentsMargins(14, 0, 14, 0)
        ul.setSpacing(10)

        role_icon = "👑" if self.user['role'] == 'admin' else "👤"
        av = QLabel(role_icon)
        av.setFont(QFont("Segoe UI Emoji", 22))
        av.setStyleSheet("background: transparent; border: none;")

        ui_box = QVBoxLayout()
        ui_box.setSpacing(2)
        un = QLabel(self.user['full_name'])
        un.setFont(QFont("Segoe UI", 9, QFont.Bold))
        un.setStyleSheet(f"color: {COLORS['text_on_dark']}; background: transparent; border: none;")

        ur_color = COLORS['accent'] if self.user['role'] == 'admin' else COLORS['success_light']
        ur = QLabel("ADMIN" if self.user['role'] == 'admin' else "USER")
        ur.setFont(QFont("Segoe UI", 8, QFont.Bold))
        ur.setStyleSheet(f"color: {ur_color}; background: transparent; border: none; letter-spacing: 1px;")

        ui_box.addWidget(un)
        ui_box.addWidget(ur)
        ul.addWidget(av)
        ul.addLayout(ui_box)
        ul.addStretch()
        sl.addWidget(uf)

        # Label section
        sec_lbl = QLabel("  CHỨC NĂNG CHÍNH")
        sec_lbl.setFixedHeight(30)
        sec_lbl.setFont(QFont("Segoe UI", 7, QFont.Bold))
        sec_lbl.setStyleSheet("color: rgba(255,255,255,0.35); background: transparent; border: none; letter-spacing: 2px;")
        sl.addWidget(sec_lbl)

        # Menu items
        menus = [
            ("📋", "Danh sách Đoàn viên"),
            ("💰", "Quản lý Đoàn phí"),
            ("🏆", "Hoạt động & Tham gia"),
            ("⭐", "Xếp loại theo Học kỳ"),
            ("📊", "Thống kê & Báo cáo"),
            ("📤", "Xuất dữ liệu"),
        ]
        if self.user['role'] == 'admin':
            menus.append(("⚙️", "Quản lý Tài khoản"))

        self.sb_btns = []
        for icon, label in menus:
            btn = SidebarBtn(icon, label)
            btn.clicked.connect(lambda _, b=btn: self._on_sb(b))
            self.sb_btns.append(btn)
            sl.addWidget(btn)

        sl.addStretch()

        # Đường kẻ ngang mỏng
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.08);")
        sl.addWidget(sep)

        # Đăng xuất
        btn_out = QPushButton("🚪   Đăng xuất")
        btn_out.setFixedHeight(48)
        btn_out.setCursor(Qt.PointingHandCursor)
        btn_out.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: rgba(230, 100, 100, 0.9);
                border: none;
                text-align: left;
                padding-left: 22px;
                font-size: 9.5pt;
                font-weight: 600;
                border-radius: 0;
            }}
            QPushButton:hover {{
                background: rgba(183,28,28,0.18);
                color: #FF6B6B;
            }}
        """)
        btn_out.clicked.connect(self._logout)
        sl.addWidget(btn_out)
        sl.addSpacing(6)

        # ── STACK PAGES ────────────────────────────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {COLORS['bg_main']};")

        from views.dv_view import DVView
        from views.doan_phi_view import DoanPhiView
        from views.hoat_dong_view import HoatDongView
        from views.xep_loai_view import XepLoaiView
        from views.stats_view import StatsView
        from views.export_view import ExportView

        self.p_dv   = DVView(self.db, self.user)
        self.p_phi  = DoanPhiView(self.db, self.user)
        self.p_hd   = HoatDongView(self.db, self.user)
        self.p_xl   = XepLoaiView(self.db, self.user)
        self.p_stat = StatsView(self.db)
        self.p_exp  = ExportView(self.db)

        for pg in [self.p_dv, self.p_phi, self.p_hd, self.p_xl, self.p_stat, self.p_exp]:
            self.stack.addWidget(pg)

        if self.user['role'] == 'admin':
            from views.users_view import UsersView
            self.p_users = UsersView(self.db)
            self.stack.addWidget(self.p_users)

        root.addWidget(sb)
        root.addWidget(self.stack)

    def _on_sb(self, btn):
        for i, b in enumerate(self.sb_btns):
            b.set_active(b is btn)
            if b is btn:
                self._switch(i)

    def _switch(self, idx):
        self.stack.setCurrentIndex(idx)
        if 0 <= idx < len(self.sb_btns):
            self.sb_btns[idx].set_active(True)
        refresh_map = {
            0: lambda: self.p_dv.load(),
            1: lambda: self.p_phi.load(),
            2: lambda: self.p_hd.load(),
            3: lambda: self.p_xl.load(),
            4: lambda: self.p_stat.refresh(),
            5: lambda: None,
        }
        if idx in refresh_map:
            refresh_map[idx]()

    def _logout(self):
        r = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc muốn đăng xuất?",
                                 QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            self.close()
            from views.login_view import LoginWindow
            self.login = LoginWindow(self.db)
            self.login.show()
