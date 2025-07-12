import csv
from collections import deque
from datetime import datetime, timedelta
import os

produk_file = 'produk.csv'
transaksi_file = 'transaksi.csv'
transaksi_queue = deque()

# -----------------------
# INISIALISASI FILE CSV
# -----------------------

def inisialisasi_csv():
    if not os.path.exists(produk_file):
        with open(produk_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'nama', 'harga', 'stok', 'deskripsi'])
            writer.writeheader()
    if not os.path.exists(transaksi_file):
        with open(transaksi_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['produk', 'jumlah', 'total', 'tanggal'])
            writer.writeheader()

# -----------------------
# FUNGSI CSV
# -----------------------

def load_produk():
    with open(produk_file, newline='') as f:
        return list(csv.DictReader(f))

def simpan_produk(data):
    with open(produk_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nama', 'harga', 'stok', 'deskripsi'])
        writer.writeheader()
        writer.writerows(data)

def simpan_transaksi(transaksi):
    with open(transaksi_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['produk', 'jumlah', 'total', 'tanggal'])
        writer.writerow(transaksi)

def load_transaksi():
    with open(transaksi_file, newline='') as f:
        return list(csv.DictReader(f))

# -----------------------
# CRUD PRODUK
# -----------------------

def tambah_produk():
    data = load_produk()
    id_baru = len(data) + 1
    nama = input("Nama produk: ")
    harga = input("Harga produk: ")
    stok = input("Stok produk: ")
    deskripsi = input("Deskripsi: ")
    data.append({'id': str(id_baru), 'nama': nama, 'harga': harga, 'stok': stok, 'deskripsi': deskripsi})
    simpan_produk(data)
    print("Produk berhasil ditambahkan!\n")

def tampilkan_produk():
    data = load_produk()
    if not data:
        print("\nProduk belum ada.\n")
        return False
    print("\n--- Daftar Produk ---")
    for p in data:
        print(f"ID {p['id']} | {p['nama']} | Harga: {p['harga']} | Stok: {p['stok']} | {p['deskripsi']}")
    print()
    return True

def ubah_produk():
    if not tampilkan_produk():
        return
    data = load_produk()
    id_edit = input("Masukkan ID produk yang ingin diubah: ")
    for p in data:
        if p['id'] == id_edit:
            p['nama'] = input("Nama baru: ")
            p['harga'] = input("Harga baru: ")
            p['stok'] = input("Stok baru: ")
            p['deskripsi'] = input("Deskripsi baru: ")
            simpan_produk(data)
            print("Produk berhasil diperbarui!\n")
            return
    print("Produk tidak ditemukan.\n")

def hapus_produk():
    if not tampilkan_produk():
        return
    data = load_produk()
    id_hapus = input("Masukkan ID produk yang ingin dihapus: ")
    data_baru = [p for p in data if p['id'] != id_hapus]
    if len(data) == len(data_baru):
        print("Produk tidak ditemukan.\n")
    else:
        simpan_produk(data_baru)
        print("Produk berhasil dihapus!\n")

# -----------------------
# TRANSAKSI
# -----------------------

def transaksi():
    if not tampilkan_produk():
        return
    data = load_produk()
    id_pilih = input("Masukkan ID produk yang dibeli: ")
    jumlah = int(input("Jumlah beli: "))

    for p in data:
        if p['id'] == id_pilih:
            if int(p['stok']) >= jumlah:
                total = int(p['harga']) * jumlah
                p['stok'] = str(int(p['stok']) - jumlah)
                waktu_transaksi = datetime.now().strftime('%Y/%m/%d')  # TANGGAL SAJA
                transaksi_data = {
                    'produk': p['nama'],
                    'jumlah': str(jumlah),
                    'total': str(total),
                    'tanggal': waktu_transaksi
                }
                simpan_transaksi(transaksi_data)
                transaksi_queue.append(transaksi_data)
                simpan_produk(data)
                print("Transaksi berhasil disimpan dan dimasukkan ke antrian.\n")
                return
            else:
                print("Stok tidak mencukupi.\n")
                return
    print("Produk tidak ditemukan.\n")

def proses_antrian():
    if transaksi_queue:
        t = transaksi_queue.popleft()
        print(f"Memproses transaksi: {t['produk']} | Jumlah: {t['jumlah']} | Total: Rp {t['total']}")
    else:
        print("Tidak ada transaksi dalam antrian.\n")

# -----------------------
# LAPORAN PENJUALAN
# -----------------------

def laporan_penjualan():
    data = load_transaksi()
    sekarang = datetime.now()
    harian = mingguan = bulanan = 0

    for t in data:
        try:
            tgl = datetime.strptime(t['tanggal'], '%Y/%m/%d')
            total = int(t['total'])

            if tgl.date() == sekarang.date():
                harian += total
            if sekarang - timedelta(days=7) <= tgl <= sekarang:
                mingguan += total
            if tgl.month == sekarang.month and tgl.year == sekarang.year:
                bulanan += total
        except Exception as e:
            print("Gagal baca transaksi:", t)
            continue

    print("\n--- Laporan Penjualan ---")
    print(f"Harian   : Rp {harian}")
    print(f"Mingguan : Rp {mingguan}")
    print(f"Bulanan  : Rp {bulanan}\n")

# -----------------------
# MENU UTAMA
# -----------------------

def menu():
    while True:
        print("=== Manajemen Jual Beli Minyak Wangi ===")
        print("1. Tambah Produk")
        print("2. Tampilkan Produk")
        print("3. Ubah Produk")
        print("4. Hapus Produk")
        print("5. Transaksi Penjualan")
        print("6. Proses Antrian Transaksi")
        print("7. Laporan Penjualan")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_produk()
        elif pilihan == "2":
            tampilkan_produk()
        elif pilihan == "3":
            ubah_produk()
        elif pilihan == "4":
            hapus_produk()
        elif pilihan == "5":
            transaksi()
        elif pilihan == "6":
            proses_antrian()
        elif pilihan == "7":
            laporan_penjualan()
        elif pilihan == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.\n")

inisialisasi_csv()
menu()
