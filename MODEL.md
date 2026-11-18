# MODEL.md — "The World: Wednesday 18 November 2026"

## What it is
A one-page newspaper front page that sums up Wednesday 18 November 2026's
world news. The program is `main.py` (stdlib only): it copies the
pre-rendered `entry.png` to the grader's output directory. The image itself
is drawn at build time by `draw_frontpage.py` (PIL) from the day's verified
headlines, because the sandbox runs with no network.

## Why this design
The judge ranks on (1) naming the day with specific events of that day,
(2) selection and breadth, (3) readability from the image alone. So the page
is a classic front page: masthead, the date in red, one lead story with an
illustration, six stories across regions and beats, and an "Also today"
strip. No story is older than the day itself; nothing in the image is copied
from anyone else's photograph or artwork — every visual is drawn in code.

## Stories chosen (all first reported 18 Nov 2026)
- **Lead, Asia:** APEC opens in Shenzhen; Trump flies in from Quad talks in
  Manila; the first Trump–Xi–Putin summit is set for Thursday.
- **Weather:** Cyclone Akvan bears down on Andhra Pradesh, landfall due
  20 November.
- **Europe:** Estonia to shut its Russia border from December; hundreds of
  thousands rally in Prague for a free press.
- **War:** Russia–Ukraine drone exchanges as Abu Dhabi peace talks go on;
  a Russian military transport plane crashes in Siberia, killing 19.
- **Middle East:** Iran and the US trade strikes around Qeshm and Bahrain;
  Kuwait reports drone attacks; Gaza ceasefire warned to face collapse.
- **Sport:** MS Dhoni retires from the IPL; India win a record 10th SAFF
  title, beating Pakistan 2–1.
- **Briefs:** Spain general strike; Stacy Keach dies at 85; India
  re-elected to the UN telecom council.
- **Also:** US presses ICAO over Taiwan flight curbs; DR Congo peace
  efforts fail; Ecuador fishermen sue over a US drone strike.

## Checks
- `python3 draw_frontpage.py` renders `entry.png` (1024x1024, ~177 KB,
  under the 1 MiB / 1024x1024 caps).
- `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py` twice gives
  byte-identical output.
