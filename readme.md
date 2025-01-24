Web Media Transcription Service

A Flask web application that extracts and transcribes media content from web pages using OpenAI's Whisper model.
Features

    Extract media URLs from web pages
    Transcribe audio/video content using Whisper
    Real-time transcription progress updates
    Clean, responsive web interface
    Comprehensive logging system

Components

    Browser: QT-based web browser for media handling
    Media Extractor: Extracts media URLs from web pages
    Transcriber: Handles audio transcription using Whisper
    Web Interface: Flask-based frontend for user interaction

Requirements

    Python 3.10+
    FFmpeg
    PyTorch
    OpenAI Whisper
    Flask
    BeautifulSoup4
    PyQt5
    Additional dependencies in pyproject.toml

Installation

All dependencies are automatically handled by Replit.
Usage

    Open the web interface
    Enter a URL containing media content
    Click "Transcribe" to start the process
    View real-time progress and results

API Endpoints

    GET /: Main web interface
    POST /transcribe: Accepts media URL and returns transcription

Architecture

    app.py: Main Flask application
    browser/: QT browser implementation
    media_extractor/: URL extraction logic
    transcriber/: Audio transcription service
    templates/: HTML templates
    static/: CSS and frontend assets
    logs/: Application logs

Error Handling

    Comprehensive error logging
    User-friendly error messages
    Graceful failure handling

Logging

Logs are stored in:

License

MIT License