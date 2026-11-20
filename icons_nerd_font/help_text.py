def show_help():
    print(
        """
Usage:
  icons-nerd-font [--font <path>]
  icons-nerd-font [--font <path>] <query>
  icons-nerd-font [--font <path>] --set <icon_set> <query>
  icons-nerd-font [--font <path>] --set <icon_set>
  icons-nerd-font [--font <path>] --sets
  icons-nerd-font [--font <path>] --copy <query>
  icons-nerd-font --help

Options:
  --font <path>
      Use a specific Nerd Font file. When omitted, the font is resolved in
      this order: $NERD_FONT, ~/.termux/font.ttf, then the first installed
      font with "nerd" in its filename (fontconfig is used when available).

  --sets
      Show all available icon sets.

  --set <icon_set> <query>
      Search for icons inside a specific icon set.

  --set <icon_set>
      Show all icons from a specific icon set.

  --copy <query>
      Copy the best matching glyph to the clipboard.

  --help
      Show this help message.

Interactive search:
  Type
      Search live.

  Backspace
      Delete the last character.

  Up / Down
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
  icons-nerd-font
  icons-nerd-font git
  icons-nerd-font python
  icons-nerd-font --set oct git
  icons-nerd-font --set dev python
  icons-nerd-font --set oct
  icons-nerd-font --sets
  icons-nerd-font --copy git_branch
  icons-nerd-font --font ~/fonts/JetBrainsMonoNerdFont-Regular.ttf git
"""
    )
