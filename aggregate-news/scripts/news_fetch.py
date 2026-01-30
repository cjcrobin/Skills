"""
News fetching module for aggregating content from multiple sources.
"""
import argparse
import json
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum

from bs4 import BeautifulSoup

try:
    from .web_scrape import scrape_webpage
except ImportError:
    from web_scrape import scrape_webpage


class NewsSource(Enum):
    """Supported news sources."""
    HACKER_NEWS = "hacker_news"
    PRODUCT_HUNT = "product_hunt"
    ALL = "all"


@dataclass
class NewsItem():
    """Represents a news item from any source."""
    url: str
    title: str
    publish_time: datetime
    popularity: int
    source: str
    content: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def parse_hacker_news(html_content: str) -> List[NewsItem]:
    """
    Parse Hacker News front page HTML and extract news items.
    
    Args:
        html_content: HTML content from Hacker News
    
    Returns:
        List of NewsItem objects
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    items = []
    
    # Find all article rows
    article_rows = soup.find_all('tr', class_='athing')
    
    for article_row in article_rows:
        try:
            # Extract title and URL
            title_link = article_row.find('span', class_='titleline').find('a')
            if not title_link:
                continue
            
            title = title_link.text.strip()
            url = title_link.get('href', '')
            
            # Handle relative URLs
            if url.startswith('item?id='):
                url = f"https://news.ycombinator.com/{url}"
            
            # Get the next row which contains metadata
            meta_row = article_row.find_next_sibling('tr')
            if not meta_row:
                continue
            
            # Extract points
            score_span = meta_row.find('span', class_='score')
            points = 0
            if score_span:
                points_text = score_span.text
                points = int(points_text.split()[0]) if points_text else 0
            
            # Extract comment count and comments URL
            comments = 0
            comments_url = None
            comment_links = meta_row.find_all('a')
            for link in comment_links:
                link_text = link.text
                if 'comment' in link_text:
                    comment_parts = link_text.split()
                    if comment_parts[0].isdigit():
                        comments = int(comment_parts[0])
                    # Extract comments URL
                    href = link.get('href', '')
                    if href and 'item?id=' in href:
                        comments_url = f"https://news.ycombinator.com/{href}"
                    break
            
            # Extract time
            time_elem = meta_row.find('span', class_='age')
            publish_time = time_elem.get('title', '') if time_elem else None
            iso_part, ts_part = publish_time.split() if isinstance(publish_time, str) else (None, None)
            
            # Calculate popularity (points + comments as a simple metric)
            popularity = points + comments
            
            # Build additional metadata
            additional_metadata = {}
            if comments_url:
                additional_metadata['comments_url'] = comments_url
            additional_metadata['points'] = points
            additional_metadata['comments'] = comments

            
            items.append(NewsItem(
                url=url,
                title=title,
                publish_time=datetime.fromtimestamp(int(ts_part)) if ts_part else (datetime.now() - timedelta(days=7)),
                popularity=popularity,
                source="hacker_news",
                additional_metadata=additional_metadata if additional_metadata else None
            ))
        except Exception as e:
            print(f"Error parsing Hacker News item: {e}", file=sys.stderr)
            continue
    
    return items


def parse_product_hunt(html_content: str) -> List[NewsItem]:
    """
    Parse Product Hunt feed HTML and extract news items.
    
    Args:
        html_content: HTML content from Product Hunt
    
    Returns:
        List of NewsItem objects
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    items = []
    
    # Product Hunt structure may vary, using common patterns
    # Look for post links
    post_links = soup.find_all('a', href=True)
    seen_urls = set()
    
    for link in post_links:
        try:
            href = link.get('href', '')
            
            # Filter for product post links
            if '/posts/' not in href:
                continue
            
            # Build full URL
            if href.startswith('/'):
                url = f"https://www.producthunt.com{href}"
            elif href.startswith('http'):
                url = href
            else:
                continue
            
            # Skip duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Extract title (from link text or nearby elements)
            title = link.text.strip()
            if not title or len(title) < 3:
                # Try to find title in parent or sibling elements
                parent = link.find_parent(['div', 'article', 'section'])
                if parent:
                    heading = parent.find(['h1', 'h2', 'h3', 'h4'])
                    if heading:
                        title = heading.text.strip()
            
            if not title or len(title) < 3:
                continue
            
            # Product Hunt doesn't always show exact publish time on feed
            # Using current date as placeholder
            publish_time = datetime.now()
            
            # Default popularity for Product Hunt items
            popularity = 10
            
            items.append(NewsItem(
                url=url,
                title=title,
                publish_time=publish_time,
                popularity=popularity,
                source="product_hunt"
            ))
            
        except Exception as e:
            print(f"Error parsing Product Hunt item: {e}", file=sys.stderr)
            continue
    
    return items


