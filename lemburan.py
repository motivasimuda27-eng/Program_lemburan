import datetime

#fungsi untuk mencatat lemburan

def catat_lemburan():
    print("Masukan data lemburan")
    
    try:
        nama = input("Nama karyawan: ").strip()

        #nama tidak boleh kosong
        if not nama:
            print("nama tidak boleh kosong")
            return

        tanggal = input("tanggal (format: YYYY-MM-DD) ").strip()

        #validasi format tanggal
        datetime.datetime.strptime(tanggal, "%Y-%m-%d")

        jam_mulai_str = input("Jam mulai lembur (format HH:MM): ")
        jam_selesai_str = input("Jam selesai lembur(format HH:MM): ")

        #parsing jam
        jam_mulai = datetime.datetime.strptime(jam_mulai_str, "%H:%M")
        jam_selesai = datetime.datetime.strptime(jam_selesai_str, "%H:%M")
      
        durasi = jam_selesai - jam_mulai

        #cek durasi harus positif
        if durasi.total_seconds() <= 0:
            print("error: jam selesai harus lebih besar dari jam mulai")
            return

        #konversi durasi ke jam
        durasi_jam = durasi.total_seconds() / 3600


        #simpan data

        with open("data_lemburan.txt", "a") as f:
            f.write(f"{nama},{tanggal},{jam_mulai_str},{jam_selesai_str},{int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit\n")
        print(f"data lemburan untuk {nama} pada {tanggal} telah dicatat")
        print(f"durasi: ({int(durasi_jam)} jam {int((durasi_jam % 1) * 60)} menit)")

    except ValueError as e:
        print(f"error,input tidak valid:periksa kembali format input")

#fungsi untuk melihat data lemburan yang sudah tercatat

def lihat_lemburan():
    try:
        with open("data_lemburan.txt", "r") as f:
            print("\nData lemburan yang tercatat: ")
            print(f.read())
    except FileNotFoundError:
        print("Belum ada data lemburan yang tercatat.")

#fungsi utama

def main():
    while True:
        print("\nMenu:")
        print("1. catat lemburan")
        print("2. lihat data lemburan")
        print("3. keluar")

        pilihan = input("pilih menu (1/2/3): ")

        if pilihan == "1":
            catat_lemburan()
        elif pilihan == "2":
            lihat_lemburan()
        elif pilihan == "3":
            print("Terima kasih! program selesai")
            break
        else:
            print("pilihan tidak valid")

if __name__ == "__main__":
    main()
