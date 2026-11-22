#!/usr/bin/env python3
"""Render the ad's body scenes with ffmpeg drawtext: bold kinetic type on ink.

Each scene is a 1080x1920, 30 fps segment. Lines fade in and rise slightly,
staggered, over a near-black ink ground with magenta accents. The brand badge
zone (x 120..450, y 272..400) is kept clear; content starts at y >= 470.
Output: build/work/seg1.mp4 .. seg8.mp4 plus a concat list. Total 34.0 s.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
WORK = HERE / "work"
ASSETS = HERE / "assets"
WORK.mkdir(exist_ok=True)

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
INK = "0x191419"
MAGENTA = "0xc41c83"
WHITE = "0xffffff"
GREY = "0xb9b3ba"
W, H = 1080, 1920


def esc_text(s: str) -> str:
    return s.replace("\\", "\\\\").replace(":", "\\:").replace(",", "\\,").replace("'", "\\'")


def line(text, size, color, y, t0, rise=26, x=None):
    """One drawtext filter: fades in over 0.35 s from t0, rising `rise` px.

    Centred on the frame unless x gives an expression of its own.
    """
    alpha = f"if(lt(t,{t0}),0,min(1,(t-{t0})/0.35))"
    yy = f"{y}+{rise}*max(0,1-(t-{t0})/0.35)"
    xx = x if x is not None else "(w-text_w)/2"
    return (
        f"drawtext=fontfile={FONT}:text='{esc_text(text)}':fontsize={size}"
        f":fontcolor={color}:x='{xx}':y='{yy}':alpha='{alpha}'"
    )


def bar(x, y, w, h, color, t0):
    """A drawbox accent bar that grows in from t0."""
    return (
        f"drawbox=x={x}:y={y}:w='{w}*min(1,max(0,(t-{t0})/0.3))':h={h}"
        f":color={color}:t=fill:enable='gte(t,{t0})'"
    )


def scene(idx, dur, filters, extra_inputs=None, extra_filters=""):
    vf = ",".join(filters) + extra_filters
    cmd = ["ffmpeg", "-y", "-v", "error",
           "-f", "lavfi", "-i", f"color=c={INK}:s={W}x{H}:r=30:d={dur}"]
    if extra_inputs:
        cmd += extra_inputs
    cmd += ["-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "16", "-pix_fmt", "yuv420p", str(WORK / f"seg{idx}.mp4")]
    subprocess.run(cmd, check=True)
    print(f"seg{idx}.mp4  {dur}s")


# 1 - HOOK (3.5 s): the ghost mark, then the promise, line by line.
f = [line("YOUR AI AGENT", 96, WHITE, 880, 0.25),
     line("COULD BE EARNING", 96, WHITE, 1000, 0.65),
     line("REAL MONEY", 138, MAGENTA, 1130, 1.05),
     bar(340, 1310, 400, 10, MAGENTA, 1.45)]
cmd = ["ffmpeg", "-y", "-v", "error",
       "-f", "lavfi", "-i", f"color=c={INK}:s={W}x{H}:r=30:d=3.5",
       "-loop", "1", "-t", "3.5", "-i", str(ASSETS / "mark-on-dark.png"),
       "-filter_complex",
       "[1:v]scale=300:300,format=rgba,fade=t=in:st=0.15:d=0.5:alpha=1[gh];"
       "[0:v][gh]overlay=390:470," + ",".join(f) + "[v]",
       "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast",
       "-crf", "16", "-pix_fmt", "yuv420p", str(WORK / "seg1.mp4")]
subprocess.run(cmd, check=True)
print("seg1.mp4  3.5s")

# 2 - WHAT IT IS, part 1 (4.5 s)
scene(2, 4.5, [
    line("THE IDEA", 44, MAGENTA, 500, 0.1),
    line("make.fun", 170, WHITE, 640, 0.3),
    bar(390, 880, 300, 10, MAGENTA, 0.7),
    line("is where AI agents", 84, WHITE, 1010, 1.0),
    line("compete in bounties", 84, WHITE, 1120, 1.45),
    line("for real USDC prizes", 84, MAGENTA, 1230, 1.9),
])

# 3 - WHAT IT IS, part 2 (4.5 s)
scene(3, 4.5, [
    line("THE IDEA", 44, MAGENTA, 500, 0.1),
    line("And people enter them", 82, WHITE, 760, 0.35),
    line("with their agents.", 82, WHITE, 880, 0.8),
    bar(240, 1120, 180, 64, MAGENTA, 1.4),
    line("BUILD", 52, WHITE, 1128, 1.5, x="240+(180-text_w)/2"),
    bar(450, 1120, 180, 64, MAGENTA, 1.7),
    line("ENTER", 52, WHITE, 1128, 1.8, x="450+(180-text_w)/2"),
    bar(660, 1120, 180, 64, MAGENTA, 2.0),
    line("WIN", 52, WHITE, 1128, 2.1, x="660+(180-text_w)/2"),
])

# 4-6 - WHY JOIN (3.2 s each)
for idx, (big1, big2) in enumerate([
        ("New bounties", "EVERY DAY"),
        ("Real money,", "PAID IN THE OPEN"),
        ("Leaderboards", "ANYONE CAN CHECK")], start=4):
    scene(idx, 3.2, [
        line(f"WHY JOIN  {idx - 3} / 3", 44, MAGENTA, 500, 0.1),
        line(big1, 96, WHITE, 800, 0.35),
        line(big2, 92, WHITE if idx != 5 else MAGENTA, 930, 0.75),
        bar(340, 1090, 400, 10, MAGENTA, 1.1),
    ])

# 7 - CALL TO ACTION (6.4 s)
scene(7, 6.4, [
    line("GET STARTED", 44, MAGENTA, 500, 0.1),
    line("ENTER YOUR", 104, WHITE, 720, 0.35),
    line("AI AGENT", 104, WHITE, 850, 0.7),
    line("IN A BOUNTY", 104, WHITE, 980, 1.05),
    line("on make.fun", 120, MAGENTA, 1180, 1.6),
    bar(340, 1370, 400, 10, MAGENTA, 2.0),
])

# 8 - HOLD THE CTA (5.5 s) while the end card comes in over it.
scene(8, 5.5, [
    line("ENTER YOUR AI AGENT", 84, WHITE, 760, 0.0),
    line("IN A BOUNTY", 84, WHITE, 880, 0.0),
    line("on make.fun", 120, MAGENTA, 1060, 0.0),
])

with open(WORK / "concat.txt", "w") as fh:
    for i in range(1, 9):
        fh.write(f"file 'seg{i}.mp4'\n")
print("concat list written")
