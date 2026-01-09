import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import datetime


#fungsi untuk menyimpan data lemburan
def simpan_lemburan():
    try:
        nama = entry_nama.get().strip()
        
        # Ambil tanggal dari DateEntry (sudah format YYYY-MM-DD)
        tanggal = entry_tanggal.get()
        
        # Ambil jam dari spinbox
        jam_mulai_str = f"{spinbox_jam_mulai.get().zfill(2)}:{spinbox_menit_mulai.get().zfill(2)}"
        jam_selesai_str = f"{spinbox_jam_selesai.get().zfill(2)}:{spinbox_menit_selesai.get().zfill(2)}"
        
        reason = entry_reason.get().strip()

        #validasi nama tidak boleh kosong
        if not nama:
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
            return
        
        #validasi format tanggal
        tanggal_obj = datetime.datetime.strptime(tanggal, "%Y-%m-%d")
                                                 
        #parsing jam dan gabung dengan tanggal
        jam_mulai = datetime.datetime.strptime(f"{tanggal} {jam_mulai_str}", "%Y-%m-%d %H:%M")
        jam_selesai = datetime.datetime.strptime(f"{tanggal} {jam_selesai_str}", "%Y-%m-%d %H:%M")

        #validasi reason tidak boleh kosong
        if not reason:
            messagebox.showerror("Error", "Reason tidak boleh kosong!")
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
        pesan = f"✓ Data lemburan {nama} telah dicatat\n\n"
        pesan += f"Dari: {tanggal} {jam_mulai_str}\n"
        pesan += f"Sampai: {tanggal_selesai} {jam_selesai_str}\n"
        pesan += f"Durasi: {int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit"

        if lintas_hari:
            pesan += "\n\n⚠ Terdeteksi lemburan lintas hari"
        
        messagebox.showinfo("Sukses", pesan)

        #kosongkan field setelah simpan
        entry_nama.delete(0, tk.END)
        entry_reason.delete(0, tk.END)
        # Reset jam ke default
        spinbox_jam_mulai.delete(0, tk.END)
        spinbox_jam_mulai.insert(0, "0")
        spinbox_menit_mulai.delete(0, tk.END)
        spinbox_menit_mulai.insert(0, "00")
        spinbox_jam_selesai.delete(0, tk.END)
        spinbox_jam_selesai.insert(0, "0")
        spinbox_menit_selesai.delete(0, tk.END)
        spinbox_menit_selesai.insert(0, "00")
    
    except ValueError as e:
        messagebox.showerror("Error", f"Format tidak valid: {str(e)}")

