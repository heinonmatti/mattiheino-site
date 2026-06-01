"""Find places where wpautop left inline text glued to a block element.

The pattern: a chunk like '<ol>...</ol>\nLone trailing paragraph'.
wpautop didn't wrap the trailing text in <p> because the chunk started
with a block tag. After markdownify, the trailing paragraph is now
indistinguishable from a list continuation, breaking the layout.
"""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\qn353\Documents\git-projects\mattiheino-site\src\content\posts")

# Heuristic: in the rendered markdown, look for a line that's part of
# a list (starts with `- ` or `\d+. ` or is indented with spaces) followed
# immediately by a non-blank, non-list line that starts at column 0.
# This signals lazy list continuation that should have been a paragraph break.

LIST_LINE = re.compile(r"^(?:\s*[-*]|\s*\d+\.|\s{2,})")  # list item or indented continuation
PARA_LINE = re.compile(r"^\S")

hits = []
for md in sorted(ROOT.glob("*.md")):
    text = md.read_text(encoding="utf-8")
    # Strip YAML
    m = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
    body = text[m.end():] if m else text
    lines = body.splitlines()
    for i in range(len(lines) - 1):
        if LIST_LINE.match(lines[i]) and not LIST_LINE.match(lines[i + 1]):
            # next line is not a list line. Is it a non-blank paragraph?
            nxt = lines[i + 1]
            if nxt and PARA_LINE.match(nxt) and not nxt.startswith("#"):
                # plausible glue. Skip if the previous line was a list closer (e.g. ended a list block at EOF)
                hits.append((md.name, i + 1, nxt[:80]))

print(f"Suspicious glue spots: {len(hits)}")
print()
# Show first 20
for name, line_no, snippet in hits[:30]:
    print(f"  {name}:{line_no}  -- {snippet!r}")
