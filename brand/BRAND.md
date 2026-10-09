# Clatty Works Brand Guide

**Direction:** Setup Wizard. Clean, credible, 90s-desktop retro.
**Status:** v1.0, approved 9 Oct 2026.

Clatty Works takes apps from Android to Windows 11 and back again. The brand borrows the feel of a good 90s software installer: grey bevelled panels, teal accents, small pixel icons, and calm, step-by-step language. It is our own design. We never copy anyone else's trade dress.

---

## 1. Who we're talking to

1. **Everyday Windows and Android users** who want an app on the other platform. They need to know what it does, whether it's safe, and how to install it.
2. **Developers and tinkerers** who care how we ported it. They want architecture notes, build steps, and honest limitations.
3. **Portfolio visitors.** They should see a tidy, legit studio with a consistent body of work.

Gamers and modders are **not** a target audience. Don't write for them specifically.

---

## 2. Colour palette

| Role | Name | Hex | Use |
|---|---|---|---|
| Primary | Wizard Teal | `#0F8A8A` | Buttons, headings at 24px or larger, icon fills, accents |
| Primary dark | Deep Teal | `#0A5C5C` | Links and teal text at any size, button hover state, footer |
| Surface | Panel Grey | `#D5D9DC` | Panels, cards, bevelled frames, table headers |
| Background | Paper White | `#FFFFFF` | Page and document background |
| Text | Charcoal | `#2A2E31` | Body text, logo wordmark, icon outlines |
| Highlight | Signal Amber | `#E39B2D` | Sparingly: "new", progress, one callout per screen |

**Bevel shades**, for the raised-panel effect only: light edge `#F2F4F5`, dark edge `#8E959A`.

**Contrast rules** (measured to WCAG 2.x):
- Charcoal on white (13.7:1) and charcoal on Panel Grey (9.6:1) pass for all text.
- Deep Teal on white (7.8:1) and on Panel Grey (5.5:1) passes for all text, so use it for links and small teal text.
- Wizard Teal on white (4.2:1) is for **large text (24px or larger, or 18.66px bold) and UI elements only**, never body text.
- White text on Wizard Teal (4.2:1) is OK for buttons with bold labels of 14px or larger. For anything smaller, use white on Deep Teal (7.8:1).
- Never put Wizard Teal text on Panel Grey (2.9:1).
- Amber goes **behind or beside** charcoal text (5.9:1), never as text on white.

**Don'ts:** no gradients on title bars, no navy-to-blue title-bar gradient, no Android green (`#3DDC84` or close), and no four-colour flag motifs.

---

## 3. Typography

| Use | Font | Weights |
|---|---|---|
| Headings and body | **IBM Plex Sans** | 400, 500, 600 (700 for the wordmark) |
| Code, versions, file names, wordmark | **IBM Plex Mono** | 400, 500, 700 |
| Pixel accents | Hand-drawn pixel icons only, not a pixel font | n/a |

- Headings use sentence case, for example "How we ported it" rather than "How We Ported It".
- Version numbers and build IDs are always in Plex Mono: `v1.2.0`, `build 0412`.
- Body text is 16px or larger on the web, with a line height of about 1.5.
- System fallbacks are `"IBM Plex Sans", system-ui, sans-serif` and `"IBM Plex Mono", ui-monospace, monospace`.

---

## 4. Logo

> **Status: final.** Approved on 9 Oct 2026. **Concept A (Classic)** is the primary mark and the basis for every lockup. **Concept C (Monogram)** is the favicon and avatar. All files live in `/brand/logo/`.

### Concept
The **mark** is two small bevelled window panes side by side. The left pane is tall and narrow, a **phone screen**. The right pane is wide, a **desktop window**. A chunky pixel arrow goes from one to the other, which says "we move apps between platforms".
The **wordmark** is `CLATTY WORKS` in IBM Plex Mono Bold, all caps, with slightly wider letter-spacing (+40).

