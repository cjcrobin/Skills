---
name: html-to-markdown
description: Convert HTML files and aggregate-news JSON files to clean markdown format with frontmatter metadata. Use when user wants to "转换HTML", "HTML转markdown", "convert html to markdown", "转换JSON中的HTML", "convert aggregate-news to markdown". Generates markdown from HTML content and optionally from HN discussion comments. Output saved to same directory as input.
---

# HTML to Markdown Skill

Convert HTML content to well-formatted markdown with metadata frontmatter. Accepts:
- HTML files (*.html, *.htm)
- JSON files from `aggregate-news` skill (origin.json)

## Source-Specific Processing

### Hacker News Items (from origin.json)
From a HackerNewsItem JSON, generates 2 markdown files:
1. **post.md** - Article content from `post_content` field
2. **comment.md** - HN discussion from `comment_content` field

### Product Hunt Items (from origin.json)
From a ProductHuntItem JSON, generates 2 markdown files:
1. **product.md** - Product page content from `product_content` field
2. **hunt.md** - Product Hunt page content from `hunt_content` field

Output is saved to the same directory as input files.

## Important: Docker Execution Only

**This skill MUST be executed using Docker only. Do NOT run TypeScript scripts directly on the host machine.**

If Docker is not available, stop execution and inform the user that Docker is required.

## Workflow

### Step 1: Load Preferences

Check for preferences in this order:
1. `{SKILL_ROOT}/PREFERENCE.md` (project-level)
2. If not found, ask user for:
   - **storage_location**: Base directory for article files (e.g., `~/articles`)
3. Create `{SKILL_ROOT}/PREFERENCE.md` with provided values

Example PREFERENCE.md:
```markdown
# HTML to Markdown Conversion Preferences

- **storage_location**: ~/articles
```

### Step 2: Gather Input

Ask the user for:
1. **Input directory or subdirectory**: Relative path from `storage_location`
   - Example: If storage_location is `~/articles` and user wants to convert `~/articles/2026-01-31/NewsSource.HACKER_NEWS/article_slug/`
   - Then input subdirectory is: `2026-01-31/NewsSource.HACKER_NEWS/article_slug`
   - Or provide full absolute path

**Output**: Markdown files will be saved in the same directory as input `origin.json` file.

### Step 3: Start Docker Container

Execute the Docker container setup script. The location of this SKILL.md file is defined as `{{SKILL_DIR}}`.

**PLEASE MAKE SURE the bash script is EXECUTED in the {{SKILL_DIR}}/scripts directory:**

```bash
cd {{SKILL_DIR}}/scripts
bash start-docker-container.sh
```

This script will:
- Build the Docker image if it doesn't exist
- Create and start the container if not running
- Mount the conversion script and temp_data directory

### Step 4: Prepare Data

Copy the input directory to the temp_data folder:

1. Determine the source path:
   - If user provided subdirectory: `{storage_location}/{subdirectory}`
   - If user provided absolute path: use that path

2. Copy to temp_data preserving structure:
   ```bash
   cd {{SKILL_DIR}}/scripts
   # Example: Copy ~/articles/2026-01-31 to temp_data/2026-01-31
   cp -r {source_path} temp_data/
   ```

3. The temp_data structure should mirror the source structure:
   ```
   temp_data/
   └── 2026-01-31/
       └── NewsSource.HACKER_NEWS/
           └── article_slug/
               └── origin.json
   ```

### Step 5: Execute Conversion in Docker

Run the conversion script using Docker exec with bun:

**DO NOT change the --input parameter - it's the path inside the Docker container:**

```bash
docker exec html-to-markdown-container \
  bun /app/convert.ts /app/temp_data/{relative_path}
```

Example:
```bash
docker exec html-to-markdown-container \
  bun /app/convert.ts /app/temp_data/2026-01-31/NewsSource.HACKER_NEWS
```

The script will:
- Process all JSON files in the directory
- Generate markdown files in the same directory as input files
- Output progress and statistics

### Step 6: Move Results Back

