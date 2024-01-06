import numpy as np
import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write

from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

# Constants
SAMPLE_RATE = 44100  # Sample rate in Hz
CHARACTER_DURATION = 0.04  # Duration of each character in seconds
VOLUME = 0.5  # Volume, as a float between 0.0 and 1.0

# Encoding frequencies for each English character
FREQUENCIES = {
    'a': [100, 1100, 2500],'b': [100, 1100, 3000],'c': [100, 1100, 3500],
    'd': [100, 1300, 2500], 'e': [100, 1300, 3000], 'f': [100, 1300, 3500],
    'g': [100, 1500, 2500], 'h': [100, 1500, 3000], 'i': [100, 1500, 3500],
    'j': [300, 1100, 2500], 'k': [300, 1100, 3000], 'l': [300, 1100, 3500],
    'm': [300, 1300, 2500], 'n': [300, 1300, 3000], 'o': [300, 1300, 3500],
    'p': [300, 1500, 2500], 'q': [300, 1500, 3000], 'r': [300, 1500, 3500],
    's': [500, 1100, 2500], 't': [500, 1100, 3000], 'u': [500, 1100, 3500],
    'v': [500, 1300, 2500], 'w': [500, 1300, 3000], 'x': [500, 1300, 3500],
    'y': [500, 1500, 2500], 'z': [500, 1500, 3000], ' ': [500, 1500, 3500]
}

def generate_character_signal(frequencies):
    tones = []
    for freq in frequencies:
        t = np.linspace(0, CHARACTER_DURATION, int(SAMPLE_RATE * CHARACTER_DURATION), False)
        tone = np.sin(freq * t * 2 * np.pi)
        tones.append(tone)
    combined_tone = sum(tones)
    combined_tone *= VOLUME / np.max(np.abs(combined_tone))
    return combined_tone

def encode_string_to_signal(input_string):
    signal = np.array([])
    for char in input_string:
        if char in FREQUENCIES:
            signal = np.concatenate((signal, generate_character_signal(FREQUENCIES[char])))

    return signal


def getInputString():
    input_text = text_entry.get("1.0", tk.END).strip().lower()
    if not input_text:
        messagebox.showerror("Error", "Please enter some text to encode.")
        return
    return input_text

def encode():
    input_text=getInputString()
    encoded_signal = encode_string_to_signal(input_text)
    return encoded_signal

def save_generated_signal():

    encoded_signal = encode()

    file_path = askstring('Name', 'Enter a name of file to save the generated signal:')
    if file_path[-4:]!=".wav":
        file_path+=".wav"

    if file_path:
        normalized_signal = np.int16((encoded_signal / encoded_signal.max()) * 32767)
        write(file_path, SAMPLE_RATE, normalized_signal)
        messagebox.showinfo("Success", f"File saved as {file_path} .")

def play_generated_signal():

    # Generate the encoded signal
    encoded_signal = encode()

    # Normalize the signal to the range -1.0 to 1.0
    encoded_signal = encoded_signal / np.max(np.abs(encoded_signal))

    # Play the sound
    sd.play(encoded_signal, 8000)

    # Wait until sound has finished playing
    sd.wait()



if __name__ == "__main__":


    #Create the main window
    root = tk.Tk()
    root.title("Voice-Frequency Encoder")

    # Create a text entry widget
    text_entry = tk.Text(root, height=10, width=50)
    text_entry.pack()

    # Create a button to trigger the encoding and saving
    save_button = tk.Button(root, text="save the generated signal as (.wav)", command=save_generated_signal)
    save_button.pack()

    # Create a button to trigger the play sound
    play_button = tk.Button(root, text="play the generated signal", command=play_generated_signal)
    play_button.pack()

    # Run the GUI event loop
    root.mainloop()