**Primary mark (A, Classic):** phone on the left, arrow pointing right, desktop on the right.
**Favicon and avatar mark (C, Monogram):** the same parts arranged as a pixel "C". The desktop pane is the top bar, the phone pane is the upright stroke, and the arrow is the bottom bar. It stays readable at 16px and in circular crops.

### Construction
- Draw on a pixel grid: 32×32 for the icon master and 16×16 for the favicon. Edges are hard, with no anti-aliasing on the pixel elements.
- Panes are Panel Grey with a 1px light top-left bevel and a 1px dark bottom-right bevel, outlined in Charcoal.
- The arrow is Wizard Teal. Each pane's thin title strip is solid Deep Teal, never a gradient.
- No window controls (minimise, maximise or close buttons) that copy any real OS. If needed, use plain square dots.

### Small-size and construction notes
- **Arrow outlines:** the arrows carry a 1px Charcoal outline, because Wizard Teal alone is too faint on Panel Grey.
- **No bevels at 16px:** the 16px favicon drops the light bevel and keeps only the dark bottom edge, because there isn't room.
- **No built-in padding:** the 32px mark A runs edge to edge on its canvas, so clear space always comes from the layout around it. The lockup files and avatars already include their clear space and padding.
- **Scaling:** always scale pixel art by whole numbers with nearest-neighbour (2×, 4×, 8×…). Never use fractional or smooth scaling. The 48px favicon is the 16px art at 3×, because the 32px art can't be scaled by 1.5× cleanly.
- The wordmark in the SVG lockups is converted to outlines, so it doesn't need the font installed. IBM Plex Mono is logged in section 9 under the SIL Open Font License 1.1 (OFL-1.1).
- The source art and the build script are in `/brand/logo/src/` (`draw.py`, `build_logo.py`). Edit the pixel grids there and rebuild; don't hand-edit the exports.

### Lockups
1. **Horizontal**, the default: mark on the left and wordmark on the right, vertically centred.
2. **Stacked**: mark above the wordmark, centred. Use it for square spaces like avatars and social cards.
3. **Mark only**: the app icon uses mark A. The favicon and GitHub org avatar use mark C.

### Files and when to use them

| File | Use it for |
|---|---|
| `clatty-works-mark.svg` | Master mark A (32×32 pixel grid). Use it wherever SVG works and the mark is shown at 32px or larger. |
| `clatty-works-mark-white.svg` | All-white mark A, for Deep Teal or Charcoal backgrounds. |
| `clatty-works-mark-64.png`, `-128.png`, `-256.png`, `-512.png` | Mark A as PNG (transparent background), for app icons, docs and slides. Pick the size closest to how it will be shown. |
| `clatty-works-lockup-horizontal.svg` | Default horizontal lockup, transparent background. Use it for the web and docs. |
| `clatty-works-lockup-horizontal-on-white.svg` | Horizontal lockup on a solid white background. |
| `clatty-works-lockup-horizontal-on-deep-teal.svg` | All-white horizontal lockup on Deep Teal. Use it for footers and dark banners. |
| `clatty-works-lockup-horizontal-800.png`, `-1600.png` | Horizontal lockup PNG on a transparent background (800×200 and 1600×400). |
| `clatty-works-lockup-horizontal-on-white-800.png`, `-1600.png` | Horizontal lockup PNG on white. |
| `clatty-works-lockup-horizontal-on-deep-teal-800.png`, `-1600.png` | All-white horizontal lockup PNG on Deep Teal. |
| `clatty-works-lockup-stacked.svg`, `clatty-works-lockup-stacked-896.png`, `clatty-works-lockup-stacked-on-white-896.png` | Stacked lockup, for square spaces, splash or about screens, and social cards. |
| `clatty-works-header.png` | README header banner (1280×320): lockup A with the tagline "Setup complete." on a bevelled Panel Grey pane. |
| `favicon.ico` | Favicon with 16, 32 and 48px frames (mark C). |
| `favicon.svg`, `favicon-16.svg` | SVG favicon (mark C). `favicon.svg` is the 32px master and `favicon-16.svg` is the simplified 16px art. |
| `favicon-16.png`, `favicon-32.png`, `favicon-48.png` | PNG favicons and small UI icons (mark C). |
| `clatty-works-avatar-deep-teal-512.png` | GitHub org avatar and social profiles. This is the default. Mark C on Deep Teal, padded for circular crops. |
| `clatty-works-avatar-panel-grey-512.png` | The same avatar on Panel Grey, for places where a light avatar fits better. |
| `src/draw.py`, `src/build_logo.py` | Source pixel grids and build script. To rebuild, run `python3 build_logo.py` (needs Pillow and fontTools, and `PLEX_MONO_DIR` pointing at the IBM Plex Mono TTF folder). |

