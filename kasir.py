import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import sqlite3
import pandas as pd
from PIL import Image, ImageTk
import os

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('toko.db')
    c = conn.cursor()
    # Tabel Produk
    c.execute('''CREATE TABLE IF NOT EXISTS produk (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    harga REAL)''')
    # Tabel Transaksi
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    produk_id INTEGER,
                    jumlah INTEGER,
                    total REAL)''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan data produk ke dalam database
def save_produk():
    nama = entry_nama_produk.get()
    harga = entry_harga_produk.get()

    if nama == "" or harga == "":
        messagebox.showwarning("Input Error", "Nama dan Harga Produk harus diisi.")
        return

    conn = sqlite3.connect('toko.db')
    c = conn.cursor()
    c.execute("INSERT INTO produk (nama, harga) VALUES (?, ?)", (nama, float(harga)))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukses", "Produk berhasil disimpan.")
    entry_nama_produk.delete(0, tk.END)
    entry_harga_produk.delete(0, tk.END)

# Fungsi untuk menambah transaksi kasir
def tambah_transaksi():
    produk_id = combo_produk.get()
    jumlah = entry_jumlah.get()

    if not produk_id or not jumlah:
        messagebox.showwarning("Input Error", "Produk dan Jumlah harus diisi.")
        return

    conn = sqlite3.connect('toko.db')
    c = conn.cursor()
    c.execute("SELECT harga FROM produk WHERE id=?", (produk_id,))
    harga = c.fetchone()[0]
    total = harga * int(jumlah)
    
    c.execute("INSERT INTO transaksi (produk_id, jumlah, total, tanggal) VALUES (?, ?, ?, datetime('now'))", 
              (produk_id, int(jumlah), total))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukses", f"Transaksi berhasil, Total: {total}")
    entry_jumlah.delete(0, tk.END)

# Fungsi untuk menampilkan transaksi
def lihat_transaksi():
    conn = sqlite3.connect('toko.db')
    c = conn.cursor()
    c.execute("SELECT t.id, p.nama, t.jumlah, t.total, t.tanggal FROM transaksi t JOIN produk p ON t.produk_id = p.id")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

# Fungsi untuk ekspor transaksi ke Excel
def export_to_excel():
    conn = sqlite3.connect('toko.db')
    c = conn.cursor()
    c.execute("SELECT t.id, p.nama, t.jumlah, t.total, t.tanggal FROM transaksi t JOIN produk p ON t.produk_id = p.id")
    rows = c.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["ID Transaksi", "Nama Produk", "Jumlah", "Total", "Tanggal"])
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {file_path}")

# Fungsi untuk menampilkan splash screen
def splash_screen():
    splash = tk.Toplevel(root)
    splash.geometry("400x300")
    splash.title("Splash Screen")
    splash_label = tk.Label(splash, text="Selamat Datang di Aplikasi Kasir Toko", font=("Arial", 20))
    splash_label.pack(expand=True)
    splash.after(2000, splash.destroy)

# Membuat jendela aplikasi utama
root = tk.Tk()
root.title("Aplikasi Kasir Toko")
root.geometry("800x600")

# Membuat menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu dropdown
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export to Excel", command=export_to_excel)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Membuat toolbar dengan ikon
toolbar = tk.Frame(root, bg="gray", height=50)
toolbar.pack(fill="x")

# Menambahkan logo ke toolbar
logo_img = Image.open("logo.png")  # Pastikan file logo.png ada di direktori yang sama
logo_img = logo_img.resize((40, 40), Image.ANTIALIAS)
logo_icon = ImageTk.PhotoImage(logo_img)
toolbar_logo = tk.Label(toolbar, image=logo_icon)
toolbar_logo.pack(side="left", padx=10)

# Form input untuk menambah produk
frame_produk = tk.Frame(root)
frame_produk.pack(pady=10)

label_nama_produk = tk.Label(frame_produk, text="Nama Produk:")
label_nama_produk.grid(row=0, column=0, padx=10, pady=5)
entry_nama_produk = tk.Entry(frame_produk)
entry_nama_produk.grid(row=0, column=1, padx=10, pady=5)

label_harga_produk = tk.Label(frame_produk, text="Harga Produk:")
label_harga_produk.grid(row=1, column=0, padx=10, pady=5)
entry_harga_produk = tk.Entry(frame_produk)
entry_harga_produk.grid(row=1, column=1, padx=10, pady=5)

button_simpan_produk = tk.Button(frame_produk, text="Simpan Produk", command=save_produk)
button_simpan_produk.grid(row=2, columnspan=2, pady=10)

# Form input untuk transaksi kasir
frame_transaksi = tk.Frame(root)
frame_transaksi.pack(pady=10)

label_produk = tk.Label(frame_transaksi, text="Pilih Produk:")
label_produk.grid(row=0, column=0, padx=10, pady=5)

# Menampilkan produk di dropdown
conn = sqlite3.connect('toko.db')
c = conn.cursor()
c.execute("SELECT id, nama FROM produk")
produk_data = c.fetchall()
conn.close()

produk_list = [str(p[0]) + " - " + p[1] for p in produk_data]
combo_produk = ttk.Combobox(frame_transaksi, values=produk_list)
combo_produk.grid(row=0, column=1, padx=10, pady=5)

label_jumlah = tk.Label(frame_transaksi, text="Jumlah:")
label_jumlah.grid(row=1, column=0, padx=10, pady=5)
entry_jumlah = tk.Entry(frame_transaksi)
entry_jumlah.grid(row=1, column=1, padx=10, pady=5)

button_tambah_transaksi = tk.Button(frame_transaksi, text="Tambah Transaksi", command=tambah_transaksi)
button_tambah_transaksi.grid(row=2, columnspan=2, pady=10)

# Menjalankan splash screen saat aplikasi dimulai
splash_screen()

# Menjalankan aplikasi
create_database()
root.mainloop()
