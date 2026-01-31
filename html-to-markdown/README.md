# HTML to Markdown Skill

Convert HTML files and aggregate-news JSON files to clean markdown with frontmatter metadata.

## Input Formats

1. **HTML files** (*.html, *.htm)
2. **JSON files** from `aggregate-news` skill

## Key Feature: Dual Markdown Generation

For each JSON file from aggregate-news, generates **up to 2 markdown files**:

1. **Article markdown** (from `content` field)
   - Filename: `{title}.md`
   - URL: article URL
   - Type: `article`

2. **Discussion markdown** (from `additional_metadata.comments_content`, if exists)
   - Filename: `{title}-discussion.md`
   - URL: comments URL (e.g., HN discussion)
   - Type: `hn_discussion`

**Output location**: Same directory as input files (no reorganization)

## Quick Start

### Convert aggregate-news JSON to markdown

```
User: 把 ~/articles/2026-01-30/NewsSource.HACKER_NEWS/ 下的 JSON 文件转换成 markdown
```

The skill will:
- Read all JSON files
- Extract HTML from `content` field → article.md
- Extract HTML from `additional_metadata.comments_content` → discussion.md (if exists)
- Preserve metadata (url, title, source, points, comments)
- Save markdown files in the same directory

### Convert HTML files

```
User: 把 ~/downloads/ 下的 HTML 文件转换成 markdown
```

## Output Example

Input directory:
```
~/articles/2026-01-30/NewsSource.HACKER_NEWS/
├── apple-patreon-tax.json
├── amazon-layoffs.json
└── postgres-features.json
```

Output (same directory):
```
~/articles/2026-01-30/NewsSource.HACKER_NEWS/
├── apple-patreon-tax.json
├── apple-patreon-tax.md              ← article
├── apple-patreon-tax-discussion.md   ← HN comments
├── amazon-layoffs.json
├── amazon-layoffs.md                 ← article
├── amazon-layoffs-discussion.md      ← HN comments
├── postgres-features.json
└── postgres-features.md              ← article only (no discussion)
```

## Frontmatter Examples

**Article markdown:**
```yaml
---
url: https://www.macrumors.com/2026/01/28/patreon-apple-tax/
title: "Apple to soon take up to 30% cut from all Patreon creators"
source: hacker_news
published: "2026-01-28T20:59:30"
type: article
---
```

**Discussion markdown:**
```yaml
---
url: https://news.ycombinator.com/item?id=46801419
title: "Apple to soon take up to 30% cut from all Patreon creators - Discussion"
source: hacker_news
type: hn_discussion
original_article: https://www.macrumors.com/2026/01/28/patreon-apple-tax/
points: 1043
comments: 863
---
```

## No Configuration Needed

This skill is designed to be simple:
- ✅ No PREFERENCE.md file required
- ✅ Output goes to same directory as input
- ✅ No directory reorganization
- ✅ Just point to input folder and go

## Workflow Integration

**Upstream**: `aggregate-news` → JSON files with HTML content
**This skill**: JSON → Markdown files (article + optional discussion)
**Downstream**: `write-tech-article` → Structured Chinese blog articles

## Files

- `SKILL.md`: Main skill documentation (loaded by AI)
- `scripts/html-to-markdown.ts`: TypeScript conversion script
- `README.md`: This file (human reference only)

## Technical Details

The TypeScript script (`scripts/html-to-markdown.ts`):
- Cleans HTML (removes nav, ads, scripts, styles)
- Extracts metadata (title, description, author, date)
- Converts to markdown (headings, lists, code, tables, links, images)
- Normalizes whitespace

For JSON from aggregate-news:
- Processes `content` field → article markdown
- Processes `additional_metadata.comments_content` → discussion markdown
- Skips files where content is null
- Preserves all metadata in frontmatter

## License

See root LICENSE file.
