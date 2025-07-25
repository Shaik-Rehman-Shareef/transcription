#!/usr/bin/env python3
"""
Audio File to Text Converter
Supports Hindi and English speech recognition
Converts audio files to text
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import speech_recognition as sr
from pydub import AudioSegment
import io

class AudioFileToTextConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        self.root = tk.Tk()
        self.root.title("Audio File to Text Converter (Hindi & English)")
        self.root.geometry("800x500")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio File to Text Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Language selection
        lang_frame = ttk.LabelFrame(main_frame, text="Language Selection", padding="10")
        lang_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.language_var = tk.StringVar(value="auto")
        ttk.Radiobutton(lang_frame, text="English", variable=self.language_var, 
                       value="en-IN").grid(row=0, column=0, padx=(0, 20))
        ttk.Radiobutton(lang_frame, text="Hindi", variable=self.language_var, 
                       value="hi-IN").grid(row=0, column=1, padx=(0, 20))
        ttk.Radiobutton(lang_frame, text="Auto-detect", variable=self.language_var, 
                       value="auto").grid(row=0, column=2)
        
        # File processing section
        file_frame = ttk.LabelFrame(main_frame, text="Audio File Processing", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Button(file_frame, text="Select Single Audio File", 
                  command=self.process_audio_file).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(file_frame, text="Select Multiple Audio Files", 
                  command=self.process_multiple_files).grid(row=0, column=1, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No files selected")
        self.file_label.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Status section
        self.status_label = ttk.Label(main_frame, text="Ready to process audio files", 
                                     font=('Arial', 10))
        self.status_label.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        # Results section
        result_frame = ttk.LabelFrame(main_frame, text="Transcription Results", padding="10")
        result_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(result_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(text_frame, height=15, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons for results
        button_frame = ttk.Frame(result_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Clear", command=self.clear_results).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Save to File", command=self.save_results).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=0, column=2)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
    
    def update_status(self, message):
        """Update status label"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
        self.root.update()
    
    def process_audio_file(self):
        """Process a single audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg"),
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.update_status("Processing audio file...")
            
            # Process file in a separate thread
            processing_thread = threading.Thread(target=self.transcribe_file, args=(file_path,))
            processing_thread.daemon = True
            processing_thread.start()
    
    def process_multiple_files(self):
        """Process multiple audio files"""
        file_paths = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.flac *.aac *.ogg"),
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_paths:
            self.file_label.config(text=f"Selected {len(file_paths)} files")
            self.update_status("Processing multiple audio files...")
            
            # Process files in a separate thread
            processing_thread = threading.Thread(target=self.transcribe_multiple_files, args=(file_paths,))
            processing_thread.daemon = True
            processing_thread.start()
    
    def transcribe_file(self, file_path):
        """Transcribe audio from a single file"""
        try:
            # Convert file to WAV if necessary
            audio_data = self.load_audio_file(file_path)
            
            if audio_data:
                language = self.language_var.get()
                text = self.transcribe_audio(audio_data, language)
                
                if text:
                    filename = os.path.basename(file_path)
                    self.append_result(f"[File: {filename} - {language}]: {text}\n\n")
                    self.update_status("File transcription complete.")
                else:
                    filename = os.path.basename(file_path)
                    self.append_result(f"[File: {filename}]: Could not understand audio\n\n")
                    self.update_status("Could not understand audio in file.")
            else:
                filename = os.path.basename(file_path)
                self.append_result(f"[File: {filename}]: Failed to load file\n\n")
                self.update_status("Failed to load audio file.")
                
        except Exception as e:
            filename = os.path.basename(file_path)
            self.append_result(f"[File: {filename}]: Error - {str(e)}\n\n")
            self.update_status(f"File processing error: {str(e)}")
    
    def transcribe_multiple_files(self, file_paths):
        """Transcribe multiple audio files"""
        total_files = len(file_paths)
        successful = 0
        
        for i, file_path in enumerate(file_paths, 1):
            try:
                self.update_status(f"Processing file {i}/{total_files}: {os.path.basename(file_path)}")
                
                # Convert file to WAV if necessary
                audio_data = self.load_audio_file(file_path)
                
                if audio_data:
                    language = self.language_var.get()
                    text = self.transcribe_audio(audio_data, language)
                    
                    if text:
                        filename = os.path.basename(file_path)
                        self.append_result(f"[File {i}: {filename} - {language}]: {text}\n\n")
                        successful += 1
                    else:
                        filename = os.path.basename(file_path)
                        self.append_result(f"[File {i}: {filename}]: Could not understand audio\n\n")
                else:
                    filename = os.path.basename(file_path)
                    self.append_result(f"[File {i}: {filename}]: Failed to load file\n\n")
                    
            except Exception as e:
                filename = os.path.basename(file_path)
                self.append_result(f"[File {i}: {filename}]: Error - {str(e)}\n\n")
        
        self.update_status(f"Completed processing {total_files} files. {successful} successful transcriptions.")
    
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
                
                # Convert to WAV format in memory
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)
                
                # Create temporary WAV file
                temp_wav = "temp_audio.wav"
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
            print(f"Error loading audio file: {e}")
            return None
    
    def transcribe_audio(self, audio_data, language):
        """Transcribe audio data to text"""
        try:
            if language == "auto":
                # Try both languages and return the first successful result
                for lang in ["en-IN", "hi-IN"]:
                    try:
                        text = self.recognizer.recognize_google(audio_data, language=lang)
                        return f"{text} [Auto-detected: {lang}]"
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        continue
                return None
            else:
                # Use specified language
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise Exception(f"Speech recognition service error: {e}")
        except Exception as e:
            raise Exception(f"Transcription error: {e}")
    
    def append_result(self, text):
        """Append text to results area"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        """Clear the results text area"""
        self.result_text.delete(1.0, tk.END)
        self.update_status("Results cleared. Ready to process audio files.")
    
    def save_results(self):
        """Save results to a file"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Results saved to {file_path}")
                self.update_status(f"Results saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        content = self.result_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Content copied to clipboard!")
            self.update_status("Content copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "No content to copy!")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = AudioFileToTextConverter()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
