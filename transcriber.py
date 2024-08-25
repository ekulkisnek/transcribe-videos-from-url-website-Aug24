import subprocess
import numpy as np
import whisper
import shutil
from whisper.audio import log_mel_spectrogram
from math import ceil

# Load the Whisper model
model = whisper.load_model("base")

def stream_and_transcribe(media_url):
    # Locate the ffmpeg binary dynamically
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("FFmpeg is not available in the system path.")

    # FFmpeg command to stream the media and convert to wav format
    command = [
        ffmpeg_path,
        '-i', media_url,
        '-f', 'wav',  # Force output to wav format
        '-ac', '1',   # Ensure mono audio
        '-ar', '16000',  # Ensure 16kHz sample rate
        'pipe:1'  # Output to pipe
    ]

    # Capture the output from FFmpeg
    ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    audio_data, error = ffmpeg_process.communicate()

    # Debugging: Check the audio data
    print("FFmpeg stderr output:", error.decode('utf-8'))
    print("Audio data length:", len(audio_data))

    # Convert the audio byte stream to a NumPy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

    # Check and handle incorrect audio shapes
    if audio_array.ndim > 1:
        audio_array = audio_array.flatten()

    if audio_array.size == 0:
        raise ValueError("Audio data is empty after processing.")

    # Normalize audio to the range expected by Whisper
    audio_array = audio_array.astype(np.float32)

    # Segment the audio into 30-second chunks (Whisper's maximum input length)
    segment_length = 30 * 16000  # 30 seconds at 16kHz
    num_segments = ceil(len(audio_array) / segment_length)

    for i in range(num_segments):
        start = i * segment_length
        end = min((i + 1) * segment_length, len(audio_array))
        segment = audio_array[start:end]

        # Convert the segment to a mel spectrogram
        mel = log_mel_spectrogram(segment)

        # Transcribe the segment using Whisper
        options = whisper.DecodingOptions(fp16=False)  # Use fp32 since fp16 is not supported on CPU
        result = whisper.decode(model, mel, options)

        # Yield the transcription text directly, without any segment information
        yield result.text.strip() + " "
