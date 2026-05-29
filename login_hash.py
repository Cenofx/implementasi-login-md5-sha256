import hashlib
import json
import os
from colorama import init, Fore, Style

init(autoreset=True)

FILE_USER = "users.json"


# FUNGSI FILE
def load_users():
    if not os.path.exists(FILE_USER):
        return {}

    with open(FILE_USER, "r") as file:
        return json.load(file)


def save_users(users):
    with open(FILE_USER, "w") as file:
        json.dump(users, file, indent=4)


# HASHING
def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# TAMPILAN
def header():
    print(Fore.CYAN + "=" * 65)
    print(Fore.YELLOW + "     SISTEM LOGIN AMAN MENGGUNAKAN MD5 & SHA-256")
    print(Fore.CYAN + "=" * 65)


def menu():
    print("\n" + Fore.GREEN + "[1] Registrasi")
    print(Fore.GREEN + "[2] Login")
    print(Fore.GREEN + "[3] Lihat Data User")
    print(Fore.RED + "[4] Keluar")


# REGISTER
def register():
    print("\n" + Fore.YELLOW + "=== REGISTRASI AKUN ===")

    username = input("Username : ")
    password = input("Password : ")

    users = load_users()

    if username in users:
        print(Fore.RED + "\n[!] Username sudah terdaftar.")
        return

    md5_result = md5_hash(password)
    sha256_result = sha256_hash(password)

    users[username] = {
        "md5": md5_result,
        "sha256": sha256_result
    }

    save_users(users)

    print("\n" + Fore.GREEN + "✓ Registrasi Berhasil")
    print(Fore.CYAN + "-" * 65)
    print("Password Asli : ", password)
    print("Hash MD5      : ", md5_result)
    print("Hash SHA-256  : ", sha256_result)
    print(Fore.CYAN + "-" * 65)


# LOGIN
def login():
    print("\n" + Fore.YELLOW + "=== LOGIN USER ===")

    username = input("Username : ")
    password = input("Password : ")

    users = load_users()

    if username not in users:
        print(Fore.RED + "\n[!] Username tidak ditemukan.")
        return

    md5_input = md5_hash(password)
    sha256_input = sha256_hash(password)

    print("\n" + Fore.BLUE + "=== PROSES VERIFIKASI ===")
    print(Fore.CYAN + "-" * 65)

    print("Password Input    :", password)
    print("Hash MD5 Input    :", md5_input)
    print("Hash SHA256 Input :", sha256_input)

    print("\nHash SHA256 Tersimpan:")
    print(users[username]["sha256"])

    print(Fore.CYAN + "-" * 65)

    if sha256_input == users[username]["sha256"]:
        print(Fore.GREEN + "✓ LOGIN BERHASIL")
    else:
        print(Fore.RED + "✗ LOGIN GAGAL")


# LIHAT USER
def lihat_user():
    users = load_users()

    print("\n" + Fore.MAGENTA + "=== DATA USER TERSIMPAN ===")

    if not users:
        print("Belum ada data.")
        return

    print(Fore.CYAN + "-" * 120)
    print(f"{'USERNAME':<15} {'MD5':<35} {'SHA-256'}")
    print(Fore.CYAN + "-" * 120)

    for username, data in users.items():
        md5_value = data.get("md5") or data.get("password_md5") or "-"
        sha256_value = data.get("sha256") or data.get("password_sha256") or "-"

        print(
            f"{username:<15} "
            f"{md5_value:<35} "
            f"{sha256_value}"
        )

    print(Fore.CYAN + "-" * 120)


# MAIN PROGRAM
while True:
    header()
    menu()

    pilihan = input("\nPilih Menu : ")

    if pilihan == "1":
        register()

    elif pilihan == "2":
        login()

    elif pilihan == "3":
        lihat_user()

    elif pilihan == "4":
        print(Fore.YELLOW + "\nTerima kasih...")
        break

    else:
        print(Fore.RED + "\nMenu tidak tersedia!")

    input("\nTekan ENTER untuk kembali...")