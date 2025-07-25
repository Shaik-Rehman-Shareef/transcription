#!/usr/bin/env python3
"""
Audio File-to-Text REST API
Supports Hindi and English speech recognition
Upload audio files and get text transcriptions via HTTP API
"""

import os
import tempfile
import uuid
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from werkzeug.utils import secure_filename
import speech_recognition as sr
from pydub import AudioSegment
import io
import traceback
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS for all routes
CORS(app, origins=['*'], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type'])

# Audio file converter class
class AudioAPIConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg'}
    
    def is_audio_file(self, filename):
        """Check if file is a supported audio format"""
        return any(filename.lower().endswith(ext) for ext in self.supported_formats)
    
    def load_audio_file(self, file_path):
        """Load audio file and convert to speech_recognition format"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Handle different audio formats
            if file_path.lower().endswith('.wav'):
                with sr.AudioFile(file_path) as source:
                    audio_data = self.recognizer.record(source)
                return audio_data
            else:
                # Convert other formats to WAV using pydub
                audio = AudioSegment.from_file(file_path)
                
                # Create temporary WAV file
                temp_wav = f"temp_{uuid.uuid4().hex}.wav"
                audio.export(temp_wav, format="wav")
                
                # Load with speech_recognition
                with sr.AudioFile(temp_wav) as source:
                    audio_data = self.recognizer.record(source)
                
                # Clean up temporary file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
                
                return audio_data
                
        except Exception as e:
            raise Exception(f"Error loading audio file: {str(e)}")
    
    def transcribe_audio(self, audio_data, language="auto"):
        """Transcribe audio data to text"""
        try:
            if language == "auto":
                # Try both languages and return the first successful result
                for lang in ["en-IN", "hi-IN"]:
                    try:
                        text = self.recognizer.recognize_google(audio_data, language=lang)
                        return {
                            "text": text,
                            "language": lang,
                            "confidence": "high"
                        }
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        continue
                
                return None
            else:
                # Use specified language
                text = self.recognizer.recognize_google(audio_data, language=language)
                return {
                    "text": text,
                    "language": language,
                    "confidence": "high"
                }
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise Exception(f"Speech recognition service error: {str(e)}")
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")

# Initialize converter
converter = AudioAPIConverter()

@app.route('/')
def home():
    """API documentation page"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Audio-to-Text API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
            h2 { color: #007bff; margin-top: 30px; }
            .endpoint { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #007bff; }
            .method { background: #28a745; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold; }
            code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
            .example { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .upload-form { background: #e7f3ff; padding: 20px; border-radius: 5px; margin: 20px 0; }
            input[type="file"] { margin: 10px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .supported { display: inline-block; background: #d4edda; color: #155724; padding: 5px 10px; margin: 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎤 Audio-to-Text REST API</h1>
            <p>Convert audio files to text using Hindi and English speech recognition.</p>
            
            <h2>📋 API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> <code>/transcribe</code>
                <p>Upload an audio file and get text transcription.</p>
                <strong>Parameters:</strong>
                <ul>
                    <li><code>file</code> - Audio file (required)</li>
                    <li><code>language</code> - Language code: en-IN, hi-IN, or auto (optional, default: auto)</li>
                </ul>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <code>/health</code>
                <p>Check API health status.</p>
            </div>
            
            <h2>🎯 Supported Audio Formats</h2>
            <div>
                <span class="supported">WAV</span>
                <span class="supported">MP3</span>
                <span class="supported">M4A</span>
                <span class="supported">FLAC</span>
                <span class="supported">AAC</span>
                <span class="supported">OGG</span>
            </div>
            
            <h2>🧪 Test the API</h2>
            <div class="upload-form">
                <form id="uploadForm" enctype="multipart/form-data">
                    <label for="audioFile">Select Audio File:</label><br>
                    <input type="file" id="audioFile" name="file" accept=".wav,.mp3,.m4a,.flac,.aac,.ogg" required><br>
                    
                    <label for="language">Language:</label><br>
                    <select id="language" name="language">
                        <option value="auto">Auto-detect</option>
                        <option value="en-IN">English (India)</option>
                        <option value="hi-IN">Hindi (India)</option>
                    </select><br><br>
                    
                    <button type="submit">Upload & Transcribe</button>
                </form>
                <div id="result" style="margin-top: 20px; padding: 10px; background: white; border-radius: 5px; display: none;"></div>
            </div>
            
            <h2>📖 Example Usage</h2>
            
            <div class="example">
                <h4>Python Example:</h4>
                <pre><code>import requests

url = "http://localhost:5000/transcribe"
files = {"file": open("audio.wav", "rb")}
data = {"language": "auto"}

response = requests.post(url, files=files, data=data)
result = response.json()
print(result["text"])</code></pre>
            </div>
            
            <div class="example">
                <h4>cURL Example:</h4>
                <pre><code>curl -X POST http://localhost:5000/transcribe \
  -F "file=@audio.wav" \
  -F "language=auto"</code></pre>
            </div>
        </div>
        
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData();
                const fileInput = document.getElementById('audioFile');
                const languageInput = document.getElementById('language');
                const resultDiv = document.getElementById('result');
                
                if (!fileInput.files[0]) {
                    alert('Please select a file');
                    return;
                }
                
                formData.append('file', fileInput.files[0]);
                formData.append('language', languageInput.value);
                
                resultDiv.innerHTML = '⏳ Processing...';
                resultDiv.style.display = 'block';
                
                try {
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        resultDiv.innerHTML = `
                            <h4>✅ Transcription Result:</h4>
                            <p><strong>Text:</strong> ${result.text}</p>
                            <p><strong>Language:</strong> ${result.language}</p>
                            <p><strong>Confidence:</strong> ${result.confidence}</p>
                        `;
                    } else {
                        resultDiv.innerHTML = `<h4>❌ Error:</h4><p>${result.error}</p>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<h4>❌ Error:</h4><p>${error.message}</p>`;
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Audio-to-Text API",
        "timestamp": datetime.now().isoformat(),
        "supported_formats": list(converter.supported_formats),
        "supported_languages": ["en-IN", "hi-IN", "auto"]
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Main transcription endpoint"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded",
                "code": "NO_FILE"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected",
                "code": "EMPTY_FILE"
            }), 400
        
        # Get language parameter
        language = request.form.get('language', 'auto')
        if language not in ['en-IN', 'hi-IN', 'auto']:
            return jsonify({
                "success": False,
                "error": "Invalid language. Use: en-IN, hi-IN, or auto",
                "code": "INVALID_LANGUAGE"
            }), 400
        
        # Check file format
        if not converter.is_audio_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"Unsupported file format. Supported: {', '.join(converter.supported_formats)}",
                "code": "UNSUPPORTED_FORMAT"
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{filename}")
        
        try:
            file.save(temp_path)
            
            # Load and transcribe audio
            audio_data = converter.load_audio_file(temp_path)
            
            if not audio_data:
                return jsonify({
                    "success": False,
                    "error": "Failed to load audio file",
                    "code": "AUDIO_LOAD_ERROR"
                }), 500
            
            # Transcribe audio
            result = converter.transcribe_audio(audio_data, language)
            
            if result:
                return jsonify({
                    "success": True,
                    "text": result["text"],
                    "language": result["language"],
                    "confidence": result["confidence"],
                    "filename": filename,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Could not understand the audio content",
                    "code": "NO_SPEECH_DETECTED"
                }), 422
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        app.logger.error(f"Transcription error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "code": "INTERNAL_ERROR"
        }), 500

@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large error"""
    return jsonify({
        "success": False,
        "error": "File too large. Maximum size is 50MB.",
        "code": "FILE_TOO_LARGE"
    }), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "code": "NOT_FOUND"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "code": "INTERNAL_ERROR"
    }), 500

if __name__ == '__main__':
    print("🎤 Starting Audio-to-Text REST API...")
    print("📊 API Documentation: http://localhost:5000")
    print("🔗 Health Check: http://localhost:5000/health")
    print("📤 Upload Endpoint: http://localhost:5000/transcribe")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
