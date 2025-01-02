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
  Tkinter - for the GUI
  
**Future Goals:** 
  * I plan to refine the note detection and have it detect more complex sets of notes
  * I plan to make it more like a teaching tool that starts with the basics and then gradually brings the user to more complex notes to play
  * I want to add a note visualizer. It shows the note you're supposed to play 
  * I want to add the ability to toggle to other octaves 

**Problems:** 
  A problem I encountered was the frequencies having NaN and infinite values, and another problem was removing invalid notes without affecting the list of notes
  * Solution: I removed all NaN values and set all infinite values to zero with np.isnan and np.isinf
  * Solution: I used list comprehension to get rid of the invalid notes
  A problem I encountered was generating notes and chords properly without it changing when you check the notes
