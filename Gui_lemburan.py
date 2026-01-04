import tkinter as tk
from tkinter import messagebox
import datetime


#fungsi untuk menyimpan data lemburan
def simpan_lemburan():
    try:
        nama = entry_nama.get().strip()
        tanggal = entry_tanggal.get().strip()
        jam_mulai_str = entry_jam_mulai.get().strip()
        jam_selesai_str = entry_jam_selesai.get().strip()
        reason = entry_reason.get().strip()

        #validasi nama tidak boleh kosong
        if not nama:
            messagebox.showerror("error, nama tidak boleh kosong")
            return
        
        #validasi format tanggal
        tanggal_obj = datetime.datetime.strptime(tanggal, "%Y-%m-%d")
                                                 
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
            jam_selesai = jam_selesai + datetime.timedelta(days=1)
            lintas_hari = True

        #hitung durasi lemburan
        durasi = jam_selesai - jam_mulai
        durasi_jam = durasi.total_seconds() / 3600

        #tanggal selesai
        tanggal_selesai = jam_selesai.strftime("%Y-%m-%d")

        #simpan data ke file
        with open("data_lemburan.txt", "a") as f:
            f.write(f"Nama karyawan: {nama}, Tanggal Mulai: {tanggal}, Jam mulai lembur: {jam_mulai_str}, Tanggal Selesai: {tanggal_selesai}, Jam selesai lembur: {jam_selesai_str}, Durasi lembur: {int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit, Reason: {reason}\n")

        #pesan sukses
        pesan = f"Data lemburan {nama} telah dicatat\n\n"
        pesan += f"Dari: {tanggal} {jam_mulai_str}\n"
        pesan += f"Sampai: {tanggal_selesai} {jam_selesai_str}\n"
        pesan += f"Durasi: {int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit"

        if lintas_hari:
            pesan += "\n\nTerdeteksi lemburan lintas hari."
        
        messagebox.showinfo("sukses", pesan)

        #kosongkan field setelah simpan
        entry_nama.delete(0, tk.END)
        entry_tanggal.delete(0, tk.END)
        entry_jam_mulai.delete(0, tk.END)
        entry_jam_selesai.delete(0, tk.END)
        entry_reason.delete(0, tk.END)
    
    except ValueError:
        messagebox.showerror("Error", "format tanggal atau jam tidak valid")

#fungsi untuk lihat data lemburan
def lihat_data():
    try:
        with open("data_lemburan.txt", "r") as f:
            data = f.read()

            #buat window untuk tampilkan data
            window_data = tk.Toplevel(window)
            window_data.title("Data lemburan")
            window_data.geometry("600x400")

            #text widget untuk tampilkan data
            text_area = tk.Text(window_data)
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            #scrollbar
            scrollbar = tk.Scrollbar(text_area)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text_area.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_area.yview)

            #insert data
            text_area.insert(tk.END, data)
            text_area.config(state=tk.DISABLED) #buat read-only

    except FileNotFoundError:
        messagebox.showwarning("peringatan", "Belum ada data lemburan yang tercatat")

#buat window utama
window = tk.Tk()
window.title("Aplikasi Pencatatan Lemburan Karyawan")
window.geometry("450x450")
window.configure(bg="#f0f0f0")

#header
header = tk.Label(window, text="Pencatatan Lemburan Karyawan", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10)
header.pack(fill=tk.X)

#form frame
frame_form = tk.Frame(window, bg="#f0f0f0")
frame_form.pack(pady=20, padx=20)

#nama karyawan
tk.Label(frame_form, text="Nama Karyawan:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="W", pady=5)
entry_nama = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_nama.grid(row=0, column=1, pady=5)

#tanggal lemburan
tk.Label(frame_form, text="Tanggal (YYYY-MM-DD):", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="W", pady=5)
entry_tanggal = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_tanggal.grid(row=1, column=1, pady=5)

#jam mulai lemburan
tk.Label(frame_form, text="Jam mulai (HH:MM):", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky="W", pady=5)
entry_jam_mulai = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_jam_mulai.grid(row=2, column=1, pady=5)

#jam selesai lemburan
tk.Label(frame_form, text="Jam selesai (HH:MM):", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
entry_jam_selesai = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_jam_selesai.grid(row=3, column=1, pady=5)

#reason lemburan
tk.Label(frame_form, text="Reason Lembur:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky="W", pady=5)
entry_reason = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_reason.grid(row=4, column=1, pady=5)

#Tombol
frame_button = tk.Frame(window, bg="#f0f0f0")
frame_button.pack(pady=10)

tombol_simpan = tk.Button(frame_button, text="Simpan Data", command=simpan_lemburan, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),width=15, height=1)
tombol_simpan.grid(row=0, column=0, padx=5)

tombol_lihat = tk.Button(frame_button, text="Data Lemburan", command=lihat_data, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=15, height=1)
tombol_lihat.grid(row=0, column=1, padx=5)

#footer
footer = tk.Label(window, text="HUDA© 2026 - Sistem Pencatatan Lemburan", font=("Arial", 8), bg="#f0f0f0", fg="gray")
footer.pack(side=tk.BOTTOM, pady=10)

#jalankan aplikasi
window.mainloop()

