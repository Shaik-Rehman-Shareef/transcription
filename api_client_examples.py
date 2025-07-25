#!/usr/bin/env python3
"""
Audio-to-Text API Client Examples
Shows how to use the REST API from different programming languages
"""

import requests
import json
import os

class AudioAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API not reachable: {str(e)}"}
    
    def transcribe_file(self, file_path, language="auto"):
        """Transcribe an audio file"""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        try:
            with open(file_path, 'rb') as audio_file:
                files = {"file": audio_file}
                data = {"language": language}
                
                response = requests.post(
                    f"{self.base_url}/transcribe",
                    files=files,
                    data=data
                )
                
                return response.json()
        
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

def demo_api_usage():
    """Demonstrate API usage"""
    print("🎤 Audio-to-Text API Client Demo")
    print("=" * 40)
    
    # Initialize client
    client = AudioAPIClient()
    
    # Test 1: Health check
    print("\n1️⃣ Testing API health...")
    health = client.health_check()
    if "error" in health:
        print(f"❌ {health['error']}")
        print("💡 Make sure to start the API server first:")
        print("   python app.py")
        return
    else:
        print(f"✅ API is healthy")
        print(f"   Supported formats: {', '.join(health['supported_formats'])}")
        print(f"   Supported languages: {', '.join(health['supported_languages'])}")
    
    # Test 2: File transcription (you would need to provide actual audio files)
    print("\n2️⃣ Example file transcription...")
    print("💡 To test with actual files, place audio files in this directory")
    
    # Example file paths (replace with your actual audio files)
    example_files = [
        "sample_english.wav",
        "sample_hindi.wav", 
        "sample_mixed.mp3"
    ]
    
    for file_path in example_files:
        if os.path.exists(file_path):
            print(f"\n📁 Processing: {file_path}")
            result = client.transcribe_file(file_path, "auto")
            
            if result.get("success"):
                print(f"✅ Success!")
                print(f"   Text: {result['text']}")
                print(f"   Language: {result['language']}")
                print(f"   Confidence: {result['confidence']}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"⏭️  Skipping {file_path} (file not found)")

def show_integration_examples():
    """Show integration examples for different languages"""
    print("\n🔗 API Integration Examples")
    print("=" * 50)
    
    print("\n🐍 PYTHON EXAMPLE:")
    print("-" * 20)
    python_example = '''
import requests

# Upload and transcribe audio file
url = "http://localhost:5000/transcribe"
files = {"file": open("audio.wav", "rb")}
data = {"language": "auto"}

response = requests.post(url, files=files, data=data)
result = response.json()

if result["success"]:
    print(f"Text: {result['text']}")
    print(f"Language: {result['language']}")
else:
    print(f"Error: {result['error']}")
'''
    print(python_example)
    
    print("\n🌐 JAVASCRIPT (Node.js) EXAMPLE:")
    print("-" * 35)
    js_example = '''
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function transcribeAudio(filePath, language = 'auto') {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    form.append('language', language);
    
    try {
        const response = await axios.post('http://localhost:5000/transcribe', form, {
            headers: form.getHeaders()
        });
        
        if (response.data.success) {
            console.log('Text:', response.data.text);
            console.log('Language:', response.data.language);
        } else {
            console.log('Error:', response.data.error);
        }
    } catch (error) {
        console.log('Request failed:', error.message);
    }
}

transcribeAudio('audio.wav');
'''
    print(js_example)
    
    print("\n💻 cURL EXAMPLE:")
    print("-" * 15)
    curl_example = '''
# Basic transcription
curl -X POST http://localhost:5000/transcribe \\
  -F "file=@audio.wav" \\
  -F "language=auto"

# With specific language
curl -X POST http://localhost:5000/transcribe \\
  -F "file=@hindi_audio.mp3" \\
  -F "language=hi-IN"

# Health check
curl http://localhost:5000/health
'''
    print(curl_example)
    
    print("\n🔧 PRODUCTION DEPLOYMENT:")
    print("-" * 25)
    deployment_info = '''
# Install production server
pip install gunicorn

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run with systemd (Linux)
# Create /etc/systemd/system/audio-api.service

# Docker deployment
# Create Dockerfile for containerization

# Environment variables
export FLASK_ENV=production
export FLASK_DEBUG=false
'''
    print(deployment_info)

def main():
    """Main function"""
    print("🎤 Audio-to-Text REST API Client")
    print("Choose an option:")
    print("1. Test API with demo")
    print("2. Show integration examples")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        demo_api_usage()
    
    if choice in ["2", "3"]:
        show_integration_examples()
    
    print("\n" + "=" * 50)
    print("🚀 Your Audio-to-Text REST API is ready!")
    print("📚 Start the server with: python app.py")
    print("🌐 API docs at: http://localhost:5000")

if __name__ == "__main__":
    main()
