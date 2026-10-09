"""Build the final Clatty Works logo files into /brand/logo/.
Approved 9 Oct 2026: concept A (Classic) = primary mark and lockups, concept C (Monogram) = favicon and avatar.
Pixel art comes from draw.py (hand-placed grids). Wordmark = IBM Plex Mono Bold (OFL-1.1), outlined to SVG paths.
Run: python3 build_logo.py   (needs Pillow and fontTools; set PLEX_MONO_DIR to the IBM Plex Mono TTF folder)"""
import os
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import draw
from draw import PAL, MONO_KEEP, concept_a32, concept_c32, concept_c16, hexrgb

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_DIR = os.environ.get("PLEX_MONO_DIR", "fonts/IBM Plex Mono/").rstrip("/") + "/"
F_BOLD = FONT_DIR + "IBMPlexMono-Bold.ttf"
F_MED = FONT_DIR + "IBMPlexMono-Medium.ttf"
WORD = "CLATTY WORKS"
TAGLINE = "Setup complete."
TRACK = 0.04          # +40 tracking (em)
CLEAR = 9             # clear space = arrow height of mark A (9 grid px incl. outline)

A, C, C16 = concept_a32(), concept_c32(), concept_c16()


# ---------------- text helpers (one metric source for SVG and PNG) ----------------
class Face:
    def __init__(s, path):
        s.path, s.tt = path, TTFont(path)
        s.upm = s.tt["head"].unitsPerEm
        s.cap = s.tt["OS/2"].sCapHeight / s.upm
        s.cmap, s.hmtx, s.gs = s.tt.getBestCmap(), s.tt["hmtx"], s.tt.getGlyphSet()

    def positions(s, text, size):
        x, out = 0.0, []
        for ch in text:
            out.append((ch, x))
            x += s.hmtx[s.cmap[ord(ch)]][0] / s.upm * size + TRACK * size
        return out, x - TRACK * size  # width without trailing tracking

    def width(s, text, size):
        return s.positions(text, size)[1]

    def svg_path(s, text, size, x0, baseline):
        d = []
        k = size / s.upm
        for ch, x in s.positions(text, size)[0]:
            if ch == " ":
                continue
            pen = SVGPathPen(s.gs)
            s.gs[s.cmap[ord(ch)]].draw(TransformPen(pen, (k, 0, 0, -k, x0 + x, baseline)))
            d.append(pen.getCommands())
        return " ".join(d)

    def pil(s, d, text, size, x0, baseline, fill, scale):
        font = ImageFont.truetype(s.path, round(size * scale))
        for ch, x in s.positions(text, size)[0]:
            d.text(((x0 + x) * scale, baseline * scale), ch, font=font, fill=fill, anchor="ls")


BOLD, MED = Face(F_BOLD), Face(F_MED)


def svg_rects(g, ox, oy, mono=False):
    out = []
    for y, row in enumerate(g.px):
        x = 0
        while x < g.n:
            c = row[x]
            if c is None or (mono and c not in MONO_KEEP):
                x += 1; continue
            x2 = x
            while x2 + 1 < g.n and row[x2 + 1] == c:
                x2 += 1
            fill = "#FFFFFF" if mono else PAL[c]
            out.append(f'<rect x="{ox+x}" y="{oy+y}" width="{x2-x+1}" height="1" fill="{fill}"/>')
            x = x2 + 1
    return "\n".join(out)


def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


# ---------------- lockups ----------------
# Layouts are in mark-grid units (1 unit = 1 pixel of the 32px mark); output scales are integers so pixels stay crisp.
def horizontal_layout():
    size = 18                                  # wordmark size; cap height ~12.6 units
    tw = BOLD.width(WORD, size)
    W, H, gap = 200, 50, 8
    padx = (W - (32 + gap + tw)) / 2
    assert padx >= CLEAR
    mx, my = round(padx), CLEAR
    base = my + 16 + BOLD.cap * size / 2
    return dict(W=W, H=H, mark=(mx, my), text=[(BOLD, WORD, size, mx + 32 + gap, base)])


