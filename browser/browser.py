import logging
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Set up logging
logging.basicConfig(
    filename='browser.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'  # Overwrite the log file each run; use 'a' to append.
)

class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Embedded Browser')
        self.urlChanged.connect(self.log_url_change)
        logging.info("Browser initialized.")

    def load_url(self, url):
        """
        Load a given URL into the browser.
        """
        try:
            logging.info(f"Loading URL: {url}")
            self.setUrl(QUrl(url))
        except Exception as e:
            logging.error(f"Error loading URL {url}: {e}")
            raise

    def log_url_change(self, url):
        """
        Log the change of URL.
        """
        logging.info(f"URL changed to: {url.toString()}")

    def start_video_transcription(self, transcription_thread):
        """
        Trigger the start of the transcription process when the video starts playing.
        This function would need to be triggered by an event that detects when a video is playing.
        """
        try:
            logging.info("Starting transcription thread.")
            transcription_thread.start()
        except Exception as e:
            logging.error(f"Error starting transcription thread: {e}")
            raise

    def stop_transcription(self, transcription_thread):
        """
        Stop the transcription process.
        """
        try:
            logging.info("Stopping transcription thread.")
            transcription_thread.terminate()
        except Exception as e:
            logging.error(f"Error stopping transcription thread: {e}")
            raise
