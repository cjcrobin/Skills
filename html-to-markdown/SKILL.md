---
name: html-to-markdown
description: Convert HTML files and aggregate-news JSON files to clean markdown format with frontmatter metadata. Use when user wants to "转换HTML", "HTML转markdown", "convert html to markdown", "转换JSON中的HTML", "convert aggregate-news to markdown". Generates markdown from HTML content and optionally from HN discussion comments. Output saved to same directory as input.
---

# HTML to Markdown Skill

Convert HTML content to well-formatted markdown with metadata frontmatter. Accepts:
- HTML files (*.html, *.htm)
- JSON files from `aggregate-news` skill

For JSON files, may generate 2 markdown files:
1. Article content (from `content` field) → article.md
2. HN comments (from `additional_metadata.comments_content`) → discussion.md (optional)

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
   - Example: If storage_location is `~/articles` and user wants to convert `~/articles/2026-01-31/NewsSource.HACKER_NEWS/`
   - Then input subdirectory is: `2026-01-31/NewsSource.HACKER_NEWS`
   - Or provide full absolute path

**Output**: Markdown files will be saved in the same directory as input files.

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
           ├── file1.json
           ├── file2.json
           └── ...
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

1. Read and parse JSON file
2. Check for `content` field (contains article HTML)
3. Check for `additional_metadata.comments_content` (contains HN discussion HTML)
4. Extract base metadata: `url`, `title`, `source`, `publish_time`

**Generate up to 2 markdown files:**

a) **Article markdown** (if `content` exists and not null):
   - Source: `content` field
   - URL: `url` field  
   - Type: `article`
   - Filename: `{sanitized-title}.md`
   - Frontmatter includes: url, title, source, published, type

b) **Discussion markdown** (if `comments_content` exists and not null):
   - Source: `additional_metadata.comments_content` field
   - URL: `additional_metadata.comments_url` field
   - Type: `hn_discussion`
   - Filename: `{sanitized-title}-discussion.md`
   - Frontmatter includes: url (comments_url), title, source, type, original_article (link to article)

JSON structure example:
```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "content": "<html>...</html>",
  "source": "hacker_news",
  "publish_time": "2026-01-30T10:00:00",
  "additional_metadata": {
    "comments_url": "https://news.ycombinator.com/item?id=123456",
    "points": 100,
    "comments": 50,
    "comments_content": "<html>...</html>"
  }
}
```

**If content is null:**
- Report: "Skipping {filename}: content field is null"
- Do not generate markdown

## HTML to Markdown Conversion

The `convert.ts` script uses the TypeScript functions from [html-to-markdown.ts](scripts/html-to-markdown.ts):

**Conversion features:**
- Handles headings, bold, italic, links, images, code, lists, tables, quotes
- Removes nav, ads, scripts, styles
- Normalizes whitespace
- Generates YAML frontmatter with metadata

## Frontmatter Format

**For article (from JSON content or HTML file):**
```yaml
---
url: https://example.com/article
title: "Article Title"
source: hacker_news
published: "2026-01-30T10:00:00"
type: article
---
```

**For HN discussion (from JSON comments_content):**
```yaml
---
url: https://news.ycombinator.com/item?id=123456
title: "Article Title - Discussion"
source: hacker_news
type: hn_discussion
original_article: https://example.com/article
points: 100
comments: 50
---
```

## File Naming

Markdown files are saved in the **same directory** as input files:
- Article: `{sanitized-title}.md`
- Discussion: `{sanitized-title}-discussion.md`

Sanitize filename: lowercase, hyphens, no special chars, max 80 chars.

## Content Types

- **article**: Technical articles, blog posts, tutorials
- **hn_discussion**: HN comment threads with threading
- **documentation**: Tech docs with TOC and cross-refs
- **product_page**: Product pages (remove marketing fluff)
- **blog_post**: General blog content

## Example Usage

**Example: Convert aggregate-news JSON files using Docker**
```
User: 把 ~/articles/2026-01-31/NewsSource.HACKER_NEWS/ 文件夹下的 JSON 文件转换成 markdown

Assistant actions:
1. Load PREFERENCE.md (storage_location: ~/articles)
2. cd to {SKILL_ROOT}/scripts
3. Execute start-docker-container.sh
4. Copy source directory to temp_data:
   cp -r ~/articles/2026-01-31 {SKILL_ROOT}/scripts/temp_data/
5. Run conversion in Docker:
   docker exec html-to-markdown-container \
     bun /app/convert.ts /app/temp_data/2026-01-31/NewsSource.HACKER_NEWS
6. Copy results back:
   cp -r {SKILL_ROOT}/scripts/temp_data/2026-01-31 ~/articles/
7. Report:
   ✓ Processed 10 JSON files
   ✓ Generated 20 markdown files
     - 10 articles: article1.md, article2.md, ...
     - 10 discussions: article1-discussion.md, article2-discussion.md, ...
```

## Troubleshooting

**Issue**: Docker is not available
**Solution**: Stop execution. Inform user that Docker is required for this skill.

**Issue**: JSON file has null content field
**Solution**: Script will skip file and report in summary

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