def stacked_layout():
    size = 12
    tw = BOLD.width(WORD, size)
    W = 112
    assert (W - tw) / 2 >= CLEAR
    my = CLEAR
    base = my + 32 + 8 + BOLD.cap * size
    H = round(base + CLEAR)
    return dict(W=W, H=H, mark=((W - 32) // 2, my), text=[(BOLD, WORD, size, (W - tw) / 2, base)])


def lockup_svg(L, path, bg=None, mono=False, title="Clatty Works"):
    ink = "#FFFFFF" if mono else PAL["K"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L["W"]} {L["H"]}" width="{L["W"]*4}" height="{L["H"]*4}">',
             f"<title>{title}</title>"]
    if bg:
        parts.append(f'<rect width="{L["W"]}" height="{L["H"]}" fill="{bg}"/>')
    parts.append(f'<g shape-rendering="crispEdges">\n{svg_rects(A, *L["mark"], mono=mono)}\n</g>')
    for face, text, size, x, base in L["text"]:
        parts.append(f'<path fill="{ink}" d="{face.svg_path(text, size, x, base)}"/>')
    parts.append("</svg>\n")
    open(path, "w").write("\n".join(parts))


def lockup_png(L, path, scale, bg=None, mono=False):
    im = Image.new("RGBA", (L["W"] * scale, L["H"] * scale), bg or (0, 0, 0, 0))
    m = A.image(scale, mono=mono)
    im.alpha_composite(m, (L["mark"][0] * scale, L["mark"][1] * scale))
    d = ImageDraw.Draw(im)
    ink = (255, 255, 255) if mono else hexrgb(PAL["K"])
    for face, text, size, x, base in L["text"]:
        face.pil(d, text, size, x, base, ink, scale)
    (im.convert("RGB") if bg else im).save(path)


# ---------------- README header banner 1280x320 ----------------
def header(path):
    s = 4                                    # 320 x 80 units
    W, H = 320, 80
    im = Image.new("RGB", (W * s, H * s), PAL["G"])
    d = ImageDraw.Draw(im)
    R = lambda x, y, w, h, c: d.rectangle([x * s, y * s, (x + w) * s - 1, (y + h) * s - 1], fill=PAL[c])
    # the banner is itself a bevelled pane: charcoal outline, solid Deep Teal title strip, 1px bevels
    R(0, 0, W, H, "K"); R(1, 1, W - 2, H - 2, "G")
    R(1, 1, W - 2, 3, "D")
    for k in range(2):                       # plain square dots, not OS controls
        R(W - 4 - 2 * k, 2, 1, 1, "G")
    R(1, 4, W - 2, 1, "L"); R(1, 4, 1, H - 5, "L")
    R(1, H - 2, W - 2, 1, "S"); R(W - 2, 5, 1, H - 6, "S")
    # content group: mark + wordmark + tagline + completed wizard progress bar
    size, tsize, gap = 18, 8, 8
    tw = BOLD.width(WORD, size)
    gx = round((W - (32 + gap + tw)) / 2)
    my = 4 + (H - 4 - 32) // 2               # centre in the area under the title strip
    im.paste(A.image(s), (gx * s, my * s), A.image(s))
    tx = gx + 32 + gap
    base = my + 1 + BOLD.cap * size
    BOLD.pil(d, WORD, size, tx, base, hexrgb(PAL["K"]), s)
    tbase = base + 5 + MED.cap * tsize
    MED.pil(d, TAGLINE, tsize, tx, tbase, hexrgb(PAL["D"]), s)
    # segmented progress bar, all segments filled = setup complete
    by, bh = my + 32 - 5, 5
    segs, sg = 8, 1
    bw = int(tw)
    segw = (bw - 2 - (segs - 1) * sg) // segs
    bw = segs * segw + (segs - 1) * sg + 2
    R(tx, by, bw, bh, "K")
    for i in range(segs):
        R(tx + 1 + i * (segw + sg), by + 1, segw, bh - 2, "T")
    im.save(path)


# ---------------- favicon and avatar (concept C) ----------------
def favicons():
    f16, f32, f48 = C16.image(1), C.image(1), C16.image(3)   # 48 = 16px art at 3x (32 art cannot scale 1.5x crisply)
    f16.save(os.path.join(OUT, "favicon-16.png"))
    f32.save(os.path.join(OUT, "favicon-32.png"))
    f48.save(os.path.join(OUT, "favicon-48.png"))
    f48.save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=[f16, f32])
    C.svg(os.path.join(OUT, "favicon.svg"), title="Clatty Works")
    C16.svg(os.path.join(OUT, "favicon-16.svg"), title="Clatty Works")


def avatar(path, bg):
    scale = 10                               # 320px mark in 512 canvas: corners stay inside a circular crop
    im = Image.new("RGBA", (512, 512), bg)
    m = C.image(scale)
    im.alpha_composite(m, ((512 - m.width) // 2, (512 - m.height) // 2))
    im.convert("RGB").save(path)


def main():
    o = lambda n: os.path.join(OUT, n)
    # primary mark (A)
    A.svg(o("clatty-works-mark.svg"), title="Clatty Works")
    A.svg(o("clatty-works-mark-white.svg"), mono=True, title="Clatty Works")
    for px in (64, 128, 256, 512):
        A.image(px // 32).save(o(f"clatty-works-mark-{px}.png"))
    # horizontal lockup
    H = horizontal_layout()
    lockup_svg(H, o("clatty-works-lockup-horizontal.svg"))
    lockup_svg(H, o("clatty-works-lockup-horizontal-on-white.svg"), bg="#FFFFFF")
    lockup_svg(H, o("clatty-works-lockup-horizontal-on-deep-teal.svg"), bg=PAL["D"], mono=True)
    for sc in (4, 8):
        w = H["W"] * sc
        lockup_png(H, o(f"clatty-works-lockup-horizontal-{w}.png"), sc)
        lockup_png(H, o(f"clatty-works-lockup-horizontal-on-white-{w}.png"), sc, bg="#FFFFFF")
        lockup_png(H, o(f"clatty-works-lockup-horizontal-on-deep-teal-{w}.png"), sc, bg=PAL["D"], mono=True)
    # stacked lockup
    S = stacked_layout()
    lockup_svg(S, o("clatty-works-lockup-stacked.svg"))
    lockup_png(S, o(f"clatty-works-lockup-stacked-{S['W']*8}.png"), 8)
    lockup_png(S, o(f"clatty-works-lockup-stacked-on-white-{S['W']*8}.png"), 8, bg="#FFFFFF")
    # README header, favicon, avatars
    header(o("clatty-works-header.png"))
    favicons()
    avatar(o("clatty-works-avatar-deep-teal-512.png"), PAL["D"])
    avatar(o("clatty-works-avatar-panel-grey-512.png"), PAL["G"])


if __name__ == "__main__":
    main()
