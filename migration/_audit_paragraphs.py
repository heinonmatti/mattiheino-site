"""One-off: count paragraph breaks (blank lines) per imported post.

Flags posts likely to still be broken — i.e., long body but very few
blank-line separators. These are candidates where wpautop didn't fire
because the WP XML body used some other separator (single \\n, <br>, etc.).
"""
from pathlib import Path
import re

ROOT = Path(r"C:\Users\qn353\Documents\git-projects\mattiheino-site\src\content\posts")

def body_of(text: str) -> str:
    # Strip YAML frontmatter
    if text.startswith("---"):
        m = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
        if m:
            return text[m.end():]
    return text

rows = []
for md in sorted(ROOT.glob("*.md")):
    text = md.read_text(encoding="utf-8")
    body = body_of(text)
    chars = len(body)
    if chars < 200:
        continue  # short stubs are uninteresting
    blanks = body.count("\n\n")
    # rough heuristic: "one paragraph per ~300 chars" is normal prose; if we
    # see < 1 blank per 500 chars, the post is probably collapsed.
    expected = chars // 500
    rows.append((blanks, expected, chars, md.name))

# Sort by lowest blank-count relative to expected
rows.sort(key=lambda r: r[0])

print(f"{'blanks':>7} {'expected':>9} {'chars':>6}  filename")
print("-" * 80)
for blanks, expected, chars, name in rows[:25]:
    flag = "  <-- suspicious" if blanks < max(2, expected // 2) else ""
    print(f"{blanks:>7} {expected:>9} {chars:>6}  {name}{flag}")

print()
print(f"Total posts (>200 chars body): {len(rows)}")
print(f"Posts with 0 blank lines: {sum(1 for r in rows if r[0] == 0)}")
print(f"Posts with 1-2 blank lines: {sum(1 for r in rows if 1 <= r[0] <= 2)}")
print(f"Posts where blanks < expected/2: {sum(1 for r in rows if r[0] < max(2, r[1] // 2))}")
