import subprocess
import numpy as np
import whisper
import shutil
import logging
import warnings
from whisper.audio import log_mel_spectrogram
from math import ceil

warnings.filterwarnings("ignore", category=FutureWarning)

# Set up logging for the transcriber
logging.basicConfig(
    filename='logs/transcriber.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'
)

class Transcriber:
    def __init__(self):
        try:
            logging.info("Loading Whisper model...")
            self.model = whisper.load_model("base")
            logging.info("Whisper model loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading Whisper model: {e}")
            raise RuntimeError("Failed to load Whisper model")

    def transcribe(self, media_url):
        """
        Transcribes the audio from a media URL.

        :param media_url: URL to the media file
        :return: Transcription text
        """
        try:
            logging.info(f"Starting transcription for URL: {media_url}")

            # Convert media to WAV format and get audio data
            audio_data = self._fetch_audio(media_url)

            # Check if audio data is empty
            if not audio_data:
                raise ValueError("Audio data is empty after processing.")

            # Transcribe the audio data
            transcription = self._transcribe_audio(audio_data)

            logging.info(f"Transcription completed for URL: {media_url}")
            return transcription

        except Exception as e:
            logging.error(f"Transcription failed for URL {media_url}: {e}")
            raise

    def _fetch_audio(self, media_url):
        """
        Fetches the audio data from a media URL using FFmpeg.

        :param media_url: URL to the media file
        :return: Raw audio data as a NumPy array
        """
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            logging.error("FFmpeg is not available in the system path.")
            raise RuntimeError("FFmpeg is required but not installed.")

        command = [
            ffmpeg_path,
            '-i', media_url,
            '-f', 'wav',  # Force output to WAV format
            '-ac', '1',   # Ensure mono audio
            '-ar', '16000',  # Ensure 16kHz sample rate
            'pipe:1'  # Output to pipe
        ]

        try:
            logging.info(f"Running FFmpeg command: {' '.join(command)}")
            ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            audio_data, error = ffmpeg_process.communicate()

            if ffmpeg_process.returncode != 0:
                logging.error(f"FFmpeg failed: {error.decode('utf-8')}")
                raise RuntimeError(f"FFmpeg error: {error.decode('utf-8')}")

            logging.info("Audio data fetched successfully.")
            return np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        except Exception as e:
            logging.error(f"Error fetching audio data: {e}")
            raise

    def _transcribe_audio(self, audio_array):
        """
        Transcribes the given audio data.

        :param audio_array: Raw audio data as a NumPy array
        :return: Transcription text
        """
        try:
            if audio_array.ndim > 1:
                audio_array = audio_array.flatten()

            segment_length = 30 * 16000  # 30 seconds at 16kHz
            num_segments = ceil(len(audio_array) / segment_length)
            transcription = ""

            for i in range(num_segments):
                start = i * segment_length
                end = min((i + 1) * segment_length, len(audio_array))
                segment = audio_array[start:end]

                # Convert the segment to a mel spectrogram
                mel = log_mel_spectrogram(segment)

                # Transcribe the segment using Whisper
                options = whisper.DecodingOptions(fp16=False)  # Use fp32 for CPU compatibility
                result = self.model.decode(mel, options)

                transcription += result.text.strip() + " "
                logging.debug(f"Segment {i+1}/{num_segments} transcribed.")

            return transcription.strip()

        except Exception as e:
            logging.error(f"Error during transcription: {e}")
            raise