Copy the generated markdown files from temp_data back to the target location, preserving the directory structure:

```bash
# Copy all generated .md files back to original location
cp -r {{SKILL_DIR}}/scripts/temp_data/* {storage_location}/
```

Example:
- If file is in `temp_data/2026-01-31/NewsSource.HACKER_NEWS/article.md`
- And storage_location is `~/articles`
- Then file should be copied to `~/articles/2026-01-31/NewsSource.HACKER_NEWS/article.md`

### Step 7: Report Results

### Step 7: Report Results

Show summary from Docker execution output:
- Total files processed
- Articles generated
- Discussions generated (if any)
- Files skipped (if content was null)

Example:
```
✓ Processed 10 files
✓ Generated 20 markdown files
  - 10 articles
  - 10 discussions
✗ Skipped 0 files
```

## Docker Container Details

**Container Name**: `html-to-markdown-container`
**Image Name**: `html-to-markdown:v1.0`

**Mounted Volumes:**
- `/app/convert.ts` - Main CLI application (entry point)
- `/app/html-to-markdown.ts` - Conversion utility library (imported by convert.ts)
- `/app/temp_data` - Working directory for input/output files

**Architecture:**
- `html-to-markdown.ts` contains pure conversion functions (library)
- `convert.ts` imports from html-to-markdown.ts and adds CLI logic
- This separation allows code reuse and better maintainability

**Execution Command:**
```bash
docker exec html-to-markdown-container bun /app/convert.ts /app/temp_data/{path}
```

## File Processing Details

**For JSON files (from aggregate-news):**

1. Read and parse `origin.json` file
2. Detect source type from JSON structure:
   - If has `post_content` and `comment_content` → HackerNewsItem
   - If has `product_content` and `hunt_content` → ProductHuntItem
3. Extract base metadata: `title`, `publish_time`, `popularity`, `source`

**Generate markdown files based on source type:**

### a) Hacker News Item Processing

From origin.json containing HackerNewsItem data, generate:

**post.md** (if `post_content` exists and not null):
- Source: `post_content` field (HTML)
- URL: `post_url` field  
- Type: `article`
- Frontmatter includes:
  ```yaml
  ---
  url: [post_url]
  title: "[title]"
  source: hacker_news
  published: "[publish_time]"
  type: article
  points: [points]
  num_comments: [num_comments]
  ---
  ```

**comment.md** (if `comment_content` exists and not null):
- Source: `comment_content` field (HTML)
- URL: `comment_url` field
- Type: `hn_discussion`
- Frontmatter includes:
  ```yaml
  ---
  url: [comment_url]
  title: "[title] - Discussion"
  source: hacker_news
  type: hn_discussion
  original_article: [post_url]
  points: [points]
  num_comments: [num_comments]
  ---
  ```

### b) Product Hunt Item Processing

From origin.json containing ProductHuntItem data, generate:

**product.md** (if `product_content` exists and not null):
- Source: `product_content` field (HTML)
- URL: `product_url` field
- Type: `product_page`
- Frontmatter includes:
  ```yaml
  ---
  url: [product_url]
  title: "[title]"
  source: product_hunt
  published: "[publish_time]"
  type: product_page
  votes: [votes]
  ---
  ```

**hunt.md** (if `hunt_content` exists and not null):
- Source: `hunt_content` field (HTML)
- URL: `hunt_url` field
- Type: `product_hunt_page`
- Frontmatter includes:
  ```yaml
  ---
  url: [hunt_url]
  title: "[title] - Product Hunt"
  source: product_hunt
  type: product_hunt_page
  original_product: [product_url]
  votes: [votes]
  ---
  ```

**If content fields are null:**
- Report: "Skipping {field_name} for {filename}: content field is null"
- Do not generate corresponding markdown file

## HTML to Markdown Conversion

The `convert.ts` script uses the TypeScript functions from [html-to-markdown.ts](scripts/html-to-markdown.ts):