**README headers:** every README header (section 7, item 1) uses `clatty-works-header.png`. For a smaller header, use the horizontal lockup (`clatty-works-lockup-horizontal.svg` or the 800px PNG) instead. Use relative links into `/brand/logo/` and set the alt text to "Clatty Works".

### Clear space and size
- Keep a clear space of at least the height of the arrow on all sides.
- The horizontal lockup is at least 120px wide on screen. The mark alone is at least 16px.

### Colour versions
- Full colour on white or Panel Grey.
- All-charcoal, single colour, for printing or watermarks.
- All-white on Deep Teal or Charcoal.

### Don't
- Don't recolour the panes, add gradients or drop shadows, rotate, stretch, or outline the wordmark.
- Don't swap the phone or desktop for any real device, OS logo, or robot.
- Don't add any Microsoft or Google logo, flag, or mascot to the mark.

---

## 5. UI motifs (web, docs, and app chrome)

- **Bevelled panels:** raised cards with the light and dark 1px bevel on Panel Grey, used for feature boxes, download boxes, and callouts.
- **Wizard steps:** walk through processes as "Step 1 of 3" with a simple segmented progress bar. The filled segments are teal and the empty ones are grey.
- **Buttons:** rectangular, 2px corner radius at most, Wizard Teal fill with white bold label, and Deep Teal on hover. Secondary buttons are Panel Grey with a bevel and a charcoal label.
- **Pixel icons:** 16×16 or 32×32, charcoal outline with teal and amber fills, drawn by us. Never ripped from an OS icon set.
- **Spacing:** an 8px grid.

---

## 6. Tone of voice

**Clear, calm, step-by-step, like a good installer.** We are confident, never hypey.

- Write in plain English, short sentences, and active voice. Say "we", not "the team".
- Lead with what the user gets, then the how.
- Be honest about limits: "Known issues" is a standard section, not something to hide.
- A little retro warmth is fine in small doses ("Setup complete. Enjoy."), but no memes and no gamer slang.
- Avoid "revolutionary", "blazing fast", "seamless", "hack" (in the cracking sense), and "crack".

| Instead of | Write |
|---|---|
| "Blazing-fast native port!!!" | "Runs natively on Windows 11, with no emulator." |
| "We hacked the APK" | "We studied how the Android app works and rebuilt it in Rust." |
| "Just run it lol" | "Step 1 of 2: Download the installer." |

**Tagline:** "Setup complete." (picked by Jay, 9 Oct 2026). Use it under the wordmark, in the README footer, and on splash or about screens. Keep the full stop.

---

## 7. README, docs and repo presentation

### Repo naming
- Repos: `kebab-case`, named after what the project is, e.g. `notes-app-windows-port`. Don't use a third party's trademark as the leading word of a repo name; prefer descriptive names (e.g. `<app>-port` only if we own or may use the name).
- Every repo description is one sentence, ending without a full stop.

### Every README follows this order
1. **Header:** `/brand/logo/clatty-works-header.png` (or the horizontal lockup), the project name, and a one-line summary.
2. **Status line**, in Plex Mono style using code formatting: `v0.3.0 · Windows 11 · Rust · Beta`.
3. **What it is:** 2 or 3 sentences for everyday users.
4. **Install:** numbered steps, written as "Step 1 of N".
5. **How we ported it:** for devs, a short summary linking to `/docs/architecture.md`.
6. **Known issues**
7. **Legal and licence:** who owns the original, the basis on which we're allowed to port it, and this repo's licence.
8. **Footer:** "Made by Clatty Works."

