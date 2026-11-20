import sys

from .clipboard import copy_to_clipboard
from .fonts import find_nerd_font
from .glyph import get_icon_sets, load_glyphs, search
from .help_text import show_help
from .ui import interactive_search


def print_results_list(results, query=None, icon_set=None):
    if query is not None:
        print(f"Search: {query}")
    if icon_set:
        print(f"Icon set: {icon_set}")
    print(f"Results: {len(results)}")
    print()
    for glyph in results:
        print(f"{glyph.character}  {glyph.unicode:<8}  {glyph.name}")


def report_glyph(glyph):
    copied = copy_to_clipboard(glyph.character)
    label = "Copied" if copied else "Glyph"
    print(f"{label}: {glyph.character}")
    print(f"Unicode: {glyph.unicode}")
    print(f"Name: {glyph.name}")


def _extract_font_arg(argv):
    """Pull a global --font <path> option out of argv.

    Returns (font_path, remaining_argv). Exits with usage on a missing value.
    """
    remaining = []
    font_path = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--font":
            if index + 1 >= len(argv):
                print("Usage: icons-nerd-font --font <path> ...")
                sys.exit(1)
            font_path = argv[index + 1]
            index += 2
        else:
            remaining.append(arg)
            index += 1
    return font_path, remaining


def _load_glyphs_or_exit(font_path):
    if font_path is None:
        print("Error: no Nerd Font found.")
        print("Pass one with --font <path>, set $NERD_FONT, or install a Nerd Font.")
        sys.exit(1)
    try:
        glyphs = load_glyphs(font_path)
    except Exception as error:
        print(f"Error: could not read font {font_path}: {error}")
        sys.exit(1)
    if not glyphs:
        print(f"Error: {font_path} has no private-use glyphs - is it a Nerd Font?")
        sys.exit(1)
    return glyphs


def main():
    font_arg, args = _extract_font_arg(sys.argv[1:])

    if args and args[0] in ("--help", "-h"):
        show_help()
        sys.exit(0)

    glyphs = _load_glyphs_or_exit(find_nerd_font(font_arg))

    if not args:
        glyph = interactive_search(glyphs)
        if glyph is not None:
            report_glyph(glyph)
        sys.exit(0)

    if args[0] == "--sets":
        icon_sets = get_icon_sets(glyphs)
        print("Icon Sets")
        print("-" * 30)
        for name, count in icon_sets.most_common():
            print(f"{name:<12} {count}")
        sys.exit(0)

    if args[0] == "--set":
        if len(args) < 2:
            print("Usage: icons-nerd-font --set <icon_set> [query]")
            sys.exit(1)
        icon_set = args[1]
        if len(args) == 2:
            results = [glyph for glyph in glyphs if glyph.prefix == icon_set]
            results.sort(key=lambda glyph: glyph.codepoint)
            print(f"Icon set: {icon_set}")
            print(f"Results: {len(results)}")
            print()
            for glyph in results:
                print(f"{glyph.character}  {glyph.unicode:<8}  {glyph.name}")
            sys.exit(0)
        query = " ".join(args[2:])
        results = search(glyphs, query, icon_set)
        if not results:
            print(f"No results found for: {query}")
            sys.exit(1)
        glyph = interactive_search(glyphs, initial_query=query, icon_set=icon_set)
        if glyph is not None:
            report_glyph(glyph)
        sys.exit(0)

    if args[0] == "--copy":
        if len(args) < 2:
            print("Usage: icons-nerd-font --copy <query>")
            sys.exit(1)
        query = " ".join(args[1:])
        results = search(glyphs, query)
        if not results:
            print(f"No results found for: {query}")
            sys.exit(1)
        report_glyph(results[0])
        sys.exit(0)

    query = " ".join(args)
    results = search(glyphs, query)
    if not results:
        print(f"No results found for: {query}")
        sys.exit(1)
    glyph = interactive_search(glyphs, initial_query=query)
    if glyph is not None:
        report_glyph(glyph)


if __name__ == "__main__":
    main()
