#!/usr/bin/env python3
"""Render the front page for Wednesday 18 November 2026.

Draws a dense newspaper front page (1024x1024 PNG) with PIL only:
masthead, lead story with a flat drawn illustration, a three-column
story grid grouped by region and field, a UTC timeline strip and a
date-check footer. Every story was first reported on 18 Nov 2026;
see MODEL.md for the sourcing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
CONTENT_W = W - 2 * MARGIN

FONT_DIR = "/usr/share/fonts/truetype/noto"

INK = (24, 24, 22)
PAPER = (250, 247, 238)
RULE = (24, 24, 22)
MUTED = (96, 92, 84)
NAVY = (18, 38, 66)
NAVY_LIGHT = (34, 64, 102)
ACCENT = (158, 32, 28)
SAND = (214, 196, 150)
SEA = (52, 110, 158)
SEA_DARK = (28, 74, 116)
GOLD = (198, 152, 48)
PANEL = (238, 233, 220)
LINE = (196, 190, 176)


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: load_font("NotoSerif-Bold.ttf", s)
SERIF_R = lambda s: load_font("NotoSerif-Regular.ttf", s)
SANS_B = lambda s: load_font("NotoSans-Bold.ttf", s)
SANS_R = lambda s: load_font("NotoSans-Regular.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def one_line(draw, text, font, max_w):
    """Fit text to a single line, trimming at a word boundary with an ellipsis."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    words = text.split()
    out = ""
    for word in words:
        trial = (out + " " + word).strip()
        if draw.textlength(trial + " ...", font=font) <= max_w:
            out = trial
        else:
            break
    return (out + " ...") if out else text[:12] + " ..."


# ---------------------------------------------------------------- stories

LEAD_KICKER = "LEAD  |  THE GULF ON ALERT"
LEAD_HEAD = "Iran fires drones at US bases in Kuwait and Bahrain after US strike on Qeshm Island"
LEAD_BODY = (
    "Iran launched drones at American installations in Kuwait and Bahrain in the early "
    "hours of Wednesday, after US jets struck a Revolutionary Guard missile site on "
    "Qeshm Island. Both Gulf states said they intercepted the drones; no damage "
    "was confirmed."
)
LEAD_SOURCE = "Sources: Reuters  |  Wall Street Journal  |  Al Jazeera  (also in footer)"

