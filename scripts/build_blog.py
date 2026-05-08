#!/usr/bin/env python3
"""
Build blog: converts blog/posts/*.md → HTML and regenerates blog/index.html.
Run from repo root: python scripts/build_blog.py
"""

import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import markdown
    import yaml
except ImportError:
    print("Missing deps. Run: pip install markdown pyyaml")
    sys.exit(1)

POSTS_DIR = Path("blog/posts")
BLOG_INDEX = Path("blog/index.html")

POST_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Sarath</title>
    <link rel="stylesheet" href="../../assets/css/style.css">
    <style>
        .post-content {{
            max-width: 800px;
            margin: 0 auto;
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        .post-header {{
            margin-bottom: 3rem;
            text-align: center;
        }}
        .post-title {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .post-content h2 {{
            font-size: 1.8rem;
            margin: 2rem 0 1rem;
            text-align: left;
        }}
        .post-content h3 {{
            font-size: 1.4rem;
            margin: 1.5rem 0 0.75rem;
        }}
        .post-content p {{
            margin-bottom: 1.5rem;
        }}
        .post-content code {{
            background: var(--bg-light);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9em;
            font-weight: 500;
        }}
        .post-content pre {{
            background: var(--bg-light);
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        .post-content pre code {{
            background: none;
            padding: 0;
        }}
        .back-link {{
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <nav class="pill-nav">
        <ul>
            <li><a href="../../index.html#home">Home</a></li>
            <li><a href="../index.html">Blog</a></li>
            <li><a href="../../research/publications.html">Research</a></li>
            <li><a href="../../work/experience.html">Experience</a></li>
        </ul>
    </nav>

    <section class="section">
        <div class="container">
            <div class="post-content">
                <div class="back-link">
                    <a href="../index.html">← Back to Blog</a>
                </div>

                <div class="post-header">
                    <div class="post-meta">{date_str}</div>
                    <h1 class="post-title">{title}</h1>
                </div>

                {body_html}

                <div class="back-link" style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border);">
                    <a href="../index.html">← Back to Blog</a>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Sarath. Built with care, deployed on GitHub Pages.</p>
        </div>
    </footer>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - Sarath</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <nav class="pill-nav">
        <ul>
            <li><a href="../index.html#home">Home</a></li>
            <li><a href="index.html">Blog</a></li>
            <li><a href="../research/publications.html">Research</a></li>
            <li><a href="../work/experience.html">Experience</a></li>
        </ul>
    </nav>

    <section class="section">
        <div class="container">
            <h2>Technical Blog</h2>
            <p style="text-align: center; color: var(--text-light); max-width: 700px; margin: 0 auto 3rem;">
                Writing about MLOps, Kubernetes, distributed systems, and ML infrastructure.
            </p>

            <div class="posts-list">
{post_entries}
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Sarath. Built with care, deployed on GitHub Pages.</p>
        </div>
    </footer>
</body>
</html>
"""

POST_ENTRY_TEMPLATE = """\
                <article class="post-preview">
                    <div class="post-meta">{date_str}</div>
                    <h3><a href="posts/{slug}.html">{title}</a></h3>
                    <p>
                        {description}
                    </p>
                </article>"""


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    fm = yaml.safe_load(content[3:end]) or {}
    body = content[end + 3:].lstrip("\n")
    return fm, body


def infer_title(body: str, slug: str) -> tuple[str, str]:
    """Return (title, body_with_h1_stripped). Strips leading H1 if used as title."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            remaining = "\n".join(lines[i + 1:]).lstrip("\n")
            return title, remaining
    return slug.replace("-", " ").title(), body


def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()


def infer_description(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("```") and not line.startswith("*") and not line.startswith("-") and not line.startswith("|"):
            return strip_markdown(line)[:200]
    return ""


def format_date(date_obj) -> str:
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
    return f"{date_obj.strftime('%B')} {date_obj.day}, {date_obj.year}"


def main():
    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    posts = []

    for md_file in sorted(POSTS_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)

        slug = md_file.stem
        if fm.get("title"):
            title = fm["title"]
        else:
            title, body = infer_title(body, slug)
        description = fm.get("description") or infer_description(body)

        raw_date = fm.get("date")
        if raw_date:
            if isinstance(raw_date, str):
                date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
            else:
                date_obj = datetime(raw_date.year, raw_date.month, raw_date.day)
        else:
            date_obj = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        date_str = format_date(date_obj)

        md.reset()
        body_html = md.convert(body)

        out_file = POSTS_DIR / f"{slug}.html"
        out_file.write_text(
            POST_TEMPLATE.format(title=title, date_str=date_str, body_html=body_html),
            encoding="utf-8",
        )
        print(f"  wrote {out_file}")

        posts.append(
            {
                "slug": slug,
                "title": title,
                "date": date_obj,
                "date_str": date_str,
                "description": description,
            }
        )

    posts.sort(key=lambda p: p["date"], reverse=True)

    post_entries = "\n\n".join(POST_ENTRY_TEMPLATE.format(**p) for p in posts)
    BLOG_INDEX.write_text(
        INDEX_TEMPLATE.format(post_entries=post_entries), encoding="utf-8"
    )
    print(f"  wrote {BLOG_INDEX} ({len(posts)} post(s))")


if __name__ == "__main__":
    main()
