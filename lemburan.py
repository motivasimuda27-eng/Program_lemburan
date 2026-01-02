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

        jam_mulai = float(input("Jam mulai lembur: "))
        jam_selesai = float(input("Jam selesai lembur: "))

        durasi = jam_selesai - jam_mulai
        if durasi < 0:
            print("Jam selesai tidak valid")
            return
#simpan data

    with open("data_lemburan.txt", "a") as f:
        f.write(f"{nama},{tanggal},{jam_mulai},{jam_selesai},{durasi} Jam\n")
    print(f"data lemburan untuk {nama} pada {tanggal} telah dicatat")

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
