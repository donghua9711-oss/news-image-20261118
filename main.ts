// Entry program for make.fun news-image-20261118 (Node 22, standard
// library only, no network, no dependencies).
//
// The entry image lives beside this file as entry.png. The grader runs
// this program twice in a fresh container; each run copies the same
// source bytes to the output file, so both runs produce a
// byte-identical /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const source = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// A copy that silently lost bytes would fail the image gate, so verify
// the written file is exactly as large as the source before exiting.
const written = statSync(target).size;
const original = statSync(source).size;
if (written !== original) {
  throw new Error(`copy incomplete: wrote ${written} of ${original} bytes`);
}

// The gate tells PNG from JPEG by the first bytes and refuses anything
// else, so check the signature of what was written: a PNG starts with
// 89 50 4E 47, a JPEG with FF D8 FF. Anything else means the embedded
// file is corrupt and the run should fail loudly, not ship it.
const head = readFileSync(target).subarray(0, 4);
const isPng = head[0] === 0x89 && head[1] === 0x50 && head[2] === 0x4e && head[3] === 0x47;
const isJpeg = head[0] === 0xff && head[1] === 0xd8 && head[2] === 0xff;
if (!isPng && !isJpeg) {
  throw new Error("copied file is neither PNG nor JPEG");
}
