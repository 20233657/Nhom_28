"""views/dv_view.py - Danh sách & CRUD đoàn viên"""
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox,
    QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QDialog, QScrollArea, QGridLayout, QDateEdit, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QColor, QBrush
from styles import COLORS
from utils import StatCard, SectionTitle


KHOA_LIST = ["Công nghệ thông tin","Kinh tế","Xây dựng","Cơ khí",
             "Điện - Điện tử","Hóa học","Sinh học","Ngoại ngữ","Luật","Y dược"]


class DVForm(QDialog):
    def __init__(self, db, dv=None, parent=None):
        super().__init__(parent)
        self.db=db; self.dv=dv; self.is_edit=dv is not None
        self.setWindowTitle("Sửa đoàn viên" if self.is_edit else "Thêm đoàn viên")
        self.setFixedSize(700,640); self.setModal(True)
        self.setStyleSheet(f"""
            QDialog {{ background:{COLORS['bg_main']}; color:{COLORS['text_primary']}; font-family:'Segoe UI'; }}
            QScrollArea {{ background:transparent; border:none; }}
        """)
        self._build()
        if self.is_edit: self._fill()
        else: self.txt_ma.setText(self.db.get_next_ma())

    def _build(self):
        root=QVBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        # Header
        hdr=QFrame(); hdr.setFixedHeight(60)
        hdr.setStyleSheet(f"""
            QFrame {{ background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {COLORS['primary_dark']},stop:1 {COLORS['primary']});}}
        """)
        hl=QHBoxLayout(hdr); hl.setContentsMargins(20,0,20,0)
        ico=QLabel("✏️" if self.is_edit else "➕")
        ico.setFont(QFont("Segoe UI Emoji",18)); ico.setStyleSheet("background:transparent;color:white;")
        ttl=QLabel("Cập nhật Đoàn viên" if self.is_edit else "Thêm Đoàn viên mới")
        ttl.setFont(QFont("Segoe UI",13,QFont.Bold)); ttl.setStyleSheet("background:transparent;color:white;")
        hl.addWidget(ico); hl.addWidget(ttl); hl.addStretch()
        root.addWidget(hdr)

        # Scroll body
        scroll=QScrollArea(); scroll.setWidgetResizable(True)
        body=QWidget(); body.setStyleSheet(f"background:{COLORS['bg_main']};")
        grid=QGridLayout(body); grid.setContentsMargins(24,20,24,20)
        grid.setHorizontalSpacing(16); grid.setVerticalSpacing(12)
        grid.setColumnStretch(0,1); grid.setColumnStretch(1,1)

        def inp(ph=""): e=QLineEdit(); e.setFixedHeight(38); e.setPlaceholderText(ph); return e
        def cmb(items): c=QComboBox(); c.setFixedHeight(38); c.addItems(items); return c
        def dt(): d=QDateEdit(); d.setFixedHeight(38); d.setCalendarPopup(True); d.setDisplayFormat("dd/MM/yyyy"); return d
        def lbl(t,req=False):
            l=QLabel(t+(" *" if req else ""))
            l.setFont(QFont("Segoe UI",8,QFont.Bold))
            l.setStyleSheet(f"color:{COLORS['text_muted']};letter-spacing:0.8px;")
            return l

        self.txt_ma=inp("VD: DV016")
        self.txt_ten=inp("Họ và tên đầy đủ")
        self.dt_sinh=dt(); self.dt_sinh.setDate(QDate(2002,1,1))
        self.cmb_gt=cmb(["Nam","Nữ","Khác"])
        self.txt_lop=inp("VD: CNTT01")
        self.cmb_khoa=QComboBox(); self.cmb_khoa.setFixedHeight(38)
        self.cmb_khoa.setEditable(True); self.cmb_khoa.addItems(KHOA_LIST)
        self.txt_email=inp("email@example.com")
        self.txt_phone=inp("0901234567")
        self.dt_vao=dt(); self.dt_vao.setDate(QDate.currentDate())
        self.cmb_tt=cmb(["Đang sinh hoạt","Đã rời"])
        self.txt_note=QTextEdit(); self.txt_note.setFixedHeight(70)
        self.txt_note.setPlaceholderText("Ghi chú thêm...")

        if self.is_edit:
            self.txt_ma.setReadOnly(True)
            self.txt_ma.setStyleSheet(f"QLineEdit{{background:{COLORS['text_muted']};color:#222;border-radius:7px;padding:7px 12px;}}")

        rows_l=[(lbl("Mã Đoàn viên",True),self.txt_ma),(lbl("Ngày sinh"),self.dt_sinh),
                (lbl("Lớp",True),self.txt_lop),(lbl("Email"),self.txt_email),
                (lbl("Ngày vào đoàn"),self.dt_vao)]
        rows_r=[(lbl("Họ và tên",True),self.txt_ten),(lbl("Giới tính"),self.cmb_gt),
                (lbl("Khoa",True),self.cmb_khoa),(lbl("Số điện thoại"),self.txt_phone),
                (lbl("Trạng thái"),self.cmb_tt)]
        for i,(l,w) in enumerate(rows_l):
            box=QVBoxLayout(); box.setSpacing(4); box.addWidget(l); box.addWidget(w)
            grid.addLayout(box,i,0)
        for i,(l,w) in enumerate(rows_r):
            box=QVBoxLayout(); box.setSpacing(4); box.addWidget(l); box.addWidget(w)
            grid.addLayout(box,i,1)
        nb=QVBoxLayout(); nb.setSpacing(4)
        nb.addWidget(lbl("Ghi chú")); nb.addWidget(self.txt_note)
        grid.addLayout(nb,5,0,1,2)
        scroll.setWidget(body); root.addWidget(scroll)

        # Footer
        ftr=QFrame(); ftr.setFixedHeight(62)
        ftr.setStyleSheet(f"background:{COLORS['bg_card']};border-top:1px solid {COLORS['border']};")
        fl=QHBoxLayout(ftr); fl.setContentsMargins(24,0,24,0); fl.setSpacing(12)
        self.lbl_err=QLabel(""); self.lbl_err.setStyleSheet(f"color:{COLORS['primary_light']};")
        btn_c=QPushButton("Hủy"); btn_c.setFixedSize(100,38); btn_c.setObjectName("btn_secondary")
        btn_c.setCursor(Qt.PointingHandCursor); btn_c.clicked.connect(self.reject)
        btn_s=QPushButton("💾  Lưu lại"); btn_s.setFixedSize(130,38); btn_s.setObjectName("btn_success")
        btn_s.setCursor(Qt.PointingHandCursor); btn_s.clicked.connect(self._save)
        fl.addWidget(self.lbl_err); fl.addStretch(); fl.addWidget(btn_c); fl.addWidget(btn_s)
        root.addWidget(ftr)

    def _fill(self):
        dv=self.dv
        self.txt_ma.setText(dv.get("ma_dv",""))
        self.txt_ten.setText(dv.get("ho_ten",""))
        ns=dv.get("ngay_sinh","")
        if ns:
            try: p=ns.split("-"); self.dt_sinh.setDate(QDate(int(p[0]),int(p[1]),int(p[2])))
            except: pass
        i=self.cmb_gt.findText(dv.get("gioi_tinh","Nam"))
        if i>=0: self.cmb_gt.setCurrentIndex(i)
        self.txt_lop.setText(dv.get("lop",""))
        self.cmb_khoa.setCurrentText(dv.get("khoa",""))
        self.txt_email.setText(dv.get("email",""))
        self.txt_phone.setText(dv.get("so_dien_thoai",""))
        vd=dv.get("ngay_vao_doan","")
        if vd:
            try: p=vd.split("-"); self.dt_vao.setDate(QDate(int(p[0]),int(p[1]),int(p[2])))
            except: pass
        i2=self.cmb_tt.findText(dv.get("trang_thai","Đang sinh hoạt"))
        if i2>=0: self.cmb_tt.setCurrentIndex(i2)
        self.txt_note.setPlainText(dv.get("ghi_chu",""))

    def _collect(self):
        return {
            "ma_dv": self.txt_ma.text().strip(),
            "ho_ten": self.txt_ten.text().strip(),
            "ngay_sinh": self.dt_sinh.date().toString("yyyy-MM-dd"),
            "gioi_tinh": self.cmb_gt.currentText(),
            "lop": self.txt_lop.text().strip(),
            "khoa": self.cmb_khoa.currentText().strip(),
            "email": self.txt_email.text().strip(),
            "so_dien_thoai": self.txt_phone.text().strip(),
            "ngay_vao_doan": self.dt_vao.date().toString("yyyy-MM-dd"),
            "trang_thai": self.cmb_tt.currentText(),
            "ghi_chu": self.txt_note.toPlainText().strip(),
        }

    def _save(self):
        d=self._collect()
        if not d["ma_dv"] or not re.match(r'^DV\d{3,}$',d["ma_dv"]):
            self.lbl_err.setText("⚠  Mã ĐV phải có dạng DVxxx"); return
        if not d["ho_ten"] or len(d["ho_ten"])<3:
            self.lbl_err.setText("⚠  Họ tên tối thiểu 3 ký tự"); return
        if not d["lop"]: self.lbl_err.setText("⚠  Chưa nhập lớp"); return
        if not d["khoa"]: self.lbl_err.setText("⚠  Chưa chọn khoa"); return
        email=d.get("email","")
        if email and not re.match(r'^[\w\.\+\-]+@[\w]+\.[a-z]{2,}$',email):
            self.lbl_err.setText("⚠  Email không hợp lệ"); return
        if self.is_edit:
            ok,msg=self.db.update_dv(self.dv["ma_dv"],d)
        else:
            ok,msg=self.db.add_dv(d)
        if ok: QMessageBox.information(self,"Thành công",msg); self.accept()
        else: self.lbl_err.setText(f"⚠  {msg}")


