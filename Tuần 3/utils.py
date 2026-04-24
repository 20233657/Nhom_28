"""
utils.py - Các widget dùng chung toàn ứng dụng
"""
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen, QPolygon
from PyQt5.QtCore import QPoint
from styles import COLORS


class StatCard(QFrame):
    """Card thống kê có icon, số, tiêu đề và màu accent - nền sáng, sạch"""
    def __init__(self, icon, title, value="0", color=None, parent=None):
        super().__init__(parent)
        color = color or COLORS['accent']
        self.setMinimumHeight(90)
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-left: 4px solid {color};
                border-radius: 10px;
            }}
            QFrame:hover {{
                border: 1px solid {color};
                border-left: 4px solid {color};
                background: #FAFAFA;
            }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)

        # Icon box
        ico_box = QFrame()
        ico_box.setFixedSize(50, 50)
        ico_box.setStyleSheet(f"""
            QFrame {{
                background: {color}18;
                border: 1.5px solid {color}55;
                border-radius: 12px;
            }}
        """)
        ico_lay = QVBoxLayout(ico_box)
        ico_lay.setContentsMargins(0, 0, 0, 0)
        ico_lbl = QLabel(icon)
        ico_lbl.setFont(QFont("Segoe UI Emoji", 20))
        ico_lbl.setAlignment(Qt.AlignCenter)
        ico_lbl.setStyleSheet("background:transparent; border:none;")
        ico_lay.addWidget(ico_lbl)

        # Text
        txt = QVBoxLayout()
        txt.setSpacing(2)
        self.val_lbl = QLabel(str(value))
        self.val_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.val_lbl.setStyleSheet(f"color:{color}; background:transparent; border:none;")

        ttl_lbl = QLabel(title)
        ttl_lbl.setFont(QFont("Segoe UI", 9))
        ttl_lbl.setStyleSheet(f"color:{COLORS['text_secondary']}; background:transparent; border:none;")
        txt.addWidget(self.val_lbl)
        txt.addWidget(ttl_lbl)

        lay.addWidget(ico_box)
        lay.addSpacing(14)
        lay.addLayout(txt)
        lay.addStretch()

    def set_value(self, v):
        self.val_lbl.setText(str(v))


class SectionTitle(QLabel):
    """Tiêu đề section - chữ đậm, không có ô border bao quanh"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.setContentsMargins(0, 0, 0, 8)
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                background: transparent;
                border: none;
                padding-bottom: 8px;
            }}
        """)


class LogoWidget(QWidget):
    """Logo Đoàn TNCS HCM vẽ bằng QPainter"""
    def __init__(self, size=48, parent=None):
        super().__init__(parent)
        self.logo_size = size
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        sz = self.logo_size
        cx, cy = sz // 2, sz // 2
        r = sz // 2 - 2

        # Vẽ nền tròn đỏ
        grad = QLinearGradient(0, 0, sz, sz)
        grad.setColorAt(0, QColor(COLORS['primary_light']))
        grad.setColorAt(1, QColor(COLORS['primary_dark']))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(QColor(COLORS['accent']), 2))
        p.drawEllipse(2, 2, sz-4, sz-4)

        # Vẽ ngôi sao 5 cánh màu vàng
        import math
        p.setBrush(QBrush(QColor(COLORS['accent'])))
        p.setPen(Qt.NoPen)
        star_r_outer = r * 0.6
        star_r_inner = r * 0.26
        points = []
        for i in range(10):
            angle = math.radians(-90 + i * 36)
            rr = star_r_outer if i % 2 == 0 else star_r_inner
            x = int(cx + rr * math.cos(angle))
            y = int(cy + rr * math.sin(angle))
            points.append(QPoint(x, y))
        p.drawPolygon(QPolygon(points))
        p.end()
