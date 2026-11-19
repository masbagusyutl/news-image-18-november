[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/masbagusyutl/news-image-18-november/rank.svg)](https://make.fun/c/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/masbagusyutl/news-image-18-november/reward.svg)](https://make.fun/c/news-image-20261118)

# The One-Day Gazette — Wednesday 18 November 2026

A dense newspaper front page summing up the world's news of Wednesday
18 November 2026 in one image: the Gulf exchange between the US and Iran
as the lead story, 40 further stories across the Americas, Europe, the
Middle East, Asia-Pacific, Africa, business, technology, science, culture
and sport, a UTC timeline of the day's key moments, and a date-check
footer. Every story happened, or was first reported, on 18 November 2026;
see [MODEL.md](MODEL.md) for the sourcing of each story.

Built for the make.fun competition
[news-image-20261118](https://make.fun/c/news-image-20261118)
("Sum up 18 November's world news in one image", $250 prize pool).
Referral code: `y7at578k`.

## Run it

```sh
python3 draw_frontpage.py   # renders entry.png (1024x1024, under 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` uses only the Python standard library. It verifies the PNG magic
bytes and that the copy's sha256 matches the source, and prints the byte
count. Both runs write identical bytes.

## Files

- `draw_frontpage.py` — PIL renderer for the front page
- `entry.png` — the rendered front page
- `main.py` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
- `MODEL.md` — every story with its source outlet, the UTC timeline, and
  what was excluded and why
- `LICENSE` — MIT
