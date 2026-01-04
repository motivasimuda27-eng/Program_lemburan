import tkinter as tk
from tkinter import messagebox
import datetime


#fungsi untuk menyimpan data lemburan
def simpan_lemburan():
    try:
        nama = entry_nama.get().strip()
        tanggal = entry_tanggal.get().strip()
        jam_mulai_str = entry_jam_mulai.get().strip()
        jam_selesai_str = entry_jam_mulai.get().strip()
        reason = enrty_reason.get().strip()

        #validasi nama tidak boleh kosong
        if not nama:
            messagebox.showerror("error, nama tidak boleh kosong")
            return
        
        #validasi format tanggal
        tanggal_obj = datetime.datetime.strptime(tanggal. %Y-%m-%d")
                                                 
        #parsing jam dan gabung dengan tanggal
        jam_mulai = datetime.datetime.strptime(f"{tanggal} {jam_mulai_str}", "%Y-%m-%d %H:%M")
        jam_selesai = datetime.datetime.strptime(f"{tanggal} {jam_selesai_str}", "%Y-%m-%d %H:%M")

        #validasi reason tidak boleh kosong
        if not reason:
            messagebox.showerror("error, Reason tidak boleh kosong")
            return

        #deteksi lintas hari
        lintas_hari = False
        if jam_selesai <= jam_mulai:
            jam_selesai = jaam_selesai + datetime.timedelta(days=1)
            lintas_hari = True

        #hitung durasi lemburan
        durasi = jam_selesai - jam_mulai
        durasi_jam = durasi.total_seconds() / 3600

        #tanggal selesai
        tanggal_selesai = jam_selesai.strftime("%Y-%m-%d")

        #simpan data ke file
        with open("data_lemburan.txt", "a") as f:
            f.write(f"Nama karyawan: {nama}, Tanggal Mulai: {tanggal}, Jam mulai lembur: {jam_mulai_str}, Tanggal Selesai: {tanggal_selesai}, Jam selesai lembur: {jam_selesai_str}, Durasi lembur: {int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit, Reason: {reason}\n")

