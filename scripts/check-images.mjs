// Guard the images in native posts at every build. Legacy imports
// (migration_source other than native) are exempt so the 41 old
// empty-alt WordPress posts do not drown the signal.
//   error (stops the build): empty alt text, or a ./-relative image
//     reference whose file does not exist.
//   warning (printed only): image file over 1 MB, or an images/<folder>/
//     name that does not match the post slug.
import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOTS = ["src/content/posts", "src/content/applied-musings"];
const MAX_BYTES = 1024 * 1024;

let errors = 0;
let warnings = 0;

for (const dir of ROOTS) {
  const files = readdirSync(dir).filter((f) => f.endsWith(".md"));
  for (const f of files) {
    const raw = readFileSync(join(dir, f), "utf8");
    const fm = raw.split("---")[1] ?? "";
    const source = /^migration_source:\s*(\S+)/m.exec(fm)?.[1] ?? "native";
    if (source !== "native") continue;

    const slug = f.replace(/^\d{4}-\d{2}-\d{2}-/, "").replace(/\.md$/, "");

    for (const [, alt, ref] of raw.matchAll(/!\[([^\]]*)\]\(\s*(\.\/[^)\s]+)\s*\)/g)) {
      if (!alt.trim()) {
        console.error(`ERROR ${dir}/${f}: ${ref} has empty alt text - describe the picture.`);
        errors++;
      }
      const rel = ref.replace(/^\.\//, "");
      const target = join(dir, rel);
      if (!existsSync(target)) {
        console.error(`ERROR ${dir}/${f}: ${ref} does not exist on disk.`);
        errors++;
        continue;
      }
      const bytes = statSync(target).size;
      if (bytes > MAX_BYTES) {
        const mb = (bytes / MAX_BYTES).toFixed(1).replace(".", ",");
        console.warn(`warn  ${dir}/${f}: ${ref} is ${mb} MB - shrink to ~1600 px wide before publishing.`);
        warnings++;
      }
      const folder = /^images\/([^/]+)\//.exec(rel)?.[1];
      if (folder && folder !== slug) {
        console.warn(`warn  ${dir}/${f}: images sit in images/${folder}/ but the slug is "${slug}" - rename the folder to match.`);
        warnings++;
      }
    }
  }
}

if (errors) {
  console.error(`check-images: ${errors} error(s), ${warnings} warning(s). Build stopped.`);
  process.exit(1);
}
console.log(`check-images: native posts OK (${warnings} warning(s)).`);
