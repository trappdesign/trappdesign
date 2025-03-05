import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd

# Inisialisasi data penjualan dan data pelanggan
data_penjualan = []
data_pelanggan = []

# Fungsi untuk menghitung total harga
def hitung_total():
    try:
        jumlah = int(entry_jumlah.get())
        harga_satuan = int(entry_harga_satuan.get())
        total = jumlah * harga_satuan
        entry_total_harga.delete(0, tk.END)
        entry_total_harga.insert(0, f"Rp {total:,}")
    except ValueError:
        messagebox.showwarning("Input Salah", "Harap masukkan angka yang valid untuk jumlah dan harga satuan!")

# Fungsi untuk menambahkan data penjualan
def tambah_penjualan():
    tanggal = entry_tanggal.get()
    nama_barang = entry_nama_barang.get()
    jumlah = entry_jumlah.get()
    harga_satuan = entry_harga_satuan.get()
    total_harga = entry_total_harga.get()

    if not tanggal or not nama_barang or not jumlah or not harga_satuan or not total_harga:
        messagebox.showwarning("Input Kosong", "Harap lengkapi semua field!")
        return

    # Tambahkan data ke list
    data_penjualan.append([tanggal, nama_barang, jumlah, harga_satuan, total_harga])
    update_tabel_penjualan()

    # Kosongkan field setelah menambahkan data
    clear_field_penjualan()

# Fungsi untuk mengosongkan field penjualan
def clear_field_penjualan():
    entry_tanggal.delete(0, tk.END)
    entry_nama_barang.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
    entry_harga_satuan.delete(0, tk.END)
    entry_total_harga.delete(0, tk.END)

