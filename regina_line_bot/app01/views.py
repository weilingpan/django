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
from linebot.models import MessageEvent, TextSendMessage, Sender

from app01.core import my_openai
from app01.core import my_speech_recognition

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
                # if isinstance(event, MessageEvent):
                #     replay_text = my_openai.chat_with_chatgpt_using_gpt35(text=event.message.text)["choices"][0]["message"]["content"].strip()
                #     # replay_text = my_openai.chat_with_chatgpt_using_openai(text=event.message.text)["choices"][0]["text"].strip()
                #     # replay_text = my_openai.chat_with_chatgpt_using_requests(text=event.message.text).json()['choices'][0]['text']
                #     line_bot_api.reply_message(
                #         event.reply_token,
                #         TextSendMessage(text=replay_text)
                #     )
                # if isinstance(event, MessageEvent):
                #     replay_text = my_openai.chat_with_chatgpt_using_gpt35(text=event.message.text)["choices"][0]["message"]["content"].strip()
                #     # replay_text = my_openai.chat_with_chatgpt_using_openai(text=event.message.text)["choices"][0]["text"].strip()
                #     # replay_text = my_openai.chat_with_chatgpt_using_requests(text=event.message.text).json()['choices'][0]['text']
                #     line_bot_api.reply_message(
                #         event.reply_token,
                #         TextSendMessage(
                #             text=replay_text,
                #             sender=Sender(
                #                 name="gpt-3.5 的回覆",
                #                 icon_url="https://media.istockphoto.com/id/1271533802/zh/%E5%90%91%E9%87%8F/%E7%BE%8E%E5%91%B3%E7%9A%84%E5%9C%96%E7%A4%BA%E9%A5%91%E9%A4%93%E7%9A%84%E7%AC%91%E8%87%89%E8%88%87%E5%98%B4%E5%92%8C%E8%88%8C%E9%A0%AD%E8%A1%A8%E6%83%85%E7%AC%A6%E8%99%9F%E7%BE%8E%E5%91%B3-%E5%81%A5%E5%BA%B7%E6%90%9E%E7%AC%91%E5%8D%88%E9%A4%90%E7%BE%8E%E5%91%B3%E5%BF%83%E6%83%85%E5%BE%AE%E7%AC%91%E9%A0%AD%E5%83%8F%E5%BF%AB%E6%A8%82%E9%BB%83%E8%89%B2%E5%AD%97%E5%85%83%E5%8F%AF%E6%84%9B%E5%90%91%E9%87%8F%E9%9A%94%E9%9B%A2%E5%8D%A1%E9%80%9A%E7%AC%A6%E8%99%9F.jpg?s=170667a&w=0&k=20&c=zdJWRnV6Ok6kEep-jRPhDt4BjEqfXKRAR0nWN5BpOp8=")
                #         )
                #     )
                    
            elif event_type == 'audio':
                # Get the audio and save it to a file
                filename = f'app01/data/{event.message.id}'
                # _file_ = f'https://api-data.line.me/v2/bot/message/{event.message.id}/content'
                message_content = line_bot_api.get_message_content(event.message.id)
                with open(f"{filename}.m4a", "wb") as f:
                    for chunk in message_content.iter_content():
                        f.write(chunk)

                audio = AudioSegment.from_file(f'{filename}.m4a', format="m4a")
                audio.export(filename+'.wav', format="wav")

                message = my_speech_recognition.audio_recognition(filename+'.wav')
                if isinstance(event, MessageEvent):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=
                        f'我正在學習如何接收audio訊息。\n\n你說: 「{message["alternative"][0]["transcript"]}」')
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
   