# Web Scraper Script

A comprehensive Python web scraping tool that extracts all types of data from any webpage.

## Installation

First, install the required dependencies:

```bash
pip install requests beautifulsoup4
```

## Usage

### Command Line

```bash
python web_scraper.py <URL> [output_file.json]
```

### Examples

```bash
# Basic usage - saves to auto-generated filename
python web_scraper.py https://docs.capillarytech.com/reference/apioverview

# Save to custom filename
python web_scraper.py https://docs.capillarytech.com/reference/apioverview my_data.json

# Example with another site
python web_scraper.py https://example.com scraped_data.json
```

## Features

The script extracts the following data from any webpage:

- **Metadata**: Title, description, and all meta tags
- **Headings**: All H1-H6 headings organized by level
- **Paragraphs**: All text content in `<p>` tags
- **Links**: All URLs (converted to absolute URLs) with anchor text
- **Images**: Image sources and alt text
- **Tables**: Structured table data with headers and rows
- **Lists**: Both ordered and unordered lists
- **Code Blocks**: All `<pre>` and `<code>` sections
- **Full Text**: Complete cleaned text content from the page

## Output

The script creates a JSON file containing all extracted data with this structure:

```json
{
  "url": "https://example.com",
  "metadata": {
    "title": "Page Title",
    "meta_description": "Page description"
  },
  "headings": {
    "h1": ["Main Heading"],
    "h2": ["Sub Heading 1", "Sub Heading 2"]
  },
  "paragraphs": ["Text of first paragraph", "Text of second paragraph"],
  "links": [
    {
      "text": "Click here",
      "url": "https://example.com/page",
      "relative_url": "/page"
    }
  ],
  "images": [
    {
      "alt": "Image description",
      "src": "https://example.com/image.jpg",
      "title": "Image title"
    }
  ],
  "tables": [
    {
      "table_index": 0,
      "headers": ["Column 1", "Column 2"],
      "rows": [["Value 1", "Value 2"]]
    }
  ],
  "lists": {
    "ul": [["Item 1", "Item 2"]],
    "ol": [["First", "Second"]]
  },
  "code_blocks": [
    {
      "index": 0,
      "type": "pre",
      "content": "code content"
    }
  ],
  "full_text": "Complete cleaned text content..."
}
```

## Python API Usage

You can also use the script as a module in your own Python code:

```python
from web_scraper import WebScraper

# Create scraper instance
scraper = WebScraper("https://docs.capillarytech.com/reference/apioverview")

# Scrape all data
data = scraper.scrape_all()

# Or extract specific data
headings = scraper.extract_headings()
links = scraper.extract_links()
tables = scraper.extract_tables()

# Save to file
scraper.save_to_json(data, "output.json")

# Print summary
scraper.print_summary(data)
```

## Advanced Usage

Extract specific data types:

```python
scraper = WebScraper("https://example.com")
scraper.fetch_page()

# Extract individual elements
text = scraper.extract_text_content()
headings = scraper.extract_headings()
links = scraper.extract_links()
tables = scraper.extract_tables()
images = scraper.extract_images()
code = scraper.extract_code_blocks()
lists = scraper.extract_lists()
metadata = scraper.extract_metadata()
```

## Error Handling

The script handles common errors gracefully:

- Network timeouts (default 10 seconds)
- Invalid URLs
- Connection errors
- File writing errors

All errors are reported with clear messages.

## Notes

- The script uses a standard User-Agent header to avoid being blocked
- Relative URLs are converted to absolute URLs
- JavaScript-generated content won't be captured (static HTML only)
- Script and style elements are removed before text extraction
- Whitespace is cleaned up automatically
- Default timeout is 10 seconds (can be customized)

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library
