"""views/xep_loai_view.py - Xếp loại đoàn viên theo học kỳ"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox,
    QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QDialog, QGridLayout, QDoubleSpinBox, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QBrush
from styles import COLORS
from utils import StatCard, SectionTitle


KQ_COLORS = {
    "Đoàn viên Xuất sắc":         COLORS['accent'],
    "Đoàn viên Hoàn thành tốt":   COLORS['success'],
    "Đoàn viên Hoàn thành":        COLORS['info'],
    "Đoàn viên Không hoàn thành": COLORS['danger'],
    "Chưa xếp loại":               COLORS['text_muted'],
}


class XepLoaiForm(QDialog):
    def __init__(self, db, xl=None, ma_dv=None, parent=None):
        super().__init__(parent)
        self.db=db; self.xl=xl; self.ma_dv=ma_dv
        self.setWindowTitle("Nhập xếp loại đoàn viên")
        self.setFixedSize(480,380); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()
        if xl: self._fill()

    def _build(self):
        root=QVBoxLayout(self); root.setContentsMargins(0,0,0,0)
        hdr=QFrame(); hdr.setFixedHeight(56)
        hdr.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {COLORS['primary_dark']},stop:1 {COLORS['primary']}); }}")
        hl=QHBoxLayout(hdr); hl.setContentsMargins(20,0,20,0)
        ttl=QLabel("⭐  Nhập xếp loại Đoàn viên"); ttl.setFont(QFont("Segoe UI",12,QFont.Bold)); ttl.setStyleSheet("color:white;background:transparent;")
        hl.addWidget(ttl); root.addWidget(hdr)

        body=QFrame(); body.setStyleSheet(f"background:{COLORS['bg_main']};")
        grid=QGridLayout(body); grid.setContentsMargins(24,16,24,16); grid.setSpacing(12)

        def lbl(t): l=QLabel(t); l.setStyleSheet(f"color:{COLORS['text_secondary']};"); return l
        def cmb(items): c=QComboBox(); c.setFixedHeight(38); c.addItems(items); return c

        self.cmb_hk =cmb(["HK1","HK2","HK3"])
        self.cmb_nh =cmb(["2023-2024","2024-2025","2025-2026"]); self.cmb_nh.setCurrentIndex(1)

        # Chọn đoàn viên (nếu tạo mới)
        self.cmb_dv=QComboBox(); self.cmb_dv.setFixedHeight(38)
        dvs=self.db.get_all_dv()
        for dv in dvs: self.cmb_dv.addItem(f"{dv['ma_dv']} - {dv['ho_ten']}", dv['ma_dv'])
        if self.xl:
            self.cmb_dv.setEnabled(False)
            for i in range(self.cmb_dv.count()):
                if self.cmb_dv.itemData(i)==self.xl.get('ma_dv'):
                    self.cmb_dv.setCurrentIndex(i); break

        self.spn_drl=QDoubleSpinBox(); self.spn_drl.setFixedHeight(38); self.spn_drl.setRange(0,100); self.spn_drl.setValue(75.0); self.spn_drl.setSuffix(" điểm")
        self.spn_dhk=QDoubleSpinBox(); self.spn_dhk.setFixedHeight(38); self.spn_dhk.setRange(0,4.0); self.spn_dhk.setSingleStep(0.1); self.spn_dhk.setValue(3.0); self.spn_dhk.setSuffix(" / 4.0")
        self.spn_hd =QSpinBox(); self.spn_hd.setFixedHeight(38); self.spn_hd.setRange(0,50); self.spn_hd.setValue(2); self.spn_hd.setSuffix(" hoạt động")
        self.chk_phi=QCheckBox("Đã đóng đoàn phí học kỳ này")
        self.chk_phi.setStyleSheet(f"color:{COLORS['text_primary']};font-size:11pt;")

        grid.addWidget(lbl("Đoàn viên:"),0,0); grid.addWidget(self.cmb_dv,0,1)
        grid.addWidget(lbl("Học kỳ:"),1,0); grid.addWidget(self.cmb_hk,1,1)
        grid.addWidget(lbl("Năm học:"),2,0); grid.addWidget(self.cmb_nh,2,1)
        grid.addWidget(lbl("Điểm rèn luyện:"),3,0); grid.addWidget(self.spn_drl,3,1)
        grid.addWidget(lbl("Điểm học tập (GPA):"),4,0); grid.addWidget(self.spn_dhk,4,1)
        grid.addWidget(lbl("Số HĐ tham gia:"),5,0); grid.addWidget(self.spn_hd,5,1)
        grid.addWidget(self.chk_phi,6,0,1,2)
        root.addWidget(body)

        ftr=QFrame(); ftr.setFixedHeight(58)
        ftr.setStyleSheet(f"background:{COLORS['bg_card']};border-top:1px solid {COLORS['border']};")
        fl=QHBoxLayout(ftr); fl.setContentsMargins(24,0,24,0); fl.setSpacing(12)
        self.lbl_err=QLabel(""); self.lbl_err.setStyleSheet(f"color:{COLORS['danger']};")
        bc=QPushButton("Hủy"); bc.setFixedSize(100,38); bc.setObjectName("btn_secondary"); bc.setCursor(Qt.PointingHandCursor); bc.clicked.connect(self.reject)
        bs=QPushButton("💾  Lưu & Xếp loại"); bs.setFixedHeight(38); bs.setObjectName("btn_success"); bs.setCursor(Qt.PointingHandCursor); bs.clicked.connect(self._save)
        fl.addWidget(self.lbl_err); fl.addStretch(); fl.addWidget(bc); fl.addWidget(bs)
        root.addWidget(ftr)

    def _fill(self):
        xl=self.xl
        hk_i=self.cmb_hk.findText(xl.get('hoc_ky','HK1'))
        if hk_i>=0: self.cmb_hk.setCurrentIndex(hk_i)
        nh_i=self.cmb_nh.findText(xl.get('nam_hoc',''))
        if nh_i>=0: self.cmb_nh.setCurrentIndex(nh_i)
        self.spn_drl.setValue(float(xl.get('diem_rl',0)))
        self.spn_dhk.setValue(float(xl.get('diem_hk',0)))
        self.spn_hd.setValue(int(xl.get('so_hd_tham_gia',0)))
        self.chk_phi.setChecked(bool(xl.get('dong_doan_phi',0)))

    def _save(self):
        ma=self.cmb_dv.currentData()
        if not ma: self.lbl_err.setText("⚠  Chọn đoàn viên"); return
        d={
            "ma_dv": ma,
            "hoc_ky": self.cmb_hk.currentText(),
            "nam_hoc": self.cmb_nh.currentText(),
            "diem_rl": self.spn_drl.value(),
            "diem_hk": self.spn_dhk.value(),
            "so_hd_tham_gia": self.spn_hd.value(),
            "dong_doan_phi": 1 if self.chk_phi.isChecked() else 0,
            "ghi_chu": "",
        }
        ok,msg=self.db.save_xep_loai(d)
        if ok: QMessageBox.information(self,"OK",msg); self.accept()
        else: self.lbl_err.setText(f"⚠  {msg}")


class XepLoaiView(QWidget):
    COLS=["Mã ĐV","Họ tên","Lớp","Khoa","Học kỳ","Năm học","Điểm RL","Xếp loại RL","GPA","Xếp loại HK","Số HĐ","Đóng phí","Kết quả"]
    KEYS=["ma_dv","ho_ten","lop","khoa","hoc_ky","nam_hoc","diem_rl","xep_loai_rl","diem_hk","xep_loai_hk","so_hd_tham_gia","dong_doan_phi","ket_qua"]

    def __init__(self, db, user):
        super().__init__()
        self.db=db; self.user=user
        self._timer=QTimer(); self._timer.setSingleShot(True); self._timer.timeout.connect(self.load)
        self._build(); self.load()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("⭐  Xếp loại Đoàn viên theo Học kỳ"))

        # Stat cards
        cr=QHBoxLayout(); cr.setSpacing(12)
        self.c_xs  =StatCard("🥇","Xuất sắc","0",COLORS['accent'])
        self.c_tot =StatCard("🥈","Hoàn thành tốt","0",COLORS['success'])
        self.c_ht  =StatCard("🥉","Hoàn thành","0",COLORS['info'])
        self.c_kht =StatCard("❌","Không hoàn thành","0",COLORS['danger'])
        for c in [self.c_xs,self.c_tot,self.c_ht,self.c_kht]: cr.addWidget(c)
        lay.addLayout(cr)

        # Toolbar
        tb=QHBoxLayout(); tb.setSpacing(10)
        self.txt_s=QLineEdit(); self.txt_s.setPlaceholderText("🔍  Tìm tên / mã ĐV...")
        self.txt_s.setFixedHeight(40); self.txt_s.setMinimumWidth(220)
        self.txt_s.textChanged.connect(lambda _: self._timer.start(280))
        self.cmb_hk=QComboBox(); self.cmb_hk.setFixedHeight(40)
        self.cmb_hk.addItems(["Tất cả","HK1","HK2","HK3"]); self.cmb_hk.currentIndexChanged.connect(self.load)
        self.cmb_nh=QComboBox(); self.cmb_nh.setFixedHeight(40)
        self.cmb_nh.addItems(["Tất cả","2023-2024","2024-2025"]); self.cmb_nh.setCurrentIndex(2); self.cmb_nh.currentIndexChanged.connect(self.load)
        self.cmb_kq=QComboBox(); self.cmb_kq.setFixedHeight(40)
        self.cmb_kq.addItems(["Tất cả","Đoàn viên Xuất sắc","Đoàn viên Hoàn thành tốt",
                               "Đoàn viên Hoàn thành","Đoàn viên Không hoàn thành","Chưa xếp loại"])
        self.cmb_kq.currentIndexChanged.connect(self.load)

        btn_them=QPushButton("➕  Nhập xếp loại"); btn_them.setFixedHeight(40)
        btn_them.setObjectName("btn_success"); btn_them.setCursor(Qt.PointingHandCursor); btn_them.clicked.connect(self._them)
        btn_auto=QPushButton("⚡  Xếp loại tự động"); btn_auto.setFixedHeight(40)
        btn_auto.setObjectName("btn_accent"); btn_auto.setCursor(Qt.PointingHandCursor); btn_auto.clicked.connect(self._auto)
        btn_sua=QPushButton("✏️  Sửa"); btn_sua.setFixedHeight(40)
        btn_sua.setCursor(Qt.PointingHandCursor); btn_sua.clicked.connect(self._sua)

        for w in [self.txt_s,self.cmb_hk,self.cmb_nh,self.cmb_kq]: tb.addWidget(w)
        tb.addStretch()
        for w in [btn_them,btn_sua,btn_auto]: tb.addWidget(w)
        lay.addLayout(tb)

        # Chú thích
        note=QLabel("  🥇 Xuất sắc: RL≥90, GPA≥3.6, ≥2 HĐ, đóng phí   |   🥈 Hoàn thành tốt: RL≥75, GPA≥2.5   |   🥉 Hoàn thành: RL≥50, GPA≥2.0")
        note.setStyleSheet(f"color:{COLORS['text_muted']};font-size:9pt;background:{COLORS['bg_card']};padding:6px 12px;border-radius:6px;")
        lay.addWidget(note)

        self.table=QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.table.doubleClicked.connect(self._sua)
        lay.addWidget(self.table)
        self.lbl_st=QLabel(""); self.lbl_st.setStyleSheet(f"color:{COLORS['text_muted']};font-size:9pt;")
        lay.addWidget(self.lbl_st)

    def load(self):
        rows=self.db.get_xep_loai(
            self.cmb_hk.currentText(), self.cmb_nh.currentText(),
            self.cmb_kq.currentText(), self.txt_s.text().strip()
        )
        self.table.setRowCount(len(rows))
        xs=tot=ht=kht=0
        for r,xl in enumerate(rows):
            kq=xl.get('ket_qua','')
            if "Xuất sắc" in kq: xs+=1
            elif "tốt" in kq: tot+=1
            elif "Hoàn thành" in kq and "tốt" not in kq: ht+=1
            elif "Không" in kq: kht+=1
            for c,k in enumerate(self.KEYS):
                val=xl.get(k,"") or ""
                if k=="diem_rl": val=f"{float(val):.1f}" if val else "0"
                elif k=="diem_hk": val=f"{float(val):.2f}" if val else "0"
                elif k=="dong_doan_phi": val="✅" if val else "❌"
                item=QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
                if k=="ket_qua":
                    clr=KQ_COLORS.get(str(val),COLORS['text_primary'])
                    item.setForeground(QBrush(QColor(clr)))
                    item.setFont(QFont("Segoe UI",9,QFont.Bold))
                elif k in ("xep_loai_rl","xep_loai_hk"):
                    clr=KQ_COLORS.get(str(val),COLORS['text_secondary'])
                    item.setForeground(QBrush(QColor(clr)))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(1,160)
        self.c_xs.set_value(xs); self.c_tot.set_value(tot)
        self.c_ht.set_value(ht); self.c_kht.set_value(kht)
        self.lbl_st.setText(f"Hiển thị {len(rows)} bản xếp loại")

    def _them(self):
        if XepLoaiForm(self.db,parent=self).exec_(): self.load()

    def _sua(self):
        r=self.table.currentRow()
        if r<0: QMessageBox.warning(self,"","Chọn một dòng."); return
        ma=self.table.item(r,0).text(); hk=self.table.item(r,4).text(); nh=self.table.item(r,5).text()
        rows=self.db.get_xep_loai(hk,nh)
        xl=next((x for x in rows if x['ma_dv']==ma),None)
        if xl and XepLoaiForm(self.db,xl,parent=self).exec_(): self.load()

    def _auto(self):
        hk=self.cmb_hk.currentText() if self.cmb_hk.currentText()!="Tất cả" else "HK1"
        nh=self.cmb_nh.currentText() if self.cmb_nh.currentText()!="Tất cả" else "2024-2025"
        r=QMessageBox.question(self,"Xác nhận",
            f"Tự động xếp loại TẤT CẢ đoàn viên đang sinh hoạt\ncho {hk}/{nh}?\n\n(Sẽ ghi đè dữ liệu cũ nếu có)",
            QMessageBox.Yes|QMessageBox.No)
        if r==QMessageBox.Yes:
            ok,msg=self.db.auto_xep_loai(hk,nh)
            if ok: QMessageBox.information(self,"Thành công",msg); self.load()
            else: QMessageBox.critical(self,"Lỗi",msg)
