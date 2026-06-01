"""One-off: test how markdownify handles wpautop-style HTML."""
from markdownify import markdownify as _md

sample = (
    "<em>English summary: foo</em>\n\n"
    "<h1>Heading</h1>\n\n"
    "Paragraph one. Has <a href='x'>a link</a>.\n\n"
    "Paragraph two.\n\n"
    "<blockquote>Block quote para.</blockquote>\n\n"
    "Paragraph three.\n\n"
    "Paragraph four."
)
print("=== markdownify direct ===")
print(_md(sample, heading_style="ATX"))
print("=== with explicit <p> wrapping ===")
# Simulate wpautop: wrap non-block-level chunks in <p>
import re
BLOCK_TAGS_RE = re.compile(
    r"^<(?:h[1-6]|p|div|blockquote|ul|ol|li|pre|table|hr|figure|img)[\s>/]",
    re.IGNORECASE,
)


def wpautop(html: str) -> str:
    chunks = re.split(r"\n\n+", html.strip())
    out = []
    for c in chunks:
        c = c.strip()
        if not c:
            continue
        if BLOCK_TAGS_RE.match(c):
            out.append(c)
        else:
            out.append(f"<p>{c}</p>")
    return "\n\n".join(out)


wrapped = wpautop(sample)
print(wrapped)
print()
print("=== markdownify on wrapped ===")
print(_md(wrapped, heading_style="ATX"))
