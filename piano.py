import librosa
import pyaudio
import wave
import sys
import numpy as np
import random

total = 0
count = 0

# list of notes
piano_notes_list = ['C4','D4','E4','F4','G4','A4','B4','C4','C#4','D#4','F#4','G#4','A#4','Eb']
chords_dict = { # list of chords
    'Chord 1 (C E G)': ['C4', 'E4', 'G4'],
    'Chord 2 (D F# A)': ['D4', 'F#4', 'A4'],
    'Chord 3 (E G# B)': ['E4', 'G#4', 'B4'],
    'Chord 4 (C Eb G)': ['C4', 'Eb4', 'G4'],
    'Chord 5 (D F A)': ['D4', 'F4', 'A4'],
    'Chord 6 (E G B)': ['E4', 'G4', 'B4']
}
note_list = []
unique_notes = []

choice = input("Do you want to play one note or multiple notes O/M")
if choice == 'O': # this is if you want to play one note
    random_note = random.choice(piano_notes_list)
    print("Play {}".format(random_note))
elif choice == 'M': # checks if you want to play multiple notes
    random_chord = random.choice(list(chords_dict.keys()))
    random_chord_notes = chords_dict[random_chord]
    print("Play {}".format(random_chord))

record = input("Enter R to record")
if record == 'R':
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 if sys.platform == 'darwin' else 2
    RATE = 44100
    RECORD_SECONDS = 5

    with wave.open('note_audio.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')
else:
    print("Wrong input try again")

# ^^^^^ This deals with recording the audio

y, sr = librosa.load('note_audio.wav') # loads audio file
f0 = librosa.pyin(y, fmin=100, fmax=2093)
freq = np.array(f0) # makes sure its a numpy array
freq_no_nan = freq[~np.isnan(freq)] # get rids of all nan values

# checks for any infinite values in the array and sets them to 0
infinite_index = np.isinf(freq_no_nan)
freq_no_nan[infinite_index] = 0
# note detection
valid_freqs = freq_no_nan[(freq_no_nan > 20) & (freq_no_nan < 4000)] # frequency range
unique_freqs = np.unique(valid_freqs) # finds unique frequencies
for i in unique_freqs: # adds the unique frequencies to the notes list
    note_list.append(librosa.hz_to_note(i))

note_list = [note for note in note_list if note in piano_notes_list] # removing any notes not in piano_notes_list w/ list comprehension
for i in note_list: # removes any duplicates
    if i not in unique_notes:
        unique_notes.append(i)


print(note_list)
print(unique_notes)
if choice == 'O':
    print(random_note)
    if unique_notes == random_note:
        print("Hooray you played the correct note!")
    else:
        print("You played the wrong note")
elif choice == 'M':
    print(random_chord)
    if unique_notes == random_chord_notes:
        print("Hooray you played the correct notes!")
    else:
        print("You played the wrong notes")

