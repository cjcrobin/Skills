---
name: aggregate-news
description: Collect content from different sources, including Hacker News, Product Hunt, etc. and save the original file (HTML) in local storage. Use when user mentions "收集新闻", "收集Hacker News", "Hacker News", "收集Product Hunt", "Product Hunt", "aggregate news", "fetch news", or wants to collect and filter tech news articles by keywords.
---

# Aggregate News Skill

This skill collects news articles from popular tech sources (Hacker News, Product Hunt) and saves them locally with metadata and optional full content.

## Supported Sources

- **Hacker News**: Front page stories with points, comments, and metadata
- **Product Hunt**: Latest product launches and updates

## Workflow

Follow the following steps when the user requests to collect news. If there is more than one option, don't assume the choice, please use the vscode.window.showQuickPick to ask user to select the option. if user doesn't select in 5 seconds, continue with the first option. 

### Step 1: Determine Sources

If the user didn't specify sources:
1. Ask user to select sources using an interactive prompt: "Which sources would you like to fetch from? (1) All sources, (2) Product Hunt, (3) Hacker News"
2. Wait 5 seconds for response
3. If no response, default to **all sources**

### Step 2: Load Preferences

Load user preferences in this order:
1. Check for `{SKILL_ROOT}/PREFERENCE.md` (project-level)
2. If not found, check for `~/.copilot/PREFERENCE.md` (user-level)
3. If neither exists, create `{SKILL_ROOT}/PREFERENCE.md` and prompt user for:
   - **limit**: Number of articles per source (default: 10)
   - **fetch_content**: Whether to fetch full article content (default: false, as it's slower)
   - **storage_location**: Base path for saving articles (default: ~/articles)

Example preference file format:
```markdown
# News Aggregation Preferences

- **limit**: 20
- **fetch_content**: false
- **storage_location**: ~/tech-news
```

### Step 3: Keyword Filtering

If user didn't specify keywords:
1. Ask: "What keywords would you like to filter for? (leave empty for no filtering)"
2. If user provides a keyword (e.g., "AI"), expand it to 10 related terms for better coverage

**Keyword Expansion Examples:**
- "AI" → AI, Artificial Intelligence, Machine Learning, Deep Learning, Neural Network, LLM, GPT, Agent, OpenAI, Claude
- "Web3" → Web3, Blockchain, Crypto, NFT, DeFi, Smart Contract, Ethereum, Decentralized, DAO, Token
- "Startup" → Startup, Founder, Entrepreneurship, Venture Capital, YC, Seed Round, MVP, Launch, Growth Hacking, SaaS

Use semantic expansion to find the most relevant related terms in the tech domain.

### Step 4: Execute News Fetch

Execute the news fetch using Docker to ensure all dependencies are properly installed. The location of this **SKILL.md** file is defined as {{SKILL_DIR}}.

**Step 4.1: Build Docker Image**
PLEASE MAKE SURE THE bash SCRIPT IS EXECUTED IN THE **{{SKILL_DIR}}**
execute script ./scripts/start-docker-container.sh

**Step 4.2: Run the Python Script in Docker**
use the docker exec to run the python script in the docker container. the argument should be correctly provided via the REFERENCE.md or user input. BUT PLEASE DON'T CHANGE THE --output PARAMETER, that is the path in the docker container.

Example：
```bash
docker exec aggregate-news-container \
  sh -c "uv run python news_fetch.py \
           --source all \
           --limit [number from preferences] \
           --keywords '[expanded keywords comma-separated]' \
           [--content if fetch_content is true] \
           --output /app/temp_data \
           --pretty"
```

**Step 4.3: Copy the file from the mounted folder to target folder**
The mounted folder is the {{SKILL_DIR}}/temp_data. Copy all the files in the mounted folder to the target folder defined in the REFERENCE.md or provided by users.  

**File Storage Convention:**
All articles must be saved following this structure:
```
{storage_location}/{YYYY-MM-DD}/{source_name}/{sanitized_title}.json
```

Examples:
- `~/articles/2026-01-29/HackerNews/introducing-mcp-protocol.json`
- `~/articles/2026-01-29/ProductHunt/new-ai-productivity-tool.json`

**Notes:**
- The `-v ~/articles:/articles` flag maps your local articles directory to the container
- The `-v $(pwd):/app` flag maps the current directory to /app in the container
- Dependencies are installed inside the container before running the script
- The `--rm` flag automatically removes the container after execution

### Step 5: Report Results

Provide a summary:
```
✓ Fetched [N] articles from [sources]
✓ Filtered by keywords: [keyword list]
✓ Saved to: {storage_location}/{date}/
  - HackerNews: [N] articles
  - ProductHunt: [N] articles
```

## Script Reference

The `news_fetch.py` script accepts these arguments:

- `--source`: Source to fetch from (hacker_news, product_hunt, all)
- `--limit`: Maximum number of items per source (default: 10)
- `--content`: Fetch full article content (slower, optional)
- `--keywords`: Comma-separated keywords for filtering
- `--output`: Output file path for JSON results
- `--pretty`: Pretty print JSON output
- `--workers`: Number of parallel workers for content fetching (default: 5)

## Example Interactions

**Example 1: Basic usage**
```
User: "收集Hacker News"
Assistant: Fetches 10 items from Hacker News using default preferences
```

**Example 2: With keywords**
```
User: "Collect news about AI from all sources"
Assistant: Expands "AI" to related terms, fetches from all sources, filters by keywords
```

**Example 3: Custom configuration**
```
User: "Get 30 articles from Product Hunt about Web3, save to ~/my-news"
Assistant: Uses limit=30, expands "Web3" keywords, saves to specified location
```

## Notes

- Fetching full content (`--content` flag) is significantly slower as it scrapes each article individually
- The script uses parallel workers for content fetching to improve performance
- Keywords are case-insensitive and matched against article titles
- Articles are sorted by popularity (points + comments for HN, default score for PH)
- Duplicate URLs are automatically filtered out

