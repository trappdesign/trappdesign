import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
from fpdf import FPDF  # Library untuk membuat PDF
import pandas as pd
import json

class CafeRestoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pembukuan Cafe dan Resto")
        self.root.geometry("1000x700")

        # Data menu
        self.menu = {
           "Nasi Goreng": {"harga": 15000, "gambar": "nasi_goreng.png"},
           "Mie Goreng": {"harga": 12000, "gambar": "mie_goreng.png"},
           "Ayam Bakar": {"harga": 25000, "gambar": "ayam_bakar.png"},
            "Baso Tahu": {"harga": 15000, "gambar": "nasi_goreng.png"},
           "Juice Alpukat": {"harga": 12000, "gambar": "mie_goreng.png"},
           "Capuccino": {"harga": 25000, "gambar": "ayam_bakar.png"},
            "Sup Kambing": {"harga": 15000, "gambar": "nasi_goreng.png"},
           "Roti Bakar": {"harga": 12000, "gambar": "mie_goreng.png"},
           "Mie Baso": {"harga": 25000, "gambar": "ayam_bakar.png"},
            "aneka Gorengan": {"harga": 15000, "gambar": "nasi_goreng.png"},
           "Teh Manis": {"harga": 12000, "gambar": "mie_goreng.png"},
           "Lemon Tea": {"harga": 25000, "gambar": "ayam_bakar.png"},
        
        }

        # Data pesanan
        self.pesanan = []

        # Data pengeluaran
        self.pengeluaran = []

        # Data laporan
        self.laporan = []

        # List untuk menyimpan referensi gambar
        self.menu_images = []

        # Tampilkan form login
        self.show_login()

    def show_login(self):
        """Menampilkan form login."""
        self.login_frame = tk.Frame(self.root, bg="lightgreen")
        self.login_frame.pack(fill="both", expand=True)

        # Frame untuk input login dengan bingkai
        frame_input_login = tk.Frame(self.login_frame, bg="lightgray", bd=10, relief=tk.RAISED)
        frame_input_login.pack(pady=20, padx=20)

        ttk.Label(frame_input_login, text="Username:").pack(pady=5)
        self.entry_username = ttk.Entry(frame_input_login, width=50)
        self.entry_username.pack(pady=5)

        ttk.Label(frame_input_login, text="Password:").pack(pady=5)
        self.entry_password = ttk.Entry(frame_input_login, width=50, show="*")
        self.entry_password.pack(pady=5)

        ttk.Button(frame_input_login, text="Login", command=self.authenticate).pack(pady=10)

   
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
        # Membuat menu bar
        self.menu_bar = tk.Menu(self.root)
       
        # Menu Utama
        self.menu_utama = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menu Utama", menu=self.menu_utama)
        self.menu_utama.add_command(label="Daftar Menu", command=self.show_daftar_menu)      
        self.menu_utama.add_command(label="Pembayaran", command=self.show_pembayaran)
        self.menu_utama.add_command(label="Kelola Pengeluaran", command=self.show_pengeluaran)
        self.menu_utama.add_command(label="Laporan Penjualan", command=self.show_laporan)
        self.menu_utama.add_command(label="Exit", command=self.root.quit)
        self.root.config(menu=self.menu_bar)  

        
        # Frame Daftar Menu
        self.frame_daftar_menu = tk.Frame(self.root, bg="lightgrey")
        self.label_daftar_menu = tk.Label(self.frame_daftar_menu, text="Daftar Menu", font=("Arial", 16))

        
        # Frame untuk menampilkan gambar menu dengan bingkai
        self.frame_gambar_menu = tk.Frame(self.frame_daftar_menu, bg="grey", bd=30, relief=tk.RIDGE)
        self.frame_gambar_menu.pack(pady=10, padx=10, fill="both", expand=True)

       
        # Frame Pembayaran
        self.frame_pembayaran = tk.Frame(self.root, bg="lightyellow")
        self.label_pembayaran = tk.Label(self.frame_pembayaran, text="Pembayaran", font=("Arial", 16))
        self.label_pembayaran.pack(pady=10)

        self.tree_pesanan = ttk.Treeview(self.frame_pembayaran,columns=("Menu", "Jumlah", "Total"),show="headings")
        self.tree_pesanan.heading("Menu", text="Menu")
        self.tree_pesanan.heading("Jumlah", text="Jumlah")
        self.tree_pesanan.heading("Total", text="Total")
        self.tree_pesanan.pack(pady=10)

        self.label_total = tk.Label(self.frame_pembayaran, text="Total: Rp 0", font=("Arial", 30))
        self.label_total.pack(pady=10)

        self.button_bayar = tk.Button(self.frame_pembayaran, text="Bayar", command=self.bayar_pesanan)
        self.button_bayar.pack(pady=10)

        self.button_hapus_pesanan = tk.Button(self.frame_pembayaran, text="Hapus Pesanan", command=self.hapus_pesanan)
        self.button_hapus_pesanan.pack(pady=10)

        self.button_cetak_struk = tk.Button(self.frame_pembayaran, text="Cetak Struk", command=self.cetak_struk_pdf)
        self.button_cetak_struk.pack(pady=10)

      

        # Frame Pengeluaran
        self.frame_pengeluaran = tk.Frame(self.root, bg="lightpink")
        self.label_pengeluaran = tk.Label(self.frame_pengeluaran, text="Pengeluaran", font=("Arial", 16))
        self.label_pengeluaran.pack(pady=10)

        self.tree_pengeluaran = ttk.Treeview(self.frame_pengeluaran, columns=("Tanggal", "Keterangan", "Jumlah"), show="headings")
        self.tree_pengeluaran.heading("Tanggal", text="Tanggal")
        self.tree_pengeluaran.heading("Keterangan", text="Keterangan")
        self.tree_pengeluaran.heading("Jumlah", text="Jumlah")
        self.tree_pengeluaran.pack(pady=10)

        self.entry_keterangan = tk.Entry(self.frame_pengeluaran)
        self.entry_keterangan.pack(pady=5)

        self.entry_jumlah_pengeluaran = tk.Entry(self.frame_pengeluaran)
        self.entry_jumlah_pengeluaran.pack(pady=5)

        self.button_tambah_pengeluaran = tk.Button(self.frame_pengeluaran, text="Tambah Pengeluaran", command=self.tambah_pengeluaran)
        self.button_tambah_pengeluaran.pack(pady=10)

        self.button_hapus_pengeluaran = tk.Button(self.frame_pengeluaran, text="Hapus Pengeluaran", command=self.hapus_pengeluaran)
        self.button_hapus_pengeluaran.pack(pady=10)

        # Frame Laporan
        self.frame_laporan = tk.Frame(self.root, bg="lightgray")
        self.label_laporan = tk.Label(self.frame_laporan, text="Laporan Penjualan", font=("Arial", 16))
        self.label_laporan.pack(pady=10)

        self.tree_laporan = ttk.Treeview(self.frame_laporan, columns=("Tanggal", "Pemasukan", "Pengeluaran", "Laba"), show="headings")
        self.tree_laporan.heading("Tanggal", text="Tanggal")
        self.tree_laporan.heading("Pemasukan", text="Pemasukan")
        self.tree_laporan.heading("Pengeluaran", text="Pengeluaran")
        self.tree_laporan.heading("Laba", text="Laba")
        self.tree_laporan.pack(pady=10)

        self.button_export = tk.Button(self.frame_laporan, text="Export to Excel", command=self.export_to_excel)
        self.button_export.pack(pady=10)

        self.button_hapus_laporan = tk.Button(self.frame_laporan, text="Hapus Laporan", command=self.hapus_laporan)
        self.button_hapus_laporan.pack(pady=10)

        # Tampilkan frame daftar menu secara default
        self.show_daftar_menu()

    def show_daftar_menu(self):
        """Menampilkan frame daftar menu."""
        self.hide_all_frames()
        self.frame_daftar_menu.pack(fill="both", expand=True)
        self.update_daftar_menu()



    def update_daftar_menu(self):
        """Memperbarui tampilan daftar menu dengan gambar."""
        # Hapus widget lama di frame gambar menu
        for widget in self.frame_gambar_menu.winfo_children():
            widget.destroy()

        # Tampilkan gambar dan harga menu
        for item, details in self.menu.items():
            frame = tk.Frame(self.frame_gambar_menu, bg="lightgrey", bd=2, relief=tk.RAISED)
            frame.pack(side=tk.LEFT, padx=10, pady=10)

            try:
                # Load gambar
                image = Image.open(details["gambar"])
            except FileNotFoundError:
                # Gunakan gambar default jika gambar tidak ditemukan
                image = Image.open("nasi_goreng.png")  # Ganti dengan path gambar default
            image = image.resize((50, 30))
            photo = ImageTk.PhotoImage(image)
            self.menu_images.append(photo)  # Simpan referensi gambar

            label_image = tk.Label(frame, image=photo, bg="white")
            label_image.pack()

            label_nama = tk.Label(frame, text=item, bg="white", font=("Arial", 12))
            label_nama.pack()

            label_harga = tk.Label(frame, text=f"Rp {details['harga']}", bg="white", font=("Arial", 12))
            label_harga.pack()

            button_pesan = tk.Button(frame, text="Pesan", bg="lightblue", command=lambda i=item: self.tambah_pesanan(i))
            button_pesan.pack(pady=5)

            button_edit_harga = tk.Button(frame, text="Edit Harga", bg="lightgreen", command=lambda i=item: self.edit_harga(i))
            button_edit_harga.pack(pady=5)

            button_upload_gambar = tk.Button(frame, text="Upload Gambar", bg="lightyellow", command=lambda i=item: self.upload_gambar_menu(i))
            button_upload_gambar.pack(pady=5)


    def upload_gambar_menu(self, menu):
        """Mengupload gambar untuk menu yang dipilih."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.menu[menu]["gambar"] = file_path
            self.update_daftar_menu()
            messagebox.showinfo("Info", f"Gambar untuk menu {menu} berhasil diupload!")

    def tambah_pesanan(self, menu):
        """Menambahkan pesanan."""
        jumlah = simpledialog.askinteger("Jumlah", f"Masukkan jumlah {menu}:", minvalue=1)
        if jumlah:
            total = self.menu[menu]["harga"] * jumlah
            self.pesanan.append((menu, jumlah, total))
            messagebox.showinfo("Info", f"{menu} x{jumlah} telah ditambahkan ke pesanan!")
            self.update_pembayaran()

    def edit_harga(self, menu):
        """Mengedit harga menu."""
        harga_baru = simpledialog.askinteger("Edit Harga", f"Masukkan harga baru untuk {menu}:", minvalue=1)
        if harga_baru:
            self.menu[menu]["harga"] = harga_baru
            self.update_daftar_menu()
            messagebox.showinfo("Info", f"Harga {menu} berhasil diubah!")

    def update_pembayaran(self):
        """Memperbarui daftar pesanan."""
        self.tree_pesanan.delete(*self.tree_pesanan.get_children())
        total = 0
        for item in self.pesanan:
            self.tree_pesanan.insert("", "end", values=item)
            total += item[2]
        self.label_total.config(text=f"Total: Rp {total}")

    def bayar_pesanan(self):
        """Melakukan pembayaran."""
        total_pesanan = sum(item[2] for item in self.pesanan)
        self.laporan.append((datetime.now().strftime("%Y-%m-%d"), total_pesanan, 0, total_pesanan))
        messagebox.showinfo("Info", f"Total pembayaran: Rp {total_pesanan}")
        self.pesanan.clear()
        self.update_pembayaran()

    def hapus_pesanan(self):
        """Menghapus pesanan yang dipilih."""
        selected_item = self.tree_pesanan.selection()
        if selected_item:
            self.pesanan.pop(self.tree_pesanan.index(selected_item))
            self.update_pembayaran()
        else:
            messagebox.showwarning("Warning", "Pilih pesanan yang akan dihapus!")

    def cetak_struk_pdf(self):
        """Mencetak struk dalam format PDF."""
        if not self.pesanan:
            messagebox.showwarning("Warning", "Tidak ada pesanan untuk dicetak!")
            return

        # Buat objek PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Judul struk
        pdf.cell(200, 10, txt="Struk Pembayaran", ln=True, align="C")
        pdf.cell(200, 10, txt="Cafe dan Resto", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(10)

        # Tabel pesanan
        pdf.set_font("Arial", size=10)
        pdf.cell(60, 10, txt="Menu", border=1)
        pdf.cell(40, 10, txt="Jumlah", border=1)
        pdf.cell(40, 10, txt="Total", border=1)
        pdf.ln()

        total_pesanan = 0
        for item in self.pesanan:
            pdf.cell(60, 10, txt=item[0], border=1)
            pdf.cell(40, 10, txt=str(item[1]), border=1)
            pdf.cell(40, 10, txt=f"Rp {item[2]}", border=1)
            pdf.ln()
            total_pesanan += item[2]

        # Total pembayaran
        pdf.ln(30)
        pdf.cell(60, 10, txt=f"Total Pembayaran: Rp {total_pesanan}", border=1, ln=True, align="C")

        # Simpan file PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Info", "Struk berhasil dicetak sebagai PDF!")

    def show_pembayaran(self):
        """Menampilkan frame pembayaran."""
        self.hide_all_frames()
        self.frame_pembayaran.pack(fill="both", expand=True)
        self.update_pembayaran()

    def show_pengeluaran(self):
        """Menampilkan frame pengeluaran."""
        self.hide_all_frames()
        self.frame_pengeluaran.pack(fill="both", expand=True)
        self.update_pengeluaran()

    def update_pengeluaran(self):
        """Memperbarui daftar pengeluaran."""
        self.tree_pengeluaran.delete(*self.tree_pengeluaran.get_children())
        for item in self.pengeluaran:
            self.tree_pengeluaran.insert("", "end", values=item)

    def tambah_pengeluaran(self):
        """Menambahkan pengeluaran."""
        tanggal = datetime.now().strftime("%Y-%m-%d")
        keterangan = self.entry_keterangan.get()
        jumlah = self.entry_jumlah_pengeluaran.get()
        if keterangan and jumlah.isdigit():
            self.pengeluaran.append((tanggal, keterangan, int(jumlah)))
            self.update_pengeluaran()
            self.entry_keterangan.delete(0, tk.END)
            self.entry_jumlah_pengeluaran.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Silakan isi semua field dengan benar!")

    def hapus_pengeluaran(self):
        """Menghapus pengeluaran yang dipilih."""
        selected_item = self.tree_pengeluaran.selection()
        if selected_item:
            self.pengeluaran.pop(self.tree_pengeluaran.index(selected_item))
            self.update_pengeluaran()
        else:
            messagebox.showwarning("Warning", "Pilih pengeluaran yang akan dihapus!")

    def show_laporan(self):
        """Menampilkan frame laporan."""
        self.hide_all_frames()
        self.frame_laporan.pack(fill="both", expand=True)
        self.update_laporan()

    def update_laporan(self):
        """Memperbarui laporan penjualan."""
        self.tree_laporan.delete(*self.tree_laporan.get_children())
        for item in self.laporan:
            self.tree_laporan.insert("", "end", values=item)

    def hapus_laporan(self):
        """Menghapus laporan yang dipilih."""
        selected_item = self.tree_laporan.selection()
        if selected_item:
            self.laporan.pop(self.tree_laporan.index(selected_item))
            self.update_laporan()
        else:
            messagebox.showwarning("Warning", "Pilih laporan yang akan dihapus!")

    def export_to_excel(self):
        """Mengekspor laporan ke Excel."""
        if not self.laporan:
            messagebox.showwarning("Warning", "Tidak ada data laporan untuk diekspor!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.laporan, columns=["Tanggal", "Pemasukan", "Pengeluaran", "Laba"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Info", "Laporan berhasil diekspor ke Excel!")

    def hide_all_frames(self):
        """Menyembunyikan semua frame."""
        for frame in [self.frame_daftar_menu, self.frame_pembayaran, self.frame_pengeluaran, self.frame_laporan]:
            frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeRestoApp(root)
    root.mainloop()