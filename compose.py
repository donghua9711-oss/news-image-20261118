#!/usr/bin/env python3
"""Compose the final entry image for news-image-20261118: a one-page
newspaper, "The World in One Day", summing up Wednesday 18 November 2026.

Layout, top to bottom, on a 1024x1024 cream page:
  * masthead  - the paper's name, the date as the headline, a deck line
  * stat band - six headline numbers from the day, each with a caption
  * lead      - story 1, the APEC summit in Shenzhen, with the entry's
                original cover illustration (assets/hero-apec.png)
  * grid      - stories 2-9, each a thumbnail illustration, a kicker,
                a headline and a two-to-three line summary
  * also      - stories 10-29 as one-line items in two columns
  * date check- a strip stating the date rule the page was built under
  * footer    - the sources the day's stories were verified against

Every letter on the page is drawn here with PIL from the story texts
below; the generated illustrations contain no text at all, so nothing
can come out garbled. The story texts are the single source of truth
for what the page says, and SOURCES.md records how each was verified.

Output: entry.png (PNG, or JPEG bytes if PNG would exceed the
1,048,576-byte gate - the grader tells formats apart by magic bytes).
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W = 1024
MX = 26                      # page margin
CW = W - 2 * MX              # content width = 972

PAPER = (246, 241, 228)
INK = (27, 26, 23)
MUTED = (92, 87, 76)
HAIR = (168, 160, 144)
RED = (158, 27, 27)
NAVY = (22, 50, 74)
GOLD = (168, 127, 20)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
NUMF = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- stories

STATS = [
    ("141", "RUSSIAN DRONES OVER UKRAINE IN ONE NIGHT", (158, 27, 27)),
    ("950,000", "DISPLACED GAZANS ON FLOOD-PRONE GROUND", (22, 50, 74)),
    ("204,070", "PEOPLE IN CYCLONE AKVAN'S EVACUATION ZONE", (15, 118, 110)),
    ("56-44", "DEMOCRATS' PROJECTED NEW SENATE MAJORITY", (91, 74, 138)),
    ("$115.8bn", "NVIDIA'S RECORD QUARTERLY REVENUE", (63, 98, 18)),
    ("1 light-day", "VOYAGER 1'S DISTANCE FROM EARTH - A FIRST", (168, 127, 20)),
]

LEAD = {
    "kicker": "1 · SHENZHEN · SUMMIT",
    "headline": "Trump, Xi and Putin hold first three-way summit",
    "summary": (
        "Xi Jinping met Vladimir Putin in Shenzhen on Wednesday, then "
        "greeted Donald Trump on arrival. The three nuclear powers sit "
        "down together on Thursday, with Ukraine, Iran and trade at "
        "the top of the table. Indonesia's Prabowo is among the "
        "leaders in town."
    ),
    "credit": "Cover: the three leaders in Shenzhen. Original illustration.",
    "image": "hero-apec.png",
    "hero_crop": (60, 400, 1540, 1185),
}

BOXES = [
    {
        "kicker": "2 · GULF · WAR",
        "headline": "Iran fires at US bases in the Gulf",
        "summary": (
            "Iran targeted US installations in Kuwait and Bahrain before "
            "dawn, after US jets struck a missile site on Qeshm Island. "
            "Shipping through Hormuz stayed disrupted."
        ),
        "image": "illo-gulf.png",
    },
    {
        "kicker": "3 · CRIMEA · WAR",
        "headline": "Ukraine hits Kerch Bridge a second night",
        "summary": (
            "Kyiv says a road span collapsed in a second straight night "
            "of strikes. Moscow confirms damage and vows to rebuild; "
            "trains run, cars go by ferry."
        ),
        "image": "illo-kerch.png",
    },
    {
        "kicker": "4 · GAZA · AID",
        "headline": "Truce warning as winter closes in",
        "summary": (
            "The US-backed Board of Peace warns the ceasefire could "
            "collapse. UN agencies say 1.7 million people remain "
            "displaced, many in flooded tents as the cold sets in."
        ),
        "image": "illo-gaza.png",
    },
    {
        "kicker": "5 · INDIA · STORM",
        "headline": "Akvan bears down on the Odisha coast",
        "summary": (
            "The severe cyclone is due ashore on Friday near Puri, with "
            "winds near 110 km/h. Over 47,000 people were already in "
            "shelters; 74 rescue teams are deployed."
        ),
        "image": "illo-akvan.png",
    },
    {
        "kicker": "6 · WASHINGTON · POLITICS",
        "headline": "Peltola's Alaska win flips the Senate",
        "summary": (
            "Democrat Mary Peltola, the first Alaska Native senator, "
            "unseats Republican Dan Sullivan, giving Democrats a "
            "projected 56-44 majority in the new Senate."
        ),
        "image": "illo-capitol.png",
    },
    {
        "kicker": "7 · TECH · MARKETS",
        "headline": "Nvidia's record quarter; no return for Huang",
        "summary": (
            "Revenue doubled to a record $115.8bn as AI demand held. "
            "The board ruled out reinstating founder Jensen Huang as "
            "chief executive."
        ),
        "image": "illo-nvidia.png",
    },
    {
        "kicker": "8 · CONGO · HEALTH",
        "headline": "Ebola cases pass 11,000 in DR Congo",
        "summary": (
            "The outbreak passed 11,000 cases on Wednesday, as response "
            "teams race to contain new hotspots in the east of the "
            "country."
        ),
        "image": "illo-ebola.png",
    },
    {
        "kicker": "9 · SPACE · SCIENCE",
        "headline": "A star eats its companion in Andromeda",
        "summary": (
            "Webb data clinches a first-of-its-kind stellar merger: a "
            "small star spiralled into a swollen supergiant 2.5 million "
            "light-years away. They call it Bao."
        ),
        "image": "illo-andromeda.png",
    },
]

ALSO = [
    "COP31 talks in Antalya enter their final 48 hours, 144 items disputed",
    "Anthropic prices its IPO tonight; demand may lift it above the range",
    "OpenAI launches GPT-6.2 Astra and Sol, with lower API prices",
    "Russia and Ukraine agree to their largest prisoner swap yet",
    "ASEAN sets out the terms for Myanmar's return to the bloc",
    "Israel's Knesset elects Matan Kahana as speaker, 66-52",
    "President Herzog asks Gadi Eisenkot to form Israel's government",
    "Turkish authorities seize control of an opposition broadcaster",
    "Indonesia and China sign $71.8bn of deals, incl. ten smart cities",
    "UK inflation jumps to 3.6% in October, a one-year high",
    "Fed minutes point to more rate rises; dollar at a 19-month high",
    "Dow falls a third day, -1.11%; gold slides 3.5% to $3,729",
    "Canada's Carney meets Trump on the APEC sidelines in Shenzhen",
    "Debris from an intercepted attack damages an Aramco tower, Riyadh",
    "The United States loses its measles-free status after 26 years",
    "Robert Pattinson is named as the new James Bond",
    "NASA: space dust holds clues to ancient ice beyond Neptune",
    "Pakistan cuts petrol by Rs3 a litre, down to Rs325",
    "Ukraine: its drone campaign has cut Russian refining by ~45%",
    "Voyager 1 crosses one light-day from Earth, a human-made first",
]

DATE_CHECK = (
    "DATE CHECK - Every story here happened, or was first reported, on "
    "Wednesday 18 November 2026. Disputed claims are attributed, not "
    "stated as fact."
)

SOURCES_LINE = (
    "Sources: AFP · AP · Reuters · Al Jazeera · UN News · WHO · NASA · "
    "IMD · IANS · Alaska Public Media · The Motley Fool · Investopedia "
    "· Open Chronicle · US Brief"
)

# ---------------------------------------------------------------- helpers


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_w, start, minimum=9):
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def wrap(draw, text, f, max_w):
    """Greedy word wrap by measured width; returns the list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked_width(draw, text, f, tracking):
    return sum(draw.textlength(ch, font=f) for ch in text) + tracking * max(
        0, len(text) - 1
    )


