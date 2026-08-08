import sys
import os
from glyph import load_glyphs, search, get_icon_sets, Glyph
from ui import interactive_search
from clipboard import copy_to_clipboard
from help_text import show_help

FONT_PATH = os.path.expanduser("~/.termux/font.ttf")


def print_results_list(results, query, icon_set=None):
    print(f"Search: {query}")
    if icon_set:
        print(f"Icon set: {icon_set}")
    print(f"Results: {len(results)}")
    print()
    for glyph in results:
        print(f"{glyph.character}  {glyph.unicode:<8}  {glyph.name}")


def main():
    glyphs = load_glyphs(FONT_PATH)

    if len(sys.argv) <= 1:
        glyph = interactive_search(glyphs)
        if glyph is not None:
            if copy_to_clipboard(glyph.character):
                print(f"Copied: {glyph.character}")
                print(f"Unicode: {glyph.unicode}")
                print(f"Name: {glyph.name}")
        sys.exit(0)

    if sys.argv[1] in ("--help", "-h"):
        show_help()
        sys.exit(0)

    if sys.argv[1] == "--sets":
        icon_sets = get_icon_sets(glyphs)
        print("Icon Sets")
        print("-" * 30)
        for name, count in icon_sets.most_common():
            print(f"{name:<12} {count}")
        sys.exit(0)

    if sys.argv[1] == "--set":
        if len(sys.argv) < 3:
            print("Usage: python main.py --set <icon_set> [query]")
            sys.exit(1)
        icon_set = sys.argv[2]
        if len(sys.argv) == 3:
            results = [
                glyph for glyph in glyphs if glyph.prefix == icon_set
            ]
            results.sort(key=lambda glyph: glyph.codepoint)
            print(f"Icon set: {icon_set}")
            print(f"Results: {len(results)}")
            print()
            for glyph in results:
                print(f"{glyph.character}  {glyph.unicode:<8}  {glyph.name}")
            sys.exit(0)
        query = " ".join(sys.argv[3:])
        results = search(glyphs, query, icon_set)
        if not results:
            print(f'No results found for: {query}')
            sys.exit(1)
        glyph = interactive_search(results)
        if glyph is not None:
            if copy_to_clipboard(glyph.character):
                print(f"Copied: {glyph.character}")
                print(f"Unicode: {glyph.unicode}")
                print(f"Name: {glyph.name}")
        sys.exit(0)

    if sys.argv[1] == "--copy":
        if len(sys.argv) < 3:
            print("Usage: python main.py --copy <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = search(glyphs, query)
        if not results:
            print(f'No results found for: {query}')
            sys.exit(1)
        glyph = results[0]
        if copy_to_clipboard(glyph.character):
            print(f"Copied: {glyph.character}")
            print(f"Unicode: {glyph.unicode}")
            print(f"Name: {glyph.name}")
        sys.exit(0)

    query = " ".join(sys.argv[1:])
    results = search(glyphs, query)
    if not results:
        print(f'No results found for: {query}')
        sys.exit(1)
    glyph = interactive_search(glyphs)
    if glyph is not None:
        if copy_to_clipboard(glyph.character):
            print(f"Copied: {glyph.character}")
            print(f"Unicode: {glyph.unicode}")
            print(f"Name: {glyph.name}")


if __name__ == "__main__":
    main()
