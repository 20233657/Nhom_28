"""views/hoat_dong_view.py - Hoạt động & Tham gia"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox,
    QFrame, QHeaderView, QAbstractItemView, QMessageBox,
    QDialog, QGridLayout, QTextEdit, QTabWidget, QSpinBox,
    QDoubleSpinBox, QScrollArea, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QColor, QBrush
from styles import COLORS
from utils import StatCard, SectionTitle


LOAI_HD = ["Hiến máu","Tình nguyện","Thiện nguyện","Mùa hè xanh",
           "Môi trường","Tiếp sức mùa thi","Kỹ năng","Văn hóa - Thể thao","Khác"]
TT_HD   = ["Sắp diễn ra","Đang diễn ra","Đã kết thúc","Tạm hoãn"]
VAI_TRO = ["Thành viên","Tổ trưởng","Ban tổ chức","Tình nguyện viên","Quan sát viên"]


class HoatDongForm(QDialog):
    def __init__(self, db, hd=None, parent=None):
        super().__init__(parent)
        self.db=db; self.hd=hd; self.is_edit=hd is not None
        self.setWindowTitle("Sửa hoạt động" if self.is_edit else "Thêm hoạt động mới")
        self.setFixedSize(620,520); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()
        if self.is_edit: self._fill()

    def _build(self):
        root=QVBoxLayout(self); root.setContentsMargins(0,0,0,0)
        hdr=QFrame(); hdr.setFixedHeight(58)
        hdr.setStyleSheet(f"QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {COLORS['primary_dark']},stop:1 {COLORS['primary']}); }}")
        hl=QHBoxLayout(hdr); hl.setContentsMargins(20,0,20,0)
        ico=QLabel("🏆"); ico.setFont(QFont("Segoe UI Emoji",18)); ico.setStyleSheet("background:transparent;color:white;")
        ttl=QLabel("Thông tin Hoạt động"); ttl.setFont(QFont("Segoe UI",13,QFont.Bold)); ttl.setStyleSheet("background:transparent;color:white;")
        hl.addWidget(ico); hl.addWidget(ttl); hl.addStretch()
        root.addWidget(hdr)

        sc=QScrollArea(); sc.setWidgetResizable(True)
        body=QWidget(); body.setStyleSheet(f"background:{COLORS['bg_main']};")
        grid=QGridLayout(body); grid.setContentsMargins(24,18,24,18); grid.setSpacing(12)

        def inp(ph=""): e=QLineEdit(); e.setFixedHeight(38); e.setPlaceholderText(ph); return e
        def cmb(items): c=QComboBox(); c.setFixedHeight(38); c.addItems(items); return c
        def lbl(t,req=False):
            l=QLabel(t+(" *" if req else ""))
            l.setFont(QFont("Segoe UI",8,QFont.Bold))
            l.setStyleSheet(f"color:{COLORS['text_muted']};letter-spacing:0.8px;")
            return l

        self.txt_ten=inp("Tên hoạt động..."); self.txt_ten.setMinimumWidth(300)
        self.cmb_loai=cmb(LOAI_HD)
        from PyQt5.QtWidgets import QDateEdit
        self.dt_ngay=QDateEdit(); self.dt_ngay.setCalendarPopup(True)
        self.dt_ngay.setDisplayFormat("dd/MM/yyyy"); self.dt_ngay.setFixedHeight(38)
        self.dt_ngay.setDate(QDate.currentDate())
        self.txt_dd=inp("Địa điểm tổ chức")
        self.spn_sl=QSpinBox(); self.spn_sl.setFixedHeight(38); self.spn_sl.setRange(1,10000); self.spn_sl.setValue(100)
        self.spn_diem=QDoubleSpinBox(); self.spn_diem.setFixedHeight(38); self.spn_diem.setRange(0,10); self.spn_diem.setValue(1.0); self.spn_diem.setSingleStep(0.5)
        self.cmb_tt=cmb(TT_HD)
        self.txt_mo_ta=QTextEdit(); self.txt_mo_ta.setFixedHeight(90); self.txt_mo_ta.setPlaceholderText("Mô tả chi tiết hoạt động...")

        rows=[(lbl("Tên hoạt động",True),self.txt_ten,0,0,1,2),
              (lbl("Loại hoạt động"),self.cmb_loai,1,0,1,1),
              (lbl("Ngày tổ chức"),self.dt_ngay,1,1,1,1),
              (lbl("Địa điểm"),self.txt_dd,2,0,1,2),
              (lbl("Số lượng tối đa"),self.spn_sl,3,0,1,1),
              (lbl("Điểm cộng"),self.spn_diem,3,1,1,1),
              (lbl("Trạng thái"),self.cmb_tt,4,0,1,1)]
        for (l,w,r,c,rs,cs) in rows:
            bx=QVBoxLayout(); bx.setSpacing(4); bx.addWidget(l); bx.addWidget(w)
            grid.addLayout(bx,r,c,rs,cs)
        mb=QVBoxLayout(); mb.setSpacing(4); mb.addWidget(lbl("Mô tả")); mb.addWidget(self.txt_mo_ta)
        grid.addLayout(mb,5,0,1,2)
        sc.setWidget(body); root.addWidget(sc)

        ftr=QFrame(); ftr.setFixedHeight(58)
        ftr.setStyleSheet(f"background:{COLORS['bg_card']};border-top:1px solid {COLORS['border']};")
        fl=QHBoxLayout(ftr); fl.setContentsMargins(24,0,24,0); fl.setSpacing(12)
        self.lbl_err=QLabel(""); self.lbl_err.setStyleSheet(f"color:{COLORS['danger']};")
        bc=QPushButton("Hủy"); bc.setFixedSize(100,36); bc.setObjectName("btn_secondary"); bc.setCursor(Qt.PointingHandCursor); bc.clicked.connect(self.reject)
        bs=QPushButton("💾  Lưu"); bs.setFixedSize(120,36); bs.setObjectName("btn_success"); bs.setCursor(Qt.PointingHandCursor); bs.clicked.connect(self._save)
        fl.addWidget(self.lbl_err); fl.addStretch(); fl.addWidget(bc); fl.addWidget(bs)
        root.addWidget(ftr)

    def _fill(self):
        hd=self.hd
        self.txt_ten.setText(hd.get("ten_hd",""))
        i=self.cmb_loai.findText(hd.get("loai_hd",""))
        if i>=0: self.cmb_loai.setCurrentIndex(i)
        ng=hd.get("ngay_to_chuc","")
        if ng:
            try: p=ng.split("-"); self.dt_ngay.setDate(QDate(int(p[0]),int(p[1]),int(p[2])))
            except: pass
        self.txt_dd.setText(hd.get("dia_diem",""))
        self.spn_sl.setValue(int(hd.get("so_luong_toi_da",100)))
        self.spn_diem.setValue(float(hd.get("diem_cong",1.0)))
        i2=self.cmb_tt.findText(hd.get("trang_thai",""))
        if i2>=0: self.cmb_tt.setCurrentIndex(i2)
        self.txt_mo_ta.setPlainText(hd.get("mo_ta",""))

    def _collect(self):
        return {
            "ten_hd": self.txt_ten.text().strip(),
            "loai_hd": self.cmb_loai.currentText(),
            "ngay_to_chuc": self.dt_ngay.date().toString("yyyy-MM-dd"),
            "dia_diem": self.txt_dd.text().strip(),
            "so_luong_toi_da": self.spn_sl.value(),
            "diem_cong": self.spn_diem.value(),
            "trang_thai": self.cmb_tt.currentText(),
            "mo_ta": self.txt_mo_ta.toPlainText().strip(),
        }

    def _save(self):
        d=self._collect()
        if not d["ten_hd"]: self.lbl_err.setText("⚠  Tên hoạt động không được trống"); return
        if self.is_edit: ok,msg=self.db.update_hoat_dong(self.hd['id'],d)
        else: ok,msg=self.db.add_hoat_dong(d)
        if ok: QMessageBox.information(self,"OK",msg); self.accept()
        else: self.lbl_err.setText(f"⚠  {msg}")


class ThamGiaDialog(QDialog):
    """Dialog xem và quản lý danh sách tham gia một hoạt động"""
    def __init__(self, db, hd, parent=None):
        super().__init__(parent)
        self.db=db; self.hd=hd
        self.setWindowTitle(f"Tham gia: {hd['ten_hd']}")
        self.setFixedSize(760,520); self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLORS['bg_main']};color:{COLORS['text_primary']};font-family:'Segoe UI';}}")
        self._build()

    def _build(self):
        root=QVBoxLayout(self); root.setContentsMargins(20,16,20,16); root.setSpacing(12)
        info=QLabel(f"🏆  {self.hd['ten_hd']}  |  📅 {self.hd.get('ngay_to_chuc','')}  |  📍 {self.hd.get('dia_diem','')}")
        info.setFont(QFont("Segoe UI",10,QFont.Bold))
        info.setStyleSheet(f"color:{COLORS['accent']};")
        root.addWidget(info)

        # Thêm đoàn viên
        add_row=QHBoxLayout()
        self.cmb_dv=QComboBox(); self.cmb_dv.setFixedHeight(36)
        dvs=self.db.get_all_dv()
        for dv in dvs: self.cmb_dv.addItem(f"{dv['ma_dv']} - {dv['ho_ten']}", dv['ma_dv'])
        self.cmb_vai=QComboBox(); self.cmb_vai.setFixedHeight(36); self.cmb_vai.addItems(VAI_TRO)
        btn_add=QPushButton("➕  Đăng ký"); btn_add.setFixedHeight(36)
        btn_add.setObjectName("btn_success"); btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._add_tham_gia)
        btn_del=QPushButton("🗑️  Xóa"); btn_del.setFixedHeight(36)
        btn_del.setObjectName("btn_danger"); btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.clicked.connect(self._xoa_tham_gia)
        add_row.addWidget(QLabel("Chọn ĐV:")); add_row.addWidget(self.cmb_dv,1)
        add_row.addWidget(QLabel("Vai trò:")); add_row.addWidget(self.cmb_vai)
        add_row.addWidget(btn_add); add_row.addWidget(btn_del)
        root.addLayout(add_row)

        # Table
        self.table=QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Mã ĐV","Họ tên","Lớp","Vai trò","Đã tham gia"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.table.setColumnHidden(0,True)
        root.addWidget(self.table)

        self.lbl_count=QLabel("")
        self.lbl_count.setStyleSheet(f"color:{COLORS['accent']};font-weight:700;")
        root.addWidget(self.lbl_count)

        btn_close=QPushButton("Đóng"); btn_close.setFixedHeight(38)
        btn_close.setObjectName("btn_secondary"); btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        root.addWidget(btn_close,alignment=Qt.AlignRight)
        self._load()

    def _load(self):
        rows=self.db.get_tham_gia(self.hd['id'])
        self.table.setRowCount(len(rows))
        for r,d in enumerate(rows):
            vals=[d['id'],d['ma_dv'],d['ho_ten'],d['lop'],d.get('vai_tro',''),
                  "✅ Có" if d.get('da_tham_gia') else "❌ Không"]
            for c,v in enumerate(vals):
                item=QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
                if c==5:
                    clr=COLORS['success'] if "Có" in str(v) else COLORS['danger']
                    item.setForeground(QBrush(QColor(clr)))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()
        self.lbl_count.setText(f"  Tổng: {len(rows)} người tham gia / Tối đa: {self.hd.get('so_luong_toi_da','-')}")

    def _add_tham_gia(self):
        ma=self.cmb_dv.currentData()
        vai=self.cmb_vai.currentText()
        self.db.dang_ky_tham_gia(ma,self.hd['id'],vai)
        self._load()

    def _xoa_tham_gia(self):
        r=self.table.currentRow()
        if r<0: QMessageBox.warning(self,"","Chọn một dòng để xóa."); return
        id_=int(self.table.item(r,0).text())
        self.db.xoa_tham_gia(id_)
        self._load()


class HoatDongView(QWidget):
    COLS=["ID","Tên hoạt động","Loại","Ngày tổ chức","Địa điểm","SL tối đa","Đã tham gia","Điểm cộng","Trạng thái"]
    KEYS=["id","ten_hd","loai_hd","ngay_to_chuc","dia_diem","so_luong_toi_da","so_tham_gia","diem_cong","trang_thai"]

    def __init__(self, db, user):
        super().__init__()
        self.db=db; self.user=user
        self._timer=QTimer(); self._timer.setSingleShot(True); self._timer.timeout.connect(self.load)
        self._build(); self.load()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("🏆  Hoạt động & Tham gia"))

        cr=QHBoxLayout(); cr.setSpacing(12)
        self.c_total=StatCard("🏆","Tổng hoạt động","0",COLORS['accent'])
        self.c_sap  =StatCard("⏰","Sắp diễn ra","0",COLORS['info'])
        self.c_dang =StatCard("🟢","Đang diễn ra","0",COLORS['success'])
        self.c_xong =StatCard("✅","Đã kết thúc","0",COLORS['text_muted'])
        for c in [self.c_total,self.c_sap,self.c_dang,self.c_xong]: cr.addWidget(c)
        lay.addLayout(cr)

        tb=QHBoxLayout(); tb.setSpacing(10)
        self.txt_search=QLineEdit(); self.txt_search.setPlaceholderText("🔍  Tìm tên hoạt động...")
        self.txt_search.setFixedHeight(40); self.txt_search.setMinimumWidth(240)
        self.txt_search.textChanged.connect(lambda _: self._timer.start(280))
        self.cmb_loai=QComboBox(); self.cmb_loai.setFixedHeight(40)
        self.cmb_loai.addItems(["Tất cả"]+LOAI_HD)
        self.cmb_loai.currentIndexChanged.connect(self.load)

        btn_add=QPushButton("➕  Thêm HĐ"); btn_add.setFixedHeight(40)
        btn_add.setObjectName("btn_success"); btn_add.setCursor(Qt.PointingHandCursor); btn_add.clicked.connect(self._add)
        btn_edit=QPushButton("✏️  Sửa"); btn_edit.setFixedHeight(40)
        btn_edit.setCursor(Qt.PointingHandCursor); btn_edit.clicked.connect(self._edit)
        btn_tg=QPushButton("👥  Tham gia"); btn_tg.setFixedHeight(40)
        btn_tg.setObjectName("btn_info"); btn_tg.setCursor(Qt.PointingHandCursor); btn_tg.clicked.connect(self._tham_gia)
        btn_del=QPushButton("🗑️  Xóa"); btn_del.setFixedHeight(40)
        btn_del.setObjectName("btn_danger"); btn_del.setCursor(Qt.PointingHandCursor); btn_del.clicked.connect(self._delete)

        for w in [self.txt_search,self.cmb_loai]: tb.addWidget(w)
        tb.addStretch()
        for w in [btn_add,btn_edit,btn_tg,btn_del]: tb.addWidget(w)
        lay.addLayout(tb)

        self.table=QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.table.setColumnHidden(0,True)
        self.table.doubleClicked.connect(self._tham_gia)
        lay.addWidget(self.table)

        tt_colors={"Sắp diễn ra":COLORS['info'],"Đang diễn ra":COLORS['success'],
                   "Đã kết thúc":COLORS['text_muted'],"Tạm hoãn":COLORS['warning']}
        self.tt_colors=tt_colors

    def load(self):
        rows=self.db.get_all_hoat_dong(self.txt_search.text().strip(),self.cmb_loai.currentText())
        self.table.setRowCount(len(rows))
        sap=dang=xong=0
        for r,hd in enumerate(rows):
            tt=hd.get('trang_thai','')
            if tt=="Sắp diễn ra": sap+=1
            elif tt=="Đang diễn ra": dang+=1
            elif tt=="Đã kết thúc": xong+=1
            for c,k in enumerate(self.KEYS):
                val=hd.get(k,"") or ""
                if k=="diem_cong": val=f"+{val}"
                item=QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignVCenter|(Qt.AlignCenter if c>4 else Qt.AlignLeft))
                if k=="trang_thai":
                    clr=self.tt_colors.get(str(val),COLORS['text_primary'])
                    item.setForeground(QBrush(QColor(clr)))
                    item.setFont(QFont("Segoe UI",9,QFont.Bold))
                self.table.setItem(r,c,item)
        self.table.resizeColumnsToContents()
        self.c_total.set_value(len(rows)); self.c_sap.set_value(sap)
        self.c_dang.set_value(dang); self.c_xong.set_value(xong)

    def _sel(self):
        r=self.table.currentRow()
        if r<0: return None
        id_=int(self.table.item(r,0).text())
        return self.db.get_hoat_dong_by_id(id_)

    def _add(self):
        if HoatDongForm(self.db,parent=self).exec_(): self.load()
    def _edit(self):
        hd=self._sel()
        if not hd: QMessageBox.warning(self,"","Chọn một hoạt động."); return
        if HoatDongForm(self.db,hd,self).exec_(): self.load()
    def _tham_gia(self):
        hd=self._sel()
        if not hd: QMessageBox.warning(self,"","Chọn một hoạt động."); return
        ThamGiaDialog(self.db,hd,self).exec_()
    def _delete(self):
        hd=self._sel()
        if not hd: QMessageBox.warning(self,"","Chọn một hoạt động."); return
        r=QMessageBox.question(self,"Xác nhận",f"Xóa hoạt động '{hd['ten_hd']}'?",QMessageBox.Yes|QMessageBox.No)
        if r==QMessageBox.Yes:
            self.db.delete_hoat_dong(hd['id']); self.load()
