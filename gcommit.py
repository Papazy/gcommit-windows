import git
# from openai import OpenAI
import os
import sys
import google.generativeai as genai

model_name = "gemini-1.5-flash-002"  

def generate_commit_message():
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
  # changes = repo.git.diff('None', cached=True)
  changes = repo.git.diff('HEAD', name_only=True).splitlines()
  
  if not changes:
    print("No changes to commit.")
    print("Please 'git add ' some changes before running this script.")
    sys.exit(0) # Keluar tanpa error karena tidak ada yang perlu di-commit
    
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
    # Menggunakan OPEN AI
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a helpful assistant that generates concise and informative commit messages."},
    #     {"role": "user", "content": prompt_text}
    #   ],
    #   max_tokens=150,
    #   temperature=0.7,
    # )
    
    # Menggunakan Google Generative AI
    response =  model.generate_content(prompt_text)
    
    
    # Mendapatkan pesan commit dari respons
    # print("Menerima respons dari API Gemini...")
    # print("response:",)
    commit_message = response.text.strip()
    print("\n--- Pesan Commit yang Disarankan ---")
    print(commit_message)
    print("------------------------------------")
    
    confirm = input("Apakah Anda ingin menggunakan pesan commit ini? (y/n): ").strip().lower()
    if confirm == 'y':
      # Melakukan commit dengan pesan yang dihasilkan
      repo.index.commit(commit_message)
      print("Commit berhasil dilakukan")
    else:
      print("Commit dibatalkan. Silakan masukkan pesan commit secara manual jika diperlukan.")
  except Exception as e:
    print(f"Error saat berkomunikasi dengan API Gemini: {e}")
    sys.exit(1)
    
  git.Repo.close(repo)  # Menutup repo untuk menghindari kebocoran memori
    
if __name__ == "__main__":
  generate_commit_message()
  
  
  
  