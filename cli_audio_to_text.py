#!/usr/bin/env python3
"""
Audio File to Text Converter (CLI)
Supports Hindi and English speech recognition
Converts audio files to text - Command Line Interface
"""

import os
import sys
import argparse
import speech_recognition as sr
from pydub import AudioSegment
import io
import traceback

class AudioFileToTextConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_file(self, file_path, language="auto"):
        """Transcribe audio from file"""
        try:
            print(f"📁 Processing file: {os.path.basename(file_path)}")
            
            # Load audio file
            audio_data = self.load_audio_file(file_path)
            
            if audio_data:
                print("🔄 Transcribing audio...")
                text = self.transcribe_audio(audio_data, language)
                
                if text:
                    print(f"\n📝 Transcription ({language}): {text}")
                    return text
                else:
                    print("❌ Could not understand the audio in the file.")
                    return None
            else:
                print("❌ Failed to load audio file.")
                return None
                
        except Exception as e:
            print(f"❌ File processing error: {e}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def load_audio_file(self, file_path):
        """Load audio file and convert to speech_recognition format"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            print(f"📂 Loading file: {os.path.basename(file_path)}")
            
            # Handle different audio formats
            if file_path.lower().endswith('.wav'):
                with sr.AudioFile(file_path) as source:
                    audio_data = self.recognizer.record(source)
                return audio_data
            else:
                # Convert other formats to WAV using pydub
                print("🔄 Converting audio format...")
                audio = AudioSegment.from_file(file_path)
                
                # Convert to WAV format in memory
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)
                
                # Create temporary WAV file
                temp_wav = "temp_audio_cli.wav"
                with open(temp_wav, "wb") as f:
                    f.write(wav_io.read())
                
                # Load with speech_recognition
                with sr.AudioFile(temp_wav) as source:
                    audio_data = self.recognizer.record(source)
                
                # Clean up temporary file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
                
                return audio_data
                
        except Exception as e:
            print(f"❌ Error loading audio file: {e}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def transcribe_audio(self, audio_data, language):
        """Transcribe audio data to text with detailed error reporting"""
        try:
            print(f"🔄 Starting transcription with language: {language}")
            
            if language == "auto":
                print("🔍 Auto-detecting language...")
                # Try both languages
                for lang in ["en-IN", "hi-IN"]:
                    try:
                        print(f"  🔍 Trying language: {lang}...")
                        text = self.recognizer.recognize_google(audio_data, language=lang)
                        print(f"  ✅ Successfully detected {lang}!")
                        return f"{text} [Auto-detected: {lang}]"
                    except sr.UnknownValueError:
                        print(f"  ❌ No speech detected for {lang}")
                        continue
                    except sr.RequestError as e:
                        print(f"  ❌ Request error for {lang}: {e}")
                        continue
                    except Exception as e:
                        print(f"  ❌ Unexpected error for {lang}: {e}")
                        continue
                
                print("❌ No successful transcription in any language")
                return None
            else:
                # Use specified language
                print(f"  🔍 Transcribing with {language}...")
                text = self.recognizer.recognize_google(audio_data, language=language)
                print(f"  ✅ Transcription successful!")
                return text
                
        except sr.UnknownValueError:
            print("❌ Could not understand the audio (UnknownValueError)")
            print("💡 This usually means the audio is unclear or there's no speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            print("💡 This might be a network issue or API problem")
            return None
        except Exception as e:
            print(f"❌ Unexpected transcription error: {e}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return None
    
    def batch_process_files(self, file_paths, language="auto", output_file=None):
        """Process multiple files and optionally save to output file"""
        results = []
        successful = 0
        total_files = len(file_paths)
        
        print(f"🔄 Processing {total_files} files...")
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n--- Processing file {i}/{total_files}: {os.path.basename(file_path)} ---")
            text = self.transcribe_file(file_path, language)
            
            if text:
                result = f"File: {os.path.basename(file_path)}\nTranscription: {text}\n"
                results.append(result)
                successful += 1
                print("✅ Success")
            else:
                result = f"File: {os.path.basename(file_path)}\nTranscription: [FAILED]\n"
                results.append(result)
                print("❌ Failed")
        
        print(f"\n📊 Summary: {successful}/{total_files} files successfully transcribed")
        
        if output_file and results:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Audio File to Text Conversion Results\n")
                    f.write("=" * 40 + "\n")
                    f.write(f"Total files: {total_files}\n")
                    f.write(f"Successful: {successful}\n")
                    f.write(f"Failed: {total_files - successful}\n")
                    f.write("=" * 40 + "\n\n")
                    for result in results:
                        f.write(result + "\n")
                print(f"💾 Results saved to: {output_file}")
            except Exception as e:
                print(f"❌ Failed to save results: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Audio File to Text Converter (CLI)")
    parser.add_argument("--file", "-f", help="Single audio file path")
    parser.add_argument("--files", nargs="+", help="Multiple audio files for batch processing")
    parser.add_argument("--language", "-l", choices=["en-IN", "hi-IN", "auto"], default="auto",
                      help="Language for transcription (default: auto)")
    parser.add_argument("--output", "-o", help="Output file for saving results")
    parser.add_argument("--debug", action="store_true",
                      help="Enable debug mode with detailed error information")
    
    args = parser.parse_args()
    
    # Create converter instance
    try:
        converter = AudioFileToTextConverter()
    except Exception as e:
        print(f"❌ Failed to initialize converter: {e}")
        if args.debug:
            traceback.print_exc()
        sys.exit(1)
    
    print("🎤 Audio File to Text Converter (Command Line)")
    print("=" * 45)
    print(f"Language: {args.language}")
    if args.debug:
        print("Debug mode: ON")
    print()
    
    try:
        if args.file:
            # Process single file
            print("📁 Single file mode")
            text = converter.transcribe_file(args.file, args.language)
            
            if text and args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(f"File: {args.file}\n")
                    f.write(f"Language: {args.language}\n")
                    f.write(f"Transcription: {text}\n")
                print(f"💾 Result saved to: {args.output}")
        
        elif args.files:
            # Process multiple files
            print("📁 Batch processing mode")
            converter.batch_process_files(args.files, args.language, args.output)
        
        else:
            # No files specified, show help
            print("❌ Error: Please specify either --file or --files")
            print("\nExamples:")
            print("  Single file:    python audio_file_to_text_cli.py --file audio.wav")
            print("  Multiple files: python audio_file_to_text_cli.py --files file1.wav file2.mp3")
            print("  With output:    python audio_file_to_text_cli.py --file audio.wav --output result.txt")
            print("  Hindi only:     python audio_file_to_text_cli.py --file audio.wav --language hi-IN")
            print("  English only:   python audio_file_to_text_cli.py --file audio.wav --language en-IN")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Application error: {e}")
        if args.debug:
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
