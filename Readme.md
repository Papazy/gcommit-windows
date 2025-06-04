# 🤖 gcommit untuk Windows dengan Virtual Environment

Panduan ini menjelaskan cara menginstal dan menggunakan **gcommit**, pembantu commit Git berbasis AI, di Windows menggunakan **Python virtual environment (venv)** dan Gemini AI .

---

## 📦 Prasyarat

Pastikan sistem Anda memiliki:

- **Python 3.x**
- **Git**

Jika belum, install:

1. Unduh Python dari [python.org](https://www.python.org/downloads/)
2. Unduh Git dari [git-scm.com](https://git-scm.com/download/windows)

Verifikasi instalasi di Command Prompt:
```batch
python --version
git --version
```

---



---

## 🗂️ 1. Clone Folder Proyek dan Simpan gcommit

```batch
# Clone repository di direktori pilihan Anda
git clone https://github.com/Papazy/gcommit-windows

cd gcommit-windows
```
---

## 🧪 2. Menyiapkan Virtual Environment (venv)

Buat virtual environment dengan menjalankan command berikut

```batch
python -m venv venv
```


---

## 📥 3. Aktifkan venv dan Install Dependencies

### Aktifkan virutal enviroment dengan command
```batch
.\venv\Scripts\activate
```

### Install paket yang diperlukan
```batch
pip install GitPython google-generativeai
```

---

## 🔐 4. Tambahkan Google Gemini API Key

Untuk menggunakan Gemini AI di gcommit, Anda memerlukan API Key.

### Cara mendapatkan API Key:
1. Kunjungi [Google AI Studio](https://ai.google.com/studio)
2. Login dengan akun Google Anda
3. Klik **"Get API key"** → **"Create API key in new project"**
4. Salin API Key yang diberikan (diawali dengan `AIza...`)

### Tambahkan API Key ke Environment Variables Windows:

1. Di pencarian windows ketik `Edit the system environment variables`, lalu klik
2. Buka tab "Advanced" → "Environment Variables"
3. Di bagian "User variables", klik "New"
4. Set Variable name: `GOOGLE_API_KEY`
5. Set Variable value: API key Anda
6. Klik "OK" untuk menyimpan

---


## 5. Tambahkan Folder ke PATH Sistem

Langkah ini memungkinkan Anda menjalankan `gcommit` dari mana saja.

1. Cari **"Edit the system environment variables"** di Start Menu.
2. Klik tombol **Environment Variables...**.
3. Di bagian **User variables**, pilih variabel `Path` dan klik **Edit...**.
4. Klik **New** dan tambahkan path lengkap ke folder `gcommit-windos` Anda (misalnya, `D:\gcommit-windows\`).
5. Klik **OK** pada semua jendela.

> **Penting**: Tutup dan buka kembali Command Prompt/PowerShell agar perubahan PATH berlaku.

---

## 🚀 Cara Menggunakan gcommit

1. Buka Command Prompt dan navigasi ke proyek Git Anda:
   ```batch
   cd folder-proyek-anda
   ```

2. Stage perubahan:
   ```batch
   git add .
   ```

3. Jalankan gcommit:
   ```batch
   gcommit
   ```

4. Ikuti instruksi di terminal:
   - Tekan `y` untuk menggunakan pesan commit yang disarankan
   - Tekan `n` untuk membatalkan

5. (opsional) push ke github
  ```batch
  git push
  ```
---

## 🧠 Tips

- Anda bisa menggunakan file `.env` sebagai alternatif environment variables
- Buat file batch berbeda seperti `gcommit-dev.bat`, `gcommit-prod.bat` untuk multiple environment

---

## ✅ Struktur Folder yang Disarankan

```
C:\Users\NamaUser\
└── Documents\
    └── gcommit-windows\
        ├── gcommit.py
        └── venv (opsional)
```

---

Selamat mencoba! 🚀