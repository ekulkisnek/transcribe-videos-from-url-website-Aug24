from flask import Flask, request, render_template, Response
from media_extractor import extract_media_urls, extract_media_urls_dynamic
from transcriber import stream_and_transcribe

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    url = data['url']
    media_urls = extract_media_urls(url)

    if not media_urls:
        media_urls = extract_media_urls_dynamic(url)

    if not media_urls:
        return Response("No media URLs found", status=400)

    def generate_transcription():
        for media_url in media_urls:
            try:
                for transcription_chunk in stream_and_transcribe(media_url):
                    yield transcription_chunk  # Send only the text without any additional info
            except Exception as e:
                yield f"Error: {str(e)}\n"

    return Response(generate_transcription(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
