[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/konservasilingkungan5-alt/makefun-news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/konservasilingkungan5-alt/makefun-news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# The World Today — Friday 27 November 2026

A one-page newspaper front page summing up the world's news of
Friday 27 November 2026: 32 stories from 6 regions, drawn by a
program written from scratch in this repository.

Bounty: [Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127) ($100, 50 places paid; closes Sunday 29 November 2026, 07:00 WIB).

## What the image shows

- **Masthead and date** — THE WORLD TODAY, Friday 27 November 2026.
- **Numbers strip** — Tokyo core CPI +2.9%, fastest in 16 months;
  430+ CV90 vehicles in the five-nation deal; 561 billion euros,
  the German 2027 budget; 64,141 UK vehicles built in October;
  40,000 school workers expected in Seoul; 65-65, the New
  Zealand Parliament deadlocked after the final count.
- **The leads** — Tokyo inflation jumps to 2.9%; five nations sign
  a 7.5 billion euro CV90 deal in Stockholm; the New Zealand
  election ends in deadlock.
- **World map** — a schematic map with the places in the day's news
  marked: London, Berlin, Warsaw, Stockholm, Johannesburg,
  New Delhi, Lusail, Beijing, Seoul, Tokyo and Wellington.
- **The day in brief** — 16 stories, from the Bundestag budget
  vote and the Poland-Palantir signing to the Finland border
  law, the North Korean border crossings and the UK car
  production figures.
- **Also on Friday** — 13 more stories, including Black Friday,
  the Qatar Grand Prix practice, the Johannesburg mayoral
  election and the China fuel price cut.
- **Date check footer** — the Tokyo CPI data was released at
  23:42 UTC on 26 November (Friday morning in Tokyo); the
  New Zealand results came out at 2pm NZDT; the China fuel
  cut was announced on 26 November and took effect from
  00:00 on 27 November; the "White Blast" figures are for
  Thursday 26 November, reported Friday; the CV90, Palantir
  and Bundestag items are scheduled events on 27 November,
  announced on 26 November.

## How it is made

`main.py` is a single self-contained Python 3.13 program using only
the standard library. It draws everything itself — its own 5x7
bitmap font, its own canvas and shapes, and its own PNG encoder —
and writes a 1024x1024 PNG. It uses no network, no clock and no
randomness, so every run writes the same bytes.

## Run it

```sh
python3 main.py /output/entry.png
```

Run it twice and compare: the two files are byte-identical.

## Sources

All 32 stories happened, or were first reported, on Friday
27 November 2026. See [SOURCES.md](SOURCES.md) for the
story-by-story list with source URLs and dates. Research ran in
the early hours of 27 November in UTC, so items scheduled later
in the day (votes, signings, matches) are framed as scheduled
events; the New Zealand final count, released at 2pm NZDT
(01:00 UTC), is reported as a result.

## Licence

MIT — see [LICENSE](LICENSE).
