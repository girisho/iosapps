#!/usr/bin/env python3
"""Render the NorthStar markdown docs into a small static HTML site.

Usage: python3 build_site.py
Outputs HTML into ./site/ next to this script.
"""
import re
from pathlib import Path

import markdown

HERE = Path(__file__).parent
OUT = HERE / "site"
OUT.mkdir(exist_ok=True)

# Ordered nav: (filename stem, sidebar label)
PAGES = [
    ("00-overview", "Overview"),
    ("01-product-strategy", "1 · Product Strategy"),
    ("02-architecture-and-design", "2 · Architecture & Design"),
    ("03-agent-system", "3 · Agent System"),
    ("04-tech-stack", "4 · Tech Stack"),
    ("05-sprint-plan", "5 · Sprint Plan"),
    ("06-gtm-deployment-playbook", "6 · GTM & Deployment"),
]

CSS = """
:root{--bg:#faf9f6;--fg:#1f2328;--muted:#646a73;--accent:#b5512f;--line:#e3e0d8;--code:#f3f1ea;--sidebar:#f4f1ea}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
.wrap{display:flex;min-height:100vh}
nav{width:280px;flex:0 0 280px;background:var(--sidebar);border-right:1px solid var(--line);padding:28px 22px;position:sticky;top:0;height:100vh;overflow-y:auto}
nav h1{font-size:18px;margin:0 0 4px;letter-spacing:.3px}
nav .tag{color:var(--muted);font-size:12.5px;margin-bottom:22px;display:block}
nav a{display:block;padding:8px 12px;margin:2px 0;border-radius:7px;color:var(--fg);text-decoration:none;font-size:14.5px}
nav a:hover{background:#eae6db}
nav a.active{background:var(--accent);color:#fff;font-weight:600}
main{flex:1;min-width:0;padding:48px 56px;max-width:980px}
article{overflow-wrap:break-word}
h1,h2,h3,h4{line-height:1.25;font-weight:680}
h1{font-size:30px;margin:.2em 0 .6em;border-bottom:2px solid var(--line);padding-bottom:.3em}
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
th{background:var(--sidebar);font-weight:650}
tr:nth-child(even) td{background:#fcfbf8}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media(max-width:860px){.wrap{flex-direction:column}nav{width:100%;height:auto;position:static;flex-basis:auto}main{padding:28px 20px}}
"""

def nav_html(active_stem):
    links = []
    for stem, label in PAGES:
        cls = ' class="active"' if stem == active_stem else ""
        links.append(f'<a href="{stem}.html"{cls}>{label}</a>')
    return (
        '<nav><h1>NorthStar</h1>'
        '<span class="tag">Agentic Pricing Intelligence · product plan</span>'
        + "".join(links)
        + "</nav>"
    )

PAGE = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · NorthStar</title><style>{css}</style></head>
<body><div class="wrap">{nav}<main><article>{body}
<div class="footer">NorthStar — Agentic Pricing Intelligence. Generated from the markdown source in <code>docs/northstar/</code>.</div>
</article></main></div></body></html>"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"])

def render(stem, label):
    src = (HERE / f"{stem}.md").read_text(encoding="utf-8")
    md.reset()
    html = md.convert(src)
    # rewrite internal links: foo.md / foo.md#anchor -> foo.html
    html = re.sub(r'href="([\w./-]+?)\.md(#[^"]*)?"', r'href="\1.html\2"', html)
    title = re.sub(r"^\d+\s*·\s*", "", label)
    (OUT / f"{stem}.html").write_text(
        PAGE.format(title=title, css=CSS, nav=nav_html(stem), body=html), encoding="utf-8"
    )

for stem, label in PAGES:
    render(stem, label)

# index.html mirrors the overview page
(OUT / "index.html").write_text(
    (OUT / "00-overview.html").read_text(encoding="utf-8"), encoding="utf-8"
)

print(f"Built {len(PAGES)} pages + index.html into {OUT}")