def fetch_news_metadata(
    source: NewsSource,
    limit: int = 10,
    keywords: Optional[List[str]] = None
) -> Dict[NewsSource, List[NewsItem]]:
    """
    Fetch news metadata from specified source(s).
    
    Args:
        source: News source to fetch from
        limit: Maximum number of items to return per source
        keywords: Optional list of keywords to filter by
    
    Returns:
        List of NewsItem objects with metadata only
    """
    items: Dict[NewsSource, List[NewsItem]] = {}
    
    if source in [NewsSource.HACKER_NEWS, NewsSource.ALL]:
        print("Fetching from Hacker News...")
        html = scrape_webpage(
            url="https://news.ycombinator.com/front",
            timeout=30000,
            wait_after_load=2000
        )
        
        if html:
            hn_items = parse_hacker_news(html)
            items[NewsSource.HACKER_NEWS] = hn_items
        else:
            print("Failed to fetch Hacker News", file=sys.stderr)
    
    if source in [NewsSource.PRODUCT_HUNT, NewsSource.ALL]:
        print("Fetching from Product Hunt...")
        html = scrape_webpage(
            url="https://www.producthunt.com/feed",
            timeout=30000,
            wait_after_load=3000
        )
        
        if html:
            ph_items = parse_product_hunt(html)
            items[NewsSource.PRODUCT_HUNT] = ph_items
        else:
            print("Failed to fetch Product Hunt", file=sys.stderr)
    
    # Filter by keywords if provided
    if keywords:
        keywords_lower = [k.lower() for k in keywords]
        
        for key in items:
            filtered_items: List[NewsItem] = []
            for item in items[key]:
                title_lower = item.title.lower()
                if any(keyword in title_lower for keyword in keywords_lower):
                    filtered_items.append(item)
            filtered_items.sort(key=lambda x: x.publish_time or "", reverse=True)
            filtered_items.sort(key=lambda x: x.popularity, reverse=True)
            if key == NewsSource.HACKER_NEWS:
                filtered_items = [item for item in filtered_items if item.popularity >= 250][:limit]
            else:
                filtered_items = filtered_items[:limit]
            items[key] = filtered_items
            print(f"Filtered to {len(items[key])} items matching keywords: {', '.join(keywords)}")
    else:
        for key in items:
            items[key].sort(key=lambda x: x.publish_time or "", reverse=True)
            items[key].sort(key=lambda x: x.popularity, reverse=True)
            if key == NewsSource.HACKER_NEWS:
                items[key] = [item for item in items[key] if item.popularity >= 250][:limit]
            else:
                print(f"Selecting top {limit} items from {key.value}, having {len(items[key])} items")
                items[key] = items[key][:limit]
            print(f"Selected top {len(items[key])} items from {key.value}")
    return items


def fetch_article_content(url: str) -> Optional[str]:
    """
    Fetch the full content of an article.
    
    Args:
        url: URL of the article to fetch
    
    Returns:
        HTML content of the article, or None if fetch failed
    """
    print(f"Fetching content from {url}...")
    return scrape_webpage(
        url=url,
        timeout=30000,
        wait_after_load=2000
    )


