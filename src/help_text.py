def show_help():
    print(
        """
Usage:
  python main.py
  python main.py <query>
  python main.py --set <icon_set> <query>
  python main.py --set <icon_set>
  python main.py --sets
  python main.py --copy <query>
  python main.py --help

Options:
  --sets
      Show all available icon sets.

  --set <icon_set> <query>
      Search for icons inside a specific icon set.

  --set <icon_set>
      Show all icons from a specific icon set.

  --copy <query>
      Copy the best matching glyph to the Termux clipboard.

  --help
      Show this help message.

Interactive search:
  Type
      Search live.

  Backspace
      Delete the last character.

  ↑ / ↓
      Move selection.

  Home
      Select the first result.

  End
      Select the last result.

  PageUp
      Move one page up.

  PageDown
      Move one page down.

  Enter
      Copy the selected glyph.

  q / Esc
      Exit.

Examples:
  python main.py
  python main.py git
  python main.py python
  python main.py --set oct git
  python main.py --set dev python
  python main.py --set oct
  python main.py --sets
  python main.py --copy git_branch
"""
    )
