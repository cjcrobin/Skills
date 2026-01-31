# HTML to Markdown Conversion Scripts

This directory contains the Docker-based conversion scripts for transforming HTML/JSON files to markdown format.

## Files

- **Dockerfile** - Defines the Docker image with Node.js and Bun runtime
- **start-docker-container.sh** - Builds image and starts container with necessary mounts
- **convert.ts** - Main CLI script (executes inside Docker container)
- **html-to-markdown.ts** - Conversion utility library (imported by convert.ts)
- **temp_data/** - Working directory for file processing (mounted to container)

## Architecture

The code is split into two files for better maintainability:

1. **html-to-markdown.ts** (Library)
   - Pure conversion functions
   - Type definitions
   - Reusable utilities
   - No file I/O or CLI logic

2. **convert.ts** (CLI Application)
   - Imports functions from html-to-markdown.ts
   - File system operations
   - Directory traversal
   - Command-line interface
   - Progress reporting

## Usage

All execution happens through Docker. Do NOT run TypeScript files directly on host machine.

### 1. Start Container

```bash
cd /path/to/html-to-markdown/scripts
bash start-docker-container.sh
```

### 2. Prepare Data

Copy source files to temp_data:
```bash
cp -r ~/articles/2026-01-31 temp_data/
```

### 3. Run Conversion

Execute inside Docker container:
```bash
docker exec html-to-markdown-container \
  bun /app/convert.ts /app/temp_data/2026-01-31/NewsSource.HACKER_NEWS
```

### 4. Copy Results

```bash
cp -r temp_data/2026-01-31 ~/articles/
```

## Container Details

- **Image**: html-to-markdown:v1.0
- **Container**: html-to-markdown-container
- **Runtime**: Bun (faster than node for TypeScript execution)

## Mounted Volumes

- `/app/convert.ts` ← `./convert.ts`
- `/app/html-to-markdown.ts` ← `./html-to-markdown.ts`
- `/app/temp_data` ← `./temp_data/`

## Supported Input Files

- **JSON files** from aggregate-news skill
  - Contains `content` field (article HTML)
  - Contains `additional_metadata.comments_content` field (HN discussion HTML)

## Output

Generated markdown files with:
- YAML frontmatter (metadata)
- Clean markdown content
- Same directory structure as input
