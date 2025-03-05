import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import pandas as pd
import json

class PricelistApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" TrappDesign Accountant v3 ")
        self.root.geometry("500x700")
        self.root.resizable(True, False) 

        # Data storage
        self.pricelist = []
        self.next_id = 1  # Untuk generate No. ID
        self.pembayaran = []  # Menyimpan data pembayaran
        self.pengeluaran = []  # Menyimpan data pengeluaran


  # Frame untuk login (akan ditampilkan pertama kali)
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill='both', expand=True)

        # Frame untuk aplikasi utama (akan ditampilkan setelah login)
        self.main_frame = ttk.Frame(self.root)

        # Tampilkan form login terlebih dahulu
        self.show_login()

      
    def show_login(self):
        """Menampilkan form login di dalam jendela utama."""
        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.entry_username = ttk.Entry(self.login_frame, width=30)
        self.entry_username.pack(pady=5)

        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.entry_password = ttk.Entry(self.login_frame, width=30, show="*")
        self.entry_password.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.authenticate).pack(pady=10)
       
    def authenticate(self):
        """Memvalidasi username dan password."""
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Contoh validasi sederhana
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login", "Login berhasil!")
            self.login_frame.pack_forget()  # Sembunyikan frame login
            self.initialize_app()  # Tampilkan aplikasi utama
        else:
            messagebox.showerror("Login", "Username atau password salah!")

    def initialize_app(self):
        """Menginisialisasi aplikasi setelah login berhasil."""
        # Tampilkan frame utama
        self.main_frame.pack(fill='both', expand=True)


       # Buat Menu Bar
        self.create_menu_bar()

    def create_menu_bar(self):
        """Membuat menu bar."""
        menubar = tk.Menu(self.root)
    
        # Menu Bar
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Convert to TXT", command=self.convert_to_txt)
        filemenu.add_separator()     
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

        
        # Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook( self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1: Daftar Harga
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Daftar Harga")

        # Form Input Daftar Harga
        input_frame = ttk.LabelFrame(self.tab1, text="Form Input Daftar Harga")
        input_frame.pack(fill="x", padx=10, pady=5)

        # Ukuran
        ttk.Label(input_frame, text="Ukuran:").grid(row=0, column=0, padx=5, pady=5)
        self.ukuran_vars = {
            "A0": tk.BooleanVar(),
            "A1": tk.BooleanVar(),
            "A2": tk.BooleanVar(),
            "A3": tk.BooleanVar(),
            "A4": tk.BooleanVar()
        }
        for i, (text, var) in enumerate(self.ukuran_vars.items()):
            ttk.Checkbutton(input_frame, text=text, variable=var).grid(row=0, column=i+1, padx=5, pady=5)

        # Jenis
        ttk.Label(input_frame, text="Jenis:").grid(row=1, column=0, padx=5, pady=5)
        self.jenis_combobox = ttk.Combobox(input_frame, values=["Kalkir", "HVS", "Kodak Trace"])
        self.jenis_combobox.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        # Harga
        ttk.Label(input_frame, text="Harga:").grid(row=2, column=0, padx=5, pady=5)
        self.harga_entry = ttk.Entry(input_frame)
        self.harga_entry.grid(row=2, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(self.tab1)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Tambah Pricelist", command=self.tambah_pricelist).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Field", command=self.clear_field).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hapus Pricelist", command=self.hapus_pricelist).pack(side="left", padx=5)

        # Form Cell (Treeview)
        self.tree = ttk.Treeview(self.tab1, columns=("ID", "Ukuran", "Jenis", "Harga"), show="headings")
        self.tree.heading("ID", text="No. ID")
        self.tree.heading("Ukuran", text="Ukuran")
        self.tree.heading("Jenis", text="Jenis")
        self.tree.heading("Harga", text="Harga")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 2: Pembayaran
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Pembayaran")

        # Form Pembayaran
        pembayaran_frame = ttk.LabelFrame(self.tab2, text="Form Pembayaran")
        pembayaran_frame.pack(fill="x", padx=10, pady=5)

        # No. ID
        ttk.Label(pembayaran_frame, text="No. ID:").grid(row=0, column=0, padx=5, pady=5)
        self.pembayaran_id_combobox = ttk.Combobox(pembayaran_frame)
        self.pembayaran_id_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.pembayaran_id_combobox.bind("<<ComboboxSelected>>", self.isi_otomatis_pembayaran)

        # Tanggal
        ttk.Label(pembayaran_frame, text="Tanggal:").grid(row=1, column=0, padx=5, pady=5)
        self.pembayaran_tanggal_entry = ttk.Entry(pembayaran_frame)
        self.pembayaran_tanggal_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.pembayaran_tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Pelanggan
        ttk.Label(pembayaran_frame, text="Pelanggan:").grid(row=2, column=0, padx=5, pady=5)
        self.pembayaran_pelanggan_entry = ttk.Entry(pembayaran_frame)
        self.pembayaran_pelanggan_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Ukuran
        ttk.Label(pembayaran_frame, text="Ukuran:").grid(row=3, column=0, padx=5, pady=5)
        self.pembayaran_ukuran_entry = ttk.Entry(pembayaran_frame, state="readonly")
        self.pembayaran_ukuran_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Jenis
        ttk.Label(pembayaran_frame, text="Jenis:").grid(row=4, column=0, padx=5, pady=5)
        self.pembayaran_jenis_entry = ttk.Entry(pembayaran_frame, state="readonly")
        self.pembayaran_jenis_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Jumlah
        ttk.Label(pembayaran_frame, text="Jumlah:").grid(row=5, column=0, padx=5, pady=5)
        self.pembayaran_jumlah_entry = ttk.Entry(pembayaran_frame)
        self.pembayaran_jumlah_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Harga
        ttk.Label(pembayaran_frame, text="Harga:").grid(row=6, column=0, padx=5, pady=5)
        self.pembayaran_harga_entry = ttk.Entry(pembayaran_frame, state="readonly")
        self.pembayaran_harga_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # Total Bayar
        ttk.Label(pembayaran_frame, text="Total Bayar:").grid(row=7, column=0, padx=5, pady=5)
        self.pembayaran_total_entry = ttk.Entry(pembayaran_frame, state="readonly")
        self.pembayaran_total_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        # Button Hitung Total
        ttk.Button(pembayaran_frame, text="Hitung Total", command=self.hitung_total_bayar).grid(row=8, column=1, padx=5, pady=5)

        # Button Tambah Pembayaran
        ttk.Button(pembayaran_frame, text="Tambah Pembayaran", command=self.tambah_pembayaran).grid(row=9, column=1, padx=5, pady=5)

        # Treeview Pembayaran
        self.tree_pembayaran = ttk.Treeview(self.tab2, columns=("ID", "Tanggal", "Pelanggan", "Ukuran", "Jenis", "Jumlah", "Harga", "Total"), show="headings")
        self.tree_pembayaran.heading("ID", text="No. ID")
        self.tree_pembayaran.heading("Tanggal", text="Tanggal")
        self.tree_pembayaran.heading("Pelanggan", text="Pelanggan")
        self.tree_pembayaran.heading("Ukuran", text="Ukuran")
        self.tree_pembayaran.heading("Jenis", text="Jenis")
        self.tree_pembayaran.heading("Jumlah", text="Jumlah")
        self.tree_pembayaran.heading("Harga", text="Harga")
        self.tree_pembayaran.heading("Total", text="Total")
        self.tree_pembayaran.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 3: Pengeluaran
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Pengeluaran")

        # Form Pengeluaran
        pengeluaran_frame = ttk.LabelFrame(self.tab3, text="Form Pengeluaran")
        pengeluaran_frame.pack(fill="x", padx=10, pady=5)

        # Tanggal
        ttk.Label(pengeluaran_frame, text="Tanggal:").grid(row=0, column=0, padx=5, pady=5)
        self.pengeluaran_tanggal_entry = ttk.Entry(pengeluaran_frame)
        self.pengeluaran_tanggal_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.pengeluaran_tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Keterangan
        ttk.Label(pengeluaran_frame, text="Keterangan:").grid(row=1, column=0, padx=5, pady=5)
        self.pengeluaran_keterangan_entry = ttk.Entry(pengeluaran_frame)
        self.pengeluaran_keterangan_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Jumlah Pengeluaran
        ttk.Label(pengeluaran_frame, text="Jumlah Pengeluaran:").grid(row=2, column=0, padx=5, pady=5)
        self.pengeluaran_jumlah_entry = ttk.Entry(pengeluaran_frame)
        self.pengeluaran_jumlah_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Button Tambah Pengeluaran
        ttk.Button(pengeluaran_frame, text="Tambah Pengeluaran", command=self.tambah_pengeluaran).grid(row=3, column=1, padx=5, pady=5)

        # Treeview Pengeluaran
        self.tree_pengeluaran = ttk.Treeview(self.tab3, columns=("Tanggal", "Keterangan", "Jumlah"), show="headings")
        self.tree_pengeluaran.heading("Tanggal", text="Tanggal")
        self.tree_pengeluaran.heading("Keterangan", text="Keterangan")
        self.tree_pengeluaran.heading("Jumlah", text="Jumlah")
        self.tree_pengeluaran.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 4: Laporan Penjualan
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="Laporan Penjualan")

        # Filter Tanggal
        filter_frame = ttk.LabelFrame(self.tab4, text="Filter Tanggal")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Dari Tanggal:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_dari_tanggal = ttk.Entry(filter_frame)
        self.filter_dari_tanggal.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(filter_frame, text="Sampai Tanggal:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_sampai_tanggal = ttk.Entry(filter_frame)
        self.filter_sampai_tanggal.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Button(filter_frame, text="Filter", command=self.filter_laporan).grid(row=0, column=4, padx=5, pady=5)

        # Total Penjualan
        self.total_penjualan_label = ttk.Label(self.tab4, text="Total Penjualan: Rp 0", font=("Arial", 12, "bold"))
        self.total_penjualan_label.pack(pady=10)

        # Treeview Laporan Penjualan
        self.tree_laporan = ttk.Treeview(self.tab4, columns=("ID", "Tanggal", "Pelanggan", "Ukuran", "Jenis", "Jumlah", "Harga", "Total"), show="headings")
        self.tree_laporan.heading("ID", text="No. ID")
        self.tree_laporan.heading("Tanggal", text="Tanggal")
        self.tree_laporan.heading("Pelanggan", text="Pelanggan")
        self.tree_laporan.heading("Ukuran", text="Ukuran")
        self.tree_laporan.heading("Jenis", text="Jenis")
        self.tree_laporan.heading("Jumlah", text="Jumlah")
        self.tree_laporan.heading("Harga", text="Harga")
        self.tree_laporan.heading("Total", text="Total")
        self.tree_laporan.pack(fill="both", expand=True, padx=10, pady=5)


    def tambah_pricelist(self):
        ukuran = ", ".join([text for text, var in self.ukuran_vars.items() if var.get()])
        jenis = self.jenis_combobox.get()
        harga = self.harga_entry.get()

        if ukuran and jenis and harga:
            # Generate No. ID
            no_id = self.next_id
            self.next_id += 1

            # Tambahkan ke pricelist dan treeview
            self.pricelist.append((no_id, ukuran, jenis, harga))
            self.tree.insert("", "end", values=(no_id, ukuran, jenis, harga))
            self.clear_field()
            self.update_pembayaran_id_combobox()  # Update combobox No. ID di form pembayaran
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")

    def clear_field(self):
        for var in self.ukuran_vars.values():
            var.set(False)
        self.jenis_combobox.set("")
        self.harga_entry.delete(0, tk.END)

    def hapus_pricelist(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            self.tree.delete(selected_item)
            self.pricelist = [entry for entry in self.pricelist if entry[0] != int(item_values[0])]
            self.update_pembayaran_id_combobox()  # Update combobox No. ID di form pembayaran
        else:
            messagebox.showwarning("Peringatan", "Pilih item yang ingin dihapus!")

    def update_pembayaran_id_combobox(self):
        # Update combobox No. ID di form pembayaran
        self.pembayaran_id_combobox["values"] = [entry[0] for entry in self.pricelist]

    def isi_otomatis_pembayaran(self, event=None):
        # Isi otomatis form pembayaran berdasarkan No. ID yang dipilih
        selected_id = self.pembayaran_id_combobox.get()
        if selected_id:
            for entry in self.pricelist:
                if entry[0] == int(selected_id):
                    self.pembayaran_ukuran_entry.config(state="normal")
                    self.pembayaran_ukuran_entry.delete(0, tk.END)
                    self.pembayaran_ukuran_entry.insert(0, entry[1])
                    self.pembayaran_ukuran_entry.config(state="readonly")

                    self.pembayaran_jenis_entry.config(state="normal")
                    self.pembayaran_jenis_entry.delete(0, tk.END)
                    self.pembayaran_jenis_entry.insert(0, entry[2])
                    self.pembayaran_jenis_entry.config(state="readonly")

                    self.pembayaran_harga_entry.config(state="normal")
                    self.pembayaran_harga_entry.delete(0, tk.END)
                    self.pembayaran_harga_entry.insert(0, entry[3])
                    self.pembayaran_harga_entry.config(state="readonly")
                    break

    def hitung_total_bayar(self):
        # Hitung total bayar berdasarkan jumlah dan harga
        try:
            jumlah = int(self.pembayaran_jumlah_entry.get())
            harga = int(self.pembayaran_harga_entry.get())
            total = jumlah * harga
            self.pembayaran_total_entry.config(state="normal")
            self.pembayaran_total_entry.delete(0, tk.END)
            self.pembayaran_total_entry.insert(0, total)
            self.pembayaran_total_entry.config(state="readonly")
        except ValueError:
            messagebox.showwarning("Input Error", "Jumlah harus berupa angka!")

    def tambah_pembayaran(self):
        # Tambahkan data pembayaran ke treeview
        no_id = self.pembayaran_id_combobox.get()
        tanggal = self.pembayaran_tanggal_entry.get()
        pelanggan = self.pembayaran_pelanggan_entry.get()
        ukuran = self.pembayaran_ukuran_entry.get()
        jenis = self.pembayaran_jenis_entry.get()
        jumlah = self.pembayaran_jumlah_entry.get()
        harga = self.pembayaran_harga_entry.get()
        total = self.pembayaran_total_entry.get()

        if no_id and tanggal and pelanggan and ukuran and jenis and jumlah and harga and total:
            self.pembayaran.append((no_id, tanggal, pelanggan, ukuran, jenis, jumlah, harga, total))
            self.tree_pembayaran.insert("", "end", values=(no_id, tanggal, pelanggan, ukuran, jenis, jumlah, harga, total))
            self.clear_pembayaran_field()
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")

    def clear_pembayaran_field(self):
        # Bersihkan form pembayaran
        self.pembayaran_id_combobox.set("")
        self.pembayaran_tanggal_entry.delete(0, tk.END)
        self.pembayaran_tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.pembayaran_pelanggan_entry.delete(0, tk.END)
        self.pembayaran_ukuran_entry.config(state="normal")
        self.pembayaran_ukuran_entry.delete(0, tk.END)
        self.pembayaran_ukuran_entry.config(state="readonly")
        self.pembayaran_jenis_entry.config(state="normal")
        self.pembayaran_jenis_entry.delete(0, tk.END)
        self.pembayaran_jenis_entry.config(state="readonly")
        self.pembayaran_jumlah_entry.delete(0, tk.END)
        self.pembayaran_harga_entry.config(state="normal")
        self.pembayaran_harga_entry.delete(0, tk.END)
        self.pembayaran_harga_entry.config(state="readonly")
        self.pembayaran_total_entry.config(state="normal")
        self.pembayaran_total_entry.delete(0, tk.END)
        self.pembayaran_total_entry.config(state="readonly")

    def tambah_pengeluaran(self):
        # Tambahkan data pengeluaran ke treeview
        tanggal = self.pengeluaran_tanggal_entry.get()
        keterangan = self.pengeluaran_keterangan_entry.get()
        jumlah = self.pengeluaran_jumlah_entry.get()

        if tanggal and keterangan and jumlah:
            self.pengeluaran.append((tanggal, keterangan, jumlah))
            self.tree_pengeluaran.insert("", "end", values=(tanggal, keterangan, jumlah))
            self.clear_pengeluaran_field()
        else:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")

    def clear_pengeluaran_field(self):
        # Bersihkan form pengeluaran
        self.pengeluaran_tanggal_entry.delete(0, tk.END)
        self.pengeluaran_tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.pengeluaran_keterangan_entry.delete(0, tk.END)
        self.pengeluaran_jumlah_entry.delete(0, tk.END)


    def filter_laporan(self):
        # Filter laporan berdasarkan tanggal
        dari_tanggal = self.filter_dari_tanggal.get()
        sampai_tanggal = self.filter_sampai_tanggal.get()

        if dari_tanggal and sampai_tanggal:
            try:
                dari_tanggal = datetime.strptime(dari_tanggal, "%Y-%m-%d")
                sampai_tanggal = datetime.strptime(sampai_tanggal, "%Y-%m-%d")

                # Bersihkan treeview laporan
                for item in self.tree_laporan.get_children():
                    self.tree_laporan.delete(item)

                total_penjualan = 0
                for entry in self.pembayaran:
                    tanggal = datetime.strptime(entry[1], "%Y-%m-%d")
                    if dari_tanggal <= tanggal <= sampai_tanggal:
                        self.tree_laporan.insert("", "end", values=entry)
                        total_penjualan += int(entry[7])

                self.total_penjualan_label.config(text=f"Total Penjualan: Rp {total_penjualan:,}")
            except ValueError:
                messagebox.showwarning("Input Error", "Format tanggal tidak valid! Gunakan format YYYY-MM-DD.")
        else:
            messagebox.showwarning("Input Error", "Isi kedua field tanggal!")

    def update_laporan(self):
        # Update laporan penjualan tanpa filter
        for item in self.tree_laporan.get_children():
            self.tree_laporan.delete(item)

        total_penjualan = 0
        for entry in self.pembayaran:
            self.tree_laporan.insert("", "end", values=entry)
            total_penjualan += int(entry[7])

        self.total_penjualan_label.config(text=f"Total Penjualan: Rp {total_penjualan:,}")


    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filepath:
            with open(filepath, "r") as file:
                data = eval(file.read())
                self.pricelist = data.get("pricelist", [])
                self.pembayaran = data.get("pembayaran", [])
                self.pengeluaran = data.get("pengeluaran", [])
                if self.pricelist:
                    self.next_id = max(entry[0] for entry in self.pricelist) + 1

            # Update treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            for entry in self.pricelist:
                self.tree.insert("", "end", values=entry)

            for item in self.tree_pembayaran.get_children():
                self.tree_pembayaran.delete(item)
            for entry in self.pembayaran:
                self.tree_pembayaran.insert("", "end", values=entry)

            for item in self.tree_pengeluaran.get_children():
                self.tree_pengeluaran.delete(item)
            for entry in self.pengeluaran:
                self.tree_pengeluaran.insert("", "end", values=entry)

            self.update_pembayaran_id_combobox()

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filepath:
            data = {
                "pricelist": self.pricelist,
                "pembayaran": self.pembayaran,
                "pengeluaran": self.pengeluaran
            }
            with open(filepath, "w") as file:
                file.write(str(data))

    def convert_to_txt(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "w") as file:
                file.write("=== Daftar Harga ===\n")
                for entry in self.pricelist:
                    file.write(f"No. ID: {entry[0]}, Ukuran: {entry[1]}, Jenis: {entry[2]}, Harga: {entry[3]}\n")

                file.write("\n=== Pembayaran ===\n")
                for entry in self.pembayaran:
                    file.write(f"No. ID: {entry[0]}, Tanggal: {entry[1]}, Pelanggan: {entry[2]}, Ukuran: {entry[3]}, Jenis: {entry[4]}, Jumlah: {entry[5]}, Harga: {entry[6]}, Total: {entry[7]}\n")

                file.write("\n=== Pengeluaran ===\n")
                for entry in self.pengeluaran:
                    file.write(f"Tanggal: {entry[0]}, Keterangan: {entry[1]}, Jumlah: {entry[2]}\n")


    def about(self):
        messagebox.showinfo("About", "\n TrappDesign Accountant\n Versi 3.0 \n Dibuat oleh \n TrappDesign - Mirza Kamal 2025")
        messagebox.showinfo("Donasi", "\n Donasi bisa di salurkan \n ke rekening BCA 8380239460 \n untuk pengembangan lebih lanjut")
        messagebox.showinfo("Kontak", "\n mirzakamal647@gmail.com \n WA 082117123880 \n ")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = PricelistApp(root)
    root.mainloop()