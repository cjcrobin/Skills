# Web Scraper

A robust web scraping tool with JavaScript rendering capabilities and anti-bot bypass features using Playwright.

## Features

- **JavaScript Rendering**: Fully renders JavaScript-heavy websites
- **Anti-Bot Bypass**: Includes stealth techniques to avoid detection
- **Command-Line Interface**: Easy-to-use CLI with multiple options
- **Configuration File Support**: Use JSON config files for repeatable scraping
- **Flexible Output**: Save to file or output to stdout
- **Configurable Timeouts**: Customize page load and wait times
- **Headless/Visible Mode**: Run browser in headless mode or visible for debugging

## Installation

1. Install dependencies:
```bash
uv sync --all-groups
```

2. Install Playwright browser:
```bash
uv run playwright install chromium
```

3. Install system dependencies (if needed):
```bash
sudo apt-get install -y libdbus-1-3
```

## Usage

### Command Line

#### Basic usage - scrape and print to stdout:
```bash
uv run python news_aggregator/scripts/web_scrape.py --url https://example.com
```

#### Save to file:
```bash
uv run python news_aggregator/scripts/web_scrape.py \
  --url https://example.com \
  --save \
  --output-dir ./output \
  --filename example.html
```

#### Run in visible mode (for debugging):
```bash
uv run python news_aggregator/scripts/web_scrape.py \
  --url https://example.com \
  --no-headless
```

#### Custom timeout settings:
```bash
uv run python news_aggregator/scripts/web_scrape.py \
  --url https://example.com \
  --timeout 30000 \
  --wait-after-load 5000
```

### Using Configuration File

Create a config file (e.g., `config.json`):
```json
{
  "url": "https://example.com",
  "save_to_file": true,
  "save_location": "./output",
  "filename": "scraped_page.html",
  "headless": true,
  "timeout": 60000,
  "wait_after_load": 2000
}
```

Run with config:
```bash
uv run python news_aggregator/scripts/web_scrape.py --config config.json
```

See [config.example.json](config.example.json) for a complete example.

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | URL to scrape (required if no config) | - |
| `--config` | Path to JSON configuration file | - |
| `--save` | Save scraped content to file | False |
| `--output-dir` | Directory to save output file | `./output` |
| `--filename` | Output filename | `page.html` |
| `--no-headless` | Run browser in visible mode | False |
| `--timeout` | Page load timeout in milliseconds | 60000 |
| `--wait-after-load` | Wait time after page load in milliseconds | 2000 |

## Python API

You can also use the scraper programmatically:

```python
from news_aggregator.scripts.web_scrape import scrape_webpage

# Basic usage
content = scrape_webpage(url="https://example.com")
if content:
    print(f"Scraped {len(content)} characters")

# Save to file
content = scrape_webpage(
    url="https://example.com",
    save_to_file=True,
    save_location="./output",
    filename="example.html"
)

# Custom settings
content = scrape_webpage(
    url="https://example.com",
    headless=False,
    timeout=30000,
    wait_after_load=5000
)
```

## Testing

### Run all tests:
```bash
uv run pytest
```

### Run only unit tests:
```bash
uv run pytest tests/unit/ -v
```

### Run only integration tests:
```bash
uv run pytest tests/integration/ -v
```

### Run with coverage:
```bash
uv run pytest --cov=news_aggregator --cov-report=html
```

## How It Works

1. **Browser Launch**: Launches a Chromium browser with stealth settings to avoid detection
2. **Stealth Techniques**: Modifies browser properties to hide automation markers
3. **Page Navigation**: Navigates to the target URL and waits for network to be idle
4. **Content Extraction**: Waits for additional time to ensure lazy-loaded content is rendered
5. **Output**: Returns the fully rendered HTML or saves it to a file

## Anti-Bot Features

The scraper includes several techniques to bypass bot detection:
- Hides webdriver property
- Spoofs realistic browser properties (plugins, languages)
- Uses realistic user agent
- Configures viewport to common resolution
- Disables automation-controlled features

## Error Handling

The scraper handles various error scenarios:
- **Timeout Errors**: Returns `None` if page load exceeds timeout
- **Network Errors**: Returns `None` on connection failures
- **Invalid URLs**: Returns `None` for malformed URLs
- **Missing Dependencies**: Provides clear error messages

## Troubleshooting

### Browser fails to launch
```bash
uv run playwright install chromium
sudo apt-get install -y libdbus-1-3
```

### Timeout errors
Increase the timeout values:
```bash
--timeout 120000 --wait-after-load 5000
```

### Bot detection
Try running in non-headless mode to debug:
```bash
--no-headless
```

## License

See LICENSE file for details.
