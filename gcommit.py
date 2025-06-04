import git
import os
import sys
import google.generativeai as genai
import time
import threading
from datetime import datetime

model_name = "gemini-1.5-flash-002"

class LoadingSpinner:
    def __init__(self, message="Loading"):
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.message = message
        self.spinning = False
        self.thread = None
    
    def spin(self):
        while self.spinning:
            for char in self.spinner_chars:
                if not self.spinning:
                    break
                print(f"\r{char} {self.message}...", end="", flush=True)
                time.sleep(0.1)
    
    def start(self):
        self.spinning = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
    
    def stop(self):
        self.spinning = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * (len(self.message) + 10), end="\r")

def generate_commit_message(push=False, remote_name=None, branch_name=None):
    print("\n┌─────────────────────────────────────────┐")
    print("│ 🤖 GCOMMIT - AI Git Commit Generator    │")
    print("└─────────────────────────────────────────┘\n")

    # API Key validation
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(" ❌ Error: GOOGLE_API_KEY not set")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)

    try:
        repo = git.Repo('.')
        if not repo.git.rev_parse('--is-inside-work-tree'):
            print(" ❌ Error: Not a valid git repository")
            sys.exit(1)
    except git.InvalidGitRepositoryError:
        print(" ❌ Error: Not a valid git repository")
        sys.exit(1)
    except Exception as e:
        print(f" ❌ Error: {e}")
        sys.exit(1)

    # Get changes
    changes = repo.git.diff('HEAD', cached=True, name_only=True).splitlines()
    if not changes:
        print(" ⚠️ No staged changes found")
        print(" 💡 Use 'git add' to stage changes first")
        sys.exit(0)

    print(f" 📁 Files to commit: {len(changes)}")
    for file in changes[:3]:
        print(f"    • {file}")
    if len(changes) > 3:
        print(f"    • ...and {len(changes) - 3} more files")

    # Generate commit message
    spinner = LoadingSpinner("Generating commit message")
    spinner.start()

    diff_details = repo.git.diff('HEAD', cached=True)
    prompt_text = f"""Create a concise commit message for these changes:
Files changed: {changes}
Diff: {diff_details[:1500]}

Use Conventional Commits format (e.g., feat:, fix:, docs:)
Keep it under 60 characters
Example: feat: add user authentication system

Return only the commit message:"""

    try:
        response = model.generate_content(prompt_text)
        spinner.stop()
        
        commit_message = response.text.strip()
        print("\n┌─ Suggested Commit Message ─────────────┐")
        print(f"│ {commit_message:<35} │")
        print("└───────────────────────────────────────┘\n")

        confirm = input("Use this message? [Y/n]: ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            # Perform commit
            spinner = LoadingSpinner("Committing changes")
            spinner.start()
            repo.index.commit(commit_message)
            spinner.stop()
            print(" ✅ Commit successful!")

            # Handle push if requested
            if push:
                if not remote_name or not branch_name:
                    print(" ❌ Error: Remote and branch required for push")
                    sys.exit(1)

                spinner = LoadingSpinner(f"Pushing to {remote_name}/{branch_name}")
                spinner.start()
                repo.git.push(remote_name, branch_name)
                spinner.stop()
                print(f" ✅ Pushed to {remote_name}/{branch_name}")
        else:
            print(" ⚠️ Commit cancelled")
            print(f" 💡 Manual commit: git commit -m \"{commit_message}\"")

    except Exception as e:
        spinner.stop()
        print(f" ❌ Error: {str(e)[:100]}")
        sys.exit(1)

    finally:
        git.Repo.close(repo)

if __name__ == "__main__":
    push_flag = '--push' in sys.argv
    remote_name = None
    branch_name = None

    if push_flag:
        try:
            remote_name = sys.argv[sys.argv.index('--push') + 1]
            branch_name = sys.argv[sys.argv.index('--push') + 2]
        except IndexError:
            print(" ❌ Error: Missing remote/branch after --push")
            print(" 💡 Usage: gcommit --push <remote> <branch>")
            sys.exit(1)

    # Ini adalah command
    generate_commit_message(push=push_flag, remote_name=remote_name, branch_name=branch_name)