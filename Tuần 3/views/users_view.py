"""views/users_view.py - Quản lý tài khoản (Admin only)"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QDialog,
    QLineEdit, QComboBox, QMessageBox, QHeaderView,
    QAbstractItemView, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush
from styles import COLORS
from utils import SectionTitle


class AddUserDlg(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent); self.db=db
        self.setWindowTitle("Thêm tài khoản"); self.setFixedSize(400,300); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,20,24,16); lay.setSpacing(12)
        ttl=QLabel("👤  Tạo tài khoản mới"); ttl.setFont(QFont("Segoe UI",12,QFont.Bold))
        ttl.setStyleSheet(f"color:{COLORS['accent']};"); lay.addWidget(ttl)
        grid=QGridLayout(); grid.setSpacing(10)
        def lbl(t): l=QLabel(t); l.setStyleSheet(f"color:{COLORS['text_secondary']};"); return l
        self.txt_u=QLineEdit(); self.txt_u.setFixedHeight(36)
        self.txt_f=QLineEdit(); self.txt_f.setFixedHeight(36)
        self.txt_p=QLineEdit(); self.txt_p.setFixedHeight(36); self.txt_p.setEchoMode(QLineEdit.Password); self.txt_p.setPlaceholderText("Tối thiểu 6 ký tự")
        self.cmb_r=QComboBox(); self.cmb_r.setFixedHeight(36); self.cmb_r.addItems(["user","admin"])
        grid.addWidget(lbl("Tên đăng nhập:"),0,0); grid.addWidget(self.txt_u,0,1)
        grid.addWidget(lbl("Họ tên:"),1,0); grid.addWidget(self.txt_f,1,1)
        grid.addWidget(lbl("Mật khẩu:"),2,0); grid.addWidget(self.txt_p,2,1)
        grid.addWidget(lbl("Quyền:"),3,0); grid.addWidget(self.cmb_r,3,1)
        lay.addLayout(grid)
        self.lbl_e=QLabel(""); self.lbl_e.setStyleSheet(f"color:{COLORS['danger']};"); lay.addWidget(self.lbl_e)
        lay.addStretch()
        bts=QHBoxLayout()
        bc=QPushButton("Hủy"); bc.setObjectName("btn_secondary"); bc.setFixedHeight(36); bc.setCursor(Qt.PointingHandCursor); bc.clicked.connect(self.reject)
        bs=QPushButton("💾  Lưu"); bs.setObjectName("btn_success"); bs.setFixedHeight(36); bs.setCursor(Qt.PointingHandCursor); bs.clicked.connect(self._save)
        bts.addStretch(); bts.addWidget(bc); bts.addWidget(bs); lay.addLayout(bts)

    def _save(self):
        u=self.txt_u.text().strip(); f=self.txt_f.text().strip(); p=self.txt_p.text()
        if not u or not f or not p: self.lbl_e.setText("⚠  Điền đầy đủ thông tin!"); return
        if len(p)<6: self.lbl_e.setText("⚠  Mật khẩu tối thiểu 6 ký tự!"); return
        ok,msg=self.db.add_user(u,p,self.cmb_r.currentText(),f)
        if ok: QMessageBox.information(self,"OK",msg); self.accept()
        else: self.lbl_e.setText(f"⚠  {msg}")


class UsersView(QWidget):
    def __init__(self, db):
        super().__init__(); self.db=db; self._build(); self._load()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("⚙️  Quản lý Tài khoản"))
        note=QLabel("⚠  Không thể xóa tài khoản 'admin' gốc. Mật khẩu mã hóa SHA-256.")
        note.setStyleSheet(f"color:{COLORS['warning']};font-style:italic;font-size:10pt;")
        lay.addWidget(note)
        tb=QHBoxLayout()
        btn_add=QPushButton("➕  Thêm tài khoản"); btn_add.setFixedHeight(38)
        btn_add.setObjectName("btn_success"); btn_add.setCursor(Qt.PointingHandCursor); btn_add.clicked.connect(self._add)
        btn_del=QPushButton("🗑️  Xóa"); btn_del.setFixedHeight(38)
        btn_del.setObjectName("btn_danger"); btn_del.setCursor(Qt.PointingHandCursor); btn_del.clicked.connect(self._del)
        tb.addStretch(); tb.addWidget(btn_add); tb.addWidget(btn_del)
        lay.addLayout(tb)
        self.table=QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Tên đăng nhập","Họ tên","Quyền","Ngày tạo"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        lay.addWidget(self.table)

    def _load(self):
        users=self.db.get_all_users(); self.table.setRowCount(len(users))
        for r,u in enumerate(users):
            for c,val in enumerate([u['id'],u['username'],u['full_name'],u['role'],u['created_at']]):
                item=QTableWidgetItem(str(val) if val else "")
                item.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if c==3:
                    clr=COLORS['accent'] if val=='admin' else COLORS['success']
                    item.setForeground(QBrush(QColor(clr))); item.setFont(QFont("Segoe UI",9,QFont.Bold))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()

    def _add(self):
        if AddUserDlg(self.db,self).exec_(): self._load()

    def _del(self):
        r=self.table.currentRow()
        if r<0: QMessageBox.warning(self,"","Chọn tài khoản để xóa."); return
        uname=self.table.item(r,1).text()
        if uname=='admin': QMessageBox.critical(self,"","Không thể xóa tài khoản admin gốc!"); return
        if QMessageBox.question(self,"Xác nhận",f"Xóa tài khoản '{uname}'?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            self.db.delete_user(int(self.table.item(r,0).text())); self._load()