# Fungsi untuk menyimpan data penjualan ke file
def save_data():
    if not data_penjualan:
        messagebox.showwarning("Data Kosong", "Tidak ada data penjualan untuk disimpan!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write("Tanggal,Nama Barang,Jumlah,Harga Satuan,Total Harga\n")
            for data in data_penjualan:
                file.write(",".join(map(str, data)) + "\n")
        messagebox.showinfo("Saved", "Data penjualan berhasil disimpan!")

# Fungsi untuk mengekspor data penjualan ke Excel
def export_to_excel():
    if not data_penjualan:
        messagebox.showwarning("Data Kosong", "Tidak ada data penjualan untuk diekspor!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df = pd.DataFrame(data_penjualan, columns=["Tanggal", "Nama Barang", "Jumlah", "Harga Satuan", "Total Harga"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Exported", "Data penjualan berhasil diekspor ke Excel!")

# Fungsi untuk memperbarui tabel laporan penjualan
def update_tabel_penjualan():
    for row in tabel_penjualan.get_children():
        tabel_penjualan.delete(row)
    for data in data_penjualan:
        tabel_penjualan.insert("", "end", values=data)

# Fungsi untuk menampilkan form data pelanggan
def show_form_pelanggan():
    form_pelanggan_frame.pack(padx=10, pady=10, fill="x")
    laporan_penjualan_frame.pack_forget()  # Sembunyikan frame laporan penjualan

# Fungsi untuk menyimpan data pelanggan
def simpan_pelanggan():
    nama = entry_nama_pelanggan.get()
    alamat = entry_alamat.get()
    telepon = entry_telepon.get()

    if not nama or not alamat or not telepon:
        messagebox.showwarning("Input Kosong", "Harap lengkapi semua field!")
        return

    # Tambahkan data pelanggan ke list
    data_pelanggan.append([nama, alamat, telepon])
    update_tabel_pelanggan()

    # Kosongkan field setelah menyimpan data
    clear_field_pelanggan()

# Fungsi untuk mengosongkan field pelanggan
def clear_field_pelanggan():
    entry_nama_pelanggan.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_telepon.delete(0, tk.END)

# Fungsi untuk memperbarui tabel data pelanggan
def update_tabel_pelanggan():
    for row in tabel_pelanggan.get_children():
        tabel_pelanggan.delete(row)
    for data in data_pelanggan:
        tabel_pelanggan.insert("", "end", values=data)

# Fungsi untuk keluar dari aplikasi
def exit_app():
    app.quit()

# Fungsi untuk menampilkan informasi tentang aplikasi
def show_about():
    messagebox.showinfo("About", "Jurnal Penjualan \nVersi 1.0\nDibuat Mirza Kamal - TrappDesign 2025")
def show_kontak():
    messagebox.showinfo("Kontak", "\n Mirza Kamal\n WA 082117123880")
def show_donasi():
    messagebox.showinfo("Donasi", " \nDonasi bisa di salurkan ke rekening BCA 8380239460 untuk pengembangan lebih lanjut")


# Membuat GUI
app = tk.Tk()
app.title("Aplikasi Pembukuan Toko")
app.geometry("1000x500")
app.resizable(False, False)


# Menu Bar
menubar = tk.Menu(app)

# Menu File
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Save", command=save_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
file_menu.add_separator()
menubar.add_cascade(label="File", menu=file_menu)

# Menu Data
data_menu = tk.Menu(menubar, tearoff=0)
data_menu.add_command(label="Data Pelanggan", command=show_form_pelanggan)
menubar.add_cascade(label="Data", menu=data_menu)

app.config(menu=menubar)

# Menu export
export_to_excel_menu = tk.Menu(menubar, tearoff=0)
export_to_excel_menu.add_command(label="Export to Excel", command=export_to_excel)
menubar.add_cascade(label="Export", menu=export_to_excel_menu)

app.config(menu=menubar)

# Menu About
about_menu = tk.Menu(menubar, tearoff=0)
about_menu.add_command(label="about", command=show_about)
about_menu.add_separator()
about_menu.add_command(label="Kontak", command=show_kontak)
about_menu.add_separator()
about_menu.add_command(label="Donasi", command=show_donasi)
menubar.add_cascade(label="about", menu=about_menu)
about_menu.add_separator()

app.config(menu=menubar)

# Frame untuk input data penjualan
input_frame = tk.LabelFrame(app, text="Input Data Penjualan", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="x")

# Label dan Entry untuk Tanggal
tk.Label(input_frame, text="Tanggal:").grid(row=0, column=0, sticky="w", pady=5)
entry_tanggal = tk.Entry(input_frame, width=30)
entry_tanggal.grid(row=0, column=1, pady=5)

# Label dan Entry untuk Nama Barang
tk.Label(input_frame, text="Nama Barang:").grid(row=1, column=0, sticky="w", pady=5)
entry_nama_barang = tk.Entry(input_frame, width=30)
entry_nama_barang.grid(row=1, column=1, pady=5)

# Label dan Entry untuk Jumlah
tk.Label(input_frame, text="Jumlah:").grid(row=2, column=0, sticky="w", pady=5)
entry_jumlah = tk.Entry(input_frame, width=30)
entry_jumlah.grid(row=2, column=1, pady=5)

# Label dan Entry untuk Harga Satuan
tk.Label(input_frame, text="Harga Satuan:").grid(row=3, column=0, sticky="w", pady=5)
entry_harga_satuan = tk.Entry(input_frame, width=30)
entry_harga_satuan.grid(row=3, column=1, pady=5)

# Label dan Entry untuk Total Harga
tk.Label(input_frame, text="Total Harga:").grid(row=4, column=0, sticky="w", pady=5)
entry_total_harga = tk.Entry(input_frame, width=30 )
entry_total_harga.grid(row=4, column=1, pady=5)

# Tombol Hitung Total
button_hitung = tk.Button(input_frame, text="Hitung Total", command=hitung_total)
button_hitung.grid(row=5, column=1, pady=10)

# Tombol Tambah Penjualan
button_tambah = tk.Button(input_frame, text="Tambah Penjualan", command=tambah_penjualan)
button_tambah.grid(row=6, column=1, pady=10)

# Frame untuk laporan penjualan
laporan_penjualan_frame = tk.LabelFrame(app, text="Laporan Penjualan", padx=10, pady=10)
laporan_penjualan_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Tabel untuk menampilkan laporan penjualan
columns_penjualan = ("Tanggal", "Nama Barang", "Jumlah", "Harga Satuan", "Total Harga")
tabel_penjualan = ttk.Treeview(laporan_penjualan_frame, columns=columns_penjualan, show="headings")
tabel_penjualan.heading("Tanggal", text="Tanggal")
tabel_penjualan.heading("Nama Barang", text="Nama Barang")
tabel_penjualan.heading("Jumlah", text="Jumlah")
tabel_penjualan.heading("Harga Satuan", text="Harga Satuan")
tabel_penjualan.heading("Total Harga", text="Total Harga")
tabel_penjualan.pack(fill="both", expand=True)

# Frame untuk form data pelanggan (awalnya disembunyikan)
form_pelanggan_frame = tk.LabelFrame(app, text="Form Data Pelanggan", padx=10, pady=10)

# Label dan Entry untuk Nama Pelanggan
tk.Label(form_pelanggan_frame, text="Nama Pelanggan:").grid(row=0, column=0, sticky="w", pady=5)
entry_nama_pelanggan = tk.Entry(form_pelanggan_frame, width=30)
entry_nama_pelanggan.grid(row=0, column=1, pady=5)

# Label dan Entry untuk Alamat
tk.Label(form_pelanggan_frame, text="Alamat:").grid(row=1, column=0, sticky="w", pady=5)
entry_alamat = tk.Entry(form_pelanggan_frame, width=30)
entry_alamat.grid(row=1, column=1, pady=5)

# Label dan Entry untuk Nomor Telepon
tk.Label(form_pelanggan_frame, text="Nomor Telepon:").grid(row=2, column=0, sticky="w", pady=5)
entry_telepon = tk.Entry(form_pelanggan_frame, width=30)
entry_telepon.grid(row=2, column=1, pady=5)

# Tombol Simpan Pelanggan
button_simpan_pelanggan = tk.Button(form_pelanggan_frame, text="Simpan", command=simpan_pelanggan)
button_simpan_pelanggan.grid(row=3, column=1, pady=10)

# Frame untuk tabel data pelanggan
tabel_pelanggan_frame = tk.LabelFrame(app, text="Data Pelanggan", padx=10, pady=10)

# Tabel untuk menampilkan data pelanggan
columns_pelanggan = ("Nama Pelanggan", "Alamat", "Nomor Telepon")
tabel_pelanggan = ttk.Treeview(tabel_pelanggan_frame, columns=columns_pelanggan, show="headings")
tabel_pelanggan.heading("Nama Pelanggan", text="Nama Pelanggan")
tabel_pelanggan.heading("Alamat", text="Alamat")
tabel_pelanggan.heading("Nomor Telepon", text="Nomor Telepon")
tabel_pelanggan.pack(fill="both", expand=True)

# Jalankan aplikasi
app.mainloop()