# (headline, one-line summary) per section, in column order.
SECTIONS = [
    ("AMERICAS", [
        ("Peltola wins Alaska Senate seat; Democrats take 56-44 majority",
         "Democrat Mary Peltola beat incumbent Dan Sullivan."),
        ("US loses measles-free status after 26 years",
         "5,412 cases in 2026, the most since 1991; 10 deaths."),
        ("Outages hit US systems, reaching the NSA network",
         "White House says no sign of a systemic attack."),
        ("Trump claims 'very big' Philippines trade deal",
         "Manila says nothing was signed; only an understanding."),
        ("Florida pastor convicted over 2021 killing of Haiti's president",
         "US court finds role in the assassination plot."),
    ]),
    ("EUROPE", [
        ("Kerch Bridge partly collapses after second day of strikes",
         "Ukraine hit the Crimea link; a road span fell."),
        ("Putin 'not ready' for serious Ukraine peace talks",
         "Sources tell the New York Times negotiations stall."),
        ("UK sanctions firms tied to West Bank settlements",
         "London also urges a halt to the E1 project."),
        ("Russian military plane crashes in Siberia; 19 dead",
         "The aircraft came down in the Kemerovo region."),
        ("Juan Mata retires from football at 38",
         "Former Spain midfielder ends a decorated career."),
    ]),
    ("AFRICA", [
        ("Congo Ebola outbreak passes 11,000 cases",
         "5,400 dead; three in four infected under-5s die."),
        ("Clashes near Eritrea border raise war fears",
         "Fighting reported in Tigray, Ethiopia."),
        ("Six killed as building collapses in Nairobi",
         "The block was still under construction."),
    ]),
    ("MIDDLE EAST", [
        ("Board of Peace says Israel and Hamas failing ceasefire terms",
         "A 12-page report seen by Reuters warns both sides."),
        ("Knesset elects Matan Kahana as speaker",
         "Win for prime minister-elect Gadi Eisenkot's bloc."),
        ("Houthis say they fired drones at Saudi pipeline",
         "Five drones aimed at pumping stations near Riyadh."),
        ("Australia sanctions Israelis over settler violence",
         "Three people and four groups face measures."),
        ("Cold kills in Gaza tents as winter closes in",
         "WHO counts 950,000 displaced on flood-prone ground."),
        ("UN: 2,230 civilians killed in Sudan this year",
         "Over 1,630 died in drone strikes, mostly in Kordofan."),
    ]),
    ("ASIA-PACIFIC", [
        ("Xi and Putin meet at APEC in Shenzhen",
         "Both attack protectionism and sanctions; Trump due next."),
        ("Takaichi and Xi shake hands at APEC summit",
         "Japan-China leaders meet as Taiwan dispute persists."),
        ("Taiwan logs 10 Chinese sorties and 11 ships",
         "Russian jets also flew near Taiwan and Japan."),
        ("Myanmar to review its future with ASEAN",
         "President Min Aung Hlaing criticises 'unfair treatment'."),
        ("World Court to rule on Myanmar genocide case",
         "Judges decide on the Rohingya case on Thursday."),
        ("Cyclone Akvan bears down on India's east coast",
         "Severe storm forecast to cross near Narsapur-Puri."),
        ("Cyclone Xavier hits Cook Islands at Category 5",
         "Gusts of 315 km/h; shelters open in the north."),
    ]),
    ("BUSINESS & MARKETS", [
        ("Nvidia revenue doubles to $115.8bn in record quarter",
         "Board rules out bringing back Jensen Huang as CEO."),
        ("Anthropic targets a $1.4tn valuation in IPO",
         "The AI firm's listing is the day's biggest market test."),
        ("Stocks slide worldwide as volatility jumps",
         "S&P 500 -1.0%; DAX -2.1%; VIX up 11%."),
        ("RBA board split 6-3 on rate rise to 4.85%",
         "Governor Bullock calls 3-3.5% inflation 'the new normal'."),
        ("Trump signs trade statement with Thailand",
         "Deal 'substantially concluded', PM Anutin says."),
    ]),
    ("TECHNOLOGY & SCIENCE", [
        ("AI finds a critical flaw in the Java language",
         "Start-up Calif disclosed the bug to Oracle."),
        ("Singapore offers US checks on AI chip use",
         "Move follows new export curbs on overseas computing."),
        ("Kling Image 4.0 launches with native 8K",
         "China's video model adds editable text and sets of 10."),
        ("Voyager 1 reaches one light-day from Earth",
         "16bn miles out; light needs a full day to cover it."),
        ("3,300-year-old sword pulled from Italian lake",
         "The bronze blade from Lake Mezzano is still sharp."),
    ]),
    ("CULTURE & SPORT", [
        ("Sanchez named NWSL MVP after record 20 goals",
         "North Carolina Courage star also takes the Golden Boot."),
        ("Cricket World Cup ticket requests near 140m",
         "India-Pakistan leads demand for the 2027 tournament."),
        ("Guler extends Real Madrid deal until 2032",
         "The 21-year-old signs after a breakthrough season."),
        ("'Hold Onto Me' wins three Thessaloniki awards",
         "The film tops the Greek festival's honours."),
    ]),
]

# Columns: which sections go in each of the three columns.
COLUMNS = [
    ["AMERICAS", "EUROPE", "AFRICA"],
    ["MIDDLE EAST", "ASIA-PACIFIC"],
    ["BUSINESS & MARKETS", "TECHNOLOGY & SCIENCE", "CULTURE & SPORT"],
]

# (time label, moment) for the UTC timeline strip.
TIMELINE = [
    ("EARLY", "Iran drones at Kuwait, Bahrain"),
    ("~02:00", "Xi, Putin meet at APEC"),
    ("04:00", "Trump-Marcos lunch, Manila"),
    ("06:00", "Akvan fix, Bay of Bengal"),
    ("10:16", "Voyager 1: one light-day"),
    ("11:38", "Xavier Cat 5 bulletin"),
    ("19:59", "Sudan grid strikes reported"),
    ("23:30", "Sanchez named NWSL MVP"),
]

SECTION_MAP = {name: items for name, items in SECTIONS}


