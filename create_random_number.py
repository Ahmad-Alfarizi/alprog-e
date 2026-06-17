import random
import string

def buat_sepuluh_ribu_kode():
    codes = set()
    total_target = 1757600

    print("Sedang memproses 10.000 kode unik...")
    
    while len(codes) < total_target:
        # Format: 2 + 3 huruf kecil + 2 angka
        letters = ''.join(random.choices(string.ascii_lowercase, k=3))
        digits = ''.join(random.choices(string.digits, k=2))
        code = f"2{letters}{digits}"
        codes.add(code)
    
    # Simpan langsung ke file.txt (Satu baris satu kode)
    with open("file.txt", "w") as file:
        file.write("\n".join(sorted(list(codes))))
        
    print(f"Berhasil! 10.000 kode unik telah disimpan ke dalam file 'file.txt'")

if __name__ == "__main__":
    buat_sepuluh_ribu_kode()

