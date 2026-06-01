// Print one-line MSM publish-state summary at every build.
// Does not fail the build.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const dir = "src/content/applied-musings";
const files = readdirSync(dir).filter((f) => f.endsWith(".md"));

let total = 0;
let live = 0;
const liveSlugs = [];

for (const f of files) {
  const body = readFileSync(join(dir, f), "utf8");
  const fm = body.split("---")[1] ?? "";
  if (!fm.includes("migration_source: motivationselfmanagement")) continue;
  total++;
  const draft = /^draft:\s*(true|false)/m.exec(fm)?.[1] ?? "true";
  if (draft === "false") {
    live++;
    liveSlugs.push(f.replace(/\.md$/, ""));
  }
}

console.log(`MSM recovered: ${total}. Currently drafts: ${total - live}. Live: ${live}.`);
if (liveSlugs.length) {
  console.log("  Live MSM slugs:");
  for (const s of liveSlugs) console.log(`    - ${s}`);
}
