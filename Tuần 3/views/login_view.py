"""views/login_view.py - Màn hình đăng nhập sạch, không ô border thừa"""
import math
from PyQt5.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QLinearGradient, QBrush,
    QPen, QPolygon, QRadialGradient
)
from styles import COLORS


class LoginWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Đăng nhập - Quản lý Đoàn viên")
        self.setFixedSize(920, 580)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._build()
        self._center()

    def _center(self):
        from PyQt5.QtWidgets import QDesktopWidget
        sc = QDesktopWidget().screenGeometry()
        self.move((sc.width()-self.width())//2, (sc.height()-self.height())//2)

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Container chính
        container = QFrame()
        container.setObjectName("loginContainer")
        container.setStyleSheet("""
            QFrame#loginContainer {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: none;
            }
        """)
        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(60)
        sh.setColor(QColor(0, 0, 0, 160))
        sh.setOffset(0, 12)
        container.setGraphicsEffect(sh)

        main = QHBoxLayout(container)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── CỘT TRÁI: Banner đỏ ───────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(390)
        left.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0.3, y2:1,
                    stop:0 #6A0000,
                    stop:0.4 #C62828,
                    stop:1 #3A0000);
                border-radius: 20px 0 0 20px;
            }
            QLabel {
                background: transparent;
                border: none;
                color: white;
            }
        """)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(32, 36, 32, 28)
        ll.setSpacing(0)
        ll.setAlignment(Qt.AlignCenter)

        # Logo ngôi sao
        star = _StarWidget(96)
        ll.addStretch(1)
        ll.addWidget(star, 0, Qt.AlignHCenter)
        ll.addSpacing(20)

        # Tên tổ chức - KHÔNG có border, KHÔNG có ô bao quanh
        lbl_org = QLabel("ĐOÀN TNCS HỒ CHÍ MINH")
        lbl_org.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl_org.setAlignment(Qt.AlignCenter)
        lbl_org.setStyleSheet("color: #FFD54F; background: transparent; border: none; letter-spacing: 1px;")
        ll.addWidget(lbl_org)

        ll.addSpacing(12)

        # Dải vàng mỏng (dùng QFrame trực tiếp, không phải QLabel)
        bar = QFrame()
        bar.setFixedSize(60, 2)
        bar.setStyleSheet("background: #F9A825; border: none;")
        ll.addWidget(bar, 0, Qt.AlignHCenter)

        ll.addSpacing(14)

        # Tiêu đề hệ thống - 2 dòng, không có ô
        lbl_sys = QLabel("HỆ THỐNG QUẢN LÝ")
        lbl_sys.setFont(QFont("Segoe UI", 15, QFont.Bold))
        lbl_sys.setAlignment(Qt.AlignCenter)
        lbl_sys.setStyleSheet("color: white; background: transparent; border: none;")
        ll.addWidget(lbl_sys)

        lbl_dv = QLabel("ĐOÀN VIÊN")
        lbl_dv.setFont(QFont("Segoe UI", 17, QFont.Bold))
        lbl_dv.setAlignment(Qt.AlignCenter)
        lbl_dv.setStyleSheet("color: #FFD54F; background: transparent; border: none; letter-spacing: 2px;")
        ll.addWidget(lbl_dv)

        ll.addSpacing(10)

        lbl_school = QLabel("TRƯỜNG ĐẠI HỌC")
        lbl_school.setFont(QFont("Segoe UI", 9))
        lbl_school.setAlignment(Qt.AlignCenter)
        lbl_school.setStyleSheet("color: rgba(255,255,255,0.6); background: transparent; border: none; letter-spacing: 2px;")
        ll.addWidget(lbl_school)

        ll.addStretch(2)

        # Gợi ý tài khoản - nền hộp nhỏ bo góc
        hint_box = QWidget()
        hint_box.setStyleSheet("""
            QWidget {
                background: rgba(0,0,0,0.25);
                border-radius: 10px;
                border: none;
            }
            QLabel {
                background: transparent;
                border: none;
                color: #FFD54F;
            }
        """)
        hint_lay = QVBoxLayout(hint_box)
        hint_lay.setContentsMargins(14, 10, 14, 10)
        hint_lay.setSpacing(4)
        h1 = QLabel("🔑  admin / admin123")
        h1.setFont(QFont("Segoe UI", 9))
        h2 = QLabel("👤  user / user123")
        h2.setFont(QFont("Segoe UI", 9))
        hint_lay.addWidget(h1)
        hint_lay.addWidget(h2)
        ll.addWidget(hint_box)

        # ── CỘT PHẢI: Form đăng nhập ─────────────────────────────────────
        right = QWidget()
        right.setStyleSheet("""
            QWidget { background: transparent; border: none; }
            QLabel  { background: transparent; border: none; }
        """)
        rl = QVBoxLayout(right)
        rl.setContentsMargins(52, 36, 52, 36)
        rl.setSpacing(0)

        # Nút đóng
        row_close = QHBoxLayout()
        row_close.addStretch()
        btn_x = QPushButton("✕")
        btn_x.setFixedSize(34, 34)
        btn_x.setCursor(Qt.PointingHandCursor)
        btn_x.setStyleSheet(f"""
            QPushButton {{
                background: #F0F0F4;
                color: {COLORS['text_secondary']};
                border: none;
                border-radius: 17px;
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {COLORS['primary']};
                color: white;
            }}
        """)
        btn_x.clicked.connect(self.close)
        row_close.addWidget(btn_x)
        rl.addLayout(row_close)
        rl.addSpacing(8)

        # Tiêu đề form
        lbl_hi = QLabel("Chào mừng!")
        lbl_hi.setFont(QFont("Segoe UI", 26, QFont.Bold))
        lbl_hi.setStyleSheet(f"color: {COLORS['text_primary']}; background: transparent; border: none;")
        rl.addWidget(lbl_hi)

        lbl_sub = QLabel("Đăng nhập để tiếp tục quản lý")
        lbl_sub.setFont(QFont("Segoe UI", 10))
        lbl_sub.setStyleSheet(f"color: {COLORS['text_secondary']}; background: transparent; border: none;")
        rl.addWidget(lbl_sub)
        rl.addSpacing(28)

        # Tên đăng nhập
        lbl_u = QLabel("TÊN ĐĂNG NHẬP")
        lbl_u.setFont(QFont("Segoe UI", 8, QFont.Bold))
        lbl_u.setStyleSheet(f"color: {COLORS['text_muted']}; background: transparent; border: none; letter-spacing: 1px;")
        rl.addWidget(lbl_u)
        rl.addSpacing(6)

        self.txt_user = QLineEdit()
        self.txt_user.setFixedHeight(48)
        self.txt_user.setPlaceholderText("Nhập tên đăng nhập...")
        self.txt_user.setText("admin")
        self.txt_user.setFont(QFont("Segoe UI", 11))
        self.txt_user.setStyleSheet(f"""
            QLineEdit {{
                background: #F8F9FA;
                color: {COLORS['text_primary']};
                border: 1.5px solid {COLORS['border_dark']};
                border-radius: 10px;
                padding: 0 14px;
                font-size: 11pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
                background: white;
            }}
        """)
        rl.addWidget(self.txt_user)
        rl.addSpacing(16)

        # Mật khẩu
        lbl_p = QLabel("MẬT KHẨU")
        lbl_p.setFont(QFont("Segoe UI", 8, QFont.Bold))
        lbl_p.setStyleSheet(f"color: {COLORS['text_muted']}; background: transparent; border: none; letter-spacing: 1px;")
        rl.addWidget(lbl_p)
        rl.addSpacing(6)

        self.txt_pass = QLineEdit()
        self.txt_pass.setFixedHeight(48)
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setPlaceholderText("Nhập mật khẩu...")
        self.txt_pass.setText("admin123")
        self.txt_pass.setFont(QFont("Segoe UI", 11))
        self.txt_pass.setStyleSheet(self.txt_user.styleSheet())
        self.txt_pass.returnPressed.connect(self._login)
        rl.addWidget(self.txt_pass)
        rl.addSpacing(8)

        # Label lỗi
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color: {COLORS['primary']}; font-size: 10pt; background: transparent; border: none;")
        self.lbl_err.setAlignment(Qt.AlignCenter)
        rl.addWidget(self.lbl_err)
        rl.addSpacing(16)

        # Nút đăng nhập
        btn_login = QPushButton("ĐĂNG NHẬP")
        btn_login.setFixedHeight(52)
        btn_login.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 12pt;
                font-weight: 700;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background: {COLORS['primary_light']};
            }}
            QPushButton:pressed {{
                background: {COLORS['primary_dark']};
            }}
        """)
        btn_login.clicked.connect(self._login)
        rl.addWidget(btn_login)
        rl.addStretch()

        main.addWidget(left)
        main.addWidget(right)
        outer.addWidget(container)

    def _login(self):
        u = self.txt_user.text().strip()
        p = self.txt_pass.text()
        if not u or not p:
            self.lbl_err.setText("⚠  Vui lòng nhập đầy đủ!")
            return
        user = self.db.verify_login(u, p)
        if user:
            self.accept()
            from views.main_window import MainWindow
            self.mw = MainWindow(self.db, user)
            self.mw.show()
        else:
            self.lbl_err.setText("❌  Sai tên đăng nhập hoặc mật khẩu!")
            self.txt_pass.clear()
            self.txt_pass.setFocus()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._dp = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and hasattr(self, '_dp'):
            self.move(e.globalPos() - self._dp)


