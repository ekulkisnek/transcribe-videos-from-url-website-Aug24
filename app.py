from flask import Flask, request, jsonify, render_template, Response
from transcriber.transcriber import Transcriber
from media_extractor.media_extractor import MediaExtractor
import logging

# Set up logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'
)

app = Flask(__name__)

# Create an instance of the MediaExtractor and Transcriber
extractor = MediaExtractor()  # No headless argument needed now
transcriber = Transcriber()

@app.route('/')
def index():
    """
    Renders the index page where users can input a URL to start transcription.
    """
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Failed to render index page: {e}")
        return "An error occurred while loading the page.", 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Handles the transcription request. Receives a URL, attempts to extract media URLs if necessary,
    and streams and transcribes the media content.
    """
    try:
        data = request.json
        logging.info(f"Request data received: {data}")

        url = data.get('url')
        if not url:
            logging.warning("No URL provided in the request.")
            return jsonify({"error": "No URL provided."}), 400

        logging.info(f"Transcription requested for URL: {url}")

        # Attempt to extract media URLs from the given URL
        media_urls = extractor.extract_media_urls_static(url)
        if not media_urls:
            logging.warning(f"No media URLs found for {url}")
            return jsonify({"error": f"No media URLs found for {url}"}), 400

        def generate_transcription():
            """
            Generator function to stream and transcribe media, yielding the transcription chunks.
            """
            for media_url in media_urls:
                try:
                    logging.info(f"Starting transcription for media URL: {media_url}")
                    transcription = transcriber.transcribe(media_url)
                    yield transcription
                    logging.info(f"Completed transcription for media URL: {media_url}")
                except Exception as e:
                    logging.error(f"Error during transcription of {media_url}: {e}")
                    yield f"Error during transcription: {str(e)}\n"

        return Response(generate_transcription(), mimetype='text/plain')

    except Exception as e:
        logging.error(f"Failed to process transcription: {e}")
        return jsonify({"error": f"An error occurred during transcription: {str(e)}"}), 500


if __name__ == '__main__':
    try:
        logging.info("Starting the Transcribe Web Media app.")
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        logging.critical(f"Failed to start the app: {e}")
