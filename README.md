# 🎤 Audio File to Text Converter

Convert audio files to text in **Hindi and English** without using LLMs. Supports multiple audio formats and provides both GUI and command-line interfaces.

## ✨ Features

- **Audio File Processing**: Convert WAV, MP3, M4A, FLAC, AAC, OGG files to text
- **Dual Language Support**: English (en-IN) and Hindi (hi-IN) 
- **Auto Language Detection**: Automatically detect the spoken language
- **Multiple Interfaces**: Both GUI and command-line versions
- **Batch Processing**: Process multiple audio files at once
- **Export Results**: Save transcriptions to text files
- **No LLMs Required**: Uses traditional speech recognition technology

## 🚀 Quick Start

### Installation

1. **Clone or download** this project
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements_optimized.txt
   ```

### Usage

#### GUI Version (Recommended)
```bash
python audio_file_to_text.py
```

#### Command Line Version
```bash
# Single file
python audio_file_to_text_cli.py --file audio.wav

# Multiple files
python audio_file_to_text_cli.py --files file1.wav file2.mp3 file3.m4a

# With output file
python audio_file_to_text_cli.py --file audio.wav --output transcription.txt

# Specific language
python audio_file_to_text_cli.py --file audio.wav --language hi-IN
```

## 📁 Project Structure

```
Audio File to Text Converter/
├── audio_file_to_text.py          # GUI version
├── audio_file_to_text_cli.py      # Command-line version
├── requirements_optimized.txt     # Python dependencies
└── README.md                      # This documentation
```

## 🛠️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--file` | Single audio file | `--file audio.wav` |
| `--files` | Multiple audio files | `--files file1.wav file2.mp3` |
| `--language` | Language (en-IN, hi-IN, auto) | `--language hi-IN` |
| `--output` | Output text file | `--output result.txt` |
| `--debug` | Enable debug mode | `--debug` |

## 🎯 Supported Audio Formats

- **WAV** (recommended, no conversion needed)
- **MP3** (requires FFmpeg)
- **M4A** (requires FFmpeg)
- **FLAC** (requires FFmpeg)
- **AAC** (requires FFmpeg)
- **OGG** (requires FFmpeg)

## 🔧 Technical Details

- **Speech Recognition**: Google's Speech Recognition API (free)
- **Audio Processing**: Pydub for format conversion
- **Languages Supported**: 
  - English (India): `en-IN`
  - Hindi (India): `hi-IN`  
  - Auto-detection: `auto`
- **Dependencies**: Minimal - only SpeechRecognition and Pydub
- **No Microphone**: Only processes audio files (no live recording)

## 💡 Tips for Best Results

1. **Use clear audio**: Minimize background noise
2. **Good quality files**: Higher bitrate audio works better
3. **WAV format**: Use WAV files when possible (no conversion needed)
4. **Auto-detect**: Use auto language detection for mixed content
5. **Batch processing**: Process multiple files efficiently

## 🔍 Examples

### GUI Usage
1. Run `python audio_file_to_text.py`
2. Select language (Auto-detect recommended)
3. Click "Select Single Audio File" or "Select Multiple Audio Files"
4. View results in the text area
5. Save results or copy to clipboard

### CLI Examples
```bash
# Basic usage
python audio_file_to_text_cli.py --file interview.wav

# Hindi audio
python audio_file_to_text_cli.py --file hindi_speech.mp3 --language hi-IN

# Batch processing with output
python audio_file_to_text_cli.py --files *.wav --output batch_results.txt

# Auto-detect language
python audio_file_to_text_cli.py --file mixed_language.mp3 --language auto
```

## ⚠️ Requirements

- **Python 3.7+**
- **Internet connection** (for Google Speech Recognition API)
- **FFmpeg** (optional, for non-WAV audio formats)

## 🎉 Advantages

- **Simple and focused**: Only file-to-text conversion
- **Lightweight**: Minimal dependencies
- **Fast processing**: Efficient audio file handling
- **Reliable**: Uses Google's robust speech recognition
- **Flexible**: Supports multiple audio formats and languages
- **No setup complexity**: No microphone configuration needed

## 📝 Output Format

Transcriptions include:
- Filename
- Detected/specified language
- Transcribed text
- Processing status

Example output:
```
[File: interview.wav - auto]: Hello, this is a test recording. [Auto-detected: en-IN]

[File: hindi_audio.mp3 - hi-IN]: नमस्ते, यह एक परीक्षण रिकॉर्डिंग है।
```

---

**Perfect for:** Converting recorded interviews, meetings, lectures, voice notes, and any audio content to readable text in Hindi and English.
