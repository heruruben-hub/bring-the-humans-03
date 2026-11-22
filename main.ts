// bring-the-humans-03 entry program (Node 22, standard library only).
//
// The entry itself is the video: an original short vertical ad for make.fun
// (ad.mp4 in this repository), posted publicly on TikTok. This program's one
// job is to hand the graders the pointer to that video: it copies VIDEO.json
// from the repository root into the output directory, where the gate reads
// it. Nothing about the video is scored from this file; the house reads the
// video's views from TikTok itself.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, "VIDEO.json"), join(OUTPUT_DIR, "VIDEO.json"));
  console.log(`VIDEO.json copied from ${BOT_DIR} to ${OUTPUT_DIR}`);
} catch (err) {
  console.error(`VIDEO.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
