# piano-project
My second personal project using Python with libraries including librosa, numpy, pyaudio and random

This piano tool allows users to practice and learn notes and chords. The program tells the user to play a note or a chord, records the audio, analyzes it with note detection, and compares the results to the correct note or chord to provide feedback

**Features:** 
  Option to play a single note or chord
  Record input for note detection
  Compares detected notes against the correct ones and provides feedback
**Libraries used:**
  Librosa - for note detection
  Numpy - handling frequencies, cleaning frequencies
  Random - to pick a random note or chord in the list/dictionary
  Pyaudio - to record audio

**Currently Working On:** 
  I plan to improve from having a command line interface to using Tkinter to improve the GUI and make it more pleasing
  
**Future Goals:** 
  * I plan to refine the note detection and have it detect more complex sets of notes
  * I plan to make it more like a teaching tool that starts with the basics and then gradually brings the user to more complex notes to play
  * I want to add a note visualizer, it shows the note your supposed to play 

**Problems:** 
  A problem I encountered was the frequencies having NaN and infinite values, and another problem was removing invalid notes without affecting the list of notes
  * Solution: I removed all NaN values and set all infinite values to zero
  * Solution: I used list comprehension to get rid of the invalid notes
