# 🎤 Audio-to-Text REST API Documentation

## 🚀 Quick Start

Your audio-to-text converter is now available as a REST API! Here are all the ways to use it:

## 📱 Web Interface (Easiest)

**Open in browser:** `web_interface.html`
- Drag and drop audio files
- Select language (Auto-detect, English, Hindi)
- Get instant transcriptions
- Works with multiple files

## 🔗 REST API Endpoints

### 1. Health Check
```bash
GET http://localhost:5000/health
```

**Response:**
```json
{
  "service": "Audio-to-Text API",
  "status": "healthy",
  "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg"],
  "supported_languages": ["en-IN", "hi-IN", "auto"]
}
```

### 2. Transcribe Audio
```bash
POST http://localhost:5000/transcribe
```

**Parameters:**
- `audio` (file): Audio file to transcribe
- `language` (string, optional): "en-IN", "hi-IN", or "auto" (default)

**Example using curl:**
```bash
curl -X POST http://localhost:5000/transcribe \
  -F "audio=@your_audio_file.wav" \
  -F "language=auto"
```

**Success Response:**
```json
{
  "success": true,
  "transcription": "Your transcribed text here",
  "language": "en-IN",
  "filename": "audio.wav",
  "processing_time": 2.34
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error description"
}
```

## 💻 Code Examples

### Python (using requests)
```python
import requests

# Single file
url = "http://localhost:5000/transcribe"
files = {'audio': open('audio.wav', 'rb')}
data = {'language': 'auto'}

response = requests.post(url, files=files, data=data)
result = response.json()

if result['success']:
    print(f"Transcription: {result['transcription']}")
else:
    print(f"Error: {result['error']}")
```

### JavaScript (fetch API)
```javascript
const formData = new FormData();
formData.append('audio', audioFile);
formData.append('language', 'auto');

fetch('http://localhost:5000/transcribe', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Transcription:', data.transcription);
    } else {
        console.error('Error:', data.error);
    }
});
```

### PHP
```php
$url = 'http://localhost:5000/transcribe';
$file = new CURLFile('audio.wav');

$data = [
    'audio' => $file,
    'language' => 'auto'
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$result = json_decode($response, true);

if ($result['success']) {
    echo "Transcription: " . $result['transcription'];
} else {
    echo "Error: " . $result['error'];
}
```

### Node.js (using form-data)
```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

const form = new FormData();
form.append('audio', fs.createReadStream('audio.wav'));
form.append('language', 'auto');

fetch('http://localhost:5000/transcribe', {
    method: 'POST',
    body: form
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Transcription:', data.transcription);
    } else {
        console.error('Error:', data.error);
    }
});
```

## 🎯 Supported Audio Formats

- ✅ **WAV** (recommended)
- ✅ **MP3**
- ✅ **M4A**
- ✅ **FLAC**
- ✅ **AAC**
- ✅ **OGG**

## 🌐 Supported Languages

- **en-IN**: English (India)
- **hi-IN**: Hindi (India)
- **auto**: Auto-detect language (default)

## 🔧 Starting the API Server

```bash
# Install dependencies
pip install -r requirements_api.txt

# Start the server
python app.py
```

The API will be available at:
- **Local:** http://localhost:5000
- **Network:** http://your-ip:5000

## 📊 API Features

- ✅ **File Upload**: Upload audio files via HTTP POST
- ✅ **Multiple Formats**: Supports all major audio formats
- ✅ **Language Detection**: Auto-detect Hindi/English
- ✅ **Error Handling**: Detailed error messages
- ✅ **CORS Enabled**: Works with web applications
- ✅ **File Validation**: Checks file types and sizes
- ✅ **Processing Time**: Reports conversion duration

## 🛡️ Error Codes

- **400**: Bad request (missing file, invalid format)
- **413**: File too large (>50MB)
- **500**: Server error (transcription failed)

## 💡 Tips for Best Results

1. **Audio Quality**: Use clear, high-quality recordings
2. **Background Noise**: Minimize background noise
3. **File Size**: Keep files under 50MB for faster processing
4. **Format**: WAV format provides best compatibility
5. **Language**: Use auto-detection for mixed content

## 🔗 Integration Examples

### With React
```jsx
const handleFileUpload = async (file) => {
  const formData = new FormData();
  formData.append('audio', file);
  formData.append('language', 'auto');
  
  try {
    const response = await fetch('http://localhost:5000/transcribe', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    setTranscription(result.transcription);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### With Vue.js
```javascript
methods: {
  async uploadAudio(file) {
    const formData = new FormData();
    formData.append('audio', file);
    formData.append('language', 'auto');
    
    try {
      const response = await this.$http.post('/transcribe', formData);
      this.transcription = response.data.transcription;
    } catch (error) {
      console.error('Error:', error);
    }
  }
}
```

---

## 🎉 Your Audio-to-Text Converter is Production Ready!

You now have:
- ✅ **REST API** for programmatic access
- ✅ **Web Interface** for easy file uploads
- ✅ **Multiple integration options**
- ✅ **Support for Hindi and English**
- ✅ **Batch processing capabilities**
