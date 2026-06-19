#!/usr/bin/env python3
"""Render all NorthStar markdown docs into ONE long self-contained HTML page.

Usage: python3 build_onepage.py
Outputs ./site/northstar-plan.html
"""
import re
from pathlib import Path

import markdown

HERE = Path(__file__).parent
OUT = HERE / "site"
OUT.mkdir(exist_ok=True)

# (filename stem, section id, short menu label)
PAGES = [
    ("00-overview", "overview", "Overview"),
    ("01-product-strategy", "strategy", "1 · Strategy"),
    ("02-architecture-and-design", "architecture", "2 · Architecture"),
    ("03-agent-system", "agents", "3 · Agents"),
    ("04-tech-stack", "techstack", "4 · Tech Stack"),
    ("05-sprint-plan", "sprints", "5 · Sprints"),
    ("06-gtm-deployment-playbook", "gtm", "6 · GTM"),
]

CSS = """
:root{--bg:#faf9f6;--fg:#1f2328;--muted:#646a73;--accent:#b5512f;--line:#e3e0d8;--code:#f3f1ea;--bar:#f4f1ea}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
header.topbar{position:sticky;top:0;z-index:20;background:var(--bar);border-bottom:1px solid var(--line);padding:10px 20px;display:flex;flex-wrap:wrap;align-items:center;gap:6px}
header.topbar .brand{font-weight:700;margin-right:14px;font-size:15px;white-space:nowrap}
header.topbar a{color:var(--fg);text-decoration:none;font-size:13.5px;padding:6px 11px;border-radius:7px;white-space:nowrap}
header.topbar a:hover{background:#eae6db}
main{max-width:940px;margin:0 auto;padding:16px 32px 80px}
section.doc{padding-top:26px;border-top:1px dashed var(--line);margin-top:34px}
section.doc:first-of-type{border-top:0;margin-top:8px}
article{overflow-wrap:break-word}
h1,h2,h3,h4{line-height:1.25;font-weight:680}
h1{font-size:30px;margin:.3em 0 .6em;border-bottom:2px solid var(--line);padding-bottom:.3em}
h2{font-size:22px;margin:1.7em 0 .5em}
h3{font-size:17px;margin:1.4em 0 .4em}
a{color:var(--accent)}
p,li{color:#2a2e33}
blockquote{margin:1.2em 0;padding:.6em 1.1em;border-left:4px solid var(--accent);background:#fff;color:#3a3f45;border-radius:0 7px 7px 0}
code{background:var(--code);padding:.15em .4em;border-radius:5px;font-size:.88em;font-family:"SF Mono",Menlo,Consolas,monospace}
pre{background:var(--code);padding:16px 18px;border-radius:9px;overflow-x:auto;border:1px solid var(--line);font-size:13px;line-height:1.5}
pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:14px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
th{background:var(--bar);font-weight:650}
tr:nth-child(even) td{background:#fcfbf8}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.totop{display:inline-block;margin-top:10px;font-size:13px;color:var(--muted);text-decoration:none}
.footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media(max-width:860px){main{padding:14px 18px 60px}}
"""

# map "<stem>.md[#anchor]" -> "#<section-id>"  (so cross-doc links jump within the page)
STEM_TO_ID = {stem: sid for stem, sid, _ in PAGES}

def rewrite_links(html):
    def repl(m):
        stem = m.group(1).lstrip("./")
        sid = STEM_TO_ID.get(stem)
        return f'href="#{sid}"' if sid else m.group(0)
    return re.sub(r'href="([\w./-]+?)\.md(?:#[^"]*)?"', repl, html)

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])

menu = '<header class="topbar"><span class="brand">NorthStar</span>' + "".join(
    f'<a href="#{sid}">{label}</a>' for _, sid, label in PAGES
) + "</header>"

sections = []
for stem, sid, _ in PAGES:
    md.reset()
    body = rewrite_links(md.convert((HERE / f"{stem}.md").read_text(encoding="utf-8")))
    sections.append(
        f'<section class="doc" id="{sid}"><article>{body}'
        f'<a class="totop" href="#top">↑ back to top</a></article></section>'
    )

doc = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NorthStar — Agentic Pricing Intelligence (full plan)</title><style>{CSS}</style></head>
<body id="top">{menu}<main>{''.join(sections)}
<div class="footer">NorthStar — Agentic Pricing Intelligence. Single-page build of the plan in <code>docs/northstar/</code>.</div>
</main></body></html>"""

(OUT / "northstar-plan.html").write_text(doc, encoding="utf-8")
print(f"Built single-page site: {OUT / 'northstar-plan.html'}")
