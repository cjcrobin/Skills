# HTML to Markdown Conversion Preferences

Configure how HTML/JSON files are converted to markdown.

## Configuration

- **storage_location**: ~/articles
  - Base directory where source files are located and where markdown output will be saved
  - Files will maintain their subdirectory structure

## Notes

- The conversion process uses Docker to ensure consistent execution environment
- Markdown files are generated in the same directory as their source files
- Supports both HTML files and JSON files from aggregate-news skill
