import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json


class AplikasiPembukuan:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pembukuan")
        self.root.geometry("800x400")
        self.root.resizable(False, False) 

        # Data stok barang (simpan dalam list of dictionaries)
        self.stock_data = []

        # Buat Menu Bar
        self.create_menu_bar()

        # Buat Notebook (Tab)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Tab Stock Barang
        self.tab_stock = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stock, text='Stock Barang')
        self.setup_tab_stock()

        # Tab Penjualan
        self.tab_penjualan = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_penjualan, text='Penjualan')
        self.setup_tab_penjualan()

        # Tab Pengeluaran
        self.tab_pengeluaran = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pengeluaran, text='Pengeluaran')
        self.setup_tab_pengeluaran()

        # Tab Laporan Penjualan
        self.tab_laporan_penjualan = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_laporan_penjualan, text='Laporan Penjualan')
        self.setup_tab_laporan_penjualan()

        # Tab Laporan Untung/Rugi
        self.tab_laporan_untung_rugi = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_laporan_untung_rugi, text='Laporan Untung/Rugi')
        self.setup_tab_laporan_untung_rugi()

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_data)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu About
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="About", menu=about_menu)

        self.root.config(menu=menubar)

    def show_about(self):
        # Tampilkan dialog About
        messagebox.showinfo("About", "Aplikasi Pembukuan\nVersi 1.0\nDibuat oleh TrappDesign - Mirza Kamal 2025")
        messagebox.showinfo("Donasi", "\nDonasi bisa di salurkan ke rekening BCA 8380239460 untuk pengembangan lebih lanjut")
        messagebox.showinfo("Kontak", "\n mirzakamal647@gmail.com \n 082117123880 \n ")
               
               
        
    def setup_tab_stock(self):
        label = ttk.Label(self.tab_stock, text="Manajemen Stock Barang")
        label.pack(pady=10)

        # Input Form untuk Tambah Stock
        frame_input = ttk.Frame(self.tab_stock)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Nama Barang:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nama_barang = ttk.Entry(frame_input)
        self.entry_nama_barang.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_jumlah_stock = ttk.Entry(frame_input)
        self.entry_jumlah_stock.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Harga Satuan:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_harga_satuan = ttk.Entry(frame_input)
        self.entry_harga_satuan.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_input, text="Tambah Stock", command=self.tambah_stock).grid(row=3, column=0, columnspan=2, pady=10)

        # Tabel Stock Barang
        columns = ("ID", "Nama Barang", "Jumlah", "Harga Satuan")
        self.tree_stock = ttk.Treeview(self.tab_stock, columns=columns, show='headings')
        for col in columns:
            self.tree_stock.heading(col, text=col)
        self.tree_stock.pack(fill='both', expand=True)

        # Load data ke tabel
        self.load_data_to_table()

    def setup_tab_penjualan(self):
        label = ttk.Label(self.tab_penjualan, text="Manajemen Penjualan")
        label.pack(pady=10)

        # Contoh input penjualan
        ttk.Label(self.tab_penjualan, text="ID Barang:").pack()
        self.entry_id_barang = ttk.Entry(self.tab_penjualan)
        self.entry_id_barang.pack()

        ttk.Label(self.tab_penjualan, text="Jumlah:").pack()
        self.entry_jumlah = ttk.Entry(self.tab_penjualan)
        self.entry_jumlah.pack()

        ttk.Button(self.tab_penjualan, text="Tambah Penjualan", command=self.tambah_penjualan).pack(pady=10)

    def setup_tab_pengeluaran(self):
        label = ttk.Label(self.tab_pengeluaran, text="Manajemen Pengeluaran")
        label.pack(pady=10)

        # Contoh input pengeluaran
        ttk.Label(self.tab_pengeluaran, text="Keterangan:").pack()
        self.entry_keterangan = ttk.Entry(self.tab_pengeluaran)
        self.entry_keterangan.pack()

        ttk.Label(self.tab_pengeluaran, text="Jumlah:").pack()
        self.entry_jumlah_pengeluaran = ttk.Entry(self.tab_pengeluaran)
        self.entry_jumlah_pengeluaran.pack()

        ttk.Button(self.tab_pengeluaran, text="Tambah Pengeluaran", command=self.tambah_pengeluaran).pack(pady=10)

    def setup_tab_laporan_penjualan(self):
        label = ttk.Label(self.tab_laporan_penjualan, text="Laporan Penjualan")
        label.pack(pady=10)

        # Contoh grafik penjualan
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [10, 20, 15])
        ax.set_title("Laporan Penjualan Mingguan")

        canvas = FigureCanvasTkAgg(fig, master=self.tab_laporan_penjualan)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def setup_tab_laporan_untung_rugi(self):
        label = ttk.Label(self.tab_laporan_untung_rugi, text="Laporan Untung/Rugi")
        label.pack(pady=10)

        # Contoh grafik untung/rugi
        fig, ax = plt.subplots()
        ax.bar(["Minggu 1", "Minggu 2", "Minggu 3"], [500000, 600000, 450000])
        ax.set_title("Laporan Untung/Rugi per Minggu")

        canvas = FigureCanvasTkAgg(fig, master=self.tab_laporan_untung_rugi)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def tambah_stock(self):
        nama_barang = self.entry_nama_barang.get()
        jumlah = self.entry_jumlah_stock.get()
        harga_satuan = self.entry_harga_satuan.get()

        if not nama_barang or not jumlah or not harga_satuan:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
            return

        try:
            jumlah = int(jumlah)
            harga_satuan = int(harga_satuan)
        except ValueError:
            messagebox.showwarning("Input Error", "Jumlah dan Harga Satuan harus berupa angka!")
            return

        # Tambahkan data ke list
        new_id = len(self.stock_data) + 1
        self.stock_data.append({
            "ID": new_id,
            "Nama Barang": nama_barang,
            "Jumlah": jumlah,
            "Harga Satuan": harga_satuan
        })

        # Update tabel
        self.load_data_to_table()

        # Clear input fields
        self.entry_nama_barang.delete(0, tk.END)
        self.entry_jumlah_stock.delete(0, tk.END)
        self.entry_harga_satuan.delete(0, tk.END)

    def load_data_to_table(self):
        # Clear tabel
        for row in self.tree_stock.get_children():
            self.tree_stock.delete(row)

        # Isi tabel dengan data
        for item in self.stock_data:
            self.tree_stock.insert("", "end", values=(
                item["ID"], item["Nama Barang"], item["Jumlah"], item["Harga Satuan"]
            ))

    def save_data(self):
        # Simpan data ke file (contoh: JSON)
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            import json
            with open(file_path, "w") as file:
                json.dump(self.stock_data, file)
            messagebox.showinfo("Save", "Data berhasil disimpan!")

    def open_data(self):
        # Buka file JSON
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                self.stock_data = json.load(file)
            self.load_data_to_table()
            messagebox.showinfo("Open", "Data berhasil dibuka!")

    def export_to_excel(self):
        # Export data ke Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.stock_data)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export", "Data berhasil diexport ke Excel!")

    def tambah_penjualan(self):
        id_barang = self.entry_id_barang.get()
        jumlah = self.entry_jumlah.get()
        print(f"Penjualan ditambahkan: ID Barang {id_barang}, Jumlah {jumlah}")

    def tambah_pengeluaran(self):
        keterangan = self.entry_keterangan.get()
        jumlah = self.entry_jumlah_pengeluaran.get()
        print(f"Pengeluaran ditambahkan: Keterangan {keterangan}, Jumlah {jumlah}")

    
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiPembukuan(root)
    root.mainloop()