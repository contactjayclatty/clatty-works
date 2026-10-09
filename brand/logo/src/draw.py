"""Clatty Works pixel logo concepts. Hand-placed pixel grids -> rect SVG + nearest-neighbour PNG.
Run: python3 draw.py"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAL = {
    "K": "#2A2E31",  # Charcoal outline
    "T": "#0F8A8A",  # Wizard Teal (arrow)
    "D": "#0A5C5C",  # Deep Teal (title strip)
    "G": "#D5D9DC",  # Panel Grey (pane body)
    "W": "#FFFFFF",  # Paper White (screen inset)
    "L": "#F2F4F5",  # bevel light
    "S": "#8E959A",  # bevel dark
    "A": "#E39B2D",  # Signal Amber (used sparingly)
}
# all-white single-colour version: structure pixels white, body pixels transparent
MONO_KEEP = set("KTD")
_PLEX_DIR = os.environ.get("PLEX_MONO_DIR", "fonts/IBM Plex Mono/").rstrip("/") + "/"
FONT_MONO_B = _PLEX_DIR + "IBMPlexMono-Bold.ttf"
FONT_MONO_M = _PLEX_DIR + "IBMPlexMono-Medium.ttf"


class Grid:
    def __init__(s, n):
        s.n = n
        s.px = [[None] * n for _ in range(n)]

    def set(s, x, y, c):
        if 0 <= x < s.n and 0 <= y < s.n:
            s.px[y][x] = c

    def rect(s, x, y, w, h, c):
        for j in range(y, y + h):
            for i in range(x, x + w):
                s.set(i, j, c)

    def pane(s, x, y, w, h, strip=2, dots=0, inset=None):
        """Bevelled pane: charcoal outline, solid Deep Teal title strip, grey body with 1px bevels."""
        s.rect(x, y, w, h, "K")
        s.rect(x + 1, y + 1, w - 2, strip, "D")
        # plain square dots (not real OS controls): grey squares on the strip
        for k in range(dots):
            s.set(x + w - 3 - 2 * k, y + 1 + (strip - 1) // 2, "G")
        by = y + 1 + strip
        s.rect(x + 1, by, w - 2, y + h - 1 - by, "G")
        s.rect(x + 1, by, w - 2, 1, "L")          # top bevel
        s.rect(x + 1, by, 1, y + h - 1 - by, "L")  # left bevel
        s.rect(x + 1, y + h - 2, w - 2, 1, "S")    # bottom bevel
        s.rect(x + w - 2, by + 1, 1, y + h - 2 - by, "S")  # right bevel
        if inset:
            ix, iy, iw, ih = inset
            s.rect(x + ix, y + iy, iw, ih, "W")

    def draw(s, art, ox, oy):
        """Stamp ascii art; '.' = untouched."""
        for j, row in enumerate(art):
            for i, ch in enumerate(row):
                if ch != ".":
                    s.set(ox + i, oy + j, ch)

    # ---- output ----
    def svg(s, path, mono=False, title=""):
        rects = []
        for y, row in enumerate(s.px):
            x = 0
            while x < s.n:
                c = row[x]
                if c is None or (mono and c not in MONO_KEEP):
                    x += 1
                    continue
                x2 = x
                while x2 + 1 < s.n and row[x2 + 1] == c:
                    x2 += 1
                fill = "#FFFFFF" if mono else PAL[c]
                rects.append(f'<rect x="{x}" y="{y}" width="{x2-x+1}" height="1" fill="{fill}"/>')
                x = x2 + 1
        with open(path, "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.n} {s.n}" width="{s.n}" height="{s.n}" shape-rendering="crispEdges">\n')
            if title:
                f.write(f"<title>{title}</title>\n")
            f.write("\n".join(rects) + "\n</svg>\n")

    def image(s, scale=1, mono=False, mono_color="#FFFFFF"):
        im = Image.new("RGBA", (s.n, s.n), (0, 0, 0, 0))
        for y, row in enumerate(s.px):
            for x, c in enumerate(row):
                if c is None:
                    continue
                if mono:
                    if c in MONO_KEEP:
                        im.putpixel((x, y), Image.new("RGB", (1, 1), mono_color).getpixel((0, 0)) + (255,))
                else:
                    h = PAL[c]
                    im.putpixel((x, y), (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255))
        if scale != 1:
            im = im.resize((s.n * scale, s.n * scale), Image.NEAREST)
        return im


# ---------------- arrows (with charcoal outline) ----------------
ARROW_R = [  # 11 wide x 9 tall, points right
    "......K....",
    "......KK...",
    "KKKKKKKTK..",
    "KTTTTTTTTK.",
    "KTTTTTTTTTK",
    "KTTTTTTTTK.",
    "KKKKKKKTK..",
    "......KK...",
    "......K....",
]
ARROW_R = [  # chunkier head
    "......KK....",
    "......KTK...",
    "KKKKKKKTTK..",
    "KTTTTTTTTTK.",
    "KTTTTTTTTTTK",
    "KTTTTTTTTTK.",
    "KKKKKKKTTK..",
    "......KTK...",
    "......KK....",
]


def flip(art):
    return [r[::-1] for r in art]



def arrow(g, x0, cy, shaft, t, hh, direction=1, outline=True, fill="T"):
    """Chunky pixel arrow. x0 = first fill column at the tail; direction 1 = right, -1 = left.
    t = shaft thickness (odd), hh = head half-height. Head is a clean 45-degree triangle.
    Outline is a 1px 4-connected charcoal ring."""
    pts = set()
    for k in range(shaft):
        for dy in range(-(t // 2), t // 2 + 1):
            pts.add((x0 + direction * k, cy + dy))
    for k in range(hh + 1):
        for dy in range(-(hh - k), hh - k + 1):
            pts.add((x0 + direction * (shaft + k), cy + dy))
    if outline:
        ring = set()
        for (x, y) in pts:
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if (nx, ny) not in pts:
                    ring.add((nx, ny))
        for p in ring:
            g.set(*p, "K")
    for p in pts:
        g.set(*p, fill)


def pane16(g, x, y, w, h):
    g.rect(x, y, w, h, "K")
    g.rect(x + 1, y + 1, w - 2, 1, "D")
    g.rect(x + 1, y + 2, w - 2, h - 3, "G")
    g.rect(x + 1, y + h - 2, w - 2, 1, "S")


# ---------------- Concept A: Classic ----------------
def concept_a32():
    g = Grid(32)
    g.pane(0, 3, 7, 26, strip=2, inset=(2, 5, 3, 15))            # phone (tall, narrow)
    g.set(3, 25, "K")                                             # plain square home dot
    g.pane(15, 9, 17, 14, strip=2, dots=2, inset=(2, 5, 13, 6))  # desktop (wide, landscape)
    arrow(g, 7, 16, 2, 3, 3, 1)                                   # tail on phone, tip 1px short of desktop
    return g


def concept_a16():
    g = Grid(16)
    pane16(g, 0, 1, 4, 14)
    pane16(g, 9, 5, 7, 6)
    arrow(g, 4, 8, 1, 1, 2, 1)
    return g


# ---------------- Concept B: Two-way ----------------
def concept_b32():
    g = Grid(32)
    g.pane(0, 3, 7, 26, strip=2, inset=(2, 5, 3, 15))
    g.set(3, 25, "K")
    g.pane(15, 9, 17, 14, strip=2, dots=2, inset=(2, 5, 13, 6))
    arrow(g, 7, 12, 3, 3, 2, 1)       # phone -> desktop
    arrow(g, 14, 20, 3, 3, 2, -1)     # desktop -> phone
    return g


def concept_b16():
    g = Grid(16)
    pane16(g, 0, 1, 4, 14)
    pane16(g, 10, 5, 6, 6)
    g.draw(["...T..", "TTTTT.", "TTTTTT", "TTTTT.", "...T.."], 4, 2)   # right arrow, chunky, no outline at 16px
    g.draw(["..T...", ".TTTTT", "TTTTTT", ".TTTTT", "..T..."], 4, 9)   # left arrow
    return g


# ---------------- Concept C: Monogram "C" ----------------
# Desktop pane = top bar of the C, phone pane = the spine, arrow = the bottom bar.
def concept_c32():
    g = Grid(32)
    g.pane(4, 2, 27, 10, strip=2, dots=2, inset=(9, 5, 15, 3))   # desktop across the top
    g.pane(1, 5, 10, 25, strip=2, inset=(2, 5, 6, 14))           # phone as the spine (in front)
    g.set(5, 26, "K"); g.set(6, 26, "K")
    arrow(g, 11, 25, 15, 3, 3, 1)                                 # bottom bar of the C
    return g


def concept_c16():
    g = Grid(16)
    pane16(g, 2, 1, 14, 6)
    pane16(g, 0, 3, 6, 13)
    arrow(g, 6, 12, 6, 1, 2, 1)
    return g


CONCEPTS = [
    ("A", "classic", "Classic", concept_a32, concept_a16),
    ("B", "two-way", "Two-way", concept_b32, concept_b16),
    ("C", "monogram", "Monogram", concept_c32, concept_c16),
]


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def tracked_text(draw, xy, text, font, fill, tracking_em=0.04):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + tracking_em * font.size
    return x


def text_width(text, font, tracking_em=0.04):
    return sum(font.getlength(c) for c in text) + tracking_em * font.size * (len(text) - 1)


def lockup(g, path, width=800):
    scale = 5  # 160px mark
    mark = g.image(scale)
    font = ImageFont.truetype(FONT_MONO_B, 56)
    word = "CLATTY WORKS"
    gap, pad = 40, 48
    tw = text_width(word, font, 0.04)
    # fit to target width by adjusting font size
    for size in range(80, 30, -1):
        font = ImageFont.truetype(FONT_MONO_B, size)
        tw = text_width(word, font, 0.04)
        if pad * 2 + mark.width + gap + tw <= width:
            break
    H = mark.height + pad * 2
    im = Image.new("RGB", (width, H), "white")
    mx = int((width - (mark.width + gap + tw)) // 2)
    im.paste(mark, (mx, pad), mark)
    d = ImageDraw.Draw(im)
    # vertically centre on cap height
    asc = font.getbbox("C")
    cap_h = asc[3] - asc[1]
    ty = pad + mark.height // 2 - cap_h // 2 - asc[1]
    tracked_text(d, (mx + mark.width + gap, ty), word, font, hexrgb(PAL["K"]))
    im.save(path)


def main():
    built = []
    for letter, slug, name, f32, f16 in CONCEPTS:
        g32, g16 = f32(), f16()
        base = os.path.join(OUT, f"{letter}-{slug}")
        g32.svg(f"{base}-mark-32.svg", title=f"Clatty Works mark concept {letter} ({name})")
        g32.svg(f"{base}-mark-32-white.svg", mono=True, title=f"Clatty Works mark concept {letter} ({name}), all-white")
        g16.svg(f"{base}-favicon-16.svg", title=f"Clatty Works favicon concept {letter} ({name})")
        g32.image(8).save(f"{base}-mark-256.png")
        g16.image(16).save(f"{base}-favicon-16-preview-256.png")
        g16.image(1).save(f"{base}-favicon-16.png")
        lockup(g32, f"{base}-lockup-horizontal.png")
        built.append((letter, name, g32, g16))
    sheet(built)


def sheet(built):
    S = 5            # mark display 160px
    cell_w, mark_px = 300, 32 * S
    col_x0 = 220
    W = col_x0 + cell_w * 3 + 40
    rows = [("On Paper White", "#FFFFFF", False),
            ("On Panel Grey", "#D5D9DC", False),
            ("All-white on Deep Teal", "#0A5C5C", True)]
    row_h = 220
    top = 150
    fav_h = 170
    H = top + row_h * len(rows) + fav_h + 60
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(FONT_MONO_B, 30)
    fm = ImageFont.truetype(FONT_MONO_M, 16)
    fl = ImageFont.truetype(FONT_MONO_B, 20)
    K = hexrgb(PAL["K"])
    tracked_text(d, (40, 30), "CLATTY WORKS  /  LOGO CONCEPTS", fb, K)
    d.text((40, 76), "Setup Wizard direction - pixel mark drafts for review (32px master shown at 5x)", font=fm, fill=hexrgb(PAL["D"]))
    for i, (letter, name, g32, g16) in enumerate(built):
        cx = col_x0 + cell_w * i
        d.text((cx + 20, top - 40), f"{letter}  {name.upper()}", font=fl, fill=K)
    for r, (label, bg, mono) in enumerate(rows):
        y = top + row_h * r
        d.rectangle([col_x0, y, col_x0 + cell_w * 3 - 1, y + row_h - 21], fill=bg, outline=hexrgb("#8E959A"))
        d.multiline_text((40, y + 80), label.replace(" on ", "\non "), font=fm, fill=K)
        for i, (letter, name, g32, g16) in enumerate(built):
            cx = col_x0 + cell_w * i + (cell_w - mark_px) // 2
            m = g32.image(S, mono=mono)
            im.paste(m, (cx, y + 20), m)
        for i in range(1, 3):
            x = col_x0 + cell_w * i
            d.line([x, y, x, y + row_h - 21], fill=hexrgb("#8E959A"))
    # favicon row: real size 16px + 32px, on white, grey and deep teal, plus 8x zoom
    y = top + row_h * len(rows)
    d.multiline_text((40, y + 40), "Favicon 16px\n(real size)\n+ 32px real\n+ 16px at 6x", font=fm, fill=K)
    for i, (letter, name, g32, g16) in enumerate(built):
        cx = col_x0 + cell_w * i + 20
        for k, (bg, mono) in enumerate([("#FFFFFF", False), ("#D5D9DC", False), ("#0A5C5C", True)]):
            bx = cx + k * 40
            d.rectangle([bx, y + 10, bx + 31, y + 41], fill=bg, outline=hexrgb("#8E959A"))
            f = g16.image(1, mono=mono)
            im.paste(f, (bx + 8, y + 18), f)
        bx = cx + 130
        m = g32.image(1)
        im.paste(m, (bx, y + 10), m)
        z = g16.image(6)
        im.paste(z, (cx, y + 55), z)
        d.text((cx + 110, y + 130), "16px @ 6x", font=fm, fill=hexrgb("#8E959A"))
    im.save(os.path.join(OUT, "concepts-sheet.png"))


if __name__ == "__main__":
    main()