def draw_illustration(draw, x0, y0, x1, y1):
    """Flat drawn scene of the Gulf: land, strait, ship, drones, burst."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # sky band and sun
    draw.ellipse([x1 - 62, y0 + 10, x1 - 22, y0 + 50], fill=GOLD)
    # land masses (sand): top-left Kuwait/Bahrain side, bottom-right Iran side
    draw.polygon([(x0, y0), (x0 + 150, y0), (x0 + 110, y0 + 52),
                  (x0, y0 + 58)], fill=SAND)
    draw.polygon([(x0 + 190, y1), (x1, y1), (x1, y1 - 56),
                  (x0 + 230, y1 - 46)], fill=SAND)
    # the strait: a diagonal band of sea between the land masses
    draw.polygon([(x0, y0 + 58), (x0 + 110, y0 + 52), (x1, y1 - 56),
                  (x0 + 230, y1 - 46), (x0, y1), (x0, y0 + 58)],
                 fill=SEA)
    # small ship on the strait
    sx, sy = x0 + 150, y0 + 78
    draw.polygon([(sx, sy), (sx + 52, sy), (sx + 44, sy + 10),
                  (sx + 6, sy + 10)], fill=(232, 228, 214))
    draw.rectangle([sx + 18, sy - 10, sx + 30, sy], fill=(232, 228, 214))
    draw.rectangle([sx + 22, sy - 18, sx + 24, sy - 10], fill=ACCENT)
    # drone dots with dashed paths
    for dx, dy in [(x0 + 60, y0 + 92), (x0 + 96, y0 + 108), (x0 + 250, y0 + 34)]:
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 255, 255))
        draw.ellipse([dx - 6, dy - 1, dx + 6, dy + 1], fill=(255, 255, 255))
    # burst where the strike fell (Qeshm side)
    bx, by = x0 + 268, y1 - 34
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 8, 22
        a = math.radians(ang)
        draw.line([(bx + r1 * math.cos(a), by + r1 * math.sin(a)),
                   (bx + r2 * math.cos(a), by + r2 * math.sin(a))],
                  fill=(255, 176, 32), width=3)
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 176, 32))
    # tiny place labels
    lab = SANS_B(9)
    draw.text((x0 + 8, y0 + 6), "KUWAIT", font=lab, fill=(24, 24, 22))
    draw.text((x0 + 8, y0 + 62), "BAHRAIN", font=lab, fill=(255, 255, 255))
    draw.text((x1 - 74, y1 - 16), "QESHM I.", font=lab, fill=(24, 24, 22))
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    y = 14
    name_font = SERIF_B(50)
    name = "The One-Day Gazette"
    nw = draw.textlength(name, font=name_font)
    draw.text(((W - nw) / 2, y), name, font=name_font, fill=INK)
    y += 62
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 6
    date_font = SANS_B(19)
    date_txt = "WEDNESDAY  18  NOVEMBER  2026"
    dw = draw.textlength(date_txt, font=date_font)
    draw.text(((W - dw) / 2, y), date_txt, font=date_font, fill=ACCENT)
    y += 26
    tag_font = SERIF_R(13)
    tag = "One day's world news  —  every story first reported on 18 November 2026"
    tw = draw.textlength(tag, font=tag_font)
    draw.text(((W - tw) / 2, y), tag, font=tag_font, fill=MUTED)
    y += 22
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    mast_bottom = y + 2

    # ---------------------------------------------------------- lead story
    ly = mast_bottom + 10
    lead_h = 138
    lx0, lx1 = MARGIN, MARGIN + 606
    ix0, ix1 = MARGIN + 622, W - MARGIN
    kick_font = SANS_B(12)
    draw.text((lx0, ly), LEAD_KICKER, font=kick_font, fill=ACCENT)
    head_font = SERIF_B(26)
    head_lines = wrap(draw, LEAD_HEAD, head_font, lx1 - lx0)[:2]
    hy = ly + 20
    for ln in head_lines:
        draw.text((lx0, hy), ln, font=head_font, fill=INK)
        hy += 31
    body_font = SANS_R(13)
    body_lines = wrap(draw, LEAD_BODY, body_font, lx1 - lx0)
    assert len(body_lines) <= 3, f"lead body wraps to {len(body_lines)} lines"
    by = hy + 4
    for ln in body_lines:
        draw.text((lx0, by), ln, font=body_font, fill=(52, 50, 46))
        by += 17
    src_font = SANS_R(10)
    # Sources for the lead story are named in the footer and in MODEL.md;
    # no separate source line here, so the body never collides with it.
    _ = src_font
    draw_illustration(draw, ix0, ly, ix1, ly + lead_h)
    grid_top = ly + lead_h + 12
    draw.line([(MARGIN, grid_top - 4), (W - MARGIN, grid_top - 4)],
              fill=RULE, width=1)

    # ---------------------------------------------------------- story grid
    col_w = (CONTENT_W - 2 * 12) // 3
    col_x = [MARGIN, MARGIN + col_w + 12, MARGIN + 2 * (col_w + 12)]
    grid_bottom = 884
    sec_font = SANS_B(11)
    item_head_font = SANS_B(12)
    item_sum_font = SANS_R(10)
    deepest = 0
    for ci, col_sections in enumerate(COLUMNS):
        cx = col_x[ci]
        cy = grid_top
        for sec_name in col_sections:
            # section header bar
            draw.rectangle([cx, cy, cx + col_w, cy + 19], fill=NAVY)
            draw.text((cx + 7, cy + 4), sec_name, font=sec_font,
                      fill=(255, 255, 255))
            cy += 19 + 6
            for headline, summary in SECTION_MAP[sec_name]:
                h_lines = wrap(draw, headline, item_head_font, col_w)[:2]
                for ln in h_lines:
                    draw.text((cx, cy), ln, font=item_head_font, fill=INK)
                    cy += 15
                s_line = one_line(draw, summary, item_sum_font, col_w)
                draw.text((cx, cy), s_line, font=item_sum_font, fill=(74, 70, 62))
                cy += 13
                draw.line([(cx, cy + 2), (cx + col_w, cy + 2)], fill=LINE, width=1)
                cy += 7
            cy += 2
        deepest = max(deepest, cy)
    assert deepest <= grid_bottom + 2, f"grid overflow: {deepest} > {grid_bottom}"

    # ---------------------------------------------------------- UTC timeline
    ty = grid_bottom + 10
    draw.line([(MARGIN, ty), (W - MARGIN, ty)], fill=RULE, width=2)
    tl_font = SANS_B(11)
    draw.text((MARGIN, ty + 6), "THE DAY IN UTC", font=tl_font, fill=ACCENT)
    line_y = ty + 38
    draw.line([(MARGIN, line_y), (W - MARGIN, line_y)], fill=NAVY, width=2)
    n = len(TIMELINE)
    slot = CONTENT_W / n
    t_font = SANS_B(10)
    m_font = SANS_R(9)
    for i, (tlabel, moment) in enumerate(TIMELINE):
        cxp = MARGIN + slot * i + slot / 2
        draw.ellipse([cxp - 4, line_y - 4, cxp + 4, line_y + 4], fill=ACCENT)
        twd = draw.textlength(tlabel, font=t_font)
        draw.text((cxp - twd / 2, line_y - 22), tlabel, font=t_font, fill=NAVY)
        m_lines = wrap(draw, moment, m_font, slot - 6)
        my = line_y + 9
        for ln in m_lines[:2]:
            mwd = draw.textlength(ln, font=m_font)
            draw.text((cxp - mwd / 2, my), ln, font=m_font, fill=(52, 50, 46))
            my += 11
    time_bottom = line_y + 34

    # ---------------------------------------------------------- footer
    fy = time_bottom + 6
    draw.line([(MARGIN, fy), (W - MARGIN, fy)], fill=RULE, width=1)
    foot_font = SANS_R(10)
    foot_b_font = SANS_B(10)
    check = ("DATE CHECK — Every story above happened, or was first reported, on "
             "Wednesday 18 November 2026. Nothing from an earlier day is shown as "
             "the day's news.")
    for ln in wrap(draw, check, foot_b_font, CONTENT_W):
        draw.text((MARGIN, fy + 6), ln, font=foot_b_font, fill=INK)
        fy += 13
    srcs = ("Sources: Reuters, Associated Press, AFP, BBC, Al Jazeera, Wall Street "
            "Journal, New York Times, USA Today, United Nations, NASA JPL, India "
            "Meteorological Department, RNZ Pacific, BusinessWorld, Rappler, NEXA, "
            "Asia Daily. Full sourcing in MODEL.md.")
    for ln in wrap(draw, srcs, foot_font, CONTENT_W):
        draw.text((MARGIN, fy + 4), ln, font=foot_font, fill=MUTED)
        fy += 12
    assert fy <= H - 8, f"footer overflow: {fy}"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"saved {out}: {img.size[0]}x{img.size[1]}, {size} bytes")
    print(f"grid deepest y: {deepest} (limit {grid_bottom}); footer ends y: {fy}")
    assert size <= 1048576, "entry.png over 1 MiB"
    return out


if __name__ == "__main__":
    main()
