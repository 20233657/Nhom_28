"""
styles.py - Theme Đoàn TNCS Hồ Chí Minh - Sạch, rõ, không ô border thừa
"""

COLORS = {
    "primary":        "#C62828",
    "primary_light":  "#E53935",
    "primary_dark":   "#8E0000",
    "accent":         "#F9A825",
    "accent_light":   "#FFD54F",
    "accent_dark":    "#F57F17",

    "success":        "#2E7D32",
    "success_light":  "#43A047",
    "warning":        "#E65100",
    "warning_light":  "#FF8F00",
    "info":           "#1565C0",
    "info_light":     "#1E88E5",
    "danger":         "#C62828",

    "bg_dark":        "#1A1A2E",
    "bg_main":        "#F4F6F8",
    "bg_card":        "#FFFFFF",
    "bg_sidebar":     "#1C1C2E",
    "bg_input":       "#FFFFFF",

    "border":         "#E0E3E8",
    "border_dark":    "#BEC3CC",

    "text_primary":   "#1A1A2E",
    "text_secondary": "#5A6478",
    "text_muted":     "#9AA3B0",
    "text_on_dark":   "#E8ECF0",
    "text_accent":    "#F9A825",

    "table_header":   "#8E0000",
    "table_row":      "#FFFFFF",
    "table_row_alt":  "#FEF9F9",
    "table_select":   "#FFEBEE",
    "table_select_fg":"#8E0000",

    "white":          "#FFFFFF",
    "star":           "#F9A825",
}

