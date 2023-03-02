# speech recognition (py)

# 環境

- flac.exe
    - 可能面臨到的錯誤訊息: Installing Flac command line tool on Windows
    - 解決方法: 
        - 下載 flac.exe
        - paste it inside C:\Windows\System32 this directory 或者專案目錄
        - 可以試跑看看，如仍報錯，將 flac.exe 改成 flac 檔即可
    - ref: https://stackoverflow.com/questions/65939571/installing-flac-command-line-tool-on-windows

- 下載 ffmpeg，並將 bin 路徑(路徑放在哪裡都可以)添加到環境變數
    - 解壓縮後，重開一個 cmd，輸入 ffmpeg --version，有訊息表示安裝成功
    - ref:
        - python库ffmpeg的错误解决方法：“Couldn‘t find ffmpeg or avconv - defaulting to ffmpeg, but may not work“: https://blog.csdn.net/qq_44921056/article/details/119615360
        - https://ffmpeg.org/download.html#build-windows
        - 最後使用的下載點: https://www.gyan.dev/ffmpeg/builds/ (下載-full_build.7z)
- 如出現以下錯誤，可參考:https://blog.csdn.net/qq_38161040/article/details/91501760
    RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
    warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)

- python packages:
    - speech recognition
    - pydub (用來將 mp3 轉成 wav，因 python speech recognition 目前只支援 wav 格式)
    - 補充: mp3 轉 wav 方法
        1) subprocess (內建的package) 
            ```
           import subprocess
           subprocess.call(['ffmpeg', '-i', 'data/audio.mp3','test2.wav'])
            ```
        2) pydub
            ```
            from pydub import AudioSegment # uses FFMPEG
            sound = AudioSegment.from_mp3("data/audio.mp3")
            sound.export("test.wav", format="wav")
            ```

- code
    - demo.py
    ```
    from pydub import AudioSegment # uses FFMPEG
    import speech_recognition as sr
    from pathlib import Path
    import subprocess

    '''mp3 to wav - subprocess'''
    # subprocess.call(['ffmpeg', '-i', 'data/audio.mp3','test2.wav'])
    '''mp3 to wav - pydub'''
    # sound = AudioSegment.from_mp3("data/audio.mp3")
    # sound.export("test.wav", format="wav")


    '''speech recognition'''
    recognize = sr.Recognizer()
    audioFile = "test.wav"

    with sr.AudioFile(audioFile) as source:
        audio = recognize.record(source)

    print(audio)
    try:
        text = recognize.recognize_google(audio) 
        #text = recognize.recognize_google(audio, language='en-IN', show_all=True)
        print(text)
    except Exception as e:
        print(e)
    ```
    
### references

1. How to Convert Speech to Text in Python: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
2. Installing Flac command line tool on Windows: https://stackoverflow.com/questions/65939571/installing-flac-command-line-tool-on-windows