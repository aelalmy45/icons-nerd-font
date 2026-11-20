import os
import shutil
import subprocess

FONT_EXTENSIONS = (".ttf", ".otf", ".ttc")

# Directories scanned (recursively) for a Nerd Font when no explicit path is
# given and the Termux default does not exist.
FONT_DIRS = (
    "~/.local/share/fonts",
    "~/fonts",
    "/usr/local/share/fonts",
    "/usr/share/fonts",
    "~/Library/Fonts",
    "/Library/Fonts",
)

TERMUX_FONT = "~/.termux/font.ttf"
ENV_VAR = "NERD_FONT"


def _looks_like_nerd_font(path):
    name = os.path.basename(path).lower()
    return "nerd" in name


def _walk_font_files(directory):
    for root, _dirs, files in os.walk(directory):
        for filename in sorted(files):
            if filename.lower().endswith(FONT_EXTENSIONS):
                yield os.path.join(root, filename)


def _fc_list_nerd_fonts():
    """Yield Nerd Font paths reported by fontconfig, when available."""
    if shutil.which("fc-list") is None:
        return
    try:
        output = subprocess.run(
            ["fc-list", ":fontformat=TrueType", "file"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (subprocess.CalledProcessError, OSError):
        return
    for line in output.splitlines():
        path = line.split(":", 1)[0].strip()
        if path and _looks_like_nerd_font(path):
            yield path


def font_candidates():
    """Yield candidate font paths in priority order."""
    termux = os.path.expanduser(TERMUX_FONT)
    if os.path.isfile(termux):
        yield termux
    env_font = os.environ.get(ENV_VAR, "").strip()
    if env_font:
        yield os.path.expanduser(env_font)
    for directory in FONT_DIRS:
        directory = os.path.expanduser(directory)
        if not os.path.isdir(directory):
            continue
        for path in _walk_font_files(directory):
            if _looks_like_nerd_font(path):
                yield path
    yield from _fc_list_nerd_fonts()


def has_private_use_glyphs(font_path):
    """True when the font maps codepoints in the private use areas."""
    from fontTools.ttLib import TTFont

    from .glyph import is_private_use

    try:
        font = TTFont(font_path, fontNumber=0, lazy=True)
    except Exception:
        return False
    try:
        cmap = font.getBestCmap()
        if cmap is None:
            return False
        return any(is_private_use(codepoint) for codepoint in cmap)
    finally:
        font.close()


def find_nerd_font(explicit_path=None):
    """Resolve the font to use.

    Order: explicit --font path, $NERD_FONT, ~/.termux/font.ttf, installed
    fonts with "nerd" in the filename (font directories, then fontconfig).
    Returns the path, or None when nothing usable was found.
    """
    if explicit_path:
        path = os.path.expanduser(explicit_path)
        return path if os.path.isfile(path) else None
    seen = set()
    for path in font_candidates():
        if path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path) and has_private_use_glyphs(path):
            return path
    return None
