# Write Tech Article Preferences

Configure this skill's behavior by creating a `PREFERENCE.md` file with the following settings:

## Required Settings

- **output_directory**: Directory where generated articles will be saved
  - Example: `~/articles/published`
  - Example: `/home/robin/blog/content/posts`

## Optional Settings

- **default_category**: Default category tag for articles
  - Default: `hacknews-daily`
  - Example: `tech-insights`, `ai-research`, `dev-tools`

- **author**: Author name for article metadata
  - Default: (none)
  - Example: `Robin Zhang`

- **language**: Output language for articles
  - Default: `zh-CN`
  - Options: `zh-CN`, `en`, `zh-TW`

- **writing_style**: Writing style/perspective for articles
  - Default: `objective`
  - Options: `objective` (third-person), `first-person` (personal experience)

- **tags_auto_generate**: Automatically generate tags from content
  - Default: `true`
  - Options: `true`, `false`

- **max_tags**: Maximum number of tags to generate
  - Default: `8`
  - Range: `3-15`

- **include_toc**: Include table of contents in article
  - Default: `false`
  - Options: `true`, `false`

- **fetch_images**: Download and save referenced images locally
  - Default: `false`
  - Options: `true`, `false`

- **image_directory**: Directory for downloaded images (relative to output_directory)
  - Default: `images`
  - Example: `assets/images`, `static/img`

## Example Configuration

```markdown
# Write Tech Article Preferences

- **output_directory**: ~/blog/content/posts
- **default_category**: tech-analysis
- **author**: Robin Zhang
- **language**: zh-CN
- **writing_style**: objective
- **tags_auto_generate**: true
- **max_tags**: 8
- **include_toc**: false
- **fetch_images**: false
```

## Notes

- Create `PREFERENCE.md` in the skill root directory: `/home/robin/sources/skills/write-tech-article/PREFERENCE.md`
- Or create user-level preferences: `~/.copilot/skills/write-tech-article/PREFERENCE.md`
- Project-level preferences take precedence over user-level preferences
