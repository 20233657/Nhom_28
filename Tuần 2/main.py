import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("doanvien.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS doanvien (
    ma TEXT PRIMARY KEY,
    ten TEXT,
    lop TEXT,
    khoa TEXT,
    ngaysinh TEXT
)
""")
conn.commit()

# ================= GUI =================
root = tk.Tk()
root.title("Quản Lý Đoàn Viên")
root.geometry("850x600")

tk.Label(root, text="QUẢN LÝ ĐOÀN VIÊN", font=("Arial", 16, "bold")).pack(pady=10)

# ===== FORM =====
frame_form = tk.Frame(root)
frame_form.pack()

labels = ["Mã", "Họ tên", "Lớp", "Khoa"]
entries = []

for i, text in enumerate(labels):
    tk.Label(frame_form, text=text + ":", width=15, anchor="w").grid(row=i, column=0)
    entry = tk.Entry(frame_form, width=30)
    entry.grid(row=i, column=1, pady=5)
    entries.append(entry)

# ===== DATE =====
tk.Label(frame_form, text="Ngày sinh:", width=15, anchor="w").grid(row=4, column=0)
date_entry = DateEntry(frame_form, width=27, date_pattern="dd/mm/yyyy")
date_entry.grid(row=4, column=1, pady=5)

# ===== SEARCH =====
frame_search = tk.Frame(root)
frame_search.pack(pady=5)

tk.Label(frame_search, text="Tìm (Mã hoặc Tên):").pack(side=tk.LEFT)
search_entry = tk.Entry(frame_search, width=25)
search_entry.pack(side=tk.LEFT, padx=5)

# ================= TABLE =================
columns = ("ma", "ten", "lop", "khoa", "ns")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("ma", text="Mã")
tree.heading("ten", text="Họ tên")
tree.heading("lop", text="Lớp")
tree.heading("khoa", text="Khoa")
tree.heading("ns", text="Ngày sinh")

tree.pack(pady=10, fill="both", expand=True)

# ================= FUNCTIONS =================

def load_data():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM doanvien")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def clear_input():
    for e in entries:
        e.delete(0, tk.END)
    date_entry.set_date("01/01/2000")

def them():
    values = [e.get() for e in entries]
    values.append(date_entry.get())

    if "" in values:
        messagebox.showwarning("Lỗi", "Nhập đầy đủ!")
        return

    try:
        cursor.execute("INSERT INTO doanvien VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        load_data()
        clear_input()
    except:
        messagebox.showerror("Lỗi", "Mã bị trùng!")

def xoa():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chọn dòng cần xóa!")
        return

    ma = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM doanvien WHERE ma=?", (ma,))
    conn.commit()
    load_data()

def sua():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chọn dòng cần sửa!")
        return

    values = [e.get() for e in entries]
    values.append(date_entry.get())

    cursor.execute("""
    UPDATE doanvien
    SET ten=?, lop=?, khoa=?, ngaysinh=?
    WHERE ma=?
    """, (values[1], values[2], values[3], values[4], values[0]))

    conn.commit()
    load_data()
    messagebox.showinfo("OK", "Sửa thành công!")

def tim():
    keyword = search_entry.get()

    if keyword == "":
        load_data()
        return

    tree.delete(*tree.get_children())

    cursor.execute("""
    SELECT * FROM doanvien 
    WHERE ma LIKE ? OR ten LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def chon_dong(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])["values"]

        for i in range(4):
            entries[i].delete(0, tk.END)
            entries[i].insert(0, values[i])

        date_entry.set_date(values[4])

tree.bind("<<TreeviewSelect>>", chon_dong)

# ================= BUTTON =================
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Thêm", width=10, command=them).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Sửa", width=10, command=sua).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Xóa", width=10, command=xoa).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Tìm", width=10, command=tim).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Reload", width=10, command=load_data).grid(row=0, column=4, padx=5)

# load dữ liệu ban đầu
load_data()

root.mainloop()