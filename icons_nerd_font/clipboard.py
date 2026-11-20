import shutil
import subprocess

# (command, uses_stdin) in the order they are tried.
_CLIPBOARD_TOOLS = (
    ("termux-clipboard-set", False),  # Termux:API on Android
    ("pbcopy", True),                 # macOS
    ("wl-copy", True),                # Wayland
    ("xclip", True),                  # X11
    ("xsel", True),                   # X11
)

_EXTRA_ARGS = {
    "xclip": ["-selection", "clipboard"],
    "xsel": ["--clipboard", "--input"],
}


def _available(tool):
    return shutil.which(tool) is not None


def copy_to_clipboard(text):
    """Copy text with the first available clipboard tool.

    Returns True on success. Prints a hint and returns False when no
    clipboard tool is installed or the copy fails.
    """
    for tool, uses_stdin in _CLIPBOARD_TOOLS:
        if not _available(tool):
            continue
        command = [tool, *_EXTRA_ARGS.get(tool, [])]
        if not uses_stdin:
            command.append(text)
        try:
            subprocess.run(
                command,
                input=text if uses_stdin else None,
                text=True,
                check=True,
                capture_output=True,
            )
            return True
        except (subprocess.CalledProcessError, OSError):
            continue
    print("No clipboard tool found "
          "(tried: termux-clipboard-set, pbcopy, wl-copy, xclip, xsel).")
    print("The glyph is printed below so you can copy it manually.")
    return False