**Conversion features:**
- Handles headings, bold, italic, links, images, code, lists, tables, quotes
- Removes nav, ads, scripts, styles
- Normalizes whitespace
- Generates YAML frontmatter with metadata

## Frontmatter Format

### For Hacker News post (post.md):
```yaml
---
url: https://example.com/article
title: "Article Title"
source: hacker_news
published: "2026-01-30T10:00:00"
type: article
points: 100
num_comments: 50
---
```

### For Hacker News discussion (comment.md):
```yaml
---
url: https://news.ycombinator.com/item?id=123456
title: "Article Title - Discussion"
source: hacker_news
type: hn_discussion
original_article: https://example.com/article
points: 100
num_comments: 50
---
```

### For Product Hunt product page (product.md):
```yaml
---
url: https://example.com/product
title: "Product Title"
source: product_hunt
published: "2026-01-30T10:00:00"
type: product_page
votes: 150
---
```

### For Product Hunt hunt page (hunt.md):
```yaml
---
url: https://www.producthunt.com/posts/product-slug
title: "Product Title - Product Hunt"
source: product_hunt
type: product_hunt_page
original_product: https://example.com/product
votes: 150
---
```

## File Naming

Markdown files are saved in the **same directory** as the input `origin.json` file:
- Hacker News: `post.md` and `comment.md`
- Product Hunt: `product.md` and `hunt.md`

Example directory structure after conversion:
```
2026-01-31/
└── NewsSource.HACKER_NEWS/
    └── how_ai_assistance_impacts_coding_skills/
        ├── origin.json
        ├── post.md
        └── comment.md
```

## Content Types

- **article**: Technical articles from Hacker News posts, blog posts, tutorials
- **hn_discussion**: HN comment threads with threading structure
- **product_page**: Official product website content
- **product_hunt_page**: Product Hunt discussion and launch page
- **documentation**: Tech docs with TOC and cross-refs
- **blog_post**: General blog content

## Example Usage

**Example: Convert aggregate-news JSON files using Docker**
```
User: 把 ~/articles/2026-01-31/NewsSource.HACKER_NEWS/article_slug/ 文件夹下的 origin.json 文件转换成 markdown

Assistant actions:
1. Load PREFERENCE.md (storage_location: ~/articles)
2. cd to {SKILL_ROOT}/scripts
3. Execute start-docker-container.sh
4. Copy source directory to temp_data:
   cp -r ~/articles/2026-01-31/NewsSource.HACKER_NEWS/article_slug {SKILL_ROOT}/scripts/temp_data/2026-01-31/NewsSource.HACKER_NEWS/
5. Run conversion in Docker:
   docker exec html-to-markdown-container \
     bun /app/convert.ts /app/temp_data/2026-01-31/NewsSource.HACKER_NEWS/article_slug
6. Copy results back:
   cp -r {SKILL_ROOT}/scripts/temp_data/2026-01-31/NewsSource.HACKER_NEWS/article_slug/*.md ~/articles/2026-01-31/NewsSource.HACKER_NEWS/article_slug/
7. Report:
   ✓ Processed 1 origin.json file
   ✓ Generated 2 markdown files
     - post.md (article content)
     - comment.md (HN discussion)
```

## Troubleshooting

**Issue**: Docker is not available
**Solution**: Stop execution. Inform user that Docker is required for this skill.

**Issue**: JSON file has null content fields
**Solution**: Script will skip null fields and report in summary (e.g., "post_content is null, skipping post.md")

**Issue**: Can't parse JSON file
**Solution**: Script will skip file, report error with filename

**Issue**: Container fails to start
**Solution**: Check if Docker daemon is running, check port conflicts, rebuild image

**Issue**: Files not found in temp_data after execution
**Solution**: Check if source files were copied correctly to temp_data before execution

**Issue**: Permission errors when copying files
**Solution**: Check directory permissions for source and temp_data directories

## Related Skills

- `write-tech-article`: Uses markdown output from this skill as input (required preprocessing)
- `aggregate-news`: Generates JSON files that this skill can convert to markdown
- `post-to-blogs`: Downstream publishing after article generation
