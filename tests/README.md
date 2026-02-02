# Tests

This directory contains unit and integration tests for the skills project.

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration
├── data/                          # Test data for html-to-markdown
│   ├── moltbook.json              # Sample JSON input
│   ├── expected/                  # Expected output (baseline)
│   └── generated/                 # Generated output (for comparison)
├── unit/                          # Unit tests with mocked dependencies
│   ├── test_news_fetch.py         # Tests for news fetching
│   └── test_web_scrape.py         # Tests for web scraping
├── integration/                   # Integration tests (real requests)
│   ├── test_web_scrape_integration.py
│   └── test_html_to_markdown_docker.py  # Docker-based conversion test
└── test_html_to_markdown.sh      # Bash test script
```

## Running Tests

### All Tests
```bash
cd /home/robin/sources/skills
uv run pytest
```

### Specific Test Suite
```bash
# Unit tests only
uv run pytest tests/unit/

# Integration tests only
uv run pytest tests/integration/

# Specific test file
uv run pytest tests/integration/test_html_to_markdown_docker.py -v
```

### HTML to Markdown Docker Test

**Using Bash Script:**
```bash
cd /home/robin/sources/skills/tests
./test_html_to_markdown.sh
```

**Using Python/Pytest:**
```bash
cd /home/robin/sources/skills
uv run pytest tests/integration/test_html_to_markdown_docker.py -v -s
```

## HTML to Markdown Test Details

The `test_html_to_markdown_docker.py` test validates the complete Docker-based conversion workflow.

### Test Steps

1. **Start Docker Container** - Executes start-docker-container.sh
2. **Prepare Test Data** - Copies moltbook.json to temp_data/test/
3. **Execute Conversion** - Runs conversion in Docker container
4. **Move Results** - Copies generated .md files to data/generated/
5. **Compare Results** - Compares with data/expected/ baseline

### Expected Behavior

**First Run:**
- Creates baseline in `expected/` directory
- Test passes (baseline established)

**Subsequent Runs:**
- Compares generated output with baseline
- Test passes if output matches expected
- Test fails if differences detected (shows diff)

### Updating Baseline

```bash
# Delete expected files
rm -rf tests/data/expected/*.md

# Re-run test to create new baseline
./test_html_to_markdown.sh
```

## Troubleshooting

**Docker container not starting:**
```bash
docker ps
cd ../html-to-markdown/scripts && bash start-docker-container.sh
```

**Test fails with differences:**
- Review the diff output
- Update baseline if change is intentional

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run only unit tests
```bash
uv run pytest -m unit
```

### Run only integration tests (requires internet connection and Playwright browser)
```bash
uv run pytest -m integration
```

### Run tests with coverage
```bash
uv run pytest --cov=. --cov-report=html
```

### Run specific test file
```bash
uv run pytest tests/unit/test_web_scrape.py
```

### Run tests with verbose output
```bash
uv run pytest -v
```

## Test Requirements

- **Unit tests**: Only require pytest and pytest-mock
- **Integration tests**: Require Playwright and internet connection
  - Before running integration tests, install Playwright browsers:
    ```bash
    uv run playwright install chromium
    ```

## Writing Tests

- Use `@pytest.mark.unit` for unit tests
- Use `@pytest.mark.integration` for integration tests
- Follow the Arrange-Act-Assert pattern
- Use descriptive test names that explain what is being tested
- Mock external dependencies in unit tests
- Use fixtures from `conftest.py` for common test data
