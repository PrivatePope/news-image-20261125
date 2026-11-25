#!/usr/bin/env python3
"""Draw entry.png for news-image-20261125: a newspaper front page summing up
Wednesday 25 November 2026's world news. Flat vector-style art, PIL only.
Run: python3 build_image.py  ->  writes entry.png (1024x1024) in this dir."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 22, 22)
RED = (168, 32, 24)
NAVY = (22, 50, 79)
GOLD = (184, 138, 44)
GREY = (90, 86, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, fill=INK, width=3):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28  # margin
R = W - M

# ---- outer frame ----
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

# ---- masthead ----
y = 26
f_mast = font(SERIF_B, 58)
title = "THE WORLD IN ONE DAY"
tw = d.textlength(title, font=f_mast)
d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
y += 72
hrule(d, M, R, y, fill=RED, width=5)
y += 10
f_date = font(SANS_B, 32)
date = "WEDNESDAY  ·  25 NOVEMBER 2026"
tw = d.textlength(date, font=f_date)
d.text(((W - tw) / 2, y), date, font=f_date, fill=RED)
y += 42
f_sub = font(SERIF, 20)
sub = "The day's world news in one image"
tw = d.textlength(sub, font=f_sub)
d.text(((W - tw) / 2, y), sub, font=f_sub, fill=GREY)
y += 28
hrule(d, M, R, y, fill=INK, width=3)
y += 12

# ---- LEAD: Pacific treaty ----
lead_top = y
lead_h = 352
f_kick = font(SANS_B, 20)
d.text((M, lead_top), "PACIFIC  ·  LEAD STORY", font=f_kick, fill=RED)
# illustration box (left)
ill_x, ill_y = M, lead_top + 32
ill_w, ill_h = 380, lead_h - 32
d.rectangle([ill_x, ill_y, ill_x + ill_w, ill_y + ill_h], fill=(214, 232, 240),
            outline=NAVY, width=3)
# sky + sea
d.rectangle([ill_x + 3, ill_y + 3, ill_x + ill_w - 3, ill_y + 140], fill=(178, 214, 232))
d.rectangle([ill_x + 3, ill_y + 140, ill_x + ill_w - 3, ill_y + ill_h - 3], fill=(58, 128, 168))
# sun between the flags
d.ellipse([ill_x + 168, ill_y + 18, ill_x + 214, ill_y + 64], fill=(240, 196, 66))
# waves
for wy, off in ((ill_y + 178, 0), (ill_y + 226, 36), (ill_y + 274, 0)):
    for k in range(5):
        x0 = ill_x + 8 + k * 76 + off
        d.arc([x0, wy, x0 + 56, wy + 32], 180, 360, fill=(255, 255, 255), width=5)
# two flagpoles with flags
pole_y0, pole_y1 = ill_y + 44, ill_y + 108
# Australia flag (left): blue field, simplified stars
fx, fy, fw, fh = ill_x + 24, ill_y + 44, 112, 62
d.line([(fx + 6, pole_y0), (fx + 6, pole_y1)], fill=INK, width=5)
d.rectangle([fx, fy, fx + fw, fy + fh], fill=(18, 52, 110), outline=INK, width=2)
d.polygon([(fx, fy), (fx + 48, fy), (fx + 48, fy + 28), (fx, fy + 28)], fill=(200, 30, 30))
d.line([(fx, fy), (fx + 48, fy + 28)], fill=(255, 255, 255), width=3)
d.line([(fx + 48, fy), (fx, fy + 28)], fill=(255, 255, 255), width=3)
for sx, sy in ((fx + 78, fy + 15), (fx + 94, fy + 42), (fx + 62, fy + 45)):
    d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 255, 255))
d.text((fx - 2, fy + fh + 8), "AUSTRALIA", font=font(SANS_B, 16), fill=INK)
# Solomon Islands flag (right): blue over green, yellow diagonal, white stars
fx2 = ill_x + 244
d.line([(fx2 + 6, pole_y0), (fx2 + 6, pole_y1)], fill=INK, width=5)
d.rectangle([fx2, fy, fx2 + fw, fy + fh], fill=(20, 90, 160), outline=INK, width=2)
d.polygon([(fx2, fy + fh), (fx2 + fw, fy), (fx2 + fw, fy + fh)], fill=(30, 130, 70))
d.polygon([(fx2, fy + fh), (fx2 + fw, fy + 8), (fx2 + fw, fy + 21), (fx2, fy + fh - 13)],
          fill=(240, 200, 40))
for sx, sy in ((fx2 + 20, fy + 15), (fx2 + 40, fy + 11), (fx2 + 31, fy + 28),
               (fx2 + 54, fy + 20), (fx2 + 44, fy + 37)):
    d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 255, 255))
d.text((fx2 + 2, fy + fh + 8), "SOLOMONS", font=font(SANS_B, 16), fill=INK)
# treaty document between the flags, foreground
dx, dy = ill_x + 118, ill_y + 168
d.rectangle([dx, dy, dx + 144, dy + 104], fill=(255, 255, 255), outline=INK, width=3)
d.line([(dx + 14, dy + 20), (dx + 130, dy + 20)], fill=INK, width=3)
for j, yy in enumerate((42, 58, 74)):
    d.line([(dx + 14, dy + yy), (dx + 130 - j * 18, dy + yy)], fill=GREY, width=3)
d.ellipse([dx + 100, dy + 80, dx + 126, dy + 106], fill=RED, outline=(120, 20, 12), width=2)
d.text((dx + 14, dy + 84), "SIGNED", font=font(SANS_B, 15), fill=RED)
# headline block (right of illustration)
tx = M + ill_w + 26
tw_ = R - tx
f_head = font(SERIF_B, 48)
hl = ["SOLOMONS", "CHOOSE", "AUSTRALIA"]
yy = lead_top + 28
for ln in hl:
    d.text((tx, yy), ln, font=f_head, fill=INK)
    yy += 54
yy += 4
hrule(d, tx, R, yy, fill=RED, width=4)
yy += 12
f_body = font(SERIF, 24)
body = ("A historic treaty makes Canberra the islands' security "
        "partner of choice — and ends the China pact.")
lines = wrap(d, body, f_body, tw_)
yy = text_block(d, tx, yy, lines, f_body, INK, leading=30)
yy += 8
f_fact = font(SANS_B, 20)
d.text((tx, yy), "Signed in Canberra  ·  $740m  ·  No foreign bases",
       font=f_fact, fill=NAVY)

# ---- divider ----
y = lead_top + lead_h + 4
hrule(d, M, R, y, fill=INK, width=3)
y += 12

# ---- three columns ----
col_w = (R - M - 2 * 24) // 3
col_tops = y
col_h = 258
cols = [
    ("NORTH KOREA", "SWISS ENVOY EXPELLED",
     "North Korea orders Switzerland's man out in 48 hours over camp sanctions."),
    ("MARKETS", "AI STOCKS SLIDE IN ASIA",
     "Tech shares tumble as faith in the AI boom wobbles after Wall Street falls."),
    ("MYANMAR", "NATIONS BACK GENOCIDE RULING",
     "Britain sanctions Myanmar generals after the UN court's Rohingya verdict."),
]
for i, (kick, head, body) in enumerate(cols):
    cx = M + i * (col_w + 24)
    d.text((cx, col_tops), kick, font=f_kick, fill=RED)
    # illustration strip
    iy = col_tops + 28
    ih = 72
    d.rectangle([cx, iy, cx + col_w, iy + ih], outline=NAVY, width=2)
    if i == 0:
        # DPRK flag simplified + 48 HOURS stamp
        d.rectangle([cx + 2, iy + 2, cx + col_w - 2, iy + ih - 2], fill=(210, 40, 30))
        d.rectangle([cx + 2, iy + 28, cx + col_w - 2, iy + 42], fill=(255, 255, 255))
        d.rectangle([cx + 2, iy + 42, cx + col_w - 2, iy + 50], fill=(30, 60, 140))
        d.ellipse([cx + col_w // 2 - 15, iy + 20, cx + col_w // 2 + 15, iy + 52],
                  fill=(255, 255, 255), outline=(210, 40, 30), width=3)
        d.polygon([(cx + col_w // 2, iy + 26), (cx + col_w // 2 + 5, iy + 37),
                   (cx + col_w // 2 + 10, iy + 37), (cx + col_w // 2 + 6, iy + 43),
                   (cx + col_w // 2 + 7, iy + 49), (cx + col_w // 2, iy + 45),
                   (cx + col_w // 2 - 7, iy + 49), (cx + col_w // 2 - 6, iy + 43),
                   (cx + col_w // 2 - 10, iy + 37), (cx + col_w // 2 - 5, iy + 37)],
                  fill=(210, 40, 30))
        d.text((cx + col_w - 112, iy + 52), "48 HOURS", font=font(SANS_B, 15),
               fill=(255, 255, 255))
    elif i == 1:
        # falling chart
        d.rectangle([cx + 2, iy + 2, cx + col_w - 2, iy + ih - 2], fill=(255, 255, 255))
        for gy in range(iy + 14, iy + ih - 6, 15):
            d.line([(cx + 8, gy), (cx + col_w - 8, gy)], fill=(220, 220, 220), width=1)
        pts = [(cx + 14, iy + 14), (cx + 70, iy + 24), (cx + 126, iy + 20),
               (cx + 182, iy + 40), (cx + 238, iy + 36), (cx + col_w - 14, iy + 60)]
        d.line(pts, fill=RED, width=5, joint="curve")
        d.polygon([(cx + col_w - 30, iy + 46), (cx + col_w - 14, iy + 60),
                   (cx + col_w - 30, iy + 64)], fill=RED)
        d.text((cx + 12, iy + 48), "▼ AI SHARES", font=font(SANS_B, 16), fill=RED)
    else:
        # scales of justice
        d.rectangle([cx + 2, iy + 2, cx + col_w - 2, iy + ih - 2], fill=(238, 232, 214))
        mx = cx + col_w // 2
        d.line([(mx, iy + 10), (mx, iy + 60)], fill=GOLD, width=5)
        d.line([(cx + 34, iy + 19), (cx + col_w - 34, iy + 19)], fill=GOLD, width=5)
        d.ellipse([mx - 6, iy + 5, mx + 6, iy + 17], fill=GOLD)
        for sx in (cx + 34, cx + col_w - 34):
            d.line([(sx, iy + 19), (sx - 21, iy + 52)], fill=GOLD, width=3)
            d.line([(sx, iy + 19), (sx + 21, iy + 52)], fill=GOLD, width=3)
            d.arc([sx - 21, iy + 40, sx + 21, iy + 68], 0, 180, fill=GOLD, width=4)
        d.rectangle([mx - 26, iy + 60, mx + 26, iy + 68], fill=GOLD)
    # headline + body
    f_ch = font(SERIF_B, 25)
    hy = iy + ih + 10
    hlines = wrap(d, head, f_ch, col_w)
    hy = text_block(d, cx, hy, hlines, f_ch, INK, leading=29)
    hy += 4
    f_cb = font(SERIF, 19)
    blines = wrap(d, body, f_cb, col_w)
    text_block(d, cx, hy, blines, f_cb, INK, leading=24)
    if i < 2:
        d.line([(cx + col_w + 12, col_tops), (cx + col_w + 12, col_tops + col_h)],
               fill=GREY, width=2)

# ---- bottom strip: ALSO TODAY ----
y = col_tops + col_h + 10
hrule(d, M, R, y, fill=INK, width=3)
y += 10
f_strip_k = font(SANS_B, 20)
d.text((M, y), "ALSO TODAY", font=f_strip_k, fill=RED)
y += 30
# item 1: cricket
sx1 = M
d.ellipse([sx1, y + 4, sx1 + 44, y + 48], fill=(200, 60, 40), outline=INK, width=2)
d.arc([sx1 + 8, y + 12, sx1 + 36, y + 40], 200, 340, fill=(255, 255, 255), width=3)
f_s = font(SERIF, 20)
f_sb = font(SANS_B, 20)
d.text((sx1 + 56, y), "CRICKET", font=f_sb, fill=NAVY)
s1 = "Vaibhav Suryavanshi, 15, hits a world-record 204* off 53 balls."
lines = wrap(d, s1, f_s, 430)
text_block(d, sx1 + 56, y + 24, lines, f_s, INK, leading=23)
# item 2: Nepal quake
sx2 = M + 520
d.polygon([(sx2, y + 48), (sx2 + 22, y + 4), (sx2 + 44, y + 48)], fill=(120, 120, 120),
          outline=INK, width=2)
d.polygon([(sx2 + 14, y + 20), (sx2 + 22, y + 4), (sx2 + 30, y + 20)], fill=(255, 255, 255))
d.text((sx2 + 56, y), "NEPAL", font=f_sb, fill=NAVY)
s2 = "5.3-magnitude quake shakes the Himalayas; tremors felt in Sikkim."
lines = wrap(d, s2, f_s, 390)
text_block(d, sx2 + 56, y + 24, lines, f_s, INK, leading=23)
y += 78
hrule(d, M, R, y, fill=INK, width=3)
y += 8
f_foot = font(SANS, 18)
foot = "Wednesday 25 November 2026  ·  The World in One Day"
tw = d.textlength(foot, font=f_foot)
d.text(((W - tw) / 2, y), foot, font=f_foot, fill=GREY)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)
