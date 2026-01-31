---
name: write-tech-article
description: Generate comprehensive Chinese tech blog articles from markdown source files. Use when user wants to "写技术文章", "生成博客", "整理文章", "write article", "generate blog post" or transform markdown content into structured blog format. Accepts multiple markdown files as input. Outputs natural Chinese writing without AI-style language.
---

# Write Tech Article Skill

This skill transforms markdown source files (containing articles, HN discussions, documentation) into comprehensive, naturally-written Chinese blog posts following a specific structure.

## Core Capabilities

- Accept multiple markdown files as input sources
- Analyze content types via frontmatter metadata (type field)
- Generate structured blog articles with frontmatter metadata
- Produce natural Chinese writing without AI-style language
- Support multiple article structures and templates
- Save to user-specified locations

## Input Requirements

**Source files must be markdown format** with frontmatter containing:
- `url`: Original source URL
- `title`: Article title
- `type`: Content type (article, hn_discussion, documentation, blog_post, etc.)
- `captured_at`: Timestamp of capture

Example input frontmatter:
```yaml
---
url: https://marginlab.ai/trackers/claude-code/
title: "Claude Code Daily Benchmarks"
type: article
captured_at: "2026-01-30T10:00:00Z"
---
```

## Workflow

### Step 1: Gather Input

Ask the user for:
1. **Source markdown files** (required): One or more markdown files containing the content
   - Primary article file
   - Optional: HN discussion file
   - Optional: Additional reference files
2. **Additional context** (optional): Any specific angles or topics to emphasize

**Note**: Source files should be prepared using the `html-to-markdown` skill first if starting from HTML.

### Step 2: Load Preferences

Check for preferences in this order:
1. `{SKILL_ROOT}/PREFERENCE.md` (project-level)
2. `~/.copilot/skills/write-tech-article/PREFERENCE.md` (user-level)
3. If neither exists, prompt user and create `{SKILL_ROOT}/PREFERENCE.md`

Required preferences:
- **output_directory**: Where to save generated articles (e.g., `~/articles/published`)
- **default_category**: Default category tag (e.g., `hacknews-daily`)
- **author**: Author name for metadata (optional)
- **language**: Output language (default: `zh-CN`)

See [PREFERENCE_TEMPLATE.md](PREFERENCE_TEMPLATE.md) for complete example.

### Step 3: Read and Parse Source Files

Read all provided markdown files:
1. Parse frontmatter to identify content type
2. Extract markdown content body
3. Identify content relationships (e.g., article + discussion)

**Content Type Handling:**
- `article`: Primary technical content
- `hn_discussion`: Hacker News discussion thread
- `documentation`: Technical documentation
- `blog_post`: Blog post content
- `product_page`: Product/service description

### Step 4: Analyze and Structure

Analyze the markdown content to extract:
- **Core topic**: Main subject matter from primary article
- **Key insights**: 3-7 main takeaways from all sources
- **Technical details**: Code examples, architecture, tools mentioned
- **Community perspectives**: Insights from discussion files (if provided)
- **Practical value**: How-to applications, use cases
- **Source attribution**: Track which insights come from which source filee [ARTICLE_STRUCTURE.md](references/ARTICLE_STRUCTURE.md)):
1. Frontmatter (YAML metadata)
2. Article summary (摘要)
3. Background and problem (背景与问题)
4. Core content analysis (核心内容解析)
5. Deep analysis and reflection (深度分析与思考)
6. Tech stack/tools (技术栈/工具清单)
7. Related resources (相关资源)

### Step 5: Generate Article

**Critical: Writing Style Requirements**

The generated article MUST follow these natural writing principles:

❌ **Avoid AI-style language:**
- No "让我们一起探索..." (let's explore together)
- No "值得注意的是..." overuse
- No "在...的背景下" formulaic patterns
- No excessive transitional phrases
- No generic opening like "在当今快速发展的..."

✅ **Use natural Chinese writing:**
- Direct, clear statements
- Varied sentence structures
- Concrete examples before abstract concepts
- Technical precision without verbosity
- Conversational tone where appropriate
- Mix of short and long sentences

**Example - Bad (AI style):**
> 在当今快速发展的技术环境中，我们不难发现 AI 编程助手已经成为开发者工作流中不可或缺的一部分。值得注意的是，这些工具虽然带来了巨大的便利，但同时也面临着性能稳定性的挑战。让我们深入探讨这个问题。

**Example - Good (Natural style):**
> AI 编程助手如今已是开发者的标配工具。但一个被忽视的问题正在浮现：模型更新后，代码生成质量是提升了，还是倒退了？MarginLab 的每日基准测试项目就是为了回答这个问题。

**Generation Process:**
1. Extract key facts and technical details
2. Organize into logical flow
3. Write each section with natural language
4. Include code examples with proper formatting
5. Add technical depth where relevant
6. Cite sources and provide links

### Step 6: Format and Save

1. Generate filename from article title (slugified)
2. Add YAML frontmatter with metadata:
   - title, date, tags, categories
   - description (50-200 words)
   - slug (URL-friendly identifier)
3. Format markdown with proper headings, lists, code blocks
4. Save to: `{output_directory}/{YYYY-MM-DD}/{slug}.md`

Example path: `~/articles/published/2026-01-30/claude-code-daily-benchmarks.md`

### Step 7: Verify and Report

1. Verify file was created successfully
2. Show user:
   - File location
   - Word count
   - Structure completeness checklist
3. Ask if any revisions needed

## Quality Checklist

Before finalizing, ensure the article has:
- [ ] Clear, specific title (not generic)
- [ ] Comprehensive 3-5 sentence summary
- [ ] Well-defined problem/background section
- [ ] At least 5-7 key insights
- [ ] Technical examples or code where relevant
- [ ] Practical application scenarios
- [ ] Natural Chinese without AI clichés
- [ ] Proper source attribution
- [ ] Complete frontmatter metadata

## Example Usage

**User**: 我有两个 markdown 文件，一个是文章内容 article.md，一个是 HN 讨论 discussion.md，帮我整理成文章

**Assistant Actions**:
1. Check for PREFERENCE.md (finds user's output directory)
2. Read article.md and parse frontmatter (type: article)
3. Read discussion.md and parse frontmatter (type: hn_discussion)
4. Analyze both sources and extract key insights
5. Generate article following ARTICLE_STRUCTURE.md guidelines
6. Apply WRITING_STYLE.md principles (natural Chinese)
7. Save to: `~/articles/published/2026-01-30/claude-code-daily-benchmarks.md`
8. Report: "✓ Article generated: 4,200 words, saved to ~/articles/published/"

## Important Notes

### Writing Style is Critical

The most important aspect of this skill is producing **natural Chinese writing**. Before generating any article:

1. Review [WRITING_STYLE.md](references/WRITING_STYLE.md) principles
2. Avoid all AI-style clichés and formulaic phrases
3. Use concrete examples before abstract concepts
4. Vary sentence structure and length
5. Write as if explaining to a technical colleague

### Source File Integration

When working with multiple source files:
- Identify primary content vs. supporting content via `type` field
- Cross-reference insights between sources
- Attribute community perspectives to discussion sources
- Preserve technical accuracy from all sources
- Synthesize cohesive narrative from multiple inputs

### Content Quality

Generate comprehensive articles (3500-5500 words) with:
- Original analysis, not just summarization
- Technical depth with code examples
- Practical applications and use cases
- Critical perspective (pros AND cons)
- Proper source attribution

### Metadata Accuracy

Ensure frontmatter is accurate:
- `date`: Use current date (YYYY-MM-DD)
- `title`: Specific, not generic (15-25 Chinese chars)
- `tags`: 5-8 relevant technical tags
- `description`: Compelling 50-200 word summary
- `slug`: URL-friendly identifier
- `categories`: From user preferences

## Troubleshooting

**Issue**: Can't find PREFERENCE.md
**Solution**: Prompt user for output_directory and create file

**Issue**: Source files missing frontmatter
**Solution**: Prompt user to use `html-to-markdown` skill first or manually add frontmatter

**Issue**: Content is too short
**Solution**: Expand analysis sections, add more examples, include community insights

**Issue**: Writing sounds too "AI-like"
**Solution**: Review WRITING_STYLE.md, use more concrete examples, vary sentence structure

**Issue**: Missing technical details
**Solution**: Re-read source files, extract code examples, add implementation specifics

**Issue**: Can't identify content types
**Solution**: Check frontmatter `type` field, or ask user to clarify source file purposes

## Related Skills

- `html-to-markdown`: Convert HTML sources to markdown before using this skill (required preprocessing)
- `aggregate-news`: For collecting source material from HN/PH
- `post-to-blogs`: For publishing generated articles
- `google-official-seo-guide`: For optimizing article SEO