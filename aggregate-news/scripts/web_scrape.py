"""
Web scraping module with support for bypassing blocks and JavaScript rendering.
"""
import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


@dataclass
class ScraperConfig:
    """Configuration for the web scraper."""
    url: str
    save_to_file: bool = False
    save_location: Optional[str] = None
    filename: str = "page.html"
    headless: bool = True
    timeout: int = 60000
    wait_after_load: int = 2000
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ScraperConfig':
        """Create ScraperConfig from a dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'ScraperConfig':
        """Load configuration from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)


def scrape_webpage(
    url: str,
    save_to_file: bool = False,
    save_location: Optional[str] = None,
    filename: str = "page.html",
    headless: bool = True,
    timeout: int = 60000,
    wait_after_load: int = 2000
) -> Optional[str]:
    """
    Scrape a webpage with JavaScript rendering and bypass common blocks.
    
    Args:
        url: The URL to scrape (required)
        save_to_file: Whether to save the scraped content to a file (default: False)
        save_location: Directory path where to save the file (required if save_to_file is True)
        filename: Name of the file to save (default: "page.html")
        headless: Whether to run browser in headless mode (default: True)
        timeout: Page load timeout in milliseconds (default: 60000)
        wait_after_load: Wait time after page load in milliseconds (default: 2000)
    
    Returns:
        The scraped HTML content as a string, or None if scraping failed
    
    Raises:
        ValueError: If save_to_file is True but save_location is not provided
    """
    if save_to_file and not save_location:
        raise ValueError("save_location is required when save_to_file is True")
    
    try:
        with sync_playwright() as playwright:
            # Launch browser with stealth settings to bypass detection
            browser = playwright.chromium.launch(
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )
            
            # Create context with realistic browser settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            # Add stealth JavaScript to avoid detection
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Override the plugins property
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Override the languages property
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
            """)
            
            page = context.new_page()
            
            # Navigate to the URL with a more forgiving wait strategy
            print(f"Navigating to {url}...")
            try:
                # Try networkidle first (best for most sites)
                page.goto(url, wait_until='networkidle', timeout=timeout)
            except PlaywrightTimeoutError:
                print(f"Warning: networkidle timeout, retrying with 'load' strategy...")
                try:
                    # Fallback to 'load' which just waits for DOM load event
                    page.goto(url, wait_until='load', timeout=timeout)
                except PlaywrightTimeoutError:
                    print(f"Warning: load timeout, retrying with 'domcontentloaded' strategy...")
                    # Last resort: just wait for DOM to be parsed
                    page.goto(url, wait_until='domcontentloaded', timeout=timeout)
            
            # Wait a bit more for any lazy-loaded content
            page.wait_for_timeout(wait_after_load)
            
            # Get the fully rendered HTML content
            content = page.content()
            print(f"Successfully scraped {len(content)} characters from {url}")
            
            # Save to file if requested
            if save_to_file:
                assert save_location is not None  # for type checker
                save_path = Path(save_location)
                save_path.mkdir(parents=True, exist_ok=True)
                
                file_path = save_path / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Saved content to {file_path}")
            
            browser.close()
            return content
            
    except PlaywrightTimeoutError as e:
        print(f"Timeout error: Failed to load {url} within the timeout period: {e}")
        return None
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Web scraper with JavaScript rendering and anti-bot bypass'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to JSON configuration file'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='URL to scrape'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save scraped content to file'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Directory to save output file (default: ./output)'
    )
    parser.add_argument(
        '--filename',
        type=str,
        default='page.html',
        help='Output filename (default: page.html)'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=60000,
        help='Page load timeout in milliseconds (default: 60000)'
    )
    parser.add_argument(
        '--wait-after-load',
        type=int,
        default=2000,
        help='Wait time after page load in milliseconds (default: 2000)'
    )
    
    args = parser.parse_args()
    
    # Load configuration from file if provided
    if args.config:
        try:
            config = ScraperConfig.from_json_file(args.config)
        except Exception as e:
            print(f"Error loading config file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Build config from command line arguments
        if not args.url:
            parser.error('Either --config or --url is required')
        
        config = ScraperConfig(
            url=args.url,
            save_to_file=args.save,
            save_location=args.output_dir if args.save else None,
            filename=args.filename,
            headless=not args.no_headless,
            timeout=args.timeout,
            wait_after_load=args.wait_after_load
        )
    
    # Perform scraping
    content = scrape_webpage(
        url=config.url,
        save_to_file=config.save_to_file,
        save_location=config.save_location,
        filename=config.filename,
        headless=config.headless,
        timeout=config.timeout,
        wait_after_load=config.wait_after_load
    )
    
    if content:
        if not config.save_to_file:
            print(content)
        sys.exit(0)
    else:
        print("Failed to scrape webpage", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
