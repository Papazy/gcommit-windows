import git
import os
import sys
import google.generativeai as genai

model_name = "gemini-1.5-flash-002"

def generate_commit_message(push=False, remote_name=None, branch_name=None):
  # Mendapatkan API KEY
  api_key = os.getenv("GOOGLE_API_KEY")
  if not api_key:
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    sys.exit(1)

  # Inisialisasi klien Google Generative AI
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel(model_name=model_name)

  try:
    # mendapatkan repo
    repo = git.Repo('.')

    # memastikan repo valid
    if not repo.git.rev_parse('--is-inside-work-tree'):
      print("Error: Not a valid git repository.")
      print("Please run this script inside a git repository.")
      sys.exit(1)

  except git.InvalidGitRepositoryError:
    print("Error: Not a valid git repository.")
    print("Please run this script inside a git repository.")
    sys.exit(1)
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

  # mendapatkan daftar perubahan
  changes = repo.git.diff('HEAD', name_only=True).splitlines()

  if not changes:
    print("No changes to commit.")
    print("Please 'git add ' some changes before running this script.")
    sys.exit(0)  # Keluar tanpa error karena tidak ada yang perlu di-commit

  # membuat prompt untuk OpenAI
  prompt_text = f"""Berikut adalah perubahan kode Git (git diff) yang telah dilakukan: {changes} 
  Hasilkan pesan commit Git yang singkat, ringkas, informatif, dan deskriptif berdasarkan perubahan di atas.
  Pesan commit harus mematuhi format Conventional Commits (misal: "feat:", "fix:", "docs:", "chore:", "refactor:").
  Contoh:
  feat: Tambahkan fitur otentikasi pengguna
  fix: Perbaiki bug pada fungsi login
  docs: Perbarui dokumentasi README

  Mohon sertakan hanya pesan commit, tanpa penjelasan tambahan atau header"""

  # mengirim permintaan ke OpenAI
  try:
    print("Mengirim permintaan ke API Gemini untuk menghasilkan pesan commit...")
    response = model.generate_content(prompt_text)

    commit_message = response.text.strip()
    print("\n--- Pesan Commit yang Disarankan ---")
    print(commit_message)
    print("------------------------------------")

    confirm = input("Apakah Anda ingin menggunakan pesan commit ini? (y/n): ").strip().lower()
    if confirm == 'y':
      # Melakukan commit dengan pesan yang dihasilkan
      repo.index.commit(commit_message)
      print("Commit berhasil dilakukan")

      # Push jika argumen push=True
      if push:
        if not remote_name or not branch_name:
          print("Error: Remote name and branch name must be specified for push.")
          sys.exit(1)

        print(f"Melakukan push ke {remote_name} {branch_name}...")
        repo.git.push(remote_name, branch_name)
        print("Push berhasil dilakukan.")
    else:
      print("Commit dibatalkan. Silakan masukkan pesan commit secara manual jika diperlukan.")
  except Exception as e:
    print(f"Error saat berkomunikasi dengan API Gemini: {e}")
    sys.exit(1)

  git.Repo.close(repo)  # Menutup repo untuk menghindari kebocoran memori

if __name__ == "__main__":
  # Memproses argumen dari command line
  push_flag = '--push' in sys.argv
  remote_name = None
  branch_name = None

  if push_flag:
    try:
      remote_name = sys.argv[sys.argv.index('--push') + 1]
      branch_name = sys.argv[sys.argv.index('--push') + 2]
    except IndexError:
      print("Error: Remote name and branch name must be specified after '--push'.")
      sys.exit(1)

  generate_commit_message(push=push_flag, remote_name=remote_name, branch_name=branch_name)