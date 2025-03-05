import sqlite3
from datetime import datetime
import os

#create game window
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 100


# Fungsi untuk menampilkan wallpaper awal
def tampilkan_wallpaper():
    wallpaper = """
    ======================================
    |                                     |
    |      SELAMAT DATANG DI LAPORAN      |
    |     BUKU BESAR TOKO TRAPP DESIGN    |
    |                                     |
    ======================================
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(wallpaper)

def jeda():
    input("\nTekan Enter untuk melanjutkan...")

# Membuat atau menghubungkan ke database
conn = sqlite3.connect('buku_besar.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS produk (
    id_produk INTEGER PRIMARY KEY,
    nama_produk TEXT NOT NULL,
    stok INTEGER NOT NULL,
    harga_beli INTEGER NOT NULL,
    harga_jual INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS penjualan (
    id_penjualan INTEGER PRIMARY KEY,
    id_produk INTEGER NOT NULL,
    jumlah_terjual INTEGER NOT NULL,
    total_harga INTEGER NOT NULL,
    tanggal TEXT NOT NULL,
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pembelian (
    id_pembelian INTEGER PRIMARY KEY,
    id_produk INTEGER NOT NULL,
    jumlah_beli INTEGER NOT NULL,
    total_harga INTEGER NOT NULL,
    tanggal TEXT NOT NULL,
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
)
''')

conn.commit()

# Fungsi untuk menambahkan produk baru
def tambah_produk(nama_produk, stok, harga_beli, harga_jual):
    cursor.execute('''INSERT INTO produk (nama_produk, stok, harga_beli, harga_jual) VALUES (?, ?, ?, ?)''', (nama_produk, stok, harga_beli, harga_jual))
    conn.commit()
    print(f"Produk '{nama_produk}' berhasil ditambahkan.")

# Fungsi untuk mencatat penjualan
def catat_penjualan(id_produk, jumlah_terjual):
    cursor.execute('SELECT stok, harga_jual FROM produk WHERE id_produk = ?', (id_produk,))
    result = cursor.fetchone()
    
    if result is None:
        print("Produk tidak ditemukan.")
        return

    stok, harga_jual = result

    if jumlah_terjual > stok:
        print("Stok tidak mencukupi.")
        return

    total_harga = jumlah_terjual * harga_jual
    tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    INSERT INTO penjualan (id_produk, jumlah_terjual, total_harga, tanggal)
    VALUES (?, ?, ?, ?)
    ''', (id_produk, jumlah_terjual, total_harga, tanggal))

    cursor.execute('''UPDATE produk SET stok = stok - ? WHERE id_produk = ?''', (jumlah_terjual, id_produk))

    conn.commit()
    print(f"Penjualan untuk produk ID {id_produk} berhasil dicatat.")

# Fungsi untuk mencatat pembelian
def catat_pembelian(id_produk, jumlah_beli, harga_beli):
    cursor.execute('SELECT stok FROM produk WHERE id_produk = ?', (id_produk,))
    result = cursor.fetchone()

    if result is None:
        print("Produk tidak ditemukan.")
        return

    total_harga = jumlah_beli * harga_beli
    tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    INSERT INTO pembelian (id_produk, jumlah_beli, total_harga, tanggal)
    VALUES (?, ?, ?, ?)
    ''', (id_produk, jumlah_beli, total_harga, tanggal))

    cursor.execute('''UPDATE produk SET stok = stok + ? WHERE id_produk = ?''', (jumlah_beli, id_produk))

    conn.commit()
    print(f"Pembelian untuk produk ID {id_produk} berhasil dicatat.")

# Fungsi untuk laporan penjualan
def laporan_penjualan():
    cursor.execute('''
    SELECT p.id_penjualan, pr.nama_produk, p.jumlah_terjual, p.total_harga, p.tanggal
    FROM penjualan p
    JOIN produk pr ON p.id_produk = pr.id_produk
    ORDER BY p.tanggal DESC
    ''')
    laporan = cursor.fetchall()

    print("\nLaporan Penjualan:")
    print("ID Penjualan | Nama Produk | Jumlah Terjual | Total Harga | Tanggal")
    print("-" * 60)
    for row in laporan:
        print(f"{row[0]:<13} | {row[1]:<12} | {row[2]:<14} | {row[3]:<11} | {row[4]}")

# Fungsi untuk laporan pembelian
def laporan_pembelian():
    cursor.execute('''
    SELECT b.id_pembelian, pr.nama_produk, b.jumlah_beli, b.total_harga, b.tanggal
    FROM pembelian b
    JOIN produk pr ON b.id_produk = pr.id_produk
    ORDER BY b.tanggal DESC
    ''')
    laporan = cursor.fetchall()

    print("\nLaporan Pembelian:")
    print("ID Pembelian | Nama Produk | Jumlah Beli | Total Harga | Tanggal")
    print("-" * 60)
    for row in laporan:
        print(f"{row[0]:<13} | {row[1]:<12} | {row[2]:<12} | {row[3]:<11} | {row[4]}")

# Fungsi untuk laporan untung rugi
def laporan_untung_rugi():
    cursor.execute('''
    SELECT SUM(penjualan.total_harga) as total_penjualan,
           (SELECT SUM(pembelian.total_harga) FROM pembelian) as total_pembelian
    FROM penjualan
    ''')
    result = cursor.fetchone()

    total_penjualan = result[0] if result[0] else 0
    total_pembelian = result[1] if result[1] else 0

    keuntungan = total_penjualan - total_pembelian

    print("\nLaporan Untung Rugi:")
    print(f"Total Penjualan: {total_penjualan}")
    print(f"Total Pembelian: {total_pembelian}")
    print(f"Keuntungan: {keuntungan}")

# Fungsi untuk melihat stok produk
def lihat_stok():
    cursor.execute('SELECT id_produk, nama_produk, stok, harga_beli, harga_jual FROM produk')
    stok = cursor.fetchall()

    print("\nStok Produk:")
    print("ID Produk | Nama Produk | Stok | Harga Beli | Harga Jual")
    print("-" * 50)
    for row in stok:
        print(f"{row[0]:<9} | {row[1]:<12} | {row[2]:<5} | {row[3]:<11} | {row[4]:<11}")

# Contoh penggunaan
def main():
    tampilkan_wallpaper()
    jeda()

    while True:
        print("\nMenu:")
        print("1. Tambah Produk")
        print("2. Catat Penjualan")
        print("3. Catat Pembelian")
        print("4. Laporan Penjualan")
        print("5. Laporan Pembelian")
        print("6. Laporan Untung Rugi")
        print("7. Lihat Stok")
        print("8. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            nama = input("Nama produk: ")
            stok = int(input("Stok: "))
            harga_beli = int(input("Harga Beli: "))
            harga_jual = int(input("Harga Jual: "))
            tambah_produk(nama, stok, harga_beli, harga_jual)
        elif pilihan == '2':
            id_produk = int(input("ID Produk: "))
            jumlah = int(input("Jumlah Terjual: "))
            catat_penjualan(id_produk, jumlah)
        elif pilihan == '3':
            id_produk = int(input("ID Produk: "))
            jumlah = int(input("Jumlah Beli: "))
            harga_beli = int(input("Harga Beli: "))
            catat_pembelian(id_produk, jumlah, harga_beli)
        elif pilihan == '4':
            laporan_penjualan()
        elif pilihan == '5':
            laporan_pembelian()
        elif pilihan == '6':
            laporan_untung_rugi()
        elif pilihan == '7':
            lihat_stok()
        elif pilihan == '8':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()

# Menutup koneksi database saat program selesai
def tutup_koneksi():
    conn.close()
tutup_koneksi()