class _StarWidget(QWidget):
    """Logo ngôi sao vàng trên nền đỏ - vẽ bằng QPainter, không có border ô"""
    def __init__(self, size=96, parent=None):
        super().__init__(parent)
        self.sz = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        sz = self.sz
        cx, cy = sz // 2, sz // 2
        r = sz // 2 - 4

        # Vòng tròn nền vàng (viền ngoài)
        p.setBrush(QBrush(QColor("#F9A825")))
        p.setPen(Qt.NoPen)
        p.drawEllipse(0, 0, sz, sz)

        # Vòng tròn đỏ bên trong
        g = QRadialGradient(cx, cy, r - 4)
        g.setColorAt(0, QColor("#E53935"))
        g.setColorAt(1, QColor("#7B0000"))
        p.setBrush(QBrush(g))
        p.setPen(Qt.NoPen)
        p.drawEllipse(5, 5, sz - 10, sz - 10)

        # Ngôi sao vàng
        p.setBrush(QBrush(QColor("#F9A825")))
        p.setPen(Qt.NoPen)
        outer = r * 0.60
        inner = r * 0.26
        pts = []
        for i in range(10):
            angle = math.radians(-90 + i * 36)
            rr = outer if i % 2 == 0 else inner
            pts.append(QPoint(int(cx + rr * math.cos(angle)), int(cy + rr * math.sin(angle))))
        p.drawPolygon(QPolygon(pts))
        p.end()
