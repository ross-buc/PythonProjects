import tkinter as tk
import requests
from bs4 import BeautifulSoup
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext

# Dictionary to store the Morse code mappings
MORSE_CODE_DICT = {
    "A": "",
    "B": "",
    "C": "",
    "D": "",
    "E": "",
    "F": "",
    "G": "",
    "H": "",
    "I": "",
    "J": "",
    "K": "",
    "L": "",
    "M": "",
    "N": "",
    "O": "",
    "P": "",
    "Q": "",
    "R": "",
    "S": "",
    "T": "",
    "U": "",
    "V": "",
    "W": "",
    "X": "",
    "Y": "",
    "Z": "",
}


def convert_to_morse_code():
    # Fetching Morse code data from Wikipedia
    response = requests.get(url="https://en.wikipedia.org/wiki/Morse_code")
    data = response.text
    soup = BeautifulSoup(data, "html.parser")

    # Updating Morse code mappings from the Wikipedia page
    for item, value in MORSE_CODE_DICT.items():
        html_title = f"File:{item} morse code.ogg"
        morse_code = soup.find("a", title=html_title)
        MORSE_CODE_DICT[item] = morse_code.text

    # Get user input from the text entry
    input_word = input_entry.get()

    # Splitting the input word into a list of characters and converting them to uppercase
    split_string = list(input_word.upper())

    # Converting the input word to Morse code using the Morse code dictionary
    morse_code = [MORSE_CODE_DICT.get(letter, "") for letter in split_string]

    # Checking for invalid characters in the input word
    if "" in morse_code:
        result_text.delete("1.0", tk.END)
        messagebox.showerror("Error", "Please enter a word with no numbers or spaces")
    else:
        # Printing the word in Morse code
        morse_code_str = " ".join(morse_code)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, morse_code_str)


def copy_morse_code():
    # Allowing the user to copy the result
    morse_code = result_text.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(morse_code)
    messagebox.showinfo("Copied", "Morse code copied to clipboard!")


# Create the main window
window = tk.Tk()
window.title("Morse Code Converter")

# Create and pack the input label and entry
input_label = tk.Label(window, text="Enter a word:")
input_label.pack()

input_entry = tk.Entry(window)
input_entry.pack()

# Create and pack the convert button
convert_button = tk.Button(window, text="Convert", command=convert_to_morse_code)
convert_button.pack()

# Create the result label
result_label = tk.Label(window, text="Morse Code:")
result_label.pack()

# Create and pack the scrolled text widget for displaying the Morse code
result_text = scrolledtext.ScrolledText(window, height=5)
result_text.pack()

# Create and pack the copy button
copy_button = tk.Button(window, text="Copy", command=copy_morse_code)
copy_button.pack()

window.mainloop()
