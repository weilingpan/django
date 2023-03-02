from pydub import AudioSegment # uses FFMPEG
import speech_recognition as sr
from pathlib import Path
import subprocess

'''mp3 to wav - subprocess'''
# subprocess.call(['ffmpeg', '-i', 'data/audio.mp3','test2.wav'])
'''mp3 to wav - pydub'''
# sound = AudioSegment.from_mp3("data/audio.mp3")
# sound.export("test.wav", format="wav")


# '''speech recognition'''
# recognize = sr.Recognizer()
# audioFile = "test.wav"

# with sr.AudioFile(audioFile) as source:
#     audio = recognize.record(source)

# print(audio)
# try:
#     text = recognize.recognize_google(audio) 
#     #text = recognize.recognize_google(audio, language='en-IN', show_all=True)
#     print(text)
# except Exception as e:
#     print(e)