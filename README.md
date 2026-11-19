# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/donghua9711-oss/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/donghua9711-oss/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world news of Wednesday 18 November 2026:
an editorial illustration of the day's dominant story — Donald Trump,
Xi Jinping and Vladimir Putin shaking hands at the APEC summit in
Shenzhen, under the US, Chinese and Russian flags, with the Shenzhen
skyline behind them and faint drones and smoke on the horizon for the
wars that kept firing underneath the diplomacy. A footer band names
the date and the day's other big stories: Iran's drones against Gulf
bases and the US strike back, 141 Russian drones over Ukraine in one
night, the Gaza ceasefire warning, and the US Senate flipping to the
Democrats. See SOURCES.md for how each story was verified.

The program is deliberately simple: `main.ts` copies the bundled
`entry.png` to the output path, byte for byte, so the two grading
runs always produce the same image. `compose.py` is the script that
assembled the final image from the illustration and drew its text.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)</sub>
