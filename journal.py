#!/usr/bin/env python3
"""
Mindful Journal CLI
Aplikasi jurnal harian berbasis teks.
"""

import json
import os
import sys
from datetime import datetime

# Pastikan output stdout menggunakan UTF-8 (diperlukan untuk karakter Unicode di Windows)
sys.stdout.reconfigure(encoding='utf-8')

LOGS_DIR = "logs"
SENTINEL = "SELESAI"


# ──────────────────────────────────────────────
# Fungsi: Sapaan Pembuka
# ──────────────────────────────────────────────
def greet():
    print()
    print("╔══════════════════════════════════════════╗")
    print("║      🧘  Mindful Journal CLI  🧘         ║")
    print("║   Jurnal harian untuk merenungi hari    ║")
    print("╚══════════════════════════════════════════╝")
    print()


# ──────────────────────────────────────────────
# Fungsi: Tanya Tingkat Kepuasan
# ──────────────────────────────────────────────
def ask_satisfaction():
    print("📊  Bagaimana tingkat kepuasan kamu hari ini?")
    print("    (1 = sangat buruk, 10 = sangat bahagia)")
    print()

    while True:
        raw = input("    Masukkan angka 1–10: ").strip()
        try:
            val = int(raw)
            if 1 <= val <= 10:
                print(f"    ✅  Tingkat kepuasan: {val}/10")
                return val
            else:
                print("    ⚠️  Masukkan angka antara 1 sampai 10.")
        except ValueError:
            print("    ⚠️  Input tidak valid. Masukkan angka, misalnya 7.")


# ──────────────────────────────────────────────
# Fungsi: Tanya 3 Hal Syukur
# ──────────────────────────────────────────────
def ask_gratitude():
    print()
    print("🙏  Sebutkan 3 hal yang paling kamu syukuri hari ini.")
    print("    (tekan Enter untuk melanjutkan ke pertanyaan berikutnya)")
    print()

    gratitude = []

    for i in range(1, 4):
        while True:
            item = input(f"    {i}. ").strip()
            if item:
                gratitude.append(item)
                break
            else:
                print("    ⚠️  Jangan kosong. Tulis setidaknya satu kata.")
        print()

    print("📝  Ringkasan rasa syukur:")
    for item in gratitude:
        print(f"    • {item}")
    print()

    return gratitude


# ──────────────────────────────────────────────
# Fungsi: Tanya Catatan Evaluasi
# ──────────────────────────────────────────────
def ask_notes():
    print("📓  Tulis catatan evaluasi hari ini.")
    print(f"    (ketik '{SENTINEL}' di baris baru untuk mengakhiri)")
    print()

    lines = []
    while True:
        line = input("    ")
        if line.strip().upper() == SENTINEL:
            break
        lines.append(line)

    notes = "\n".join(lines).strip()
    print()

    if notes:
        print("📋  Catatan yang kamu tulis:")
        for line in notes.split("\n"):
            print(f"    {line}")
    else:
        print("    (tidak ada catatan)")
    print()

    return notes


# ──────────────────────────────────────────────
# Fungsi: Pastikan folder logs ada
# ──────────────────────────────────────────────
def ensure_logs_folder():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        print(f"📁  Folder '{LOGS_DIR}/' dibuat.")
    else:
        print(f"📁  Folder '{LOGS_DIR}/' sudah ada.")


# ──────────────────────────────────────────────
# Fungsi: Muat entri dari file JSON
# ──────────────────────────────────────────────
def load_entries(date_str):
    filepath = os.path.join(LOGS_DIR, f"{date_str}.json")

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []


# ──────────────────────────────────────────────
# Fungsi: Simpan / append entri ke JSON
# ──────────────────────────────────────────────
def save_entry(date_str, entry):
    filepath = os.path.join(LOGS_DIR, f"{date_str}.json")
    entries = load_entries(date_str)
    entries.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# Fungsi: Tanya append atau tidak
# ──────────────────────────────────────────────
def ask_append():
    print("⚠️  File untuk hari ini sudah ada.")
    print("    Ingin menambahkan entri baru di bawahnya? (y/n)")
    print()

    while True:
        answer = input("    Jawaban: ").strip().lower()
        if answer in ("y", "yes", "ya", "yya"):
            print("    ✅  Akan menambahkan entri baru.")
            return True
        elif answer in ("n", "no", "tidak", "ndak"):
            print("    👋  Baiknya. Jurnal kamu tetap aman.")
            return False
        else:
            print("    ⚠️  Masukkan 'y' untuk ya atau 'n' untuk tidak.")


# ──────────────────────────────────────────────
# Fungsi: Konfirmasi sukses
# ──────────────────────────────────────────────
def confirm_saved(date_str):
    print()
    print("╔══════════════════════════════════════════╗")
    print("║  🎉  Entri jurnal berhasil disimpan! 🎉  ║")
    print("╚══════════════════════════════════════════╝")
    print(f"    📂  File: {LOGS_DIR}/{date_str}.json")
    print()
    print("    Terima kasih sudah menulis jurnal hari ini.")
    print("    Sampai jumpa besok! 💚")
    print()


# ──────────────────────────────────────────────
# Orchestrator Utama
# ──────────────────────────────────────────────
def main():
    greet()

    # Minta data dari pengguna
    satisfaction = ask_satisfaction()
    gratitude = ask_gratitude()
    notes = ask_notes()

    # Siapkan timestamp dan nama file
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.strftime("%Y-%m-%dT%H:%M:%S")

    # Bangun entri
    entry = {
        "timestamp": timestamp_str,
        "satisfaction": satisfaction,
        "gratitude": gratitude,
        "notes": notes,
    }

    # Pastikan folder logs ada
    ensure_logs_folder()

    # Cek apakah file sudah ada
    filepath = os.path.join(LOGS_DIR, f"{date_str}.json")
    if os.path.exists(filepath):
        if not ask_append():
            return

    # Simpan entri
    save_entry(date_str, entry)
    confirm_saved(date_str)


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
