import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if not file_path:
        return

    try:
        # Convert MP3 to WAV if needed
        if file_path.endswith(".mp3"):
            sound = AudioSegment.from_mp3(file_path)
            wav_path = file_path.replace(".mp3", ".wav")
            sound.export(wav_path, format="wav")
            file_path = wav_path

        recognizer = sr.Recognizer()

        with sr.AudioFile(file_path) as source:
            status_label.config(text="Transcribing...")
            window.update()
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        # Display in text area
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, text)
        status_label.config(text="Transcription complete.")

        # Optional: Save to file
        with open("transcription.txt", "w") as f:
            f.write(text)

        messagebox.showinfo("Success", "Transcription completed and saved to 'transcription.txt'.")

    except sr.UnknownValueError:
        status_label.config(text="Could not understand the audio.")
    except sr.RequestError as e:
        status_label.config(text=f"Google API error: {e}")
    except Exception as e:
        status_label.config(text="Error occurred.")
        messagebox.showerror("Error", str(e))

# ----- UI -----
window = tk.Tk()
window.title("Speech-to-Text Transcription")
window.geometry("600x400")

title = tk.Label(window, text="Speech-to-Text Transcription Tool", font=("Arial", 16))
title.pack(pady=10)

transcribe_button = tk.Button(window, text="Select Audio & Transcribe", command=transcribe_audio, font=("Arial", 12))
transcribe_button.pack(pady=10)

text_area = ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

status_label = tk.Label(window, text="", font=("Arial", 10), fg="green")
status_label.pack(pady=5)

window.mainloop()
