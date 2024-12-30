import librosa
import pyaudio
import wave
import sys
import os
import numpy as np
import random
import tkinter as tk
from tkinter import ttk

# list of notes
piano_notes_list = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C4', 'C#4', 'D#4', 'F#4', 'G#4', 'A#4', 'Eb4']
chords_dict = {  # list of chords
    'Chord 1 (C E G)': ['C4', 'E4', 'G4'],
    'Chord 2 (D F# A)': ['D4', 'F#4', 'A4'],
    'Chord 3 (E G# B)': ['E4', 'G#4', 'B4'],
    'Chord 4 (C Eb G)': ['C4', 'Eb4', 'G4'],
    'Chord 5 (D F A)': ['D4', 'F4', 'A4'],
    'Chord 6 (E G B)': ['E4', 'G4', 'B4']
}

note_list = []
unique_notes = []

generated_note = None  # sets these global variables as empty
generated_chord = None


def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2
    RATE = 44100
    RECORD_SECONDS = 5

    # checks if the file exists then deletes it if it does
    if os.path.exists('note_audio.wav'):
        os.remove('note_audio.wav')

    with wave.open('note_audio.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))


def detect_notes():
    global note_list
    unique_notes.clear()
    note_list.clear()

    # loads audio file
    y, sr = librosa.load('note_audio.wav')
    f0 = librosa.pyin(y, fmin=100, fmax=2093)
    freq = np.array(f0)  # makes sure it's a numpy array
    freq_no_nan = freq[~np.isnan(freq)]  # get rid of all nan values

    # check for any infinite values and set them to 0
    infinite_index = np.isinf(freq_no_nan)
    freq_no_nan[infinite_index] = 0

    # note detection
    valid_freqs = freq_no_nan[(freq_no_nan > 20) & (freq_no_nan < 4000)]  # frequency range
    unique_freqs = np.unique(valid_freqs)  # find unique frequencies
    for i in unique_freqs:  # add the unique frequencies to the notes list
        note_list.append(librosa.hz_to_note(i))

    note_list = [note for note in note_list if note in piano_notes_list]  # remove any notes not in piano_notes_list
    for i in note_list:  # remove duplicates
        if i not in unique_notes:
            unique_notes.append(i)

    return unique_notes


def generate_note():
    global generated_note
    generated_note = random.choice(piano_notes_list)
    note_label.config(text=generated_note)
    return generated_note


def generate_chord():
    global generated_chord  # Make sure to use the global variable
    random_chord = random.choice(list(chords_dict.keys()))
    generated_chord = chords_dict[random_chord]
    note_label.config(text=generated_chord)
    return generated_chord


def check_note():
    detected_notes = detect_notes()  # gets the unique_note from the function

    if generated_note is not None:  # checks if a note has been generated
        if detected_notes[0] == generated_note:  # checks if the unique_note is equal to the generated note
            note_label.config(text="You played the correct note!")
        else:
            note_label.config(text="You played the wrong note")
    else:
        note_label.config(text="Please generate a note or chord first.")

    if generated_chord is not None:  # checks if a chord has been generated
        if detected_notes == generated_chord:  # checks if the unique_note is equal to the generated chord
            note_label.config(text="You played the correct chord!")
        else:
            note_label.config(text="You played the wrong chord!")


# opens the window
window = tk.Tk()
window.title("Piano")
window.geometry("500x300")
# frame that holds the note_label
window_frame = tk.Frame(window, bg="white", width=250, height=250)
window_frame.pack()
# label that displays the note 
note_label = tk.Label(window_frame, bg="white", text="Notes will appear here", font=("Arial", "15"))
note_label.pack(pady=50, padx=50)
# button to generate one note
onenote_button = ttk.Button(window, text="Generate one note", width=20, command=generate_note)
onenote_button.pack()
# button to generate a chord
chord_button = ttk.Button(window, text="Generate a chord", width=20, command=generate_chord)
chord_button.pack()
# button to record notes
record_button = ttk.Button(window, text="Record", command=record_audio, width=20)
record_button.pack()
# button to analyze the recording and check the notes played
checknote_button = ttk.Button(window, text="Check Notes", width=20, command=check_note)
checknote_button.pack()


window.mainloop()
