import openai
import requests

import secret

openai.api_key = secret.openai_api_key

# list models
models = openai.Model.list()
# print(models)


def chat_with_chatgpt_using_openai(text:str):
    response = openai.Completion.create(
        engine = "text-davinci-003", #model
        prompt = text,     
        max_tokens = 512, # 回覆文句的 token 數與 prompt 的 token 數合計不能超過所使用模型的限制。text-davinci-003 加總後不能超過 4097
        temperature = 0.6, # 0~1 的冒險程度。設為 0 就會像是一個背答案的機器人, 永遠只選預測機率最高的那一個 token, 同樣的提示就會回答一樣的文句。
        top_p = 0.75,
        n = 3, # 回覆的語句
        #presence_penalty: -2.0~2.0, 值越大越會懲罰用過的 token, 也就是鼓勵產生語句時使用新的 token。
    )
    return response

def chat_with_chatgpt_using_gpt35(text:str):
    message_log = [
        {"role": "system", "content": "一位資深軟體工程師"}, #設定人設
        {"role": "user", "content": text}
    ]

    response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",  
            messages = message_log, 
            max_tokens = 3800,
            stop = None,
            temperature = 0.7, 
    )
    return response

def chat_with_chatgpt_using_requests(text:str):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {secret.openai_api_key}'
        },
        json = {
            'model': 'text-davinci-003',
            'prompt': text,
            'temperature': 0.6,
            'max_tokens': 512,
            'top_p': 0.75,
            'n': 3
        }
    )
    return response

# response_result = chat_with_chatgpt_using_openai(text='chatgpt簡介')
# reply_text = response_result["choices"][0]["text"]
# print(reply_text)

# response_result = chat_with_chatgpt_using_requests(text='chatgpt簡介')
# reply_text = response_result.json()['choices'][0]['text']
# print(reply_text)