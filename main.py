import sqlite3
import datetime
import os

conn = sqlite3.connect('pos.db')
cursor = conn.cursor()


def menuUtama():
    print("===============================")
    print("Program Kasir Sederhana")
    print("===============================")
    print("[1] Mulai program kasir")
    print("[2] Lihat stok barang")
    print("\n[0] Keluar Program")
    print("===============================")
    pilihan = int(input("Pilihan >> "))

    if(pilihan==1):
        keranjangBelanjaMenu()
    elif(pilihan==2):
        lihatBarang()
    elif(pilihan==0):
        quit()
    else:
        print("Invalid input menu!")


def lihatBarang():
  print("=================================================================")
  print("\t\t\tLihat Barang")
  print("=================================================================")

  sql = """SELECT * FROM barang"""
  cursor.execute(sql)
  listbarang = cursor.fetchall()

  print("{:<3} {:<25} {:<12} {:<5}".format('ID','Nama barang','Stok','Harga'))
  for barang in listbarang:
      print("{:<3} {:<25} {:<12} {:<5}".format(barang[0],barang[1],barang[2],barang[3]))
  print("=================================================================")
  pause()


def keranjangBelanjaMenu():
  id_barang = int(input("Masukkan ID barang: "))

  sql = """SELECT * FROM barang WHERE id_barang = ?"""
  cursor.execute(sql, (id_barang,))

  if cursor.fetchone():
    keranjangBelanjaSistem(id_barang)
  else:
    print("\nBarang tidak dapat ditemukan")


def keranjangBelanjaSistem(id_barang):
  sql = """SELECT * FROM barang WHERE id_barang = ?"""
  cursor.execute(sql, (id_barang,))

  listbarang = cursor.fetchall()
  for barang in listbarang:
    print("\nNama barang:",barang[1])
    print("Harga barang:",barang[3])
    jumlah_barang_keranjang = int(input("Jumlah barang: "))
    jumlah_barang_baru = barang[2] - jumlah_barang_keranjang
    updateStok(barang[0],jumlah_barang_baru)
    pilihan = input("\nIngin tambahkan barang? (Y/N): ")

    sql = "INSERT INTO keranjang(id_barang,nama_barang,jumlah_barang,harga_barang) VALUES (?, ?, ?, ?)"
    record = (id_barang, barang[1], jumlah_barang_keranjang, barang[3])
    cursor.execute(sql,record)
    conn.commit()

    if(pilihan=="Y" or pilihan=="y"):
      keranjangBelanjaMenu()
    elif(pilihan=="N" or pilihan=="n"):
      cetakStruk()


def cetakStruk():
  tanggal = datetime.datetime.now()
  tanggal_transaksi = tanggal.strftime("%d-%m-%Y %H:%M")
  total_harga_belanja = 0
  jumlah_barang_dibeli = 0

  sql = """SELECT * FROM keranjang"""
  cursor.execute(sql)

  listbarang = cursor.fetchall()
  print("=================================")
  print("\tStruk Pembayaran")
  print("\t" + tanggal_transaksi)
  print("=================================\n")
  for barang in listbarang:
    print(" ",barang[1])
    total_harga = barang[3] * barang[2]
    print(" ",barang[3],"x",barang[2],"=",total_harga,"\n")
    total_harga_belanja = total_harga_belanja + total_harga
    jumlah_barang_dibeli = jumlah_barang_dibeli + barang[2]
  print("=================================")
  print(" Total Belanja: Rp",total_harga_belanja)
  total_tunai = int(input(" Tunai: Rp "))
  total_kembali = total_tunai - total_harga_belanja
  print(" Kembali: Rp",total_kembali)
  print("=================================")
  pause()
  clearKeranjang()


def clearKeranjang():
  sql ='''DELETE FROM keranjang;'''
  cursor.execute(sql)
  conn.commit()


def updateStok(id_barang,jumlah_baru):
    sql = """UPDATE barang SET jumlah_barang= ? WHERE id_barang= ?"""
    cursor.execute(sql, (jumlah_baru,id_barang,))
    conn.commit()

def pause():
  pilihan = input("Ingin kembali ke menu utama? (Y/N) ")
  if(pilihan=="Y" or pilihan=="y"):
    os.system("cls")
    menuUtama()
  elif(pilihan=="N" or pilihan=="n"):
    quit()


#Start program
menuUtama()
