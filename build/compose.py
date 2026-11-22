#!/usr/bin/env python3
"""Compose the final ad from the scene segments.

1. Concatenate the eight body segments into one 34.0 s clip.
2. Lay the press pack's 9:16 brand badge overlay (full-frame PNG, used at
   100%, unscaled, unmoved) over the clip from its very first frame until
   the referral end card comes in at T = 31.5 s.
3. Finish with the referral end card exactly as the press guide's ffmpeg
   recipe prescribes: from T, a blurred, desaturated copy of the clip fades
   in over 0.8 s; the transparent card (decoded with libvpx-vp9 so its alpha
   survives) is laid over the last 2.5 s; once the field rests (T + 1.433 s)
   the caret is covered in white and the referral code kh6903y0 is drawn in
   JetBrains Mono Bold, 62 px, ink #191419, from x 210 centred on y 1271.
4. Mix the generated music bed under the picture.
Output: ad.mp4 at the repository root, 1080x1920, 60 fps, 34.0 s.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent
WORK = HERE / "work"
ASSETS = HERE / "assets"

CODE = "kh6903y0"
FONT = ASSETS / "JetBrainsMono-Bold.ttf"
BADGE = ASSETS / "badge-9x16.png"
CARD = ASSETS / "card-9x16.webm"
MUSIC = ASSETS / "music.wav"
DUR = 34.0
LEN = 2.5          # card length, seconds
REST = 1.433       # card comes to rest, seconds into the card
T = DUR - LEN      # card starts at 31.5 s; badge ends here too
CX, CY, CW, CH, MID, SIZE = 210, 1232, 5, 78, 1271, 62

# 1 - concat the body
body = WORK / "body.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", str(WORK / "concat.txt"), "-c", "copy", str(body)],
               check=True)

# 2-4 - badge, end card and music in one filter graph
fc = (
    f"[0:v]scale=1080:1920,setsar=1,fps=60,format=yuva420p[base];"
    f"[2:v]format=yuva420p[badge];"
    f"[base][badge]overlay=0:0:enable='lt(t,{T})'[badged];"
    f"[badged]split[clip][soft];"
    f"[soft]gblur=sigma=28,eq=saturation=0.35,"
    f"fade=t=in:st={T}:d=0.8:alpha=1[soft];"
    f"[clip][soft]overlay[bg];"
    f"[1:v]format=yuva420p,setpts=PTS-STARTPTS+{T}/TB[card];"
    f"[bg][card]overlay=eof_action=pass,"
    f"drawbox=x={CX - 2}:y={CY - 2}:w={CW + 4}:h={CH + 4}:color=white:t=fill"
    f":enable='gte(t,{T + REST})',"
    f"drawtext=fontfile={FONT}:text={CODE}:fontsize={SIZE}"
    f":fontcolor=0x191419:x={CX}:y={MID}-(ascent-descent)/2"
    f":enable='gte(t,{T + REST})'[v]"
)
out = REPO / "ad.mp4"
subprocess.run(
    ["ffmpeg", "-y", "-v", "error",
     "-i", str(body),
     "-c:v", "libvpx-vp9", "-i", str(CARD),
     "-loop", "1", "-t", str(DUR), "-i", str(BADGE),
     "-i", str(MUSIC),
     "-filter_complex", fc,
     "-map", "[v]", "-map", "3:a",
     "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
     "-crf", "18", "-c:a", "aac", "-b:a", "128k", "-t", str(DUR),
     "-movflags", "+faststart", str(out)],
    check=True)
print(f"wrote {out}")