#fungsi untuk lihat data lemburan
def lihat_data():
    try:
        with open("data_lemburan.txt", "r") as f:
            lines = f.readlines()

            if not lines:
                messagebox.showwarning("Peringatan", "Belum ada data lemburan yang tercatat")
                return
            
            #buat window baru untuk tampilkan data
            window_data = tk.Toplevel(window)
            window_data.title("Data Lemburan Karyawan")
            window_data.geometry("1000x500")

            #frame untuk table
            frame_table =  tk.Frame(window_data)
            frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            #buat treeview untuk tampilkan data
            columns = ("No", "Nama", "Tanggal mulai", "Jam mulai", "Tanggal selesai", "Jam selesai", "Durasi", "Reason")
            tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)

            #definisikan kolom
            tree.heading("No", text="No")
            tree.heading("Nama", text="Nama Karyawan")
            tree.heading("Tanggal mulai", text="Tgl Mulai")
            tree.heading("Jam mulai", text="Jam Mulai")
            tree.heading("Tanggal selesai", text="Tgl Selesai")
            tree.heading("Jam selesai", text="Jam Selesai")
            tree.heading("Durasi", text="Durasi")
            tree.heading("Reason", text="Reason")

            #lebar kolom
            tree.column("No", width=40, anchor="center")
            tree.column("Nama", width=150, anchor="w")
            tree.column("Tanggal mulai", width=100, anchor="center")
            tree.column("Jam mulai", width=80, anchor="center")
            tree.column("Tanggal selesai", width=100, anchor="center")
            tree.column("Jam selesai", width=80, anchor="center")
            tree.column("Durasi", width=120, anchor="center")
            tree.column("Reason", width=200, anchor="w")

            #scrollbar vertikal
            scrollbar_y = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar_y.set)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

            #scrollbar horizontal
            scrollbar_x = ttk.Scrollbar(frame_table, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview.Heading", background="#4CAF50", foreground="white", font=("Arial", 10, "bold"))
            style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")

            tree.pack(fill=tk.BOTH, expand=True)

            for idx, line in enumerate(lines, start=1):
                #parse dari format
                try:
                    parts = line.strip().split(", ")
                    
                    nama = parts[0].split(": ")[1] if len(parts) > 0 else "-"
                    tanggal = parts[1].split(": ")[1] if len(parts) > 1 else "-"
                    jam_mulai = parts[2].split(": ")[1] if len(parts) > 2 else "-"
                    tanggal_selesai = parts[3].split(": ")[1] if len(parts) > 3 else "-"
                    jam_selesai = parts[4].split(": ")[1] if len(parts) > 4 else "-"
                    durasi = parts[5].split(": ")[1] if len(parts) > 5 else "-"
                    reason = parts[6].split(": ")[1] if len(parts) > 6 else "-"

                    #insert ke treeview
                    tree.insert("", tk.END, values=(idx, nama, tanggal, jam_mulai, tanggal_selesai, jam_selesai, durasi, reason))
                
                except:
                    #jika parsing gagal, lewati baris ini
                    continue
            
            #style alternatif warna
            tree.tag_configure('oddrow', background='#f0f0f0')
            tree.tag_configure('evenrow', background='white')

            #apply tags
            for idx, item in enumerate(tree.get_children()):
                if idx % 2 ==0:
                    tree.item(item, tags=('evenrow',))
                else:
                    tree.item(item, tags=('oddrow', ))

            #label info data
            label_total = tk.Label(window_data, text=f"total data lemburan: {len(lines)} lemburan", font=("Arial", 10, "bold"), fg="#4CAF50")
            label_total.pack(pady=5)
        
    except FileNotFoundError:
        messagebox.showwarning("Peringatan", "Belum ada data lemburan yang tercatat")




#fungsi untuk validasi input hanya angka
def validate_number(value):
    if value == "":
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

#buat window utama
window = tk.Tk()
window.title("Aplikasi Pencatatan Lemburan Karyawan")
window.geometry("500x550")
window.configure(bg="#f0f0f0")

# Register validasi untuk input angka
vcmd = (window.register(validate_number), '%P')

#header
header = tk.Label(window, text="📋 Pencatatan Lemburan Karyawan", 
                  font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10)
header.pack(fill=tk.X)

#form frame
frame_form = tk.Frame(window, bg="#f0f0f0")
frame_form.pack(pady=20, padx=20)

#nama karyawan
tk.Label(frame_form, text="Nama Karyawan:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="W", pady=10)
entry_nama = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_nama.grid(row=0, column=1, columnspan=3, pady=10, sticky="W")

#tanggal lemburan dengan DateEntry (Calendar Picker)
tk.Label(frame_form, text="Tanggal:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="W", pady=10)

#frame untuk tanggal dan tombol pilih
frame_tanggal = tk.Entry(frame_form, bg="#f0f0f0")
frame_tanggal.grid(row=1, column=1, columnspan=3, sticky="W")

entry_tanggal = tk.Entry(frame_tanggal, width=15, font=("Arial", 10))
entry_tanggal.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
entry_tanggal.pack(side=tk.LEFT)

def pilih_tanggal():
    #buat window baru
    top=tk.Toplevel(window)
    top.title("Pilih tanggal")
    top.geometry("250x250")
    
    #calendar wigdet
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)
    
    def ambil_tanggal():
        entry_tanggal.delete(0, tk.END)
        entry_tanggal.insert(0, cal.get_date())
        top.destroy()
        
    tk.Button(top, text="pilih", command=ambil_tanggal, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=5)
    
tombol_calendar = tk.Button(frame_tanggal, text="📆", command=pilih_tanggal, font=("Arial", 12), width=3)
tombol_calendar.pack(side=tk.LEFT, padx=5)
        


#jam mulai lemburan
tk.Label(frame_form, text="Jam Mulai:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky="W", pady=10)

frame_jam_mulai = tk.Frame(frame_form, bg="#f0f0f0")
frame_jam_mulai.grid(row=2, column=1, columnspan=3, sticky="W", pady=10)

spinbox_jam_mulai = tk.Spinbox(frame_jam_mulai, from_=0, to=23, width=5, 
                                font=("Arial", 10), validate='key', 
                                validatecommand=vcmd, wrap=True)
spinbox_jam_mulai.delete(0, tk.END)
spinbox_jam_mulai.insert(0, "00")
spinbox_jam_mulai.pack(side=tk.LEFT)

tk.Label(frame_jam_mulai, text=":", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

spinbox_menit_mulai = tk.Spinbox(frame_jam_mulai, from_=0, to=59, width=5, 
                                  font=("Arial", 10), validate='key', 
                                  validatecommand=vcmd, wrap=True)
spinbox_menit_mulai.delete(0, tk.END)
spinbox_menit_mulai.insert(0, "00")
spinbox_menit_mulai.pack(side=tk.LEFT)

tk.Label(frame_jam_mulai, text="(HH : MM)", font=("Arial", 8), 
         bg="#f0f0f0", fg="gray").pack(side=tk.LEFT, padx=5)

#jam selesai lemburan
tk.Label(frame_form, text="Jam Selesai:", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="W", pady=10)

frame_jam_selesai = tk.Frame(frame_form, bg="#f0f0f0")
frame_jam_selesai.grid(row=3, column=1, columnspan=3, sticky="W", pady=10)

spinbox_jam_selesai = tk.Spinbox(frame_jam_selesai, from_=0, to=23, width=5, 
                                  font=("Arial", 10), validate='key', 
                                  validatecommand=vcmd, wrap=True)
spinbox_jam_selesai.delete(0, tk.END)
spinbox_jam_selesai.insert(0, "00")
spinbox_jam_selesai.pack(side=tk.LEFT)

tk.Label(frame_jam_selesai, text=":", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)

spinbox_menit_selesai = tk.Spinbox(frame_jam_selesai, from_=0, to=59, width=5, 
                                    font=("Arial", 10), validate='key', 
                                    validatecommand=vcmd, wrap=True)
spinbox_menit_selesai.delete(0, tk.END)
spinbox_menit_selesai.insert(0, "00")
spinbox_menit_selesai.pack(side=tk.LEFT)

tk.Label(frame_jam_selesai, text="(HH : MM)", font=("Arial", 8), 
         bg="#f0f0f0", fg="gray").pack(side=tk.LEFT, padx=5)

#reason lemburan
tk.Label(frame_form, text="Reason:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky="W", pady=10)
entry_reason = tk.Entry(frame_form, width=30, font=("Arial", 10))
entry_reason.grid(row=4, column=1, columnspan=3, pady=10, sticky="W")

#Tombol
frame_button = tk.Frame(window, bg="#f0f0f0")
frame_button.pack(pady=10)

tombol_simpan = tk.Button(frame_button, text="💾 Simpan Data", command=simpan_lemburan, 
                          bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                          width=15, height=1, cursor="hand2")
tombol_simpan.grid(row=0, column=0, padx=5)

tombol_lihat = tk.Button(frame_button, text="📄 Lihat Data", command=lihat_data, 
                         bg="#2196F3", fg="white", font=("Arial", 12, "bold"), 
                         width=15, height=1, cursor="hand2")
tombol_lihat.grid(row=0, column=1, padx=5)

#footer
footer = tk.Label(window, text="HUDA© 2026 - Sistem Pencatatan Lemburan", 
                  font=("Arial", 8), bg="#f0f0f0", fg="gray")
footer.pack(side=tk.BOTTOM, pady=10)

#jalankan aplikasi
window.mainloop()