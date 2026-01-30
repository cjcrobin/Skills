# News Aggregation Preferences

Configure how news articles are collected and stored.

## Configuration

- **limit**: 10
  - Number of articles to fetch per source
  - Range: 1-100
  
- **fetch_content**: true
  - Whether to fetch full article content (slower but more complete)
  - Options: true, false
  
- **storage_location**: ~/articles
  - Base directory for saving collected articles
  - Articles will be organized as: {storage_location}/{YYYY-MM-DD}/{source_name}/

## Notes

- This file can be placed at:
  - Project level: `{SKILL_ROOT}/PREFERENCE.md` (takes priority)
  - User level: `~/.copilot/PREFERENCE.md` (fallback)
- If neither file exists, you'll be prompted to configure preferences interactively
- You can edit this file anytime to change your preferences
