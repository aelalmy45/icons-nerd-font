from dataclasses import dataclass
from fontTools.ttLib import TTFont
from collections import Counter


@dataclass
class Glyph:
    character: str
    codepoint: int
    name: str

    @property
    def unicode(self):
        return f"U+{self.codepoint:04X}"

    @property
    def prefix(self):
        if "-" not in self.name:
            return ""
        return self.name.split("-", 1)[0]

    @property
    def icon_name(self):
        if "-" not in self.name:
            return self.name
        return self.name.split("-", 1)[1]


def is_private_use(codepoint):
    return (
        0xE000 <= codepoint <= 0xF8FF
        or 0xF0000 <= codepoint <= 0xFFFFD
        or 0x100000 <= codepoint <= 0x10FFFD
    )


def load_glyphs(font_path):
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    glyphs = []
    for codepoint, glyph_name in cmap.items():
        if not is_private_use(codepoint):
            continue
        glyphs.append(
            Glyph(
                character=chr(codepoint),
                codepoint=codepoint,
                name=glyph_name,
            )
        )
    return glyphs


def search(glyphs, query, icon_set=None):
    query = query.lower().strip()
    if not query:
        return []
    results = []
    for glyph in glyphs:
        if icon_set and glyph.prefix != icon_set:
            continue
        name = glyph.name.lower()
        icon_name = glyph.icon_name.lower()
        score = 0
        if icon_name == query:
            score = 100
        elif icon_name.startswith(query):
            score = 80
        elif query in icon_name.split("_"):
            score = 70
        elif query in icon_name:
            score = 50
        elif query in name:
            score = 10
        else:
            continue
        results.append((score, glyph))
    results.sort(key=lambda item: (-item[0], item[1].name))
    return [glyph for score, glyph in results]


def get_icon_sets(glyphs):
    return Counter(
        glyph.prefix for glyph in glyphs if glyph.prefix
    )
