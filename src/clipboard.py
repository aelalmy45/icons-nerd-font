import subprocess
import shutil


def copy_to_clipboard(text):
    command = shutil.which("termux-clipboard-set")
    if command is None:
        print("Error: termux-clipboard-set was not found.")
        print("Install Termux:API and the termux-api package.")
        return False
    try:
        subprocess.run([command, text], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error: failed to copy to clipboard.")
        return False
