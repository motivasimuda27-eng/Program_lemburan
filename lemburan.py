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

        tanggal = input("tanggal (format: YYYY-MM-DD): ").strip()

        #validasi format tanggal

        tanggal_obj = datetime.datetime.strptime(tanggal, "%Y-%m-%d")

        jam_mulai_str = input("Jam mulai lembur (format HH:MM): ").strip()
        jam_selesai_str = input("Jam selesai lembur(format HH:MM): ").strip()

        #parsing jam
        jam_mulai = datetime.datetime.strptime(f"{tanggal} {jam_mulai_str}", "%Y-%m-%d %H:%M")
        jam_selesai = datetime.datetime.strptime(f"{tanggal} {jam_selesai_str}", "%Y-%m-%d %H:%M")

        #input reason
        reason = input("Masukan reason lembur: ").strip()

        if jam_selesai <= jam_mulai:
            #tambah 1 hari ke jam selesai jika melewati tengah malam
            jam_selesai = jam_selesai + datetime.timedelta(days=1)
            print("jam melewati tengah malam")
      
        durasi = jam_selesai - jam_mulai

        #konversi durasi ke jam
        durasi_jam = durasi.total_seconds() / 3600

        #tanggal selesai
        tanggal_selesai = jam_selesai.strftime("%Y-%m-%d")


        #simpan data

        with open("data_lemburan.txt", "a") as f:
            f.write(f"Nama karyawan: {nama}, Tanggal Mulai: {tanggal}, Jam mulai lembur: {jam_mulai_str}, Tanggal selesai: {tanggal_selesai}, jam selesai lembur: {jam_selesai_str},Durasi lembur: {int(durasi_jam)} Jam {int((durasi_jam % 1) * 60)} menit, Reason: {reason}\n")
        print(f"data lemburan untuk {nama} telah dicatat")
        print(f"tanggal mulai: {tanggal}, tanggal selesai: {tanggal_selesai}")
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
