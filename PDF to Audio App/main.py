"""
A python project using Tkinter, Google Text to Speech and PDF miner to convert a pdf into a mp3 audio file
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from gtts import gTTS
from pdfminer.high_level import extract_text
import os
import pygame


class PDFToAudio:
    def __init__(self):
        pygame.mixer.init()
        self.directory = "C:/Users/Buchanan/Documents/PDF/"  # Change path to where you want the audio saved
        self.filename = None
        self.text = None
        self.audio = None
        self.filename_label = None
        self.saved_filepath_label = None
        self.converted_label = None
        self.play_button = None
        self.stop_button = None
        self.save_path = None
        self.window = Tk()
        self.window.title("PDF to Audio Converter")

        # Set window grid
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        # Create a button to add a PDF
        ttk.Button(text="Add PDF", command=self.upload_action).grid(
            row=0, column=1, padx=10, pady=10
        )

        # Create the Convert button (initially hidden)
        self.convert_button = ttk.Button(
            text="Convert PDF to Text", command=self.convert_pdf
        )
        self.convert_button.grid(row=2, column=1, padx=10, pady=10)

        # Create the Save button (initially hidden)
        self.save_button = ttk.Button(text="Save Audio", command=self.save_audio)
        self.save_button.grid(row=5, column=1, padx=10, pady=10)

        # Create a button to play the MP3 (initially hidden)
        self.play_button = ttk.Button(text="Play MP3", command=self.play_music)
        self.play_button.grid(row=7, column=0, padx=10, pady=10)

        # Create a button to stop the MP3 (initially hidden)
        self.stop_button = ttk.Button(text="Stop", command=self.stop_music)
        self.stop_button.grid(row=7, column=2, padx=10, pady=10)

        # Create the Reset button (initially hidden)
        self.reset_button = ttk.Button(text="Reset", command=self.reset_action)
        self.reset_button.grid(row=9, column=1, padx=10, pady=10)

        self.window.mainloop()

    def upload_action(self):
        """
        Opens your file directory and allows you search for an appropriate pdf file
        """
        f_types = [("PDF Files", ("*.pdf"))]
        self.filename = filedialog.askopenfilename(filetypes=f_types)
        if not self.filename:
            return  # If the user doesn't select a pdf
        self.filename_label = ttk.Label(
            text=f"{self.filename} has been loaded successfully"
        )
        self.filename_label.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def convert_pdf(self):
        self.text = extract_text(self.filename)
        self.converted_label = ttk.Label(
            text=f"{self.filename} has been converted successfully"
        )
        self.converted_label.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    def save_audio(self):
        """
        Saving the completed audio
        """
        self.audio = gTTS(self.text)

        original_file_name = os.path.basename(self.filename)
        remove_ext = os.path.splitext(original_file_name)[0]
        new_file_name = f"{remove_ext}_audio.mp3"
        self.save_path = os.path.join(self.directory, new_file_name)
        self.audio.save(self.save_path)
        self.filepath_label = ttk.Label(
            text=f"{self.save_path} has been saved successfully"
        )
        self.filepath_label.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

    def play_music(self):
        pygame.mixer.music.load(self.save_path)
        pygame.mixer.music.play()
        self.play_button.config(text="Playing")

    def stop_music(self):
        self.play_button.config(text="Play MP3")
        pygame.mixer.music.stop()

    def reset_action(self):
        """
        Removes the current pdf and resets the window back to the original state
        """
        self.filename_label.grid_forget()  # Hide the filename label
        self.filepath_label.grid_forget()  # Hide the filepath label
        self.converted_label.grid_forget()  # Hide the converted label


if __name__ == "__main__":
    PDFToAudio()
