import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class AplikasiPOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pembukuan Umum POS")
        self.root.geometry("1200x700")
        
        # Buat database dan tabel jika belum ada
        self.buat_database()
        
        # Frame utama
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook (tab)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Buat tab-tab
        self.buat_tab_transaksi()
        self.buat_tab_produk()
        self.buat_tab_stok()
        self.buat_tab_laporan()
        
    def buat_database(self):
        """Membuat database dan tabel jika belum ada"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        # Tabel produk
        c.execute('''CREATE TABLE IF NOT EXISTS produk (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kode TEXT UNIQUE,
                    nama TEXT,
                    kategori TEXT,
                    harga REAL,
                    stok INTEGER,
                    min_stok INTEGER
                    )''')
        
        # Tabel transaksi
        c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    no_transaksi TEXT,
                    tanggal TEXT,
                    total REAL,
                    bayar REAL,
                    kembalian REAL,
                    jenis TEXT
                    )''')
        
        # Tabel detail transaksi
        c.execute('''CREATE TABLE IF NOT EXISTS detail_transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_transaksi INTEGER,
                    id_produk INTEGER,
                    kode_produk TEXT,
                    nama_produk TEXT,
                    harga REAL,
                    qty INTEGER,
                    subtotal REAL,
                    FOREIGN KEY(id_transaksi) REFERENCES transaksi(id),
                    FOREIGN KEY(id_produk) REFERENCES produk(id)
                    )''')
        
        # Tabel pemasukan/pengeluaran
        c.execute('''CREATE TABLE IF NOT EXISTS keuangan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    keterangan TEXT,
                    jumlah REAL,
                    jenis TEXT,
                    kategori TEXT
                    )''')
        
        conn.commit()
        conn.close()
    
    def buat_tab_transaksi(self):
        """Membuat tab untuk transaksi penjualan"""
        tab_transaksi = ttk.Frame(self.notebook)
        self.notebook.add(tab_transaksi, text="Transaksi")
        
        # Frame input produk
        frame_input = ttk.LabelFrame(tab_transaksi, text="Input Produk")
        frame_input.pack(fill=tk.X, padx=5, pady=5)
        
        # Input kode produk
        ttk.Label(frame_input, text="Kode Produk:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_kode = ttk.Entry(frame_input)
        self.entry_kode.grid(row=0, column=1, padx=5, pady=5)
        self.entry_kode.bind('<Return>', lambda e: self.tambah_item_ke_keranjang())
        
        # Tombol cari produk
        ttk.Button(frame_input, text="Cari", command=self.cari_produk).grid(row=0, column=2, padx=5, pady=5)
        
        # Info produk
        self.label_info_produk = ttk.Label(frame_input, text="Produk: - | Harga: - | Stok: -")
        self.label_info_produk.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Input qty
        ttk.Label(frame_input, text="Qty:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_qty = ttk.Spinbox(frame_input, from_=1, to=100, width=5)
        self.entry_qty.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.entry_qty.set(1)
        
        # Tombol tambah ke keranjang
        ttk.Button(frame_input, text="Tambah ke Keranjang", command=self.tambah_item_ke_keranjang).grid(row=2, column=2, padx=5, pady=5)
        
        # Frame keranjang belanja
        frame_keranjang = ttk.LabelFrame(tab_transaksi, text="Keranjang Belanja")
        frame_keranjang.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview untuk keranjang belanja
        columns = ('no', 'kode', 'nama', 'harga', 'qty', 'subtotal')
        self.tree_keranjang = ttk.Treeview(frame_keranjang, columns=columns, show='headings')
        
        # Set heading
        self.tree_keranjang.heading('no', text='No')
        self.tree_keranjang.heading('kode', text='Kode')
        self.tree_keranjang.heading('nama', text='Nama Produk')
        self.tree_keranjang.heading('harga', text='Harga')
        self.tree_keranjang.heading('qty', text='Qty')
        self.tree_keranjang.heading('subtotal', text='Subtotal')
        
        # Set column width
        self.tree_keranjang.column('no', width=30)
        self.tree_keranjang.column('kode', width=80)
        self.tree_keranjang.column('nama', width=200)
        self.tree_keranjang.column('harga', width=80)
        self.tree_keranjang.column('qty', width=50)
        self.tree_keranjang.column('subtotal', width=100)
        
        self.tree_keranjang.pack(fill=tk.BOTH, expand=True)
        
        # Tombol hapus item
        ttk.Button(frame_keranjang, text="Hapus Item Terpilih", command=self.hapus_item_dari_keranjang).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Frame total dan pembayaran
        frame_pembayaran = ttk.Frame(tab_transaksi)
        frame_pembayaran.pack(fill=tk.X, padx=5, pady=5)
        
        # Total
        ttk.Label(frame_pembayaran, text="Total:").grid(row=0, column=0, padx=5, pady=5)
        self.label_total = ttk.Label(frame_pembayaran, text="Rp 0", font=('Arial', 12, 'bold'))
        self.label_total.grid(row=0, column=1, padx=5, pady=5)
        
        # Bayar
        ttk.Label(frame_pembayaran, text="Bayar:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_bayar = ttk.Entry(frame_pembayaran)
        self.entry_bayar.grid(row=1, column=1, padx=5, pady=5)
        
        # Kembalian
        ttk.Label(frame_pembayaran, text="Kembalian:").grid(row=2, column=0, padx=5, pady=5)
        self.label_kembalian = ttk.Label(frame_pembayaran, text="Rp 0")
        self.label_kembalian.grid(row=2, column=1, padx=5, pady=5)
        
        # Tombol proses transaksi
        ttk.Button(frame_pembayaran, text="Proses Transaksi", command=self.proses_transaksi).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Inisialisasi keranjang belanja
        self.keranjang = []
        self.no_transaksi = self.generate_no_transaksi()
    
    def buat_tab_produk(self):
        """Membuat tab untuk manajemen produk"""
        tab_produk = ttk.Frame(self.notebook)
        self.notebook.add(tab_produk, text="Manajemen Produk")
        
        # Frame form produk
        frame_form = ttk.LabelFrame(tab_produk, text="Form Produk")
        frame_form.pack(fill=tk.X, padx=5, pady=5)
        
        # Input kode
        ttk.Label(frame_form, text="Kode Produk:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_kode_produk = ttk.Entry(frame_form)
        self.entry_kode_produk.grid(row=0, column=1, padx=5, pady=5)
        
        # Input nama
        ttk.Label(frame_form, text="Nama Produk:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_nama_produk = ttk.Entry(frame_form)
        self.entry_nama_produk.grid(row=1, column=1, padx=5, pady=5)
        
        # Input kategori
        ttk.Label(frame_form, text="Kategori:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_kategori_produk = ttk.Entry(frame_form)
        self.entry_kategori_produk.grid(row=2, column=1, padx=5, pady=5)
        
        # Input harga
        ttk.Label(frame_form, text="Harga:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_harga_produk = ttk.Entry(frame_form)
        self.entry_harga_produk.grid(row=3, column=1, padx=5, pady=5)
        
        # Input stok awal
        ttk.Label(frame_form, text="Stok Awal:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_stok_produk = ttk.Spinbox(frame_form, from_=0, to=1000)
        self.entry_stok_produk.grid(row=4, column=1, padx=5, pady=5)
        self.entry_stok_produk.set(0)
        
        # Input minimal stok
        ttk.Label(frame_form, text="Minimal Stok:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_min_stok_produk = ttk.Spinbox(frame_form, from_=0, to=100)
        self.entry_min_stok_produk.grid(row=5, column=1, padx=5, pady=5)
        self.entry_min_stok_produk.set(5)
        
        # Frame tombol aksi
        frame_aksi = ttk.Frame(frame_form)
        frame_aksi.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Tombol simpan
        ttk.Button(frame_aksi, text="Simpan", command=self.simpan_produk).pack(side=tk.LEFT, padx=5)
        
        # Tombol reset
        ttk.Button(frame_aksi, text="Reset", command=self.reset_form_produk).pack(side=tk.LEFT, padx=5)
        
        # Tombol hapus
        ttk.Button(frame_aksi, text="Hapus", command=self.hapus_produk).pack(side=tk.LEFT, padx=5)
        
        # Frame daftar produk
        frame_daftar = ttk.LabelFrame(tab_produk, text="Daftar Produk")
        frame_daftar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview untuk daftar produk
        columns = ('id', 'kode', 'nama', 'kategori', 'harga', 'stok', 'min_stok')
        self.tree_produk = ttk.Treeview(frame_daftar, columns=columns, show='headings')
        
        # Set heading
        self.tree_produk.heading('id', text='ID')
        self.tree_produk.heading('kode', text='Kode')
        self.tree_produk.heading('nama', text='Nama Produk')
        self.tree_produk.heading('kategori', text='Kategori')
        self.tree_produk.heading('harga', text='Harga')
        self.tree_produk.heading('stok', text='Stok')
        self.tree_produk.heading('min_stok', text='Min Stok')
        
        # Set column width
        self.tree_produk.column('id', width=30)
        self.tree_produk.column('kode', width=80)
        self.tree_produk.column('nama', width=150)
        self.tree_produk.column('kategori', width=100)
        self.tree_produk.column('harga', width=80)
        self.tree_produk.column('stok', width=50)
        self.tree_produk.column('min_stok', width=50)
        
        self.tree_produk.pack(fill=tk.BOTH, expand=True)
        
        # Tombol refresh
        ttk.Button(frame_daftar, text="Refresh", command=self.tampilkan_produk).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Tombol cari
        ttk.Label(frame_daftar, text="Cari:").pack(side=tk.LEFT, padx=5, pady=5)
        self.entry_cari_produk = ttk.Entry(frame_daftar)
        self.entry_cari_produk.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(frame_daftar, text="Cari", command=self.cari_daftar_produk).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Bind event ketika item dipilih
        self.tree_produk.bind('<<TreeviewSelect>>', self.pilih_produk)
        
        # Tampilkan data produk
        self.tampilkan_produk()
    
    def buat_tab_stok(self):
        """Membuat tab untuk manajemen stok gudang"""
        tab_stok = ttk.Frame(self.notebook)
        self.notebook.add(tab_stok, text="Manajemen Stok")
        
        # Frame filter
        frame_filter = ttk.Frame(tab_stok)
        frame_filter.pack(fill=tk.X, padx=5, pady=5)
        
        # Filter kategori
        ttk.Label(frame_filter, text="Kategori:").pack(side=tk.LEFT, padx=5)
        self.combo_kategori_stok = ttk.Combobox(frame_filter, state='readonly')
        self.combo_kategori_stok.pack(side=tk.LEFT, padx=5)
        self.combo_kategori_stok.bind('<<ComboboxSelected>>', self.filter_stok)
        
        # Filter stok menipis
        self.var_stok_menipis = tk.IntVar()
        ttk.Checkbutton(frame_filter, text="Tampilkan stok menipis saja", variable=self.var_stok_menipis, 
                       command=self.filter_stok).pack(side=tk.LEFT, padx=5)
        
        # Tombol refresh
        ttk.Button(frame_filter, text="Refresh", command=self.tampilkan_stok).pack(side=tk.LEFT, padx=5)
        
        # Frame daftar stok
        frame_daftar = ttk.LabelFrame(tab_stok, text="Daftar Stok")
        frame_daftar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview untuk daftar stok
        columns = ('id', 'kode', 'nama', 'kategori', 'stok', 'min_stok', 'status')
        self.tree_stok = ttk.Treeview(frame_daftar, columns=columns, show='headings')
        
        # Set heading
        self.tree_stok.heading('id', text='ID')
        self.tree_stok.heading('kode', text='Kode')
        self.tree_stok.heading('nama', text='Nama Produk')
        self.tree_stok.heading('kategori', text='Kategori')
        self.tree_stok.heading('stok', text='Stok')
        self.tree_stok.heading('min_stok', text='Min Stok')
        self.tree_stok.heading('status', text='Status')
        
        # Set column width
        self.tree_stok.column('id', width=30)
        self.tree_stok.column('kode', width=80)
        self.tree_stok.column('nama', width=150)
        self.tree_stok.column('kategori', width=100)
        self.tree_stok.column('stok', width=50)
        self.tree_stok.column('min_stok', width=50)
        self.tree_stok.column('status', width=100)
        
        self.tree_stok.pack(fill=tk.BOTH, expand=True)
        
        # Frame aksi stok
        frame_aksi = ttk.Frame(frame_daftar)
        frame_aksi.pack(fill=tk.X, pady=5)
        
        # Input penyesuaian stok
        ttk.Label(frame_aksi, text="Penyesuaian Stok:").pack(side=tk.LEFT, padx=5)
        self.entry_penyesuaian_stok = ttk.Spinbox(frame_aksi, from_=-1000, to=1000, width=5)
        self.entry_penyesuaian_stok.pack(side=tk.LEFT, padx=5)
        self.entry_penyesuaian_stok.set(0)
        
        # Tombol tambah stok
        ttk.Button(frame_aksi, text="Tambah Stok", command=lambda: self.sesuaikan_stok('tambah')).pack(side=tk.LEFT, padx=5)
        
        # Tombol kurangi stok
        ttk.Button(frame_aksi, text="Kurangi Stok", command=lambda: self.sesuaikan_stok('kurang')).pack(side=tk.LEFT, padx=5)
        
        # Tampilkan data stok
        self.tampilkan_stok()
        self.isi_kategori_stok()
    
    def buat_tab_laporan(self):
        """Membuat tab untuk laporan keuangan"""
        tab_laporan = ttk.Frame(self.notebook)
        self.notebook.add(tab_laporan, text="Laporan Keuangan")
        
        # Notebook untuk sub-tab laporan
        sub_notebook = ttk.Notebook(tab_laporan)
        sub_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Sub-tab laporan transaksi
        tab_lap_transaksi = ttk.Frame(sub_notebook)
        sub_notebook.add(tab_lap_transaksi, text="Laporan Transaksi")
        
        # Frame filter transaksi
        frame_filter_trans = ttk.Frame(tab_lap_transaksi)
        frame_filter_trans.pack(fill=tk.X, padx=5, pady=5)
        
        # Filter tanggal
        ttk.Label(frame_filter_trans, text="Dari:").pack(side=tk.LEFT, padx=5)
        self.entry_tgl_awal = ttk.Entry(frame_filter_trans, width=10)
        self.entry_tgl_awal.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_filter_trans, text="Sampai:").pack(side=tk.LEFT, padx=5)
        self.entry_tgl_akhir = ttk.Entry(frame_filter_trans, width=10)
        self.entry_tgl_akhir.pack(side=tk.LEFT, padx=5)
        
        # Tombol filter
        ttk.Button(frame_filter_trans, text="Filter", command=self.filter_laporan_transaksi).pack(side=tk.LEFT, padx=5)
        
        # Tombol cetak
        ttk.Button(frame_filter_trans, text="Cetak Laporan", command=self.cetak_laporan_transaksi).pack(side=tk.LEFT, padx=5)
        
        # Treeview untuk laporan transaksi
        columns = ('id', 'no_trans', 'tanggal', 'total', 'bayar', 'kembalian', 'jenis')
        self.tree_lap_transaksi = ttk.Treeview(tab_lap_transaksi, columns=columns, show='headings')
        
        # Set heading
        self.tree_lap_transaksi.heading('id', text='ID')
        self.tree_lap_transaksi.heading('no_trans', text='No. Transaksi')
        self.tree_lap_transaksi.heading('tanggal', text='Tanggal')
        self.tree_lap_transaksi.heading('total', text='Total')
        self.tree_lap_transaksi.heading('bayar', text='Bayar')
        self.tree_lap_transaksi.heading('kembalian', text='Kembalian')
        self.tree_lap_transaksi.heading('jenis', text='Jenis')
        
        # Set column width
        self.tree_lap_transaksi.column('id', width=30)
        self.tree_lap_transaksi.column('no_trans', width=100)
        self.tree_lap_transaksi.column('tanggal', width=80)
        self.tree_lap_transaksi.column('total', width=80)
        self.tree_lap_transaksi.column('bayar', width=80)
        self.tree_lap_transaksi.column('kembalian', width=80)
        self.tree_lap_transaksi.column('jenis', width=80)
        
        self.tree_lap_transaksi.pack(fill=tk.BOTH, expand=True)
        
        # Sub-tab laporan keuangan
        tab_lap_keuangan = ttk.Frame(sub_notebook)
        sub_notebook.add(tab_lap_keuangan, text="Laporan Keuangan")
        
        # Frame filter keuangan
        frame_filter_keu = ttk.Frame(tab_lap_keuangan)
        frame_filter_keu.pack(fill=tk.X, padx=5, pady=5)
        
        # Filter tanggal
        ttk.Label(frame_filter_keu, text="Dari:").pack(side=tk.LEFT, padx=5)
        self.entry_tgl_awal_keu = ttk.Entry(frame_filter_keu, width=10)
        self.entry_tgl_awal_keu.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_filter_keu, text="Sampai:").pack(side=tk.LEFT, padx=5)
        self.entry_tgl_akhir_keu = ttk.Entry(frame_filter_keu, width=10)
        self.entry_tgl_akhir_keu.pack(side=tk.LEFT, padx=5)
        
        # Filter jenis
        ttk.Label(frame_filter_keu, text="Jenis:").pack(side=tk.LEFT, padx=5)
        self.combo_jenis_keu = ttk.Combobox(frame_filter_keu, values=['Semua', 'Pemasukan', 'Pengeluaran'])
        self.combo_jenis_keu.pack(side=tk.LEFT, padx=5)
        self.combo_jenis_keu.set('Semua')
        
        # Tombol filter
        ttk.Button(frame_filter_keu, text="Filter", command=self.filter_laporan_keuangan).pack(side=tk.LEFT, padx=5)
        
        # Tombol cetak
        ttk.Button(frame_filter_keu, text="Cetak Laporan", command=self.cetak_laporan_keuangan).pack(side=tk.LEFT, padx=5)
        
        # Treeview untuk laporan keuangan
        columns = ('id', 'tanggal', 'keterangan', 'jumlah', 'jenis', 'kategori')
        self.tree_lap_keuangan = ttk.Treeview(tab_lap_keuangan, columns=columns, show='headings')
        
        # Set heading
        self.tree_lap_keuangan.heading('id', text='ID')
        self.tree_lap_keuangan.heading('tanggal', text='Tanggal')
        self.tree_lap_keuangan.heading('keterangan', text='Keterangan')
        self.tree_lap_keuangan.heading('jumlah', text='Jumlah')
        self.tree_lap_keuangan.heading('jenis', text='Jenis')
        self.tree_lap_keuangan.heading('kategori', text='Kategori')
        
        # Set column width
        self.tree_lap_keuangan.column('id', width=30)
        self.tree_lap_keuangan.column('tanggal', width=80)
        self.tree_lap_keuangan.column('keterangan', width=150)
        self.tree_lap_keuangan.column('jumlah', width=80)
        self.tree_lap_keuangan.column('jenis', width=80)
        self.tree_lap_keuangan.column('kategori', width=80)
        
        self.tree_lap_keuangan.pack(fill=tk.BOTH, expand=True)
        
        # Frame total
        frame_total = ttk.Frame(tab_lap_keuangan)
        frame_total.pack(fill=tk.X, padx=5, pady=5)
        
        # Total pemasukan
        ttk.Label(frame_total, text="Total Pemasukan:").pack(side=tk.LEFT, padx=5)
        self.label_total_pemasukan = ttk.Label(frame_total, text="Rp 0", font=('Arial', 10, 'bold'))
        self.label_total_pemasukan.pack(side=tk.LEFT, padx=5)
        
        # Total pengeluaran
        ttk.Label(frame_total, text="Total Pengeluaran:").pack(side=tk.LEFT, padx=5)
        self.label_total_pengeluaran = ttk.Label(frame_total, text="Rp 0", font=('Arial', 10, 'bold'))
        self.label_total_pengeluaran.pack(side=tk.LEFT, padx=5)
        
        # Saldo
        ttk.Label(frame_total, text="Saldo:").pack(side=tk.LEFT, padx=5)
        self.label_saldo = ttk.Label(frame_total, text="Rp 0", font=('Arial', 10, 'bold'))
        self.label_saldo.pack(side=tk.LEFT, padx=5)
        
        # Tampilkan data awal
        self.tampilkan_laporan_transaksi()
        self.tampilkan_laporan_keuangan()
    
    # ==============================================
    # FUNGSI-FUNGSI UNTUK TAB TRANSAKSI
    # ==============================================
    
    def generate_no_transaksi(self):
        """Generate nomor transaksi unik"""
        now = datetime.now()
        return f"TRX-{now.strftime('%Y%m%d-%H%M%S')}"
    
    def cari_produk(self):
        """Mencari produk berdasarkan kode"""
        kode = self.entry_kode.get().strip()
        if not kode:
            messagebox.showwarning("Peringatan", "Masukkan kode produk terlebih dahulu")
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute("SELECT id, nama, harga, stok FROM produk WHERE kode=?", (kode,))
        produk = c.fetchone()
        
        conn.close()
        
        if produk:
            self.label_info_produk.config(text=f"Produk: {produk[1]} | Harga: Rp {produk[2]:,} | Stok: {produk[3]}")
            self.produk_terpilih = {
                'id': produk[0],
                'kode': kode,
                'nama': produk[1],
                'harga': produk[2],
                'stok': produk[3]
            }
        else:
            messagebox.showerror("Error", "Produk tidak ditemukan")
            self.label_info_produk.config(text="Produk: - | Harga: - | Stok: -")
            self.produk_terpilih = None
    
    def tambah_item_ke_keranjang(self):
        """Menambahkan item ke keranjang belanja"""
        if not hasattr(self, 'produk_terpilih') or not self.produk_terpilih:
            messagebox.showwarning("Peringatan", "Pilih produk terlebih dahulu")
            return
        
        try:
            qty = int(self.entry_qty.get())
            if qty <= 0:
                messagebox.showwarning("Peringatan", "Qty harus lebih dari 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Qty harus berupa angka")
            return
        
        if qty > self.produk_terpilih['stok']:
            messagebox.showwarning("Peringatan", f"Stok tidak mencukupi. Stok tersedia: {self.produk_terpilih['stok']}")
            return
        
        # Cek apakah produk sudah ada di keranjang
        for item in self.keranjang:
            if item['kode'] == self.produk_terpilih['kode']:
                item['qty'] += qty
                item['subtotal'] = item['harga'] * item['qty']
                self.tampilkan_keranjang()
                self.hitung_total()
                return
        
        # Jika belum ada, tambahkan ke keranjang
        subtotal = self.produk_terpilih['harga'] * qty
        self.keranjang.append({
            'id': self.produk_terpilih['id'],
            'kode': self.produk_terpilih['kode'],
            'nama': self.produk_terpilih['nama'],
            'harga': self.produk_terpilih['harga'],
            'qty': qty,
            'subtotal': subtotal
        })
        
        self.tampilkan_keranjang()
        self.hitung_total()
        
        # Reset input
        self.entry_kode.delete(0, tk.END)
        self.entry_qty.set(1)
        self.label_info_produk.config(text="Produk: - | Harga: - | Stok: -")
        self.produk_terpilih = None
        self.entry_kode.focus()
    
    def tampilkan_keranjang(self):
        """Menampilkan isi keranjang belanja di treeview"""
        # Kosongkan treeview
        for item in self.tree_keranjang.get_children():
            self.tree_keranjang.delete(item)
        
        # Isi dengan data keranjang
        for i, item in enumerate(self.keranjang, start=1):
            self.tree_keranjang.insert('', tk.END, values=(
                i,
                item['kode'],
                item['nama'],
                f"Rp {item['harga']:,}",
                item['qty'],
                f"Rp {item['subtotal']:,}"
            ))
    
    def hitung_total(self):
        """Menghitung total belanja"""
        total = sum(item['subtotal'] for item in self.keranjang)
        self.label_total.config(text=f"Rp {total:,}")
        
        # Hitung kembalian jika sudah ada input bayar
        if self.entry_bayar.get():
            try:
                bayar = float(self.entry_bayar.get())
                kembalian = bayar - total
                self.label_kembalian.config(text=f"Rp {kembalian:,}")
            except ValueError:
                pass
    
    def hapus_item_dari_keranjang(self):
        """Menghapus item terpilih dari keranjang"""
        selected_item = self.tree_keranjang.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih item terlebih dahulu")
            return
        
        # Dapatkan index item yang dipilih
        index = int(self.tree_keranjang.item(selected_item, 'values')[0]) - 1
        
        # Hapus dari keranjang
        if 0 <= index < len(self.keranjang):
            self.keranjang.pop(index)
            self.tampilkan_keranjang()
            self.hitung_total()
    
    def proses_transaksi(self):
        """Memproses transaksi penjualan"""
        if not self.keranjang:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong")
            return
        
        try:
            bayar = float(self.entry_bayar.get())
            total = sum(item['subtotal'] for item in self.keranjang)
            
            if bayar < total:
                messagebox.showwarning("Peringatan", "Jumlah pembayaran kurang")
                return
        except ValueError:
            messagebox.showerror("Error", "Masukkan jumlah pembayaran yang valid")
            return
        
        kembalian = bayar - total
        
        # Simpan transaksi ke database
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        # Simpan data transaksi
        tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO transaksi 
                    (no_transaksi, tanggal, total, bayar, kembalian, jenis)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (self.no_transaksi, tanggal, total, bayar, kembalian, 'Penjualan'))
        
        # Dapatkan ID transaksi yang baru disimpan
        id_transaksi = c.lastrowid
        
        # Simpan detail transaksi
        for item in self.keranjang:
            c.execute('''INSERT INTO detail_transaksi
                        (id_transaksi, id_produk, kode_produk, nama_produk, harga, qty, subtotal)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (id_transaksi, item['id'], item['kode'], item['nama'], item['harga'], item['qty'], item['subtotal']))
            
            # Update stok produk
            c.execute("UPDATE produk SET stok = stok - ? WHERE id = ?", (item['qty'], item['id']))
        
        conn.commit()
        conn.close()
        
        # Cetak struk
        self.cetak_struk()
        
        # Reset transaksi
        self.keranjang = []
        self.tampilkan_keranjang()
        self.label_total.config(text="Rp 0")
        self.entry_bayar.delete(0, tk.END)
        self.label_kembalian.config(text="Rp 0")
        self.no_transaksi = self.generate_no_transaksi()
        
        messagebox.showinfo("Sukses", "Transaksi berhasil diproses")
    
    def cetak_struk(self):
        """Mencetak struk transaksi"""
        # Buat nama file berdasarkan nomor transaksi
        filename = f"struk_{self.no_transaksi}.pdf"
        
        # Buat dokumen PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Style untuk dokumen
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH2 = styles['Heading2']
        
        # Header struk
        elements.append(Paragraph("TOKO MAJU JAYA", styleH))
        elements.append(Paragraph("Jl. Raya No. 123, Jakarta", styleN))
        elements.append(Paragraph("Telp: 021-12345678", styleN))
        elements.append(Paragraph("=" * 50, styleN))
        
        # Info transaksi
        elements.append(Paragraph(f"No. Transaksi: {self.no_transaksi}", styleN))
        elements.append(Paragraph(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styleN))
        elements.append(Paragraph("=" * 50, styleN))
        
        # Detail pembelian
        data = [['No', 'Nama', 'Qty', 'Harga', 'Subtotal']]
        
        for i, item in enumerate(self.keranjang, start=1):
            data.append([
                str(i),
                item['nama'],
                str(item['qty']),
                f"Rp {item['harga']:,}",
                f"Rp {item['subtotal']:,}"
            ])
        
        # Buat tabel
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(t)
        elements.append(Paragraph("=" * 50, styleN))
        
        # Total pembayaran
        total = sum(item['subtotal'] for item in self.keranjang)
        bayar = float(self.entry_bayar.get())
        kembalian = bayar - total
        
        elements.append(Paragraph(f"Total: Rp {total:,}", styleN))
        elements.append(Paragraph(f"Bayar: Rp {bayar:,}", styleN))
        elements.append(Paragraph(f"Kembali: Rp {kembalian:,}", styleN))
        elements.append(Paragraph("=" * 50, styleN))
        elements.append(Paragraph("Terima kasih atas kunjungan Anda", styleH2))
        elements.append(Paragraph("Barang yang sudah dibeli tidak dapat ditukar atau dikembalikan", styleN))
        
        # Build PDF
        doc.build(elements)
        
        messagebox.showinfo("Sukses", f"Struk berhasil dicetak ke file {filename}")
    
    # ==============================================
    # FUNGSI-FUNGSI UNTUK TAB PRODUK
    # ==============================================
    
    def tampilkan_produk(self):
        """Menampilkan daftar produk di treeview"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute("SELECT id, kode, nama, kategori, harga, stok, min_stok FROM produk ORDER BY nama")
        produk = c.fetchall()
        
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_produk.get_children():
            self.tree_produk.delete(item)
        
        # Isi dengan data produk
        for p in produk:
            self.tree_produk.insert('', tk.END, values=p)
    
    def pilih_produk(self, event):
        """Menampilkan data produk terpilih ke form"""
        selected_item = self.tree_produk.selection()
        if not selected_item:
            return
        
        # Dapatkan data produk yang dipilih
        item = self.tree_produk.item(selected_item)
        values = item['values']
        
        # Isi form dengan data produk
        self.entry_kode_produk.delete(0, tk.END)
        self.entry_kode_produk.insert(0, values[1])
        
        self.entry_nama_produk.delete(0, tk.END)
        self.entry_nama_produk.insert(0, values[2])
        
        self.entry_kategori_produk.delete(0, tk.END)
        self.entry_kategori_produk.insert(0, values[3])
        
        self.entry_harga_produk.delete(0, tk.END)
        self.entry_harga_produk.insert(0, values[4])
        
        self.entry_stok_produk.delete(0, tk.END)
        self.entry_stok_produk.insert(0, values[5])
        
        self.entry_min_stok_produk.delete(0, tk.END)
        self.entry_min_stok_produk.insert(0, values[6])
    
    def simpan_produk(self):
        """Menyimpan data produk ke database"""
        kode = self.entry_kode_produk.get().strip()
        nama = self.entry_nama_produk.get().strip()
        kategori = self.entry_kategori_produk.get().strip()
        
        if not kode or not nama:
            messagebox.showwarning("Peringatan", "Kode dan nama produk harus diisi")
            return
        
        try:
            harga = float(self.entry_harga_produk.get())
            stok = int(self.entry_stok_produk.get())
            min_stok = int(self.entry_min_stok_produk.get())
            
            if harga <= 0 or stok < 0 or min_stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Harga, stok, dan minimal stok harus berupa angka positif")
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        try:
            # Cek apakah produk sudah ada (update) atau baru (insert)
            c.execute("SELECT id FROM produk WHERE kode=?", (kode,))
            produk = c.fetchone()
            
            if produk:
                # Update produk
                c.execute('''UPDATE produk SET 
                            nama=?, kategori=?, harga=?, stok=?, min_stok=?
                            WHERE kode=?''',
                         (nama, kategori, harga, stok, min_stok, kode))
            else:
                # Insert produk baru
                c.execute('''INSERT INTO produk 
                            (kode, nama, kategori, harga, stok, min_stok)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (kode, nama, kategori, harga, stok, min_stok))
            
            conn.commit()
            messagebox.showinfo("Sukses", "Data produk berhasil disimpan")
            self.tampilkan_produk()
            self.reset_form_produk()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Kode produk sudah digunakan")
        finally:
            conn.close()
    
    def hapus_produk(self):
        """Menghapus data produk dari database"""
        kode = self.entry_kode_produk.get().strip()
        if not kode:
            messagebox.showwarning("Peringatan", "Pilih produk terlebih dahulu")
            return
        
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus produk {kode}?"):
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM produk WHERE kode=?", (kode,))
            conn.commit()
            
            if c.rowcount > 0:
                messagebox.showinfo("Sukses", "Produk berhasil dihapus")
                self.tampilkan_produk()
                self.reset_form_produk()
            else:
                messagebox.showerror("Error", "Produk tidak ditemukan")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Tidak dapat menghapus produk: {str(e)}")
        finally:
            conn.close()
    
    def reset_form_produk(self):
        """Mengosongkan form produk"""
        self.entry_kode_produk.delete(0, tk.END)
        self.entry_nama_produk.delete(0, tk.END)
        self.entry_kategori_produk.delete(0, tk.END)
        self.entry_harga_produk.delete(0, tk.END)
        self.entry_stok_produk.delete(0, tk.END)
        self.entry_min_stok_produk.delete(0, tk.END)
        
        self.entry_stok_produk.set(0)
        self.entry_min_stok_produk.set(5)
        
        # Hapus seleksi di treeview
        for item in self.tree_produk.selection():
            self.tree_produk.selection_remove(item)
    
    def cari_daftar_produk(self):
        """Mencari produk berdasarkan keyword"""
        keyword = self.entry_cari_produk.get().strip()
        if not keyword:
            self.tampilkan_produk()
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, kode, nama, kategori, harga, stok, min_stok 
                    FROM produk 
                    WHERE nama LIKE ? OR kode LIKE ? OR kategori LIKE ?
                    ORDER BY nama''',
                 (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        
        produk = c.fetchall()
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_produk.get_children():
            self.tree_produk.delete(item)
        
        # Isi dengan hasil pencarian
        for p in produk:
            self.tree_produk.insert('', tk.END, values=p)
    
    # ==============================================
    # FUNGSI-FUNGSI UNTUK TAB STOK
    # ==============================================
    
    def tampilkan_stok(self):
        """Menampilkan daftar stok produk"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, kode, nama, kategori, stok, min_stok 
                    FROM produk 
                    ORDER BY nama''')
        
        stok = c.fetchall()
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_stok.get_children():
            self.tree_stok.delete(item)
        
        # Isi dengan data stok
        for s in stok:
            status = "Cukup"
            if s[4] < s[5]:
                status = "Menipis"
            elif s[4] == 0:
                status = "Habis"
                
            self.tree_stok.insert('', tk.END, values=(s[0], s[1], s[2], s[3], s[4], s[5], status))
    
    def isi_kategori_stok(self):
        """Mengisi combobox kategori dengan data unik dari database"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute("SELECT DISTINCT kategori FROM produk WHERE kategori IS NOT NULL AND kategori != ''")
        kategori = [row[0] for row in c.fetchall()]
        
        conn.close()
        
        self.combo_kategori_stok['values'] = ['Semua'] + kategori
        self.combo_kategori_stok.set('Semua')
    
    def filter_stok(self, event=None):
        """Memfilter stok berdasarkan kategori dan status"""
        kategori = self.combo_kategori_stok.get()
        tampilkan_menipis = self.var_stok_menipis.get()
        
        query = '''SELECT id, kode, nama, kategori, stok, min_stok 
                  FROM produk 
                  WHERE 1=1'''
        
        params = []
        
        if kategori != 'Semua':
            query += " AND kategori=?"
            params.append(kategori)
        
        if tampilkan_menipis:
            query += " AND stok <= min_stok"
        
        query += " ORDER BY nama"
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute(query, params)
        stok = c.fetchall()
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_stok.get_children():
            self.tree_stok.delete(item)
        
        # Isi dengan data stok yang difilter
        for s in stok:
            status = "Cukup"
            if s[4] < s[5]:
                status = "Menipis"
            elif s[4] == 0:
                status = "Habis"
                
            self.tree_stok.insert('', tk.END, values=(s[0], s[1], s[2], s[3], s[4], s[5], status))
    
    def sesuaikan_stok(self, aksi):
        """Menyesuaikan stok produk (tambah/kurang)"""
        selected_item = self.tree_stok.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih produk terlebih dahulu")
            return
        
        try:
            penyesuaian = int(self.entry_penyesuaian_stok.get())
            if penyesuaian <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Masukkan jumlah penyesuaian yang valid (angka positif)")
            return
        
        # Dapatkan data produk yang dipilih
        item = self.tree_stok.item(selected_item)
        values = item['values']
        id_produk = values[0]
        stok_sekarang = values[4]
        
        # Hitung stok baru
        if aksi == 'tambah':
            stok_baru = stok_sekarang + penyesuaian
        else:
            stok_baru = stok_sekarang - penyesuaian
            if stok_baru < 0:
                if not messagebox.askyesno("Konfirmasi", "Stok akan menjadi negatif. Lanjutkan?"):
                    return
        
        # Update stok di database
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        try:
            c.execute("UPDATE produk SET stok=? WHERE id=?", (stok_baru, id_produk))
            conn.commit()
            
            # Catat sebagai transaksi pengeluaran (jika stok ditambah)
            if aksi == 'tambah':
                tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                keterangan = f"Penambahan stok {values[2]} sebanyak {penyesuaian}"
                jumlah = penyesuaian * values[5]  # Asumsi harga beli = min_stok (contoh saja)
                
                c.execute('''INSERT INTO keuangan 
                            (tanggal, keterangan, jumlah, jenis, kategori)
                            VALUES (?, ?, ?, ?, ?)''',
                         (tanggal, keterangan, jumlah, 'Pengeluaran', 'Stok'))
                conn.commit()
            
            messagebox.showinfo("Sukses", f"Stok berhasil disesuaikan menjadi {stok_baru}")
            self.tampilkan_stok()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Gagal menyesuaikan stok: {str(e)}")
        finally:
            conn.close()
    
    # ==============================================
    # FUNGSI-FUNGSI UNTUK TAB LAPORAN
    # ==============================================
    
    def tampilkan_laporan_transaksi(self):
        """Menampilkan laporan transaksi"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, no_transaksi, tanggal, total, bayar, kembalian, jenis 
                    FROM transaksi 
                    ORDER BY tanggal DESC''')
        
        transaksi = c.fetchall()
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_lap_transaksi.get_children():
            self.tree_lap_transaksi.delete(item)
        
        # Isi dengan data transaksi
        for t in transaksi:
            self.tree_lap_transaksi.insert('', tk.END, values=t)
    
    def filter_laporan_transaksi(self):
        """Memfilter laporan transaksi berdasarkan tanggal"""
        tgl_awal = self.entry_tgl_awal.get().strip()
        tgl_akhir = self.entry_tgl_akhir.get().strip()
        
        if not tgl_awal or not tgl_akhir:
            messagebox.showwarning("Peringatan", "Masukkan rentang tanggal terlebih dahulu")
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, no_transaksi, tanggal, total, bayar, kembalian, jenis 
                    FROM transaksi 
                    WHERE tanggal BETWEEN ? AND ?
                    ORDER BY tanggal DESC''',
                 (tgl_awal, tgl_akhir))
        
        transaksi = c.fetchall()
        conn.close()
        
        # Kosongkan treeview
        for item in self.tree_lap_transaksi.get_children():
            self.tree_lap_transaksi.delete(item)
        
        # Isi dengan data transaksi yang difilter
        for t in transaksi:
            self.tree_lap_transaksi.insert('', tk.END, values=t)
    
    def cetak_laporan_transaksi(self):
        """Mencetak laporan transaksi ke PDF"""
        # Dapatkan data yang akan dicetak
        items = []
        for item in self.tree_lap_transaksi.get_children():
            items.append(self.tree_lap_transaksi.item(item)['values'])
        
        if not items:
            messagebox.showwarning("Peringatan", "Tidak ada data transaksi untuk dicetak")
            return
        
        # Buat nama file
        filename = "laporan_transaksi.pdf"
        
        # Buat dokumen PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Style untuk dokumen
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH2 = styles['Heading2']
        
        # Header laporan
        elements.append(Paragraph("LAPORAN TRANSAKSI", styleH))
        elements.append(Paragraph("TOKO MAJU JAYA", styleH2))
        
        # Info tanggal laporan
        tgl_awal = self.entry_tgl_awal.get()
        tgl_akhir = self.entry_tgl_akhir.get()
        
        if tgl_awal and tgl_akhir:
            elements.append(Paragraph(f"Periode: {tgl_awal} s/d {tgl_akhir}", styleN))
        else:
            elements.append(Paragraph(f"Periode: Semua Data", styleN))
        
        elements.append(Paragraph(f"Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styleN))
        elements.append(Paragraph("=" * 80, styleN))
        
        # Data transaksi
        data = [['No', 'No. Trans', 'Tanggal', 'Total', 'Bayar', 'Kembali', 'Jenis']]
        
        total_penjualan = 0
        for i, item in enumerate(items, start=1):
            data.append([
                str(i),
                item[1],
                item[2],
                f"Rp {item[3]:,}",
                f"Rp {item[4]:,}",
                f"Rp {item[5]:,}",
                item[6]
            ])
            if item[6] == 'Penjualan':
                total_penjualan += item[3]
        
        # Buat tabel
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(t)
        elements.append(Paragraph("=" * 80, styleN))
        elements.append(Paragraph(f"Total Penjualan: Rp {total_penjualan:,}", styleH2))
        
        # Build PDF
        doc.build(elements)
        
        messagebox.showinfo("Sukses", f"Laporan transaksi berhasil dicetak ke file {filename}")
    
    def tampilkan_laporan_keuangan(self):
        """Menampilkan laporan keuangan"""
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, tanggal, keterangan, jumlah, jenis, kategori 
                    FROM keuangan 
                    ORDER BY tanggal DESC''')
        
        keuangan = c.fetchall()
        
        # Hitung total pemasukan dan pengeluaran
        c.execute("SELECT SUM(jumlah) FROM keuangan WHERE jenis='Pemasukan'")
        total_pemasukan = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(jumlah) FROM keuangan WHERE jenis='Pengeluaran'")
        total_pengeluaran = c.fetchone()[0] or 0
        
        saldo = total_pemasukan - total_pengeluaran
        
        conn.close()
        
        # Update label total
        self.label_total_pemasukan.config(text=f"Rp {total_pemasukan:,}")
        self.label_total_pengeluaran.config(text=f"Rp {total_pengeluaran:,}")
        self.label_saldo.config(text=f"Rp {saldo:,}")
        
        # Kosongkan treeview
        for item in self.tree_lap_keuangan.get_children():
            self.tree_lap_keuangan.delete(item)
        
        # Isi dengan data keuangan
        for k in keuangan:
            self.tree_lap_keuangan.insert('', tk.END, values=k)
    
    def filter_laporan_keuangan(self):
        """Memfilter laporan keuangan berdasarkan tanggal dan jenis"""
        tgl_awal = self.entry_tgl_awal_keu.get().strip()
        tgl_akhir = self.entry_tgl_akhir_keu.get().strip()
        jenis = self.combo_jenis_keu.get()
        
        if not tgl_awal or not tgl_akhir:
            messagebox.showwarning("Peringatan", "Masukkan rentang tanggal terlebih dahulu")
            return
        
        conn = sqlite3.connect('pos_database.db')
        c = conn.cursor()
        
        query = '''SELECT id, tanggal, keterangan, jumlah, jenis, kategori 
                  FROM keuangan 
                  WHERE tanggal BETWEEN ? AND ?'''
        
        params = [tgl_awal, tgl_akhir]
        
        if jenis != 'Semua':
            query += " AND jenis=?"
            params.append(jenis)
        
        query += " ORDER BY tanggal DESC"
        
        c.execute(query, params)
        keuangan = c.fetchall()
        
        # Hitung total pemasukan dan pengeluaran berdasarkan filter
        query_pemasukan = "SELECT SUM(jumlah) FROM keuangan WHERE jenis='Pemasukan' AND tanggal BETWEEN ? AND ?"
        query_pengeluaran = "SELECT SUM(jumlah) FROM keuangan WHERE jenis='Pengeluaran' AND tanggal BETWEEN ? AND ?"
        
        c.execute(query_pemasukan, (tgl_awal, tgl_akhir))
        total_pemasukan = c.fetchone()[0] or 0
        
        c.execute(query_pengeluaran, (tgl_awal, tgl_akhir))
        total_pengeluaran = c.fetchone()[0] or 0
        
        saldo = total_pemasukan - total_pengeluaran
        
        conn.close()
        
        # Update label total
        self.label_total_pemasukan.config(text=f"Rp {total_pemasukan:,}")
        self.label_total_pengeluaran.config(text=f"Rp {total_pengeluaran:,}")
        self.label_saldo.config(text=f"Rp {saldo:,}")
        
        # Kosongkan treeview
        for item in self.tree_lap_keuangan.get_children():
            self.tree_lap_keuangan.delete(item)
        
        # Isi dengan data keuangan yang difilter
        for k in keuangan:
            self.tree_lap_keuangan.insert('', tk.END, values=k)
    
    def cetak_laporan_keuangan(self):
        """Mencetak laporan keuangan ke PDF"""
        # Dapatkan data yang akan dicetak
        items = []
        for item in self.tree_lap_keuangan.get_children():
            items.append(self.tree_lap_keuangan.item(item)['values'])
        
        if not items:
            messagebox.showwarning("Peringatan", "Tidak ada data keuangan untuk dicetak")
            return
        
        # Buat nama file
        filename = "laporan_keuangan.pdf"
        
        # Buat dokumen PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Style untuk dokumen
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH2 = styles['Heading2']
        
        # Header laporan
        elements.append(Paragraph("LAPORAN KEUANGAN", styleH))
        elements.append(Paragraph("TOKO MAJU JAYA", styleH2))
        
        # Info tanggal laporan
        tgl_awal = self.entry_tgl_awal_keu.get()
        tgl_akhir = self.entry_tgl_akhir_keu.get()
        jenis = self.combo_jenis_keu.get()
        
        if tgl_awal and tgl_akhir:
            elements.append(Paragraph(f"Periode: {tgl_awal} s/d {tgl_akhir}", styleN))
        
        if jenis != 'Semua':
            elements.append(Paragraph(f"Jenis: {jenis}", styleN))
        
        elements.append(Paragraph(f"Dicetak pada: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styleN))
        elements.append(Paragraph("=" * 80, styleN))
        
        # Data keuangan
        data = [['No', 'Tanggal', 'Keterangan', 'Jumlah', 'Jenis', 'Kategori']]
        
        for i, item in enumerate(items, start=1):
            data.append([
                str(i),
                item[1],
                item[2],
                f"Rp {item[3]:,}",
                item[4],
                item[5]
            ])
        
        # Buat tabel
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(t)
        elements.append(Paragraph("=" * 80, styleN))
        
        # Total pemasukan dan pengeluaran
        total_pemasukan = self.label_total_pemasukan.cget("text").replace("Rp ", "").replace(",", "")
        total_pengeluaran = self.label_total_pengeluaran.cget("text").replace("Rp ", "").replace(",", "")
        saldo = self.label_saldo.cget("text").replace("Rp ", "").replace(",", "")
        
        elements.append(Paragraph(f"Total Pemasukan: Rp {float(total_pemasukan):,}", styleN))
        elements.append(Paragraph(f"Total Pengeluaran: Rp {float(total_pengeluaran):,}", styleN))
        elements.append(Paragraph(f"Saldo: Rp {float(saldo):,}", styleH2))
        
        # Build PDF
        doc.build(elements)
        
        messagebox.showinfo("Sukses", f"Laporan keuangan berhasil dicetak ke file {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiPOS(root)
    root.mainloop()