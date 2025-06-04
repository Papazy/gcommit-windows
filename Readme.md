
# Panduan Instalasi gcommit di Windows

Ikuti langkah-langkah berikut untuk mengatur alat gcommit di sistem operasi Windows.

## 1. Persiapan Awal

Sebelum memulai, pastikan Anda memiliki **Python** dan **Git** terinstal di komputer Anda.

- **Python 3.x**: Jika belum terinstal, unduh dari [python.org](https://www.python.org). Pastikan mencentang opsi "Add Python to PATH" saat instalasi.
- **Git**: Unduh dari [git-scm.com](https://git-scm.com/download/win) dan ikuti instruksi default.

Buka **Command Prompt** atau **PowerShell** untuk menjalankan semua perintah berikut. Anda dapat mencarinya di Start Menu.

---

## 2. Buat Folder Proyek dan Virtual Environment

### Buat Folder untuk gcommit
Jalankan perintah berikut untuk membuat folder khusus:

```bash
mkdir D:\gcommit-tool
cd D:\gcommit-tool
```

> **Catatan**: Anda dapat mengganti `D:\gcommit-tool` dengan lokasi lain, misalnya `C:\Users\NamaAnda\gcommit-tool`.


---

## 3. Instal Dependensi

Dengan virtual environment aktif, instal library Python yang diperlukan untuk gcommit:

```bash
pip install GitPython google-generativeai
```

---

## 4. Dapatkan dan Atur Google Gemini API Key

gcommit membutuhkan API Key dari Google Gemini untuk berkomunikasi dengan model AI.

### Dapatkan API Key
1. Buka [Google AI Studio](https://ai.google.com/studio) di browser Anda.
2. Login dengan akun Google Anda.
3. Klik **"Get API key"** di bagian kiri.
4. Klik **"Create API key in new project"** dan salin key yang muncul (diawali dengan `AIza...`).

### Atur API Key sebagai Variabel Lingkungan
1. Cari **"Edit the system environment variables"** di Start Menu Windows dan klik.
2. Pada jendela **System Properties**, klik tombol **Environment Variables...**.
3. Di bagian **User variables**, klik **New...**.
  - **Variable name**: `GOOGLE_API_KEY`
  - **Variable value**: Tempel API Key yang sudah disalin.
4. Klik **OK** pada semua jendela.

> **Penting**: Tutup dan buka kembali Command Prompt/PowerShell agar perubahan variabel lingkungan berlaku.

---


## 5. Tambahkan Folder ke PATH Sistem

Langkah ini memungkinkan Anda menjalankan `gcommit.bat` dari mana saja.

1. Cari **"Edit the system environment variables"** di Start Menu.
2. Klik tombol **Environment Variables...**.
3. Di bagian **User variables**, pilih variabel `Path` dan klik **Edit...**.
4. Klik **New** dan tambahkan path lengkap ke folder `gcommit-tool` Anda (misalnya, `D:\gcommit-tool\`).
5. Klik **OK** pada semua jendela.

> **Penting**: Tutup dan buka kembali Command Prompt/PowerShell agar perubahan PATH berlaku.

---

## Cara Menggunakan gcommit

1. Buka Command Prompt atau PowerShell.
2. Pindah ke direktori proyek Git Anda:
  ```bash
  cd C:\Users\NamaAnda\Documents\MyAwesomeProject
  ```
3. Lakukan staging perubahan:
  ```bash
  git add .
  ```
4. Jalankan alat gcommit:
  ```bash
  gcommit
  ```

gcommit akan menampilkan pesan commit yang disarankan oleh AI. Ketik `y` untuk melakukan commit atau `n` untuk membatalkannya.