def fetch_news_with_content(
    source: NewsSource,
    limit: int = 10,
    keywords: Optional[List[str]] = None,
    max_workers: int = 5
) -> Dict[NewsSource, List[NewsItem]]:
    """
    Fetch news items with full content in parallel.
    
    Args:
        source: News source to fetch from
        limit: Maximum number of items to return per source
        keywords: Optional list of keywords to filter by
        max_workers: Maximum number of parallel workers (default: 5)
    
    Returns:
        Dict of NewsSource to list of NewsItem objects with content populated
    """
    # First get metadata
    items: Dict[NewsSource, List[NewsItem]] = fetch_news_metadata(source, limit, keywords)
    
    if not items:
        return items
    
    # Then fetch content for each item in parallel
    total: int = sum(len(v) for v in items.values())
    print(f"\nFetching content for {total} articles in parallel (max {max_workers} workers)...")
    
    def fetch_with_index(index_item_tuple):
        """Helper function to fetch content with index for progress tracking."""
        key, index, item = index_item_tuple
        
        # Add random wait time to avoid being blocked (30-60 seconds)
        wait_time = random.uniform(30, 60)
        print(f"key: {key} - [{index + 1}/{len(items[key])}] Waiting {wait_time:.1f}s before fetching...")
        time.sleep(wait_time)
        
        print(f"key: {key} - [{index + 1}/{len(items[key])}] Fetching: {item.title[:60]}...")
        content = fetch_article_content(item.url)
        
        # Also fetch comments if available
        comments_content = None
        if item.additional_metadata and 'comments_url' in item.additional_metadata:
            comments_url = item.additional_metadata['comments_url']
            print(f"key: {key} - [{index + 1}/{len(items[key])}] Fetching comments from {comments_url}...")
            comments_content = fetch_article_content(comments_url)
        
        return key, index, content, comments_content
    
    # Use ThreadPoolExecutor for parallel fetching
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(fetch_with_index, (key, i, item)): (key, i)
            for key, value in items.items()
                for i, item in enumerate(value)
        }
        
        # Process completed tasks
        for future in as_completed(future_to_index):
            try:
                key, index, content, comments_content = future.result()
                items[key][index].content = content
                
                # Store comments content in additional_metadata
                if comments_content:
                    if items[key][index].additional_metadata is None:
                        items[key][index].additional_metadata = {}
                    items[key][index].additional_metadata['comments_content'] = comments_content
                    print(f"key: {key} - [{index + 1}/{len(items[key])}] ✓ Completed (with comments): {items[key][index].title[:60]}")
                elif content:
                    print(f"key: {key} - [{index + 1}/{len(items[key])}] ✓ Completed: {items[key][index].title[:60]}")
                else:
                    print(f"[{index + 1}/{len(items[key])}] ✗ Failed: {items[key][index].title[:60]}")
            except Exception as e:
                (key, index) = future_to_index[future]
                print(f"[{index + 1}/{len(items[key])}] ✗ Error fetching {items[key][index].title[:60]}: {e}")
                items[key][index].content = None
    
    print(f"\nCompleted fetching content for {len(items)} articles")
    return items


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Fetch news from multiple sources (Hacker News, Product Hunt)'
    )
    parser.add_argument(
        '--source',
        type=str,
        choices=['hacker_news', 'product_hunt', 'all'],
        default='all',
        help='News source to fetch from (default: all)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of items to return per source (default: 10)'
    )
    parser.add_argument(
        '--content',
        action='store_true',
        help='Fetch full content for each article (slower)'
    )
    parser.add_argument(
        '--keywords',
        type=str,
        help='Comma-separated keywords to filter articles'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output folder path. If not specified, prints to stdout'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty print JSON output'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Maximum number of parallel workers for content fetching (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Parse source
    source = NewsSource(args.source)
    
    # Parse keywords
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    
    # Fetch news
    if args.content:
        items = fetch_news_with_content(source, args.limit, keywords, args.workers)
    else:
        items = fetch_news_metadata(source, args.limit, keywords)
    
    # Output results
    indent = 2 if args.pretty else None
    for key in items:
        if args.output:
            for item in items[key]:
                json_data: str = json.dumps(item.to_dict(), default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o), indent=indent)
                folder_path = os.path.join(args.output, str(datetime.now().date()), str(key))
                save_content_to_file(json_data, folder_path, f"{item.title.lower().replace(' ', '_')}.json") 
        else:
            for item in items[key]:
                print_content_to_stdout(json.dumps(item.to_dict(), default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o), indent=indent))
    
    print(f"\nTotal items fetched: {len(items)}")
    sys.exit(0)

def save_content_to_file(content: str, save_path: str, filename: str) -> None:
    """
    Save content to a specified file.
    
    Args:
        content: Content to save
        save_path: Directory path to save the file
        filename: Name of the file
    """
    from pathlib import Path
    folder: Path = Path(save_path)
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved content to {file_path}")

def print_content_to_stdout(content: str) -> None:
    """
    Print content to standard output.
    
    Args:
        content: Content to print
    """
    print(content)

if __name__ == "__main__":
    main()
