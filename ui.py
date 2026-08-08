import sys
from terminal_utils import clear_screen, get_terminal_size, get_page_size, format_result
from keyboard import get_key
from glyph import search


def draw_search(query, results, selected, scroll):
    width, height = get_terminal_size()
    page_size = get_page_size()
    clear_screen()
    total = len(results)

    print(f"Search: {query}_")
    if total:
        print(f"Results: {total}    Selected: {selected + 1}/{total}")
    else:
        print("Results: 0")
    print()
    print(
        "Type to search   "
        "↑/↓ Navigate   "
        "Home/End Jump   "
        "PageUp/PageDown Page   "
        "Enter Copy   "
        "q/Esc Exit"
    )
    print()

    if not query:
        print("Type something to search...")
        sys.stdout.flush()
        return

    if not results:
        print(f'No results found for "{query}"')
        sys.stdout.flush()
        return

    visible_results = results[scroll:scroll + page_size]
    for index, glyph in enumerate(visible_results):
        real_index = scroll + index
        line = format_result(glyph, selected=(real_index == selected))
        if len(line) >= width:
            line = line[: max(width - 1, 1)]
        print(line)

    print()
    selected_glyph = results[selected]
    print(f"Selected: {selected_glyph.character}  {selected_glyph.name}")
    sys.stdout.flush()


def interactive_search(glyphs):
    query = ""
    results = []
    selected = 0
    scroll = 0

    while True:
        results = search(glyphs, query)
        if results:
            if selected >= len(results):
                selected = len(results) - 1
            page_size = get_page_size()
            if selected < scroll:
                scroll = selected
            elif selected >= scroll + page_size:
                scroll = selected - page_size + 1
            max_scroll = max(0, len(results) - page_size)
            scroll = min(scroll, max_scroll)
        else:
            selected = 0
            scroll = 0

        draw_search(query, results, selected, scroll)
        key = get_key()

        if key in ("ESC", "CTRL_C", "q", "Q"):
            clear_screen()
            return None

        if key == "ENTER":
            if results:
                clear_screen()
                return results[selected]
            continue

        if key == "BACKSPACE":
            if query:
                query = query[:-1]
                selected = 0
                scroll = 0
            continue

        if key == "UP":
            if results and selected > 0:
                selected -= 1
            continue

        if key == "DOWN":
            if results and selected < len(results) - 1:
                selected += 1
            continue

        if key == "HOME":
            if results:
                selected = 0
                scroll = 0
            continue

        if key == "END":
            if results:
                selected = len(results) - 1
                page_size = get_page_size()
                scroll = max(0, selected - page_size + 1)
            continue

        if key == "PAGE_UP":
            if results:
                page_size = get_page_size()
                selected = max(0, selected - page_size)
                scroll = max(0, scroll - page_size)
            continue

        if key == "PAGE_DOWN":
            if results:
                page_size = get_page_size()
                selected = min(len(results) - 1, selected + page_size)
                max_scroll = max(0, len(results) - page_size)
                scroll = min(max_scroll, scroll + page_size)
            continue

        if len(key) == 1 and key.isprintable():
            query += key
            selected = 0
            scroll = 0
            continue
