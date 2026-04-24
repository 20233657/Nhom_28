"""views/doan_phi_view.py - Quản lý đoàn phí"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox,
    QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QDialog, QGridLayout, QCheckBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QColor, QBrush
from styles import COLORS
from utils import StatCard, SectionTitle


class TaoPhiDialog(QDialog):
    """Dialog tạo đoàn phí hàng loạt"""
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db=db
        self.setWindowTitle("Tạo đoàn phí học kỳ")
        self.setFixedSize(420,280); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,24,28,20); lay.setSpacing(14)
        ttl=QLabel("📋  Tạo đoàn phí hàng loạt")
        ttl.setFont(QFont("Segoe UI",13,QFont.Bold))
        ttl.setStyleSheet(f"color:{COLORS['accent']};")
        lay.addWidget(ttl)
        info=QLabel("Tự động tạo bản ghi đoàn phí cho TẤT CẢ\nđoàn viên đang sinh hoạt trong học kỳ này.")
        info.setStyleSheet(f"color:{COLORS['text_secondary']};font-size:10pt;")
        lay.addWidget(info)

        grid=QGridLayout(); grid.setSpacing(10)
        def lbl(t):
            l=QLabel(t); l.setStyleSheet(f"color:{COLORS['text_secondary']};"); return l
        self.cmb_hk=QComboBox(); self.cmb_hk.setFixedHeight(38)
        self.cmb_hk.addItems(["HK1","HK2","HK3"])
        self.cmb_nh=QComboBox(); self.cmb_nh.setFixedHeight(38)
        self.cmb_nh.addItems(["2023-2024","2024-2025","2025-2026"])
        self.cmb_nh.setCurrentIndex(1)
        self.spn_tien=QDoubleSpinBox(); self.spn_tien.setFixedHeight(38)
        self.spn_tien.setRange(0,1000000); self.spn_tien.setValue(30000)
        self.spn_tien.setSuffix(" VNĐ"); self.spn_tien.setSingleStep(5000)
        grid.addWidget(lbl("Học kỳ:"),0,0); grid.addWidget(self.cmb_hk,0,1)
        grid.addWidget(lbl("Năm học:"),1,0); grid.addWidget(self.cmb_nh,1,1)
        grid.addWidget(lbl("Số tiền:"),2,0); grid.addWidget(self.spn_tien,2,1)
        lay.addLayout(grid)

        self.lbl_err=QLabel(""); self.lbl_err.setStyleSheet(f"color:{COLORS['danger']};")
        lay.addWidget(self.lbl_err)

        btns=QHBoxLayout()
        bc=QPushButton("Hủy"); bc.setObjectName("btn_secondary"); bc.setCursor(Qt.PointingHandCursor)
        bc.setFixedHeight(38); bc.clicked.connect(self.reject)
        bs=QPushButton("✅  Tạo"); bs.setObjectName("btn_success"); bs.setCursor(Qt.PointingHandCursor)
        bs.setFixedHeight(38); bs.clicked.connect(self._create)
        btns.addStretch(); btns.addWidget(bc); btns.addWidget(bs)
        lay.addLayout(btns)

    def _create(self):
        ok,msg=self.db.add_doan_phi_bulk(
            self.cmb_hk.currentText(),
            self.cmb_nh.currentText(),
            self.spn_tien.value()
        )
        if ok: QMessageBox.information(self,"Thành công",msg); self.accept()
        else: self.lbl_err.setText(msg)


class NopPhiDialog(QDialog):
    def __init__(self, row_data, db, parent=None):
        super().__init__(parent)
        self.d=row_data; self.db=db
        self.setWindowTitle("Cập nhật đóng đoàn phí")
        self.setFixedSize(380,240); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,20,24,16); lay.setSpacing(12)
        ttl=QLabel(f"💰  {self.d['ho_ten']} - {self.d['hoc_ky']}/{self.d['nam_hoc']}")
        ttl.setFont(QFont("Segoe UI",11,QFont.Bold))
        ttl.setStyleSheet(f"color:{COLORS['accent']};")
        lay.addWidget(ttl)

        grid=QGridLayout(); grid.setSpacing(10)
        def lbl(t): l=QLabel(t); l.setStyleSheet(f"color:{COLORS['text_secondary']};"); return l

        self.chk=QCheckBox("Đã nộp đoàn phí")
        self.chk.setChecked(bool(self.d.get('da_nop',0)))
        self.chk.setStyleSheet(f"color:{COLORS['text_primary']};font-size:11pt;")

        from PyQt5.QtWidgets import QDateEdit
        self.dt=QDateEdit(); self.dt.setCalendarPopup(True)
        self.dt.setDisplayFormat("dd/MM/yyyy"); self.dt.setFixedHeight(38)
        np=self.d.get('ngay_nop','')
        if np:
            try: p=np.split('-'); self.dt.setDate(__import__('PyQt5.QtCore',fromlist=['QDate']).QDate(int(p[0]),int(p[1]),int(p[2])))
            except: self.dt.setDate(QDate.currentDate())
        else: self.dt.setDate(QDate.currentDate())

        self.txt_note=QLineEdit(); self.txt_note.setFixedHeight(38)
        self.txt_note.setText(self.d.get('ghi_chu','') or '')
        self.txt_note.setPlaceholderText("Ghi chú...")

        grid.addWidget(self.chk,0,0,1,2)
        grid.addWidget(lbl("Ngày nộp:"),1,0); grid.addWidget(self.dt,1,1)
        grid.addWidget(lbl("Ghi chú:"),2,0); grid.addWidget(self.txt_note,2,1)
        lay.addLayout(grid); lay.addStretch()

        btns=QHBoxLayout()
        bc=QPushButton("Hủy"); bc.setObjectName("btn_secondary"); bc.setCursor(Qt.PointingHandCursor)
        bc.setFixedHeight(36); bc.clicked.connect(self.reject)
        bs=QPushButton("💾  Lưu"); bs.setObjectName("btn_success"); bs.setCursor(Qt.PointingHandCursor)
        bs.setFixedHeight(36); bs.clicked.connect(self._save)
        btns.addStretch(); btns.addWidget(bc); btns.addWidget(bs)
        lay.addLayout(btns)

    def _save(self):
        da_nop=1 if self.chk.isChecked() else 0
        ngay=self.dt.date().toString("yyyy-MM-dd") if da_nop else None
        self.db.update_doan_phi(self.d['id'],da_nop,ngay,self.txt_note.text())
        self.accept()


class DoanPhiView(QWidget):
    COLS=["ID","Mã ĐV","Họ tên","Lớp","Khoa","Học kỳ","Năm học","Số tiền","Đã nộp","Ngày nộp","Ghi chú"]
    KEYS=["id","ma_dv","ho_ten","lop","khoa","hoc_ky","nam_hoc","so_tien","da_nop","ngay_nop","ghi_chu"]

    def __init__(self, db, user):
        super().__init__()
        self.db=db; self.user=user
        self._timer=QTimer(); self._timer.setSingleShot(True); self._timer.timeout.connect(self.load)
        self._build(); self.load()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("💰  Quản lý Đoàn phí"))

        # Stat cards
        cr=QHBoxLayout(); cr.setSpacing(12)
        self.c_total=StatCard("📋","Tổng bản ghi","0",COLORS['accent'])
        self.c_nop  =StatCard("✅","Đã nộp","0",COLORS['success'])
        self.c_chua =StatCard("⏳","Chưa nộp","0",COLORS['danger'])
        self.c_thu  =StatCard("💵","Tổng thu (VNĐ)","0",COLORS['warning'])
        for c in [self.c_total,self.c_nop,self.c_chua,self.c_thu]: cr.addWidget(c)
        lay.addLayout(cr)

        # Toolbar
        tb=QHBoxLayout(); tb.setSpacing(10)
        self.txt_search=QLineEdit(); self.txt_search.setPlaceholderText("🔍  Tìm tên / mã ĐV...")
        self.txt_search.setFixedHeight(40); self.txt_search.setMinimumWidth(220)
        self.txt_search.textChanged.connect(lambda _: self._timer.start(280))

        self.cmb_hk=QComboBox(); self.cmb_hk.setFixedHeight(40)
        self.cmb_hk.addItems(["Tất cả","HK1","HK2","HK3"])
        self.cmb_hk.currentIndexChanged.connect(self.load)

        self.cmb_nh=QComboBox(); self.cmb_nh.setFixedHeight(40)
        self.cmb_nh.addItems(["Tất cả","2023-2024","2024-2025","2025-2026"])
        self.cmb_nh.setCurrentIndex(2)
        self.cmb_nh.currentIndexChanged.connect(self.load)

        btn_tao=QPushButton("📋  Tạo đoàn phí HK"); btn_tao.setFixedHeight(40)
        btn_tao.setObjectName("btn_info"); btn_tao.setCursor(Qt.PointingHandCursor)
        btn_tao.clicked.connect(self._tao_phi)

        btn_nop=QPushButton("✅  Cập nhật nộp phí"); btn_nop.setFixedHeight(40)
        btn_nop.setObjectName("btn_success"); btn_nop.setCursor(Qt.PointingHandCursor)
        btn_nop.clicked.connect(self._nop_phi)

        for w in [self.txt_search,self.cmb_hk,self.cmb_nh]: tb.addWidget(w)
        tb.addStretch(); tb.addWidget(btn_tao); tb.addWidget(btn_nop)
        lay.addLayout(tb)

        # Table
        self.table=QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.table.doubleClicked.connect(self._nop_phi)
        self.table.setColumnHidden(0,True)
        lay.addWidget(self.table)
        self.lbl_st=QLabel(""); self.lbl_st.setStyleSheet(f"color:{COLORS['text_muted']};font-size:9pt;")
        lay.addWidget(self.lbl_st)

    def load(self):
        rows=self.db.get_doan_phi(
            self.txt_search.text().strip(),
            self.cmb_hk.currentText(),
            self.cmb_nh.currentText()
        )
        self.table.setRowCount(len(rows))
        for r,d in enumerate(rows):
            for c,k in enumerate(self.KEYS):
                val=d.get(k,"") or ""
                if k=="so_tien": val=f"{val:,.0f}"
                elif k=="da_nop": val="✅ Đã nộp" if val else "❌ Chưa nộp"
                item=QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if k=="da_nop":
                    clr=COLORS['success'] if "Đã" in str(val) else COLORS['danger']
                    item.setForeground(QBrush(QColor(clr)))
                    item.setFont(QFont("Segoe UI",9,QFont.Bold))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()
        # Stats
        st=self.db.get_doan_phi_stats(self.cmb_hk.currentText(),self.cmb_nh.currentText())
        total=st['total'] or 0; nop=st['da_nop'] or 0; thu=st['tong_thu'] or 0
        self.c_total.set_value(total); self.c_nop.set_value(int(nop))
        self.c_chua.set_value(total-int(nop)); self.c_thu.set_value(f"{thu:,.0f}")
        self.lbl_st.setText(f"Hiển thị {len(rows)} bản ghi")

    def _tao_phi(self):
        if TaoPhiDialog(self.db,self).exec_(): self.load()

    def _nop_phi(self):
        r=self.table.currentRow()
        if r<0: QMessageBox.warning(self,"","Vui lòng chọn một dòng."); return
        # Lấy id từ cột 0 (ẩn)
        id_=int(self.table.item(r,0).text())
        rows=self.db.get_doan_phi(self.txt_search.text().strip(),
                                   self.cmb_hk.currentText(),self.cmb_nh.currentText())
        row_data=next((x for x in rows if x['id']==id_),None)
        if row_data and NopPhiDialog(row_data,self.db,self).exec_(): self.load()
