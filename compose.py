#!/usr/bin/env python3
"""Compose the final entry image for news-image-20261118.

Takes the chosen editorial illustration (candidate A: Trump, Xi and Putin
shaking hands under an APEC banner, US/China/Russia flags, Shenzhen
skyline, faint drones and smoke on the horizon) and adds a newspaper
footer band with crisp, program-drawn text — the date the image sums up
(the judge's first criterion is that the image names its day) and the
day's other big stories as short headlines (its second criterion is
breadth across regions and fields).

All text is drawn here with PIL, never by the image generator, so no
lettering can come out garbled. Output: entry.png, 1024x1024.
"""

from PIL import Image, ImageDraw, ImageFont

SRC = (
    "/home/hatch/workspace/makefun/news-image-candidates/"
    "media-generation-news-hero-a-0-81c6f2ea-f316-475c-8f90-82ef175d250b.png"
)
OUT = "/home/hatch/workspace/makefun/news-image-repo/entry.png"

W = 1024
NAVY = (13, 34, 64)
GOLD = (242, 177, 52)
WHITE = (245, 247, 250)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fit_font(draw, text, max_width, start_size):
    """Largest bold size (<= start_size) whose text fits max_width."""
    size = start_size
    while size > 10:
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(FONT, size)


def centered(draw, y, text, font, fill):
    x = (W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=fill)


def main():
    hero_src = Image.open(SRC).convert("RGB")
    # Crop the illustration: keep the APEC banner, flags, faces and the
    # handshake; drop only empty sky at the top and ground at the bottom.
    crop = hero_src.crop((0, 40, 1600, 1350))
    hero_h = round(crop.height * W / crop.width)  # 838
    hero = crop.resize((W, hero_h), Image.LANCZOS)

    band_h = W - hero_h  # 186 px footer band
    canvas = Image.new("RGB", (W, W), NAVY)
    canvas.paste(hero, (0, 0))
    draw = ImageDraw.Draw(canvas)

    y = hero_h + 10
    date_line = "WEDNESDAY 18 NOVEMBER 2026"
    font = fit_font(draw, date_line, W - 40, 46)
    centered(draw, y, date_line, font, GOLD)
    y += 58

    caption = "SHENZHEN: TRUMP, XI & PUTIN MEET AT APEC"
    font = fit_font(draw, caption, W - 40, 30)
    centered(draw, y, caption, font, WHITE)
    y += 42

    headlines = [
        "IRAN DRONES HIT GULF BASES - U.S. STRIKES BACK",
        "141 DRONES OVER UKRAINE - GAZA TRUCE WARNING - SENATE FLIPS",
    ]
    for line in headlines:
        font = fit_font(draw, line, W - 40, 26)
        centered(draw, y, line, font, WHITE)
        y += 34

    assert y <= W, f"text overflow: y={y}"
    canvas.save(OUT, optimize=True)
    print(f"wrote {OUT}: {canvas.size}, band {band_h}px")


if __name__ == "__main__":
    main()