def draw_tracked(draw, x, y, text, f, fill, tracking=2):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def thumb(path, w, h, crop=None):
    """Center-crop (or explicit crop) an image to exactly w x h."""
    im = Image.open(path).convert("RGB")
    if crop is not None:
        im = im.crop(crop)
    target = w / h
    cw, ch = im.size
    if cw / ch > target:  # too wide: trim sides
        nw = int(ch * target)
        x0 = (cw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ch))
    else:  # too tall: trim top/bottom
        nh = int(cw / target)
        y0 = (ch - nh) // 2
        im = im.crop((0, y0, cw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def line_h(f):
    a, d = f.getmetrics()
    return a + d


# ---------------------------------------------------------------- layout


def build():
    canvas = Image.new("RGB", (W, W), PAPER)
    draw = ImageDraw.Draw(canvas)

    # ---- masthead -------------------------------------------------
    draw.rectangle([MX, 14, W - MX, 17], fill=INK)
    draw.line([MX, 21, W - MX, 21], fill=INK, width=1)
    f_small = font(SANS_B, 12)
    draw_tracked(draw, MX, 27, "THE WORLD IN ONE DAY", f_small, INK, 3)
    right = "ONE PAGE · 29 STORIES"
    rw = tracked_width(draw, right, f_small, 3)
    draw_tracked(draw, W - MX - rw, 27, right, f_small, INK, 3)

    title = "Wednesday 18 November 2026"
    f_title = fit_font(draw, title, SERIF_BLACK, CW, 50)
    draw.text(
        ((W - draw.textlength(title, font=f_title)) / 2, 40),
        title, font=f_title, fill=INK,
    )
    deck = ("Three leaders meet in Shenzhen · a span falls in Crimea "
            "· Voyager crosses one light-day")
    f_deck = fit_font(draw, deck, SERIF_IT, CW, 17)
    draw.text(
        ((W - draw.textlength(deck, font=f_deck)) / 2, 109),
        deck, font=f_deck, fill=MUTED,
    )
    draw.line([MX, 130, W - MX, 130], fill=INK, width=1)
    draw.rectangle([MX, 134, W - MX, 137], fill=INK)

    # ---- stat band -------------------------------------------------
    band_y = 142
    col_w = CW // 6
    f_num_max = 33
    for i, (num, label, color) in enumerate(STATS):
        x = MX + i * col_w
        draw.rectangle([x + 4, band_y, x + col_w - 4, band_y + 4], fill=color)
        f_num = fit_font(draw, num, NUMF, col_w - 12, f_num_max, 18)
        nw = draw.textlength(num, font=f_num)
        draw.text((x + (col_w - nw) / 2, band_y + 10), num,
                  font=f_num, fill=INK)
        f_lab = font(SANS_B, 9)
        lab_lines = wrap(draw, label, f_lab, col_w - 10)
        assert len(lab_lines) <= 3, f"stat label too long: {label}"
        ly = band_y + 48
        for ln in lab_lines:
            lw = draw.textlength(ln, font=f_lab)
            draw.text((x + (col_w - lw) / 2, ly), ln, font=f_lab, fill=MUTED)
            ly += 11
        if i:
            draw.line([x, band_y + 10, x, band_y + 76], fill=HAIR, width=1)
    draw.line([MX, band_y + 82, W - MX, band_y + 82], fill=INK, width=1)

    # ---- lead story -------------------------------------------------
    lead_y = band_y + 88
    img_w, img_h = 384, 184
    hero = thumb(os.path.join(ASSETS, LEAD["image"]), img_w, img_h,
                 crop=LEAD["hero_crop"])
    canvas.paste(hero, (MX, lead_y))
    draw.rectangle([MX, lead_y, MX + img_w, lead_y + img_h],
                   outline=INK, width=1)
    tx = MX + img_w + 16
    tw = W - MX - tx
    draw_tracked(draw, tx, lead_y + 2, LEAD["kicker"],
                 font(SANS_B, 13), RED, 2)
    f_head = font(SERIF_BOLD, 33)
    head_lines = wrap(draw, LEAD["headline"], f_head, tw)
    assert len(head_lines) <= 3, "lead headline overflow"
    hy = lead_y + 24
    for ln in head_lines:
        draw.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 38
    draw.line([tx, hy + 2, W - MX, hy + 2], fill=HAIR, width=1)
    f_sum = font(SANS, 14)
    sum_lines = wrap(draw, LEAD["summary"], f_sum, tw)
    sy = hy + 10
    for ln in sum_lines:
        draw.text((tx, sy), ln, font=f_sum, fill=INK)
        sy += 18
    assert sy <= lead_y + img_h, f"lead summary overflow: {sy}"
    f_cred = font(SERIF_IT, 10)
    draw.text((MX, lead_y + img_h + 3), LEAD["credit"],
              font=f_cred, fill=MUTED)

    # ---- story grid -------------------------------------------------
    grid_y = lead_y + img_h + 16
    gap = 12
    box_w = (CW - 3 * gap) // 4
    box_h = 174
    thumb_h = 62
    for idx, box in enumerate(BOXES):
        bx = MX + (idx % 4) * (box_w + gap)
        by = grid_y + (idx // 4) * (box_h + 10)
        draw.line([bx, by - 5, bx + box_w, by - 5], fill=HAIR, width=1)
        im = thumb(os.path.join(ASSETS, box["image"]), box_w, thumb_h)
        canvas.paste(im, (bx, by))
        draw.rectangle([bx, by, bx + box_w, by + thumb_h],
                       outline=HAIR, width=1)
        ky = by + thumb_h + 5
        draw_tracked(draw, bx, ky, box["kicker"], font(SANS_B, 10),
                     NAVY, 1)
        f_bh = font(SERIF_BOLD, 15)
        blines = wrap(draw, box["headline"], f_bh, box_w)
        assert len(blines) <= 2, f"box headline overflow: {box['headline']}"
        hy2 = ky + 15
        for ln in blines:
            draw.text((bx, hy2), ln, font=f_bh, fill=INK)
            hy2 += 17
        f_bs = font(SANS, 11)
        slines = wrap(draw, box["summary"], f_bs, box_w)
        assert len(slines) <= 4, f"box summary overflow: {box['headline']}"
        sy2 = hy2 + 3
        for ln in slines:
            draw.text((bx, sy2), ln, font=f_bs, fill=INK)
            sy2 += 13.5
        assert sy2 <= by + box_h, f"box overflow: {box['headline']} -> {sy2}"

    # ---- also on wednesday -------------------------------------------
    also_y = grid_y + 2 * box_h + 10 + 12
    draw.line([MX, also_y, W - MX, also_y], fill=INK, width=1)
    draw_tracked(draw, MX, also_y + 6, "ALSO ON WEDNESDAY",
                 font(SANS_B, 13), INK, 2)
    items_y = also_y + 28
    col2_w = (CW - 24) // 2
    f_item = font(SANS, 12)
    f_num2 = font(SANS_B, 12)
    row_h = 13.2
    for j, item in enumerate(ALSO):
        col = j // 10
        row = j % 10
        x = MX + col * (col2_w + 24)
        y = items_y + row * row_h
        num = f"{j + 10}."
        draw.text((x, y), num, font=f_num2, fill=RED)
        nw2 = draw.textlength(num + " ", font=f_num2)
        ilines = wrap(draw, item, f_item, col2_w - nw2)
        assert len(ilines) == 1, f"also item wraps: {item} -> {ilines}"
        draw.text((x + nw2, y), ilines[0], font=f_item, fill=INK)

    # ---- date check + sources ----------------------------------------
    dc_y = items_y + 10 * row_h + 6
    draw.rectangle([MX, dc_y, W - MX, dc_y + 26], outline=RED, width=2)
    f_dc = fit_font(draw, DATE_CHECK, SANS_B, CW - 20, 12)
    dw = draw.textlength(DATE_CHECK, font=f_dc)
    draw.text(((W - dw) / 2, dc_y + 6), DATE_CHECK, font=f_dc, fill=RED)

    src_y = dc_y + 31
    draw.line([MX, src_y, W - MX, src_y], fill=HAIR, width=1)
    f_src = fit_font(draw, SOURCES_LINE, SANS, CW, 11)
    sw = draw.textlength(SOURCES_LINE, font=f_src)
    draw.text(((W - sw) / 2, src_y + 6), SOURCES_LINE,
              font=f_src, fill=MUTED)
    assert src_y + 6 + line_h(f_src) <= W - 4, "page overflow"

    return canvas


def main():
    canvas = build()
    canvas.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    fmt = "PNG"
    if size > 1_048_576:
        canvas.save(OUT, format="JPEG", quality=88)
        size = os.path.getsize(OUT)
        fmt = "JPEG q88"
    if size > 1_048_576:
        canvas.save(OUT, format="JPEG", quality=80)
        size = os.path.getsize(OUT)
        fmt = "JPEG q80"
    print(f"wrote {OUT}: {canvas.size}, {fmt}, {size} bytes")
    assert size <= 1_048_576, "entry image exceeds the 1 MiB gate"


if __name__ == "__main__":
    main()
