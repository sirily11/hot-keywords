import os
import pandas as pd
from tqdm import tqdm
from time import sleep
import requests, uuid, json


def translate(content: str):
    subscription_key = os.getenv('key')
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    location = "global"
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'zh-CN',
        'to': ['en']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': content
    }]
    error = 0
    while error < 3:
        try:
            request = requests.post(constructed_url, params=params, headers=headers, json=body)
            response = request.json()
            result = response[0]['translations'][0]['text']
            return result
        except Exception as e:
            print(e)
            sleep(1)
            error += 1
            continue

    return None


data = pd.read_csv("/Users/liqiwei/Desktop/Sina_keyword.csv", error_bad_lines=False,
                   names=['Keyword', 'Content', 'Time', 'Rank', 'Number'])
data = data.sample(20000)

tqdm.pandas()

data['English_content'] = data.progress_apply(lambda row: translate(row['Content']), axis=1)
data.to_csv('translated.csv')

