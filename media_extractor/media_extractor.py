import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(
    filename='logs/media_extractor.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'
)

class MediaExtractor:
    def __init__(self):
        """
        Initialize the MediaExtractor.
        """
        logging.info(f"MediaExtractor initialized.")

    def extract_media_urls_static(self, url):
        """
        Extract media URLs from a static web page using BeautifulSoup.

        :param url: The URL of the web page to extract media URLs from.
        :return: List of media URLs extracted from the page.
        """
        logging.info(f"Attempting to extract media URLs from: {url}")
        media_urls = []

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Log the HTML content for debugging
            logging.debug(f"HTML content of the page: {soup.prettify()}")

            # Extract URLs from <iframe> tags
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src')
                if src and 'bitchute' in src:
                    media_urls.append(src)

            # Extract URLs from <script> tags that might be loading video players
            for script in soup.find_all('script'):
                if script.string and 'video' in script.string:
                    logging.debug(f"Found potential video script: {script.string}")
                    # Extract video URLs or identifiers from the script
                    # This may require custom parsing based on how the script loads the video

            # Extract URLs from <embed> tags
            for embed in soup.find_all('embed'):
                src = embed.get('src')
                if src and src.startswith('http'):
                    media_urls.append(src)

            # Filter out non-media URLs
            media_urls = self._filter_valid_media_urls(media_urls)

            logging.info(f"Extracted media URLs: {media_urls}")
            return media_urls

        except requests.RequestException as e:
            logging.error(f"Error fetching URL: {e}")
            return []




    def _filter_valid_media_urls(self, urls):
        """
        Filters a list of URLs to include only valid media URLs based on file extensions and content type.

        :param urls: List of URLs to filter.
        :return: Filtered list of valid media URLs.
        """
        valid_extensions = ('.mp4', '.m4a', '.mov', '.avi', '.flv', '.wmv', '.mp3', '.wav', '.webm')
        media_urls = []

        for url in urls:
            if url.lower().endswith(valid_extensions):
                media_urls.append(url)
            else:
                try:
                    response = requests.head(url, allow_redirects=True)
                    content_type = response.headers.get('Content-Type', '')
                    if 'video' in content_type or 'audio' in content_type:
                        media_urls.append(url)
                except Exception as e:
                    logging.warning(f"Error validating URL {url}: {e}")

        logging.info(f"Filtered valid media URLs: {media_urls}")
        return media_urls

    def close(self):
        """
        Clean up any resources used by the MediaExtractor.
        """
        logging.info("MediaExtractor cleanup complete.")

# Example usage:
# extractor = MediaExtractor()
# urls = extractor.extract_media_urls_static('http://example.com')
# print(urls)
# extractor.close()
