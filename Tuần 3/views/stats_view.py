"""views/stats_view.py - Thống kê biểu đồ matplotlib"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTabWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from styles import COLORS
from utils import StatCard, SectionTitle


class StatsView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db=db
        self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(24,24,24,16); lay.setSpacing(16)
        lay.addWidget(SectionTitle("📊  Thống kê & Báo cáo"))

        cr=QHBoxLayout(); cr.setSpacing(12)
        self.c_total=StatCard("👥","Tổng đoàn viên","0",COLORS['accent'])
        self.c_act  =StatCard("✅","Đang sinh hoạt","0",COLORS['success'])
        self.c_left =StatCard("🔴","Đã rời","0",COLORS['danger'])
        self.c_hd   =StatCard("🏆","Tổng hoạt động","0",COLORS['warning'])
        for c in [self.c_total,self.c_act,self.c_left,self.c_hd]: cr.addWidget(c)
        lay.addLayout(cr)

        tabs=QTabWidget()
        self.tab_khoa=QWidget(); self.tab_lop=QWidget(); self.tab_xl=QWidget()
        tabs.addTab(self.tab_khoa,"  🏫  Theo Khoa  ")
        tabs.addTab(self.tab_lop, "  📚  Theo Lớp   ")
        tabs.addTab(self.tab_xl,  "  ⭐  Xếp loại   ")
        self._setup_tab(self.tab_khoa,"khoa")
        self._setup_tab(self.tab_lop,"lop")
        self._setup_tab(self.tab_xl,"xl")
        lay.addWidget(tabs)

    def _setup_tab(self, tab, kind):
        l=QVBoxLayout(tab); l.setContentsMargins(12,12,12,12)
        try:
            import matplotlib
            matplotlib.use("Qt5Agg")
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure
            fig=Figure(figsize=(10,4.5),facecolor=COLORS['bg_card'])
            canvas=FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            setattr(self,f"fig_{kind}",fig)
            setattr(self,f"canvas_{kind}",canvas)
            l.addWidget(canvas)
        except:
            lb=QLabel("⚠  Cần cài matplotlib:\npip install matplotlib")
            lb.setAlignment(Qt.AlignCenter)
            lb.setStyleSheet(f"color:{COLORS['warning']};font-size:12pt;")
            l.addWidget(lb)

    def refresh(self):
        s=self.db.get_stats()
        self.c_total.set_value(s['total']); self.c_act.set_value(s['active'])
        self.c_left.set_value(s['left']); self.c_hd.set_value(s['hoat_dong'])
        try:
            self._draw_khoa(); self._draw_lop(); self._draw_xl()
        except Exception as e:
            print(f"Chart error: {e}")

    def _palette(self, n):
        p=["#C62828","#E53935","#FFD600","#1565C0","#2E7D32","#FB8C00",
           "#6A1B9A","#00838F","#4E342E","#37474F","#880E4F","#1A237E"]
        return [p[i%len(p)] for i in range(n)]

    def _draw_khoa(self):
        if not hasattr(self,'fig_khoa'): return
        data=self.db.get_stats_by_khoa()
        if not data: return
        names=[d['khoa'] for d in data]; vals=[d['sl'] for d in data]
        clrs=self._palette(len(names))
        fig=self.fig_khoa; fig.clear()
        ax1=fig.add_subplot(121); ax2=fig.add_subplot(122)
        for ax in [ax1,ax2]: ax.set_facecolor(COLORS['bg_card'])
        fig.patch.set_facecolor(COLORS['bg_card'])
        bars=ax1.bar(range(len(names)),vals,color=clrs,width=0.6,edgecolor='none',zorder=2)
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels([n[:10]+"…" if len(n)>10 else n for n in names],
                            rotation=35,ha='right',fontsize=8,color=COLORS['text_secondary'])
        ax1.tick_params(axis='y',colors=COLORS['text_secondary'])
        ax1.set_title("Số ĐV theo Khoa",color=COLORS['text_primary'],fontsize=11,fontweight='bold')
        ax1.spines[:].set_visible(False); ax1.yaxis.grid(True,color=COLORS['border'],linestyle='--',alpha=0.4,zorder=1); ax1.set_axisbelow(True)
        for b,v in zip(bars,vals):
            ax1.text(b.get_x()+b.get_width()/2,b.get_height()+0.05,str(v),ha='center',va='bottom',color=COLORS['text_primary'],fontsize=9,fontweight='bold')
        wedges,texts,auto=ax2.pie(vals,labels=None,colors=clrs,autopct='%1.1f%%',startangle=90,
                                   wedgeprops={'linewidth':2,'edgecolor':COLORS['bg_card']},pctdistance=0.75)
        for at in auto: at.set_color('white'); at.set_fontsize(8); at.set_fontweight('bold')
        ax2.set_title("Tỉ lệ theo Khoa",color=COLORS['text_primary'],fontsize=11,fontweight='bold')
        ax2.legend(wedges,names,loc='lower center',bbox_to_anchor=(0.5,-0.2),ncol=2,fontsize=7,framealpha=0,labelcolor=COLORS['text_secondary'])
        fig.tight_layout(pad=2.0); self.canvas_khoa.draw()

    def _draw_lop(self):
        if not hasattr(self,'fig_lop'): return
        data=self.db.get_stats_by_lop()
        if not data: return
        names=[d['lop'] for d in data]; vals=[d['sl'] for d in data]
        clrs=self._palette(len(names))
        fig=self.fig_lop; fig.clear()
        ax=fig.add_subplot(111); ax.set_facecolor(COLORS['bg_card']); fig.patch.set_facecolor(COLORS['bg_card'])
        bars=ax.barh(range(len(names)),vals,color=clrs,height=0.6,edgecolor='none',zorder=2)
        ax.set_yticks(range(len(names))); ax.set_yticklabels(names,fontsize=9,color=COLORS['text_secondary'])
        ax.tick_params(axis='x',colors=COLORS['text_secondary'])
        ax.set_title("Số ĐV theo Lớp",color=COLORS['text_primary'],fontsize=12,fontweight='bold')
        ax.spines[:].set_visible(False); ax.xaxis.grid(True,color=COLORS['border'],linestyle='--',alpha=0.4,zorder=1); ax.set_axisbelow(True)
        for b,v in zip(bars,vals):
            ax.text(b.get_width()+0.05,b.get_y()+b.get_height()/2,str(v),va='center',color=COLORS['text_primary'],fontsize=9,fontweight='bold')
        fig.tight_layout(pad=2.0); self.canvas_lop.draw()

    def _draw_xl(self):
        if not hasattr(self,'fig_xl'): return
        xls=self.db.get_xep_loai("HK1","2024-2025")
        if not xls: xls=self.db.get_xep_loai()
        from collections import Counter
        cnt=Counter(x['ket_qua'] for x in xls)
        cats=["Đoàn viên Xuất sắc","Đoàn viên Hoàn thành tốt","Đoàn viên Hoàn thành","Đoàn viên Không hoàn thành"]
        vals=[cnt.get(c,0) for c in cats]
        clrs=[COLORS['accent'],COLORS['success'],COLORS['info'],COLORS['danger']]
        labels=["Xuất sắc","Hoàn thành tốt","Hoàn thành","Không HT"]
        fig=self.fig_xl; fig.clear()
        ax=fig.add_subplot(111); ax.set_facecolor(COLORS['bg_card']); fig.patch.set_facecolor(COLORS['bg_card'])
        bars=ax.bar(labels,vals,color=clrs,width=0.5,edgecolor='none',zorder=2)
        ax.tick_params(colors=COLORS['text_secondary'])
        ax.set_title("Phân bố Xếp loại Đoàn viên (HK1/2024-2025)",color=COLORS['text_primary'],fontsize=11,fontweight='bold')
        ax.spines[:].set_visible(False); ax.yaxis.grid(True,color=COLORS['border'],linestyle='--',alpha=0.4,zorder=1); ax.set_axisbelow(True)
        for b,v in zip(bars,vals):
            ax.text(b.get_x()+b.get_width()/2,b.get_height()+0.05,str(v),ha='center',va='bottom',color=COLORS['text_primary'],fontsize=12,fontweight='bold')
        fig.tight_layout(pad=2.0); self.canvas_xl.draw()
