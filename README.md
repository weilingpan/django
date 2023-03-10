# Enviorment

> pip install Django

> conda install -c conda-forge django

> pip install line-bot-sdk

> 建立專案: django-admin startproject '專案名稱'

> 建立 APP: python manage.py startapp 'APP名稱'

`一個專案底下，可以同時進行多個LINE BOT的開發，每個LINE BOT都有一個獨立的APP資料夾，但在同一個專案底下會使用共用的專案設定`

# Django 設定
0. 在專案底下建立兩個空資料夾，方便後續使用
    ```shell
    md templates
    md static
    ```

1. 專案底下更改 settings.py

    1.1 設定個人的 LINE Channel Access Token & Channel Secret
    ```python
    LINE_CHANNEL_ACCESS_TOKEN = '你的LINE Channel Access Token'
    LINE_CHANNEL_SECRET = '你的LINE Channel Secret'
    ```

    1.2 更改 INSTALLED_APPS: 在INSTALLED_APPS內新增剛剛建立的APP名稱

    1.3 在TEMPLATES中新增，templates的資料夾路徑
    ```python
    'DIRS': [os.path.join(BASE_DIR,'templates')],#指定templates資料夾路徑
    ```

    1.4 新增static路徑
    ```python
    STATICILES_DIRS = [
    os.path.join(BASE_DIR,'static')#指定static資料夾路徑
    ]
    ```

    1.5 語系、時區的設定，預設是美國
    ```python
    LANGUAGE_CODE = 'zh-hant'
    TIME_ZONE = 'Asia/Taipei'
    ```

    1.6 ALLOWED_HOSTS

    開發階段Allowed_Host也先設定為*，若是有固定的Host或後續使用ngrok等進行測試時，需在此修改。

2. 專案底下更改urls.py
    目前預設的是當進入127.0.0.1:8000/admin的時候，會進入Django內建後台的設定，如後續有建立line bot時，需添加 webhook URL。

3. 資料庫遷移的初始化
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

4. 創建後台 superuser 用戶
    ```shell
    python manage.py createsuperuser
    ```
    會請你輸入使用者名稱、電子信箱以及密碼

5. 執行
    ```shell
    python manage.py runserver
    ```
    開啟網頁確認:127.0.0.1:8000/admin

    便可以使用步驟 4 設定的權限進入

# Line Bot 實作

*在設計LINE BOT的過程中，主程式可以是任何的檔案，這邊以內建的views.py為範例

## 實作1 - 如何建立 echo bot

- 在views.py檔案當中定義了一個名為callback的函數，當此函數被呼叫使用時，將是收到由LINE官方所發過來到你的LINE BOT的webhook
    ```python
    from django.shortcuts import render

    # Create your views here.
    from django.conf import settings
    from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
    from django.views.decorators.csrf import csrf_exempt

    from linebot import LineBotApi, WebhookParser
    from linebot.exceptions import InvalidSignatureError, LineBotApiError
    from linebot.models import MessageEvent, TextSendMessage

    line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

    @csrf_exempt
    def callback(request):
    
        if request.method == 'POST':
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body = request.body.decode('utf-8')
    
            try:
                events = parser.parse(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()
            except LineBotApiError:
                return HttpResponseBadRequest()
    
            for event in events:
                if isinstance(event, MessageEvent):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    ```
- 在urls.py對url/callback的觸發進行配置
    ```python
    from 'APP名稱' import views # Add this line
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("callback/", views.callback) # Add this line
    ]
    ```
- 在setting.py設定ALLOWED_HOSTS
    ```python
    ALLOWED_HOSTS = ['xxxxx.ngrok.io']
    ```

- LINE Developer後台貼的webhook URL貼上
    'https://xxxx.ngrok.io/callback/'


## 實作2 - 搭配 OpenAI 服務，建立 GPT3.5 聊天機器人
> pip install openai

> 準備 openai key: [連結](https://platform.openai.com/)

[參考 regina_line_bot/app01/core/my_openai.py](regina_line_bot/app01/core/my_openai.py)

[ref: 【技術分享】2023/03/01 ChatGPT API可以用啦！快速Setup你的ChatGPTAPI](https://axk51013.medium.com/%E6%8A%80%E8%A1%93%E5%88%86%E4%BA%AB-2023-03-01-chatgpt-api%E5%8F%AF%E4%BB%A5%E7%94%A8%E5%95%A6-2435b6d23bbd)

## 實作3 - 建立 speech recognition bot
[參考 regina_line_bot/app01/core/my_speech_recognition.py](regina_line_bot/app01/core/my_speech_recognition.py)

> pip install pyaudio

> pip install SpeechRecognition

> pip install pydub

- flac.exe

    - 可能面臨到的錯誤訊息: Installing Flac command line tool on Windows
    - 解決方法:
    下載 flac.exe paste it inside C:\Windows\System32 this directory 或者專案目錄
    可以試跑看看，如仍報錯，將 flac.exe 改成 flac 檔即可。
    - 留意是否有 libFLAC.dll 檔案
    - ref: [installing-flac-command-line-tool-on-windows](https://stackoverflow.com/questions/65939571/installing-flac-command-line-tool-on-windows)

- 下載 ffmpeg，並將 bin 路徑(路徑放在哪裡都可以)添加到環境變數

    - 解壓縮後，重開一個 cmd，輸入 ffmpeg --version，有訊息表示安裝成功
    - ref:
        - python库ffmpeg的错误解决方法：“Couldn‘t find ffmpeg or avconv - defaulting to ffmpeg, but may not work“: [ref](https://blog.csdn.net/qq_44921056/article/details/119615360)
        - [ref](https://ffmpeg.org/download.html#build-windows)
        - 最後使用的 [下載點](https://www.gyan.dev/ffmpeg/builds/) (下載-full_build.7z)

<br>

# 補充

1. 如何移除專案下其中一個APP
https://thomsawyer.medium.com/how-to-delete-remove-an-app-from-a-django-project-bc847553804c
