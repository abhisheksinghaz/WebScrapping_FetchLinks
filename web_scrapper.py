import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import sys
from typing import Dict, List, Any
import time

class WebScraper:
    def __init__(self, url: str, timeout: int = 10):
        """
        Initialize the web scraper.

        Args:
            url: The URL to scrape
            timeout: Request timeout in seconds
        """
        self.url = url
        self.timeout = timeout
        self.soup = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_page(self) -> bool:
        """
        Fetch the webpage content.

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Fetching {self.url}...")
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            print(f"✓ Successfully fetched the page")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching the page: {e}")
            return False

    def extract_text_content(self) -> str:
        """Extract all text content from the page."""
        if not self.soup:
            return ""

        # Remove script and style elements
        for script in self.soup(["script", "style"]):
            script.decompose()

        text = self.soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def extract_headings(self) -> Dict[str, List[str]]:
        """Extract all headings from the page."""
        if not self.soup:
            return {}

        headings = {}
        for level in range(1, 7):
            tag = f'h{level}'
            heading_list = [h.get_text(strip=True) for h in self.soup.find_all(tag)]
            if heading_list:
                headings[tag] = heading_list

        return headings

    def extract_links(self) -> List[Dict[str, str]]:
        """Extract all links from the page."""
        if not self.soup:
            return []

        links = []
        for a_tag in self.soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            # Convert relative URLs to absolute URLs
            absolute_url = urljoin(self.url, href)
            links.append({
                'text': text,
                'url': absolute_url,
                'relative_url': href
            })

        return links

    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extract all tables from the page."""
        if not self.soup:
            return []

        tables = []
        for idx, table in enumerate(self.soup.find_all('table')):
            table_data = {
                'table_index': idx,
                'headers': [],
                'rows': []
            }

            # Extract headers
            thead = table.find('thead')
            if thead:
                for th in thead.find_all('th'):
                    table_data['headers'].append(th.get_text(strip=True))

            # Extract rows
            tbody = table.find('tbody')
            rows_container = tbody if tbody else table

            for tr in rows_container.find_all('tr'):
                row = []
                for td in tr.find_all(['td', 'th']):
                    row.append(td.get_text(strip=True))
                if row:
                    table_data['rows'].append(row)

            tables.append(table_data)

        return tables

    def extract_metadata(self) -> Dict[str, str]:
        """Extract metadata from the page."""
        if not self.soup:
            return {}

        metadata = {}

        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)

        # Meta tags
        meta_tags = self.soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[f'meta_{name}'] = content

        return metadata

    def extract_code_blocks(self) -> List[Dict[str, str]]:
        """Extract code blocks from the page."""
        if not self.soup:
            return []

        code_blocks = []

        # Look for code tags and pre tags
        for idx, pre in enumerate(self.soup.find_all(['pre', 'code'])):
            code_blocks.append({
                'index': idx,
                'type': pre.name,
                'content': pre.get_text()
            })

        return code_blocks

    def extract_paragraphs(self) -> List[str]:
        """Extract all paragraphs from the page."""
        if not self.soup:
            return []

        return [p.get_text(strip=True) for p in self.soup.find_all('p')]

    def extract_lists(self) -> Dict[str, List[List[str]]]:
        """Extract ordered and unordered lists from the page."""
        if not self.soup:
            return {}

        lists_data = {'ul': [], 'ol': []}

        for ul in self.soup.find_all('ul'):
            items = [li.get_text(strip=True) for li in ul.find_all('li', recursive=False)]
            if items:
                lists_data['ul'].append(items)

        for ol in self.soup.find_all('ol'):
            items = [li.get_text(strip=True) for li in ol.find_all('li', recursive=False)]
            if items:
                lists_data['ol'].append(items)

        return lists_data

    def extract_images(self) -> List[Dict[str, str]]:
        """Extract all images from the page."""
        if not self.soup:
            return []

        images = []
        for img in self.soup.find_all('img'):
            img_data = {
                'alt': img.get('alt', ''),
                'src': urljoin(self.url, img.get('src', '')),
                'title': img.get('title', '')
            }
            images.append(img_data)

        return images

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape all data from the page."""
        if not self.fetch_page():
            return None

        print("\nExtracting data...\n")

        all_data = {
            'url': self.url,
            'metadata': self.extract_metadata(),
            'headings': self.extract_headings(),
            'paragraphs': self.extract_paragraphs(),
            'links': self.extract_links(),
            'images': self.extract_images(),
            'tables': self.extract_tables(),
            'lists': self.extract_lists(),
            'code_blocks': self.extract_code_blocks(),
            'full_text': self.extract_text_content()
        }

        return all_data

    def save_to_json(self, data: Dict[str, Any], filename: str = None):
        """Save scraped data to a JSON file."""
        if filename is None:
            # Generate filename from domain
            domain = urlparse(self.url).netloc
            filename = f"{domain}_scraped_data.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Data saved to {filename}")
        except Exception as e:
            print(f"✗ Error saving to file: {e}")

    def print_summary(self, data: Dict[str, Any]):
        """Print a summary of scraped data."""
        if not data:
            return

        print("\n" + "="*60)
        print("SCRAPING SUMMARY")
        print("="*60)

        print(f"\nURL: {data['url']}")

        if data['metadata']:
            print(f"\nTitle: {data['metadata'].get('title', 'N/A')}")
            print(f"Description: {data['metadata'].get('meta_description', 'N/A')}")

        print(f"\nHeadings found: {sum(len(v) for v in data['headings'].values())}")
        print(f"Paragraphs found: {len(data['paragraphs'])}")
        print(f"Links found: {len(data['links'])}")
        print(f"Images found: {len(data['images'])}")
        print(f"Tables found: {len(data['tables'])}")
        print(f"Code blocks found: {len(data['code_blocks'])}")
        print(f"Lists found: {len(data['lists']['ul']) + len(data['lists']['ol'])}")
        print(f"Total text content: {len(data['full_text'])} characters")

        print("\n" + "="*60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <URL> [output_file.json]")
        print("Example: python web_scraper.py https://example.com scraped_data.json")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    scraper = WebScraper(url)
    data = scraper.scrape_all()

    if data:
        scraper.print_summary(data)
        scraper.save_to_json(data, output_file)
        print("\n✓ Scraping completed successfully!")
    else:
        print("\n✗ Scraping failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()