import os
import sys
import shutil as terminal


def get_terminal_size():
    size = terminal.get_terminal_size()
    return size.columns, size.lines


def get_page_size():
    _, height = get_terminal_size()
    page_size = height - 7  # search, status, help, footer etc.
    return max(page_size, 1)


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def format_result(glyph, selected=False):
    marker = "> " if selected else "  "
    return (
        f"{marker}"
        f"{glyph.character}  "
        f"{glyph.unicode:<8}  "
        f"{glyph.name}"
    )
