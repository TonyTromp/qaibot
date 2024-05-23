import requests
import logging
import sys
from bs4 import BeautifulSoup
import argparse
import re

try:
    from bot.integrations.openai_chat import process_text_with_gpt
except ImportError:
    from openai_chat import process_text_with_gpt


def validate_url(url):
    """Validate the URL format using a regular expression."""
    logging.info(f"validate_url: Validating URL: {url}.")
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http://, https://, or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain names
        r'[A-Z]{2,6}\.?|'  # top level domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # path
    return re.match(regex, url) is not None



def fetch_website_content(url):
    """Fetches and cleans website content from a URL."""
    logging.info(f"fetch_website_content: Fetching content from {url}.")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    headers = {
        "User-Agent": user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com",
        "Cache-Control": "no-cache",
    }
    try:
        response = requests.get(url, headers=headers)
        logging.info(f"fetch_website_content: Received response from {url}: {response.status_code}")
        response.raise_for_status()  # raise exception for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted tag elements
        for script in soup(["script", "style", "header", "footer", "nav", "form"]):
            script.decompose()

        # Get text from the HTML
        text = ' '.join(soup.stripped_strings)
        return text
    except Exception as e:
        logging.error(f"fetch_website_content: Failed to fetch or clean the website content: {e}")
        return None


def summarize_text(text, context_for_summary):
    """Use the LLM to generate a summary based on the extracted text."""
    logging.info("summarize_text: Summarizing the text with GPT")
    # add the context to the prompt
    system_prompt = context_for_summary
    return process_text_with_gpt(text, system_prompt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch and summarize website content.")
    parser.add_argument('url', type=str, help='The URL of the website to summarize')
    args = parser.parse_args()

    if not validate_url(args.url):
        print("Invalid URL provided.")
        sys.exit(1)

    content = fetch_website_content(args.url)
    if content:
        summary = summarize_text(content, "Please summarize this text:")
        print(summary)
    else:
        print("Failed to fetch content from the URL.")


def magic_summarize(url):
    """Fetch and summarize website content."""
    logging.info(f"fetch_website_content: Fetching content from {url}.")
    
    if not validate_url(url):
        print("Invalid URL provided.")
        sys.exit(1)

    content = fetch_website_content(url)
    if content:
        summary = summarize_text(content, "Please summarize this text:")
        print(summary)
    else:
        print("Failed to fetch content from the URL.")