### Docs
- `/docs` uses the same headings style, sentence case.
- Diagrams use the palette above. Mermaid is fine in Markdown.
- Screenshots go in `/docs/img/`, as PNG, with a descriptive alt text.

### Badges
- At most 4 badges: build, version, platform, licence. Use flat style with teal (`0F8A8A`) or charcoal (`2A2E31`) colours.

---

## 8. Placeholder and third-party asset rules for ports

1. **Never ship someone else's logo, icon, name or artwork as if it were ours.** Original app branding may only be used if we own it or have written permission. Record that permission in the repo under `Legal and licence`.
2. Until we have rights or our own art, use **Clatty Works placeholders**:
   - App icon: the Clatty Works mark on a Panel Grey bevelled square, with the project's initials in Plex Mono Bold over the top.
   - Splash and about screens: wordmark plus "Ported by Clatty Works".
   - Name every placeholder file with a `placeholder-` prefix so they're easy to find and replace.
3. **No OS trade dress in ported UIs:** no copied Windows or Android system icons, Windows logo or flag, Android robot, Segoe- or Roboto-only branded layouts that imitate official apps.
4. Fonts and icon sets added to a port must be open-licensed and logged in that repo's `/brand/LICENSES.md` (same format as section 9).
5. When in doubt, settle any brand or legal question before shipping.

---

## 9. Font and asset licence log

| Asset | Source | Licence | Notes |
|---|---|---|---|
| IBM Plex Sans | [github.com/IBM/plex](https://github.com/IBM/plex) | SIL Open Font License 1.1 | Free to use, embed, and bundle; we may not sell the font by itself |
| IBM Plex Mono | [github.com/IBM/plex](https://github.com/IBM/plex) | SIL Open Font License 1.1 | Same as above |
| Clatty Works mark and pixel icons | Drawn in-house (logo final 9 Oct 2026) | Clatty Works, all rights reserved | Logo files are in `/brand/logo/`; icons are in `/brand/icons/` |

When you add a font or asset, add a row with its source URL and licence, and keep a copy of the licence text in `/brand/licenses/`.

---

## 10. Suggested `/brand` folder layout

```
/brand
  BRAND.md          ← this guide
  palette.css       ← CSS variables below
  logo/             ← final logo files (see section 4, "Files and when to use them")
    clatty-works-mark.svg, clatty-works-mark-white.svg
    clatty-works-mark-{64,128,256,512}.png
    clatty-works-lockup-horizontal{,-on-white,-on-deep-teal}.svg
    clatty-works-lockup-horizontal{,-on-white,-on-deep-teal}-{800,1600}.png
    clatty-works-lockup-stacked.svg, clatty-works-lockup-stacked{,-on-white}-896.png
    clatty-works-header.png         ← README header banner (1280×320)
    favicon.ico, favicon.svg, favicon-16.svg, favicon-{16,32,48}.png
    clatty-works-avatar-{deep-teal,panel-grey}-512.png
    src/draw.py, src/build_logo.py  ← pixel grids + build script
  icons/            ← pixel icons
  licenses/         ← OFL.txt for IBM Plex, and others as added
```

### `palette.css`
```css
:root {
  --cw-teal: #0F8A8A;
  --cw-teal-dark: #0A5C5C;
  --cw-panel: #D5D9DC;
  --cw-paper: #FFFFFF;
  --cw-charcoal: #2A2E31;
  --cw-amber: #E39B2D;
  --cw-bevel-light: #F2F4F5;
  --cw-bevel-dark: #8E959A;
  --cw-font-sans: "IBM Plex Sans", system-ui, sans-serif;
  --cw-font-mono: "IBM Plex Mono", ui-monospace, monospace;
}
```
