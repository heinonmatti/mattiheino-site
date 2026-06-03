// Fail the build if any post carries an https:// mattiheino.com ?p= guid.
//
// WordPress's live RSS feed serves these guids over http://. RSS readers dedupe
// on the exact <guid> string, so shipping an https:// guid would make the post
// look new at the DNS cutover and re-broadcast the archive to subscribers. The
// importer (migration/lib/guid.py) normalises these to http://; this guard
// catches any that slip through a future re-import.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const dirs = ["src/content/posts", "src/content/applied-musings"];
const bad = /^wp_guid:\s*"https:\/\/mattiheino\.com\/\?p=\d+"/m;

const offenders = [];
for (const dir of dirs) {
  let files;
  try {
    files = readdirSync(dir).filter((f) => f.endsWith(".md"));
  } catch {
    continue; // directory may not exist yet
  }
  for (const f of files) {
    const fm = readFileSync(join(dir, f), "utf8").split("---")[1] ?? "";
    if (bad.test(fm)) offenders.push(join(dir, f));
  }
}

if (offenders.length) {
  console.error(
    `RSS guid check FAILED: ${offenders.length} post(s) use an https:// mattiheino.com ?p= guid.\n` +
      `WordPress serves these over http://; shipping https:// would re-broadcast the archive to subscribers.\n` +
      `Fix: re-run the importer (it normalises via migration/lib/guid.py) or change the scheme to http:// by hand.\n` +
      offenders.map((o) => `  - ${o}`).join("\n"),
  );
  process.exit(1);
}
console.log("RSS guid check: OK (no https:// mattiheino.com ?p= guids).");
