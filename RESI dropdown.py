import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

class AplikasiPembukuan:
    def __init__(self, root):
        self.root = root
        self.root.title("TrappDesign Resi ")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

    
# Fungsi untuk menghitung total harga
def calculate_total():
    try:
        satuan = int(satuan_entry.get())
        harga = float(harga_entry.get())
        total = satuan * harga
        total_label.config(text=f"Total: {total:.2f}")
    except ValueError:
        total_label.config(text="Total: Invalid input")

# Fungsi untuk menyimpan data
def save_data():
    pelanggan = pelanggan_entry.get()
    item = item_entry.get()
    jenis = jenis_combobox.get()
    ukuran = ukuran_combobox.get()
    satuan = satuan_entry.get()
    harga = harga_entry.get()
    
    if not pelanggan or not item or not jenis or not ukuran or not satuan or not harga:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    # Simpan data ke file CSV
    data = {
        'Tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Pelanggan': pelanggan,
        'Item': item,
        'Jenis': jenis,
        'Ukuran': ukuran,
        'Satuan': satuan,
        'Harga': harga,
        'Total': float(satuan) * float(harga)
    }
    
    try:
        df = pd.read_csv('resi_data.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Tanggal', 'Pelanggan', 'Item', 'Jenis', 'Ukuran', 'Satuan', 'Harga', 'Total'])
    
    df = df.append(data, ignore_index=True)
    df.to_csv('resi_data.csv', index=False)
    messagebox.showinfo("Success", "Data saved successfully.")

# Fungsi untuk mengekspor ke Excel
def export_to_excel():
    try:
        df = pd.read_csv('resi_data.csv')
        df.to_excel('resi_data.xlsx', index=False)
        messagebox.showinfo("Success", "Data exported to Excel successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data to export.")

# Fungsi untuk mencetak (sederhana, hanya menampilkan pesan)
def print_resi():
    messagebox.showinfo("Print", "Print functionality is not yet implemented.")

# Fungsi tentang aplikasi
def about():
    messagebox.showinfo("About", "Aplikasi Resi\n TrappDesign - Mirza Kamal 2025")

# Fungsi keluar dari aplikasi
def exit_app():
    root.quit()

# Fungsi untuk meng-clear semua field input
def clear_fields():
    pelanggan_entry.delete(0, tk.END)
    item_entry.delete(0, tk.END)
    jenis_combobox.set('')
    ukuran_combobox.set('')
    satuan_entry.delete(0, tk.END)
    harga_entry.delete(0, tk.END)
    total_label.config(text="Total: 0.00")  

    # Fungsi untuk mereset total
def reset_total():
    total_label.config(text="Total: 0.00")

# Membuat window utama
root = tk.Tk()
root.title("Aplikasi Resi")

# Tanggal otomatis
tanggal_label = tk.Label(root, text=f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
tanggal_label.grid(row=0, column=0, columnspan=2)

# Menambahkan label dan entry untuk pelanggan
pelanggan_label = tk.Label(root, text="Pelanggan:")
pelanggan_label.grid(row=1, column=0, sticky="e")
pelanggan_entry = tk.Entry(root)
pelanggan_entry.grid(row=1, column=1)

# Menambahkan label dan entry untuk nama item
item_label = tk.Label(root, text="Nama Item:")
item_label.grid(row=2, column=0, sticky="e")
item_entry = tk.Entry(root)
item_entry.grid(row=2, column=1)

# Dropdown untuk jenis
jenis_label = tk.Label(root, text="Jenis:")
jenis_label.grid(row=3, column=0, sticky="e")
jenis_combobox = ttk.Combobox(root, values=["Kalkir", "HVS", "DTF" ,"Sublime"])
jenis_combobox.grid(row=3, column=1)

# Dropdown untuk ukuran
ukuran_label = tk.Label(root, text="Ukuran:")
ukuran_label.grid(row=4, column=0, sticky="e")
ukuran_combobox = ttk.Combobox(root, values=["A0", "A1", "A2", "A3" ,"A4"])
ukuran_combobox.grid(row=4, column=1)

# Entry untuk satuan
satuan_label = tk.Label(root, text="Satuan:")
satuan_label.grid(row=5, column=0, sticky="e")
satuan_entry = tk.Entry(root)
satuan_entry.grid(row=5, column=1)

# Entry untuk harga
harga_label = tk.Label(root, text="Harga:")
harga_label.grid(row=6, column=0, sticky="e")
harga_entry = tk.Entry(root)
harga_entry.grid(row=6, column=1)

# Tombol untuk menghitung total
calculate_button = tk.Button(root, text="Hitung Total", command=calculate_total)
calculate_button.grid(row=7, column=0, columnspan=2)

# Label untuk menampilkan total
total_label = tk.Label(root, text="Total: 0.00")
total_label.grid(row=8, column=0, columnspan=2)

# Menambahkan menu bar
menu_bar = tk.Menu(root)

# Menu File
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command=save_data)
file_menu.add_command(label="Export to Excel", command=export_to_excel)
file_menu.add_command(label="Print", command=print_resi)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

menu_bar.add_cascade(label="Clear Fields", command=clear_fields)
menu_bar.add_cascade(label="Reset Total", command=reset_total)


# Menu Help
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

app = AplikasiPembukuan(root)



# Menjalankan aplikasi
root.mainloop()

