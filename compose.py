#!/usr/bin/env python3
"""Compose the final entry image for news-image-20261118: a one-page
newspaper, "The World in One Day", summing up Wednesday 18 November 2026.

Second design (20 November, replacing the first newspaper before the
entries deadline): a clean, modern page built to stay legible at
thumbnail size. Top to bottom, on a 1024x1024 cream page:

  * masthead  - the paper's name, the date as the headline, a deck line
  * timeline  - "THE DAY IN UTC": five moments of the day on one line
  * lead      - story 1, the APEC summit in Shenzhen, with the entry's
                original cover illustration (assets/hero-apec.png)
  * grid      - stories 2-9, numbered, each with a thumbnail, a region
                chip, a headline and a short summary
  * briefs    - stories 10-29 grouped under regional colour bands
                (Americas / Asia / Europe / Middle East / Global)
  * footer    - a DATE CHECK strip and the sources line in one block

Every story carries the colour of its region all the way down the
page, so the grouping survives a glance. Every letter is drawn here
with PIL from the story texts below; the illustrations contain no
text, so nothing can come out garbled. The story texts are the single
source of truth for what the page says, and SOURCES.md records how
each was verified. The 29 stories are the same verified set as the
first design; only the layout changed.

Output: entry.png (PNG, or JPEG bytes if PNG would exceed the
1,048,576-byte gate - the grader tells formats apart by magic bytes).
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W = 1024
MX = 30                      # page margin
CW = W - 2 * MX              # content width = 964

PAPER = (247, 243, 233)
INK = (26, 25, 22)
MUTED = (96, 90, 78)
HAIR = (178, 170, 152)

# one colour per region, used for chips, numbers and band headers
ASIA = (176, 32, 32)
EUROPE = (30, 78, 158)
AMERICAS = (16, 116, 88)
AFRICA = (198, 110, 16)
MIDEAST = (116, 58, 158)
GLOBAL = (164, 120, 18)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# ---------------------------------------------------------------- stories

LEAD = {
    "num": 1,
    "region": "ASIA",
    "color": ASIA,
    "kicker": "SHENZHEN · THE SUMMIT",
    "headline": "Trump, Xi and Putin hold first three-way summit",
    "summary": (
        "Xi Jinping met Vladimir Putin in Shenzhen on Wednesday, then "
        "greeted Donald Trump on arrival. The three nuclear powers sit "
        "down together on Thursday - Ukraine, Iran and trade top the "
        "table. Indonesia's Prabowo is among the leaders in town."
    ),
    "credit": "Cover: the three leaders in Shenzhen. Original illustration.",
    "image": "hero-apec.png",
    "hero_crop": (60, 400, 1540, 1185),
}

# five moments on the day line; labels are day-parts or places taken
# from the stories themselves, never invented clock times
TIMELINE = [
    ("BEFORE DAWN", MIDEAST, "Iran fires at US bases in the Gulf"),
    ("SHENZHEN", ASIA, "Xi greets Trump in Shenzhen"),
    ("DEEP SPACE", GLOBAL, "Voyager 1 crosses one light-day"),
    ("WASHINGTON", AMERICAS, "Peltola's win flips the Senate"),
    ("TONIGHT", AMERICAS, "Anthropic prices its IPO"),
]

BOXES = [
    {
        "num": 2, "region": "MIDDLE EAST", "color": MIDEAST,
        "headline": "Iran fires at US bases in the Gulf",
        "summary": (
            "Iran targeted US installations in Kuwait and Bahrain "
            "before dawn, after US jets struck a missile site on "
            "Qeshm Island."
        ),
        "image": "illo-gulf.png",
    },
    {
        "num": 3, "region": "EUROPE", "color": EUROPE,
        "headline": "Ukraine hits Kerch Bridge a second night",
        "summary": (
            "Kyiv says a road span collapsed in a second straight "
            "night of strikes. Moscow confirms damage, vows to rebuild."
        ),
        "image": "illo-kerch.png",
    },
    {
        "num": 4, "region": "MIDDLE EAST", "color": MIDEAST,
        "headline": "Truce warning as winter closes in",
        "summary": (
            "The US-backed Board of Peace warns the ceasefire could "
            "collapse; 1.7m people remain displaced, many in flooded "
            "tents."
        ),
        "image": "illo-gaza.png",
    },
    {
        "num": 5, "region": "ASIA", "color": ASIA,
        "headline": "Akvan bears down on the Odisha coast",
        "summary": (
            "The severe cyclone is due ashore Friday near Puri, winds "
            "near 110 km/h. Over 47,000 people are already in shelters."
        ),
        "image": "illo-akvan.png",
    },
    {
        "num": 6, "region": "AMERICAS", "color": AMERICAS,
        "headline": "Peltola's Alaska win flips the Senate",
        "summary": (
            "Democrat Mary Peltola, the first Alaska Native senator, "
            "unseats Dan Sullivan - a projected 56-44 majority."
        ),
        "image": "illo-capitol.png",
    },
    {
        "num": 7, "region": "AMERICAS", "color": AMERICAS,
        "headline": "Nvidia's record quarter; no return for Huang",
        "summary": (
            "Revenue doubled to a record $115.8bn as AI demand held. "
            "The board ruled out reinstating founder Jensen Huang."
        ),
        "image": "illo-nvidia.png",
    },
    {
        "num": 8, "region": "AFRICA", "color": AFRICA,
        "headline": "Ebola cases pass 11,000 in DR Congo",
        "summary": (
            "The outbreak passed 11,000 cases on Wednesday, as "
            "response teams race to contain new hotspots in the east."
        ),
        "image": "illo-ebola.png",
    },
    {
        "num": 9, "region": "GLOBAL", "color": GLOBAL,
        "headline": "A star eats its companion in Andromeda",
        "summary": (
            "Webb data clinches a first-of-its-kind stellar merger: "
            "a small star spiralled into a supergiant 2.5m light-years "
            "away."
        ),
        "image": "illo-andromeda.png",
    },
]

# briefs grouped by region; the count in each header covers the whole
# region, including its stories in the lead and the grid above
BRIEF_GROUPS = [
    ("AMERICAS", AMERICAS, 8, [
        (10, "Anthropic prices its IPO tonight; demand may lift it above the range"),
        (11, "OpenAI launches GPT-6.2 Astra and Sol, with lower API prices"),
        (12, "Fed minutes point to more rate rises; dollar at a 19-month high"),
        (13, "Dow falls a third day, -1.11%; gold slides 3.5% to $3,729"),
        (14, "Canada's Carney meets Trump on the APEC sidelines in Shenzhen"),
        (15, "The United States loses its measles-free status after 26 years"),
    ]),
    ("ASIA", ASIA, 6, [
        (16, "COP31 talks in Antalya enter their final 48 hours, 144 items disputed"),
        (17, "ASEAN sets out the terms for Myanmar's return to the bloc"),
        (18, "Indonesia and China sign $71.8bn of deals, incl. ten smart cities"),
        (19, "Pakistan cuts petrol by Rs3 a litre, down to Rs325"),
    ]),
    ("EUROPE", EUROPE, 4, [
        (20, "Russia and Ukraine agree to their largest prisoner swap yet"),
        (21, "UK inflation jumps to 3.6% in October, a one-year high"),
        (22, "Ukraine: its drone campaign has cut Russian refining by ~45%"),
    ]),
    ("MIDDLE EAST", MIDEAST, 6, [
        (23, "Israel's Knesset elects Matan Kahana as speaker, 66-52"),
        (24, "President Herzog asks Gadi Eisenkot to form Israel's government"),
        (25, "Turkish authorities seize control of an opposition broadcaster"),
        (26, "Debris from an intercepted attack damages an Aramco tower, Riyadh"),
    ]),
    ("GLOBAL", GLOBAL, 4, [
        (27, "Voyager 1 crosses one light-day from Earth, a human-made first"),
        (28, "NASA: space dust holds clues to ancient ice beyond Neptune"),
        (29, "Robert Pattinson is named as the new James Bond"),
    ]),
]

# brief columns: (groups in column order) - balanced by item count
BRIEF_COLUMNS = [[0], [1, 2], [3, 4]]

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
    draw.rectangle([MX, 12, W - MX, 14], fill=INK)
    draw.line([MX, 18, W - MX, 18], fill=INK, width=1)
    f_small = font(SANS_B, 12)
    draw_tracked(draw, MX, 25, "THE WORLD IN ONE DAY", f_small, INK, 3)
    right = "ONE PAGE · 29 STORIES · 6 REGIONS"
    rw = tracked_width(draw, right, f_small, 3)
    draw_tracked(draw, W - MX - rw, 25, right, f_small, INK, 3)

    title = "Wednesday 18 November 2026"
    f_title = fit_font(draw, title, SERIF_BLACK, CW, 52)
    draw.text(
        ((W - draw.textlength(title, font=f_title)) / 2, 42),
        title, font=f_title, fill=INK,
    )
    deck = ("Three leaders meet in Shenzhen · a span falls in Crimea "
            "· Voyager crosses one light-day")
    f_deck = fit_font(draw, deck, SERIF_IT, CW, 16)
    draw.text(
        ((W - draw.textlength(deck, font=f_deck)) / 2, 104),
        deck, font=f_deck, fill=MUTED,
    )
    draw.line([MX, 126, W - MX, 126], fill=INK, width=2)

    # ---- timeline: the day in UTC ----------------------------------
    tl_y = 136
    draw_tracked(draw, MX, tl_y, "THE DAY IN UTC", font(SANS_B, 11),
                 MUTED, 2)
    line_y = tl_y + 35
    draw.line([MX, line_y, W - MX, line_y], fill=HAIR, width=2)
    cell_w = CW / 5
    f_lab = font(SANS_B, 11)
    f_cap = font(SANS, 10)
    for i, (label, color, caption) in enumerate(TIMELINE):
        cx = MX + cell_w * (i + 0.5)
        lw = draw.textlength(label, font=f_lab)
        draw.text((cx - lw / 2, tl_y + 17), label, font=f_lab, fill=color)
        draw.ellipse([cx - 4, line_y - 4, cx + 4, line_y + 4], fill=color)
        clines = wrap(draw, caption, f_cap, cell_w - 10)
        assert len(clines) <= 2, f"timeline caption wraps: {caption}"
        cy = line_y + 8
        for ln in clines:
            cw2 = draw.textlength(ln, font=f_cap)
            draw.text((cx - cw2 / 2, cy), ln, font=f_cap, fill=INK)
            cy += 12.5
    draw.line([MX, 198, W - MX, 198], fill=HAIR, width=1)

    # ---- lead story -------------------------------------------------
    lead_y = 208
    draw.rectangle([MX, lead_y + 3, MX + 11, lead_y + 14], fill=ASIA)
    draw_tracked(
        draw, MX + 18, lead_y,
        f"{LEAD['num']} · {LEAD['region']} — {LEAD['kicker']}",
        font(SANS_B, 13), ASIA, 1,
    )
    img_y = lead_y + 22
    img_w, img_h = 420, 148
    hero = thumb(os.path.join(ASSETS, LEAD["image"]), img_w, img_h,
                 crop=LEAD["hero_crop"])
    canvas.paste(hero, (MX, img_y))
    draw.rectangle([MX, img_y, MX + img_w, img_y + img_h],
                   outline=INK, width=1)
    draw.text((MX, img_y + img_h + 4), LEAD["credit"],
              font=font(SERIF_IT, 10), fill=MUTED)
    tx = MX + img_w + 18
    tw = W - MX - tx
    f_head = font(SERIF_BOLD, 30)
    head_lines = wrap(draw, LEAD["headline"], f_head, tw)
    assert len(head_lines) <= 3, "lead headline overflow"
    hy = img_y
    for ln in head_lines:
        draw.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 35
    draw.line([tx, hy + 3, W - MX, hy + 3], fill=HAIR, width=1)
    f_sum = font(SANS, 13)
    sum_lines = wrap(draw, LEAD["summary"], f_sum, tw)
    assert len(sum_lines) <= 5, "lead summary too long"
    sy = hy + 11
    for ln in sum_lines:
        draw.text((tx, sy), ln, font=f_sum, fill=INK)
        sy += 16.5
    assert sy <= img_y + img_h + 22, f"lead text overflow: {sy}"

    # ---- story grid -------------------------------------------------
    grid_y = img_y + img_h + 28
    draw.line([MX, grid_y - 8, W - MX, grid_y - 8], fill=INK, width=1)
    gap = 14
    box_w = (CW - 3 * gap) // 4
    box_h = 128
    thumb_h = 34
    for idx, box in enumerate(BOXES):
        bx = MX + (idx % 4) * (box_w + gap)
        by = grid_y + (idx // 4) * (box_h + 10)
        im = thumb(os.path.join(ASSETS, box["image"]), box_w, thumb_h)
        canvas.paste(im, (bx, by))
        draw.rectangle([bx, by, bx + box_w, by + thumb_h],
                       outline=HAIR, width=1)
        draw_tracked(draw, bx, by + thumb_h + 4,
                     f"{box['num']} · {box['region']}",
                     font(SANS_B, 10), box["color"], 1)
        f_bh = font(SERIF_BOLD, 14)
        blines = wrap(draw, box["headline"], f_bh, box_w)
        assert len(blines) <= 2, f"box headline overflow: {box['headline']}"
        hy2 = by + thumb_h + 19
        for ln in blines:
            draw.text((bx, hy2), ln, font=f_bh, fill=INK)
            hy2 += 17
        f_bs = font(SANS, 11)
        slines = wrap(draw, box["summary"], f_bs, box_w)
        assert len(slines) <= 3, f"box summary overflow: {box['headline']}"
        sy2 = hy2 + 2
        for ln in slines:
            draw.text((bx, sy2), ln, font=f_bs, fill=INK)
            sy2 += 13
        assert sy2 <= by + box_h + 2, f"box overflow: {box['headline']}"

    # ---- briefs, grouped by region -----------------------------------
    brief_y = grid_y + 2 * box_h + 10 + 10
    draw_tracked(draw, MX, brief_y, "AROUND THE WORLD — THE REST OF THE DAY",
                 font(SANS_B, 12), INK, 2)
    draw.line([MX, brief_y + 18, W - MX, brief_y + 18], fill=INK, width=1)
    col_gap = 22
    col_w = (CW - 2 * col_gap) // 3
    f_gh = font(SANS_B, 11)
    f_item = font(SANS, 12)
    f_num = font(SANS_B, 12)
    briefs_bottom = 0
    for ci, group_ids in enumerate(BRIEF_COLUMNS):
        x = MX + ci * (col_w + col_gap)
        y = brief_y + 26
        for gi in group_ids:
            name, color, total, items = BRIEF_GROUPS[gi]
            draw.rectangle([x, y, x + col_w, y + 17], fill=color)
            draw.text((x + 6, y + 3), f"{name} — {total} STORIES",
                      font=f_gh, fill=PAPER)
            y += 23
            for num, text in items:
                num_s = f"{num}"
                draw.text((x, y), num_s, font=f_num, fill=color)
                nw = draw.textlength("99 ", font=f_num)
                ilines = wrap(draw, text, f_item, col_w - nw)
                assert len(ilines) <= 2, f"brief wraps: {text}"
                iy = y
                for ln in ilines:
                    draw.text((x + nw, iy), ln, font=f_item, fill=INK)
                    iy += 14.5
                y = iy + 3.5
            y += 4
        briefs_bottom = max(briefs_bottom, y)

    # ---- date check + sources ----------------------------------------
    dc_y = briefs_bottom + 4
    assert dc_y + 34 <= W - 2, f"page overflow: bottom block at {dc_y}"
    draw.rectangle([MX, dc_y, W - MX, dc_y + 34], outline=ASIA, width=2)
    f_dc = fit_font(draw, DATE_CHECK, SANS_B, CW - 20, 11)
    dw = draw.textlength(DATE_CHECK, font=f_dc)
    draw.text(((W - dw) / 2, dc_y + 5), DATE_CHECK, font=f_dc, fill=ASIA)
    f_src = fit_font(draw, SOURCES_LINE, SANS, CW - 20, 10)
    sw = draw.textlength(SOURCES_LINE, font=f_src)
    draw.text(((W - sw) / 2, dc_y + 20), SOURCES_LINE,
              font=f_src, fill=MUTED)

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