MAIN_STYLE = f"""
/* === RESET BASE === */
QMainWindow, QDialog {{
    background-color: {COLORS['bg_main']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}

/* Widget gốc - KHÔNG có border, KHÔNG có background cứng */
QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: {COLORS['text_primary']};
}}

/* === LABEL - TUYỆT ĐỐI không có border, không có background === */
QLabel {{
    background: transparent;
    border: none;
    color: {COLORS['text_primary']};
    padding: 0;
}}

/* === BUTTON === */
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 7px;
    padding: 8px 20px;
    font-size: 10pt;
    font-weight: 600;
}}
QPushButton:hover  {{ background-color: {COLORS['primary_light']}; }}
QPushButton:pressed {{ background-color: {COLORS['primary_dark']}; }}
QPushButton:disabled {{
    background-color: {COLORS['border_dark']};
    color: {COLORS['text_muted']};
}}
QPushButton#btn_success {{
    background-color: {COLORS['success']};
}}
QPushButton#btn_success:hover {{ background-color: {COLORS['success_light']}; }}
QPushButton#btn_danger {{
    background-color: {COLORS['danger']};
}}
QPushButton#btn_danger:hover {{ background-color: {COLORS['primary_light']}; }}
QPushButton#btn_warning {{
    background-color: {COLORS['warning']};
    color: white;
}}
QPushButton#btn_warning:hover {{ background-color: {COLORS['warning_light']}; }}
QPushButton#btn_info {{
    background-color: {COLORS['info']};
}}
QPushButton#btn_info:hover {{ background-color: {COLORS['info_light']}; }}
QPushButton#btn_secondary {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1.5px solid {COLORS['border_dark']};
}}
QPushButton#btn_secondary:hover {{
    border-color: {COLORS['primary']};
    color: {COLORS['primary']};
}}
QPushButton#btn_accent {{
    background-color: {COLORS['accent']};
    color: {COLORS['primary_dark']};
    font-weight: 700;
}}

/* === INPUT === */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1.5px solid {COLORS['border_dark']};
    border-radius: 7px;
    padding: 7px 12px;
    font-size: 10pt;
    selection-background-color: {COLORS['primary']};
    selection-color: white;
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {COLORS['primary']};
}}
QLineEdit:disabled, QTextEdit:disabled {{
    background-color: #F0F0F4;
    color: {COLORS['text_muted']};
}}

/* === COMBOBOX === */
QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1.5px solid {COLORS['border_dark']};
    border-radius: 7px;
    padding: 6px 12px;
    font-size: 10pt;
}}
QComboBox:focus {{ border: 2px solid {COLORS['primary']}; }}
QComboBox::drop-down {{
    border: none;
    width: 26px;
    background: transparent;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text_secondary']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border_dark']};
    selection-background-color: {COLORS['primary']};
    selection-color: white;
    outline: none;
    padding: 2px;
}}

/* === DATE EDIT === */
QDateEdit {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1.5px solid {COLORS['border_dark']};
    border-radius: 7px;
    padding: 6px 12px;
}}
QDateEdit:focus {{ border: 2px solid {COLORS['primary']}; }}
QDateEdit::drop-down {{ border: none; width: 26px; background: transparent; }}
QCalendarWidget {{
    background: {COLORS['bg_card']};
    color: {COLORS['text_primary']};
}}

/* === CHECKBOX === */
QCheckBox {{
    color: {COLORS['text_primary']};
    spacing: 8px;
    background: transparent;
    border: none;
}}
QCheckBox::indicator {{
    width: 18px; height: 18px;
    border: 2px solid {COLORS['border_dark']};
    border-radius: 4px;
    background: white;
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS['success']};
    border-color: {COLORS['success']};
}}

/* === TABLE === */
QTableWidget {{
    background-color: {COLORS['table_row']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    gridline-color: {COLORS['border']};
    outline: none;
    alternate-background-color: {COLORS['table_row_alt']};
}}
QTableWidget::item {{
    padding: 8px 10px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: {COLORS['table_select']};
    color: {COLORS['table_select_fg']};
    font-weight: 600;
}}
QTableWidget::item:hover:!selected {{
    background-color: #FFF3F3;
}}
QHeaderView::section {{
    background-color: {COLORS['table_header']};
    color: white;
    padding: 10px 10px;
    border: none;
    border-right: 1px solid rgba(255,255,255,0.12);
    font-weight: 700;
    font-size: 9pt;
    letter-spacing: 0.3px;
}}
QHeaderView::section:last-child {{ border-right: none; }}
QHeaderView::section:hover {{ background-color: {COLORS['primary']}; }}

/* === GROUPBOX === */
QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1.5px solid {COLORS['border']};
    border-radius: 10px;
    margin-top: 20px;
    padding-top: 12px;
    font-weight: 700;
    color: {COLORS['primary']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 8px;
    color: {COLORS['primary']};
    font-size: 10pt;
    background: {COLORS['bg_card']};
}}

/* === TAB === */
QTabWidget::pane {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 0 8px 8px 8px;
}}
QTabBar::tab {{
    background-color: #E8EAED;
    color: {COLORS['text_secondary']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    padding: 8px 20px;
    border-radius: 7px 7px 0 0;
    margin-right: 3px;
    font-size: 10pt;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['primary']};
    color: white;
    font-weight: 700;
    border-color: {COLORS['primary']};
}}
QTabBar::tab:hover:!selected {{
    background-color: #FFDDDD;
    color: {COLORS['primary']};
}}

/* === SCROLLBAR === */
QScrollBar:vertical {{
    background: #EEEEEE;
    width: 8px;
    border-radius: 4px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #CCCCCC;
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {COLORS['primary']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: #EEEEEE;
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #CCCCCC;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{ background: {COLORS['primary']}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* === MESSAGEBOX === */
QMessageBox {{
    background-color: {COLORS['bg_card']};
}}
QMessageBox QLabel {{
    color: {COLORS['text_primary']};
    background: transparent;
    border: none;
}}

/* === PROGRESSBAR === */
QProgressBar {{
    background: #EEEEEE;
    border: none;
    border-radius: 5px;
    height: 8px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {COLORS['primary']}, stop:1 {COLORS['accent']});
    border-radius: 5px;
}}

/* === SCROLL AREA === */
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* === SPINBOX BUTTONS === */
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    background: #EEEEEE;
    border: none;
    border-radius: 3px;
    width: 18px;
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background: {COLORS['primary']};
}}

/* === FRAME - chỉ style khi dùng đường kẻ ngang/dọc === */
QFrame[frameShape="4"] {{
    background: {COLORS['border']};
    border: none;
    max-height: 1px;
}}
QFrame[frameShape="5"] {{
    background: {COLORS['border']};
    border: none;
    max-width: 1px;
}}
"""
