from pydub import AudioSegment # uses FFMPEG
import speech_recognition as sr
from pathlib import Path
import subprocess

# '''mp3 to wav - subprocess'''
# # subprocess.call(['ffmpeg', '-i', 'data/audio.mp3','test2.wav'])
# '''mp3 to wav - pydub'''
# # sound = AudioSegment.from_mp3("audio.mp3")
# # sound.export("test.wav", format="wav")

# # '''speech recognition'''
# recognize = sr.Recognizer()
# audioFile = "harvard.wav"


# with sr.AudioFile(audioFile) as source:
#     audio = recognize.record(source)


# # text = recognize.recognize_google(audio) 
# text = recognize.recognize_google(audio, language='en-IN')
# print(text)


def audio_recognition(audioFile:str):
    print(f'Loading {audioFile} ...')
    recognize = sr.Recognizer()
    microphone = sr.Microphone()

    # print(sr.__version__)

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognize, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    try:
        with sr.AudioFile(audioFile) as audio_file:
            recognize.adjust_for_ambient_noise(audio_file)
            audio = recognize.record(audio_file)

        # text = recognize.recognize_google(audio, show_all=True)
        text = recognize.recognize_google(audio, language='zh-TW', show_all=True)
    except Exception as e:
        print(e)
    return text
