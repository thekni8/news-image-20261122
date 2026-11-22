// news-image-20261122 entry program.
// Copies the finished front-page image (entry.png, next to this script)
// into the output directory chosen by MAKEFUN_OUTPUT_DIR, or /output.
// No network, no randomness: the same input always yields the same output.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), destination);
console.log(`Wrote ${destination}`);
