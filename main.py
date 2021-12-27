import sqlite3

conn = sqlite3.connect('pos.db')
cursor = conn.cursor()

def menuKasir():
    print("==================================")
    print("Program Kasir")
    print("==================================")
    id_barang = int(input("Masukkan id barang: "))

    sql = """SELECT * FROM barang WHERE id_barang = ?"""
    cursor.execute(sql, (id_barang,))

    if cursor.fetchone():
        sistemKasir(id_barang)
    else:
        print("\nBarang tidak dapat ditemukan")

def sistemKasir(id_barang):
    sql = """SELECT * FROM barang WHERE id_barang= ?"""
    cursor.execute(sql, (id_barang,))

    listbarang = cursor.fetchall()
    for barang in listbarang:
        print("Nama barang:",barang[1])
        jumlah_barang = int(input("Masukkan jumlah beli: "))
        harga_barang = barang[3]
        total_harga = jumlah_barang * harga_barang
        print("Total Harga:",total_harga)
        jumlah_uang = int(input("Masukkan jumlah uang pembeli: "))
        total_kembalian = jumlah_uang - total_harga
        print("==================================")
        print("Total kembalian:", total_kembalian)
        print("==================================")
        jumlah_baru = barang[2] - jumlah_barang
        updateStok(id_barang,jumlah_baru)


def updateStok(id_barang,jumlah_baru):
    sql = """UPDATE barang SET jumlah_barang= ? WHERE id_barang= ?"""
    cursor.execute(sql, (id_barang,jumlah_baru,))
    conn.commit()
    print("Stok berhasil di update!")

menuKasir()
