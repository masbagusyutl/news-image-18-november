#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

All stories below were first reported on Wednesday 18 November 2026,
gathered from international wire and newspaper reporting that morning. The
program draws the page with PIL at build time; the entry's main.py only
copies the finished entry.png to the grader's output directory (the sandbox
runs with no network, so the day's news has to be baked in here).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (22, 21, 19)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
GREY = (90, 86, 78)
RULE = (180, 172, 150)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lead_art(d, x0, y0, x1, y1):
    """Stylised Shenzhen skyline under a globe: APEC opens in the city."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 240))
    # globe, top right
    gx, gy, gr = x1 - 58, y0 + 52, 44
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(38, 84, 134))
    for k in (-0.55, 0.0, 0.55):
        d.arc([gx - gr, gy - gr, gx + gr, gy + gr],
              start=90 + k * 90, end=270 + k * 90, fill=(214, 228, 240),
              width=2)
    d.ellipse([gx - gr, gy - 8, gx + gr, gy + 8], outline=(214, 228, 240),
              width=2)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=(214, 228, 240), width=2)
    # sun, top left
    d.ellipse([x0 + 16, y0 + 14, x0 + 52, y0 + 50], fill=(240, 196, 90))
    # skyline silhouette
    base = y1
    towers = [
        (x0 + 8, 150, 34), (x0 + 48, 118, 30), (x0 + 84, 168, 36),
        (x0 + 126, 96, 34), (x0 + 166, 140, 30), (x0 + 202, 176, 36),
        (x0 + 244, 128, 30),
    ]
    for tx, th, tw in towers:
        d.rectangle([tx, base - th, tx + tw, base], fill=(31, 58, 95))
    # tallest tower: tapered spire
    d.polygon([(x0 + 126, base - 96), (x0 + 160, base - 96),
               (x0 + 152, base - 196), (x0 + 134, base - 196)],
              fill=(31, 58, 95))
    d.line([(x0 + 143, base - 196), (x0 + 143, base - 216)],
           fill=(31, 58, 95), width=3)
    # lit windows
    for wx in range(x0 + 16, x1 - 12, 18):
        for wy in range(base - 120, base - 12, 22):
            if (wx * 7 + wy * 3) % 5 == 0:
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(240, 196, 90))
    # ground line
    d.rectangle([x0, base - 6, x1, base], fill=(16, 15, 14))


LEAD = {
    "kicker": "ASIA  ·  SUMMITS",
    "headline": ("APEC opens in Shenzhen ahead of first Trump\u2013Xi\u2013Putin "
                 "summit"),
    "summary": ("The APEC summit opened in Shenzhen as President Trump flew "
                "in from Quad talks in Manila. On Thursday, Trump, Xi "
                "Jinping and Vladimir Putin meet for the first time as a "
                "trio."),
}

CARDS = [
    ("WEATHER  ·  INDIA", (15, 118, 110),
     "Cyclone Akvan bears down on Andhra Pradesh",
     "The storm over the Bay of Bengal is set to strengthen into a severe "
     "cyclone, with landfall expected on 20 November; coastal districts "
     "are on alert."),
    ("EUROPE  ·  SECURITY", NAVY,
     "Estonia to shut its Russia border; Prague rallies for free press",
     "Estonia will close border crossings from December after an attack "
     "attempt on a defence firm. Hundreds of thousands marched in Prague "
     "against a media law."),
    ("WAR  ·  UKRAINE", RED,
     "Drones fly as Abu Dhabi peace talks go on",
     "Russia and Ukraine traded drone strikes despite peace talks in Abu "
     "Dhabi. A Russian military transport plane crashed in Siberia, "
     "killing 19."),
    ("MIDDLE EAST  ·  THE GULF", (180, 83, 9),
     "Iran and US trade strikes over Gulf waters",
     "Kuwait reported drone attacks as Iran and the US exchanged fire "
     "around Qeshm and Bahrain. A peace board warned Gaza's ceasefire "
     "faces imminent collapse."),
    ("SPORT  ·  INDIA", (22, 101, 52),
     "Dhoni retires from the IPL; India win 10th SAFF title",
     "MS Dhoni called time on his IPL career. India beat Pakistan 2\u20131 "
     "to lift a record 10th SAFF Championship \u2014 a third straight "
     "title."),
    ("WORLD  ·  BRIEFS", (107, 33, 168),
     "Spain hit by general strike; Stacy Keach dies at 85",
     "A general strike disrupted Spanish ports and factories. Stacy "
     "Keach, TV's Mike Hammer, died aged 85. India was re-elected to "
     "the UN telecom council."),
]

ALSO = ("US presses ICAO over Taiwan flight curbs  ·  DR Congo peace "
        "efforts fail to halt eastern violence  ·  Ecuador fishermen sue "
        "over US drone strike")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 120], fill=(16, 15, 14))
    d.text((W // 2, 22), "THE WORLD", font=font(SERIF_B, 76),
           fill=(248, 244, 234), anchor="ma")
    d.text((W // 2, 132), "WEDNESDAY, 18 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=RED, anchor="ma")
    d.text((W // 2, 162), "The day's world news, in one page",
           font=font(SERIF_R, 19), fill=GREY, anchor="ma")
    d.line([(36, 190), (W - 36, 190)], fill=RULE, width=2)

    # Lead story
    lx, lw = 36, 620
    y = 206
    d.text((lx, y), LEAD["kicker"], font=font(SANS_B, 19), fill=RED)
    y += 28
    for line in wrap(d, LEAD["headline"], font(SERIF_B, 38), lw):
        d.text((lx, y), line, font=font(SERIF_B, 38), fill=INK)
        y += 46
    y += 6
    for line in wrap(d, LEAD["summary"], font(SANS_R, 21), lw)[:4]:
        d.text((lx, y), line, font=font(SANS_R, 21), fill=INK)
        y += 27
    draw_lead_art(d, 684, 206, 988, 206 + 236)

    d.line([(36, 456), (W - 36, 456)], fill=RULE, width=2)

    # Story grid: 2 columns x 3 rows
    col_w = 464
    xs = (36, 524)
    ys = (474, 634, 794)
    for i, (kicker, colour, headline, summary) in enumerate(CARDS):
        x = xs[i % 2]
        y = ys[i // 2]
        d.text((x, y), kicker, font=font(SANS_B, 16), fill=colour)
        y += 22
        for line in wrap(d, headline, font(SERIF_B, 24), col_w)[:2]:
            d.text((x, y), line, font=font(SERIF_B, 24), fill=INK)
            y += 29
        y += 4
        for line in wrap(d, summary, font(SANS_R, 19), col_w)[:3]:
            d.text((x, y), line, font=font(SANS_R, 19), fill=(52, 50, 46))
            y += 23

    # Footer
    d.line([(36, 958), (W - 36, 958)], fill=RULE, width=2)
    fy = 966
    for line in wrap(d, "ALSO TODAY:  " + ALSO, font(SANS_B, 15), W - 72):
        d.text((36, fy), line, font=font(SANS_B, 15), fill=INK)
        fy += 20
    d.text((36, 1004), "All events first reported 18 November 2026  ·  "
           "Compiled from international wire reports",
           font=font(SANS_R, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
