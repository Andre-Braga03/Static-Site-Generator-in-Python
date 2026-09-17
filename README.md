# Static-Site-Generator-in-Python

A from-scratch **static site generator** that turns Markdown content into a full HTML site. Built as part of the [Boot.dev](https://www.boot.dev) curriculum — no third-party Markdown libraries; parsing and HTML rendering are custom.

---

## Features

- Custom Markdown → HTML pipeline (no `markdown` package)
- Inline formatting: **bold**, _italic_, `code`, links, and images
- Block types: headings, paragraphs, code blocks, quotes, ordered & unordered lists
- Recursive generation of every `.md` file under `content/`
- HTML template with `{{ Title }}` and `{{ Content }}` placeholders
- Copies `static/` assets into the output folder
- Unit tests for text nodes, HTML nodes, and Markdown blocks

---

## How it works

1. Read Markdown from `content/`
2. Split into blocks and classify each block type
3. Parse inline Markdown into `TextNode`s, then into HTML leaf/parent nodes
4. Inject the HTML into `template.html`
5. Write pages under `docs/` and copy static files (CSS, images, etc.)
