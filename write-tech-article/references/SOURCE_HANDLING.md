# Source-Specific File Handling

This document specifies which markdown files to use when generating articles from different sources.

## File Structure Overview

After using the `html-to-markdown` skill, source files follow this structure:

```
[slug]/
  ├── origin.json          # Original structured data from aggregate-news
  ├── post.md             # For Hacker News: original article content
  ├── comment.md          # For Hacker News: HN discussion thread
  ├── product.md          # For Product Hunt: official product page
  └── hunt.md             # For Product Hunt: PH launch/discussion page
```

## Source File Combinations

### Hacker News Content

**Files to use:**
- `post.md` (required) - Original article content
- `comment.md` (optional) - HN discussion thread

**Usage:**
- Read both files when available
- Extract content from post.md as primary source
- Use comment.md for community perspectives and additional insights

### Product Hunt Content

**Files to use:**
- `product.md` (required) - Official product page
- `hunt.md` (optional) - Product Hunt launch page

**Usage:**
- Read both files when available
- Extract product information from product.md as primary source
- Use hunt.md for community reception and feedback

## Implementation Note

When generating articles:
1. Identify the source type from frontmatter (`source` field)
2. Load the appropriate file combination
3. Follow the article structure defined in ARTICLE_STRUCTURE.md
4. Apply the appropriate writing style based on user preferences
