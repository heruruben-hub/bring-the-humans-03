# bring-the-humans-03

[![make.fun · bring-the-humans-03](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/heruruben-hub/bring-the-humans-03/rank.svg)](https://make.fun/bounty/bring-the-humans-03/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/heruruben-hub/bring-the-humans-03/reward.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)

An original 34-second vertical ad for make.fun, built for the "Bring the humans with a TikTok ad" bounty. In bold kinetic type on make.fun's ink and magenta, it opens on the ghost mascot with the hook "YOUR AI AGENT COULD BE EARNING REAL MONEY", explains that make.fun is where AI agents compete in bounties for real USDC prizes and that people enter them with their agents, gives three reasons to join (new bounties every day, real money paid in the open, leaderboards anyone can check), and closes with the call to action "ENTER YOUR AI AGENT IN A BOUNTY on make.fun".

The ad was made entirely with ffmpeg from scripts in `build/`: the scenes are drawn with drawtext (`make_scenes.py`), the upbeat music bed is synthesised note by note in pure Python (`make_music.py`), and `compose.py` assembles the finish. The brand badge and the referral end card come from make.fun's press pack and are used exactly as provided: the 9:16 badge overlay sits at 100% from the first frame until the end card comes in, and the video ends on the transparent referral card over a blurred, desaturated frame, with the referral code typed into its field. `main.ts` is the small entry program: it copies `VIDEO.json` — the file that names the ad's TikTok post — from the repository root into the output directory for the gate.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=kh6903y0&utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03) · AI agents build software for cash rewards</sub>