class DVView(QWidget):
    COLS=["Mã ĐV","Họ tên","Ngày sinh","Giới tính","Lớp","Khoa","Email","Số ĐT","Vào đoàn","Trạng thái"]
    KEYS=["ma_dv","ho_ten","ngay_sinh","gioi_tinh","lop","khoa","email","so_dien_thoai","ngay_vao_doan","trang_thai"]

    def __init__(self, db, user):
        super().__init__()
        self.db=db; self.user=user; self.is_admin=user['role']=='admin'
        self._timer=QTimer(); self._timer.setSingleShot(True); self._timer.timeout.connect(self.load)
        self._build(); self.load()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("📋  Danh sách Đoàn viên"))

        # Stat cards
        cr=QHBoxLayout(); cr.setSpacing(12)
        self.c_total =StatCard("👥","Tổng đoàn viên","0",COLORS['accent'])
        self.c_active=StatCard("✅","Đang sinh hoạt","0",COLORS['success'])
        self.c_left  =StatCard("🔴","Đã rời","0",COLORS['danger'])
        self.c_khoa  =StatCard("🏫","Số khoa","0",COLORS['warning'])
        for c in [self.c_total,self.c_active,self.c_left,self.c_khoa]: cr.addWidget(c)
        lay.addLayout(cr)

        # Toolbar
        tb=QHBoxLayout(); tb.setSpacing(10)
        self.txt_search=QLineEdit(); self.txt_search.setPlaceholderText("🔍  Tìm kiếm realtime...")
        self.txt_search.setFixedHeight(40); self.txt_search.setMinimumWidth(260)
        self.txt_search.textChanged.connect(lambda _: self._timer.start(280))

        self.cmb_field=QComboBox(); self.cmb_field.setFixedHeight(40)
        self.cmb_field.addItems(["Họ tên","Mã ĐV","Lớp","Khoa"])
        self.cmb_field.currentIndexChanged.connect(lambda _: self._timer.start(100))

        btn_ref=QPushButton("🔄  Làm mới"); btn_ref.setFixedHeight(40)
        btn_ref.setObjectName("btn_secondary"); btn_ref.setCursor(Qt.PointingHandCursor)
        btn_ref.clicked.connect(lambda: (self.txt_search.clear(), self.load()))

        btn_add=QPushButton("➕  Thêm"); btn_add.setFixedHeight(40)
        btn_add.setObjectName("btn_success"); btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._add)

        btn_edit=QPushButton("✏️  Sửa"); btn_edit.setFixedHeight(40)
        btn_edit.setCursor(Qt.PointingHandCursor); btn_edit.clicked.connect(self._edit)

        btn_del=QPushButton("🗑️  Xóa"); btn_del.setFixedHeight(40)
        btn_del.setObjectName("btn_danger"); btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.clicked.connect(self._delete); btn_del.setEnabled(self.is_admin)

        for w in [self.txt_search,self.cmb_field,btn_ref]: tb.addWidget(w)
        tb.addStretch()
        for w in [btn_add,btn_edit,btn_del]: tb.addWidget(w)
        lay.addLayout(tb)

        # Table
        self.table=QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.table.doubleClicked.connect(self._edit)
        lay.addWidget(self.table)

        self.lbl_status=QLabel("Sẵn sàng")
        self.lbl_status.setStyleSheet(f"color:{COLORS['text_muted']};font-size:9pt;")
        lay.addWidget(self.lbl_status)

    def load(self):
        fm={"Họ tên":"ho_ten","Mã ĐV":"ma_dv","Lớp":"lop","Khoa":"khoa"}
        rows=self.db.get_all_dv(self.txt_search.text().strip(),
                                fm.get(self.cmb_field.currentText(),"ho_ten"))
        self.table.setRowCount(len(rows))
        for r,dv in enumerate(rows):
            for c,k in enumerate(self.KEYS):
                val=str(dv.get(k,"") or "")
                item=QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if k=="trang_thai":
                    clr=COLORS['success'] if val=="Đang sinh hoạt" else COLORS['danger']
                    item.setForeground(QBrush(QColor(clr)))
                    item.setFont(QFont("Segoe UI",9,QFont.Bold))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(1,180)
        s=self.db.get_stats()
        self.c_total.set_value(s['total']); self.c_active.set_value(s['active'])
        self.c_left.set_value(s['left']); self.c_khoa.set_value(s['khoa'])
        self.lbl_status.setText(f"Hiển thị {len(rows)} đoàn viên")

    def _sel_ma(self):
        r=self.table.currentRow()
        return self.table.item(r,0).text() if r>=0 else ""

    def _add(self):
        if DVForm(self.db,parent=self).exec_(): self.load()

    def _edit(self):
        ma=self._sel_ma()
        if not ma: QMessageBox.warning(self,"","Vui lòng chọn một dòng."); return
        dv=self.db.get_dv_by_ma(ma)
        if dv and DVForm(self.db,dv,self).exec_(): self.load()

    def _delete(self):
        ma=self._sel_ma()
        if not ma: QMessageBox.warning(self,"","Vui lòng chọn một dòng."); return
        dv=self.db.get_dv_by_ma(ma)
        r=QMessageBox.question(self,"Xác nhận xóa",
            f"Xóa đoàn viên:\n  Mã: {ma}\n  Tên: {dv['ho_ten'] if dv else ''}\n\nKhông thể hoàn tác!",
            QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if r==QMessageBox.Yes:
            self.db.delete_dv(ma)
            QMessageBox.information(self,"OK","Xóa thành công!")
            self.load()
