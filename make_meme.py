#!/usr/bin/env python3
"""Build the GTA 6 meme v2: a doctor's prescription (Rx pad) from Leonida Clinic.

Screening (2026-11-20, top 12 + top-50 cutoff zone):
- Winners are all "official document" memes: Steam receipt (#1), library
  overdue notice (#2), hurricane warning (#3), parking citation (#4),
  lock screen (#5, #9), boarding pass (#6, #7), bank statement (#8),
  store receipt (#10), certificate (#11), DMV vision test (#12).
- v1 (WANTED poster) scored 8W/4L, rank 222 — outside top 50. The
  top-50 cutoff sits at ~10-11W/0-2L, so v2 must be a clearly better
  document, not a tweak of v1.
- NO medical document appears anywhere in the top 12, and the Rx pad
  gives a fresh joke angle: the 13-year wait as a treatable condition
  (dosage gags), instead of repeating the same receipt/invoice lines
  the judge has already seen a dozen times. The payout is itemised
  like #1's winning "+$250 credit" box.
- The make.fun ghost (real press-kit mark, assets/mark-1024.png) is
  the clinic's logo (header circle) and appears again in the payout
  box — the issuing institution, never a corner sticker.

Drawn entirely with PIL so every line is crisp at 480x480.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MAGENTA = (196, 28, 131)   # make.fun brand magenta
PINK_BOX = (253, 232, 243)
DARK = (20, 18, 20)
GREY = (110, 108, 115)
RED = (176, 0, 32)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(size, bold=True, serif=False):
    if serif:
        path = FONT_SERIF_BOLD if bold else FONT_SERIF
    else:
        path = FONT_BOLD if bold else FONT_BOOK
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def center(draw, y, s, f, fill=DARK):
    draw.text(((W - text_w(draw, s, f)) / 2, y), s, font=f, fill=fill)


def left(draw, x, y, s, f, fill=DARK):
    draw.text((x, y), s, font=f, fill=fill)


# --- background: deep purple -> magenta gradient (like the winners) ---
top = (43, 10, 74)
bottom = (196, 28, 131)
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    px_row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = px_row

d = ImageDraw.Draw(img)

# --- the prescription pad (white, rounded, soft shadow) ---
PAD = (70, 56, 954, 968)
d.rounded_rectangle([PAD[0] + 10, PAD[1] + 14, PAD[2] + 10, PAD[3] + 14],
                    radius=28, fill=(30, 8, 50))
d.rounded_rectangle(PAD, radius=28, fill=(255, 255, 255))
d.rounded_rectangle(PAD, radius=28, outline=(220, 220, 220), width=2)

# --- header: ghost in a pink circle + clinic name ---
ghost = Image.open("assets/mark-1024.png").convert("RGBA")
# header circle
cx, cy, cr = 168, 148, 62
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=MAGENTA)
gh = ghost.resize((88, 88), Image.LANCZOS)
img.paste(gh, (cx - 44, cy - 44), gh)
d = ImageDraw.Draw(img)

left(d, 252, 108, "LEONIDA CLINIC", font(46), fill=DARK)
left(d, 254, 162, "VICE CITY  •  EST. 2013", font(24, bold=False), fill=GREY)

# --- divider ---
d.line([(110, 232), (914, 232)], fill=(200, 200, 200), width=2)

# --- patient / date ---
left(d, 110, 252, "PATIENT:  EVERY GTA FAN", font(30), fill=DARK)
left(d, 110, 292, "DATE:  19 NOV 2026", font(30), fill=DARK)
left(d, 110, 332, "DIAGNOSIS:  CHRONIC WAITING", font(30), fill=RED)

# --- big Rx ---
d.text((110, 392), "Rx", font=font(120, serif=True), fill=MAGENTA)

# --- prescription body ---
left(d, 300, 408, "GTA VI — 1 DOSE", font(44), fill=DARK)
left(d, 300, 468, "Take once every 13 years", font(34, bold=False), fill=DARK)
left(d, 110, 552, "Take with 214 GB of water.", font(34, bold=False), fill=DARK)
left(d, 110, 596, "WARNING: may cause 2 delays,", font(34, bold=False), fill=DARK)
left(d, 110, 640, "9 sleepless nights & 1 lost childhood.", font(34, bold=False), fill=DARK)
left(d, 110, 700, "REFILLS: NONE — 13 YEARS WAS ENOUGH", font(32), fill=MAGENTA)

# --- divider ---
d.line([(110, 752), (914, 752)], fill=(200, 200, 200), width=2)

# --- payout box: the make.fun pitch, itemised like the #1 winner ---
BOX = (110, 776, 914, 896)
d.rounded_rectangle(BOX, radius=16, fill=PINK_BOX, outline=MAGENTA, width=3)
gh2 = ghost.resize((76, 76), Image.LANCZOS)
img.paste(gh2, (132, 806), gh2)
d = ImageDraw.Draw(img)
left(d, 226, 792, "PAID BY MY AI AGENT ON make.fun", font(30), fill=DARK)
left(d, 226, 830, "+$250.00 bounty payout — real money,", font(28, bold=False), fill=DARK)
left(d, 226, 862, "not store credit.", font(28, bold=False), fill=DARK)

# --- footer: signature ---
left(d, 110, 916, "Dr. Ghost, MD", font(26, serif=True, bold=False), fill=GREY)
right_x = 914
sig = "Leonida Clinic — the wait is over."
w = text_w(d, sig, font(26, bold=False))
d.text((right_x - w, 916), sig, font=font(26, bold=False), fill=GREY)

img.save("meme.png")
# also save a 480x480 preview, the size the judge sees
img.resize((480, 480), Image.LANCZOS).save("meme-480.png")
print("saved meme.png", img.size)
