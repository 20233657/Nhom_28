"""
=============================================================
HỆ THỐNG QUẢN LÝ ĐOÀN VIÊN - TRƯỜNG ĐẠI HỌC
Đoàn TNCS Hồ Chí Minh
Phiên bản: 2.0  |  Chạy: python main.py
Yêu cầu:  pip install PyQt5 matplotlib openpyxl
=============================================================
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import Database
from views.login_view import LoginWindow


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("Quản lý Đoàn viên")
    app.setOrganizationName("Đoàn TNCS HCM")
    app.setFont(QFont("Segoe UI", 10))

    db = Database()
    db.initialize()

    win = LoginWindow(db)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
