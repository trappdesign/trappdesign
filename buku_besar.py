import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
import os

# Data simulasi
stock_data = [
    {"item": "Buku", "quantity": 50, "price": 20000},
    {"item": "Pulpen", "quantity": 100, "price": 5000},
    {"item": "Penghapus", "quantity": 30, "price": 3000},
]

sales_data = [
    {"item": "Buku", "quantity": 10, "price": 20000},
    {"item": "Pulpen", "quantity": 20, "price": 5000},
]

# Fungsi utama
def show_main_menu():
    main_window = tk.Tk()
    main_window.title("Aplikasi Buku Besar")
    main_window.geometry("600x400")
    
    def show_stock():
        display_data("Stock", stock_data)

    def show_sales():
        display_data("Penjualan", sales_data)
    
    def show_profit_loss():
        total_sales = sum(sale["quantity"] * sale["price"] for sale in sales_data)
        total_stock_value = sum(stock["quantity"] * stock["price"] for stock in stock_data)
        profit = total_sales - total_stock_value
        messagebox.showinfo("Laporan Untung Rugi", f"Total Penjualan: Rp {total_sales}\nNilai Stock: Rp {total_stock_value}\nKeuntungan: Rp {profit}")
    
    def print_report():
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        generate_report(file_path)
        os.startfile(file_path, "print")
        messagebox.showinfo("Cetak Laporan", "Laporan berhasil dicetak ke printer.")
    
    tk.Label(main_window, text="Menu Utama", font=("Arial", 16)).pack(pady=10)
    
    tk.Button(main_window, text="Lihat Stock", command=show_stock, width=20, pady=5).pack(pady=5)
    tk.Button(main_window, text="Lihat Penjualan", command=show_sales, width=20, pady=5).pack(pady=5)
    tk.Button(main_window, text="Laporan Untung Rugi", command=show_profit_loss, width=20, pady=5).pack(pady=5)
    tk.Button(main_window, text="Cetak Laporan", command=print_report, width=20, pady=5).pack(pady=5)
    
    main_window.mainloop()

def display_data(title, data):
    display_window = tk.Toplevel()
    display_window.title(f"{title} Data")
    display_window.geometry("400x300")
    
    tk.Label(display_window, text=title, font=("Arial", 16)).pack(pady=10)
    
    for record in data:
        record_text = ", ".join(f"{key}: {value}" for key, value in record.items())
        tk.Label(display_window, text=record_text).pack(anchor="w", padx=10)

def generate_report(file_path):
    pdf = canvas.Canvas(file_path)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "Laporan Stock dan Penjualan")
    
    y = 760
    pdf.drawString(100, y, "Stock:")
    y -= 20
    for stock in stock_data:
        pdf.drawString(120, y, f"{stock['item']} - Qty: {stock['quantity']}, Price: {stock['price']}")
        y -= 20
    
    y -= 20
    pdf.drawString(100, y, "Penjualan:")
    y -= 20
    for sale in sales_data:
        pdf.drawString(120, y, f"{sale['item']} - Qty: {sale['quantity']}, Price: {sale['price']}")
        y -= 20

    total_sales = sum(sale["quantity"] * sale["price"] for sale in sales_data)
    total_stock_value = sum(stock["quantity"] * stock["price"] for stock in stock_data)
    profit = total_sales - total_stock_value

    y -= 20
    pdf.drawString(100, y, f"Total Penjualan: Rp {total_sales}")
    y -= 20
    pdf.drawString(100, y, f"Nilai Stock: Rp {total_stock_value}")
    y -= 20
    pdf.drawString(100, y, f"Keuntungan: Rp {profit}")

    pdf.save()

if __name__ == "__main__":
    show_main_menu()
