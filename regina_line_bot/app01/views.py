from django.shortcuts import render
import json
import os
from pydub import AudioSegment

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
            print(f'message info: {event}')
            event_type = event.message.type
            if event_type == 'text':
                if isinstance(event, MessageEvent):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=event.message.text)
                    )
            elif event_type == 'audio':
                # Get the audio and save it to a file
                content = request.body
                filename = f'{event.message.id}'
                filepath = os.path.join(filename+'.wav')
                with open(filepath, 'wb') as f:
                    f.write(content)
                

                # audio = AudioSegment.from_file(f'{filename}.m4a', format="m4a")
                # audio.export(filename+'.wav', format="wav")

                if isinstance(event, MessageEvent):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='我正在學習如何接收audio訊息')
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
   