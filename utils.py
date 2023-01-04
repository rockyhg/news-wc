import os
from datetime import datetime, timedelta

import openai


def jp_time_now():
    return datetime.utcnow() + timedelta(hours=9)


def jp_today():
    return jp_time_now().date()


def generate_news_text(words: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.organization = "org-y155exy2X3GLXAAxqJwgQWxr"
    prompt = f'''単語: 東京証券取引所 大発会 株価 値下がり 取り引き 滑り出し
ニュース: 東京証券取引所でことし最初の取り引きが始まり、恒例の大発会で出席者らが活発な取り引きを祈願しました。ただ、株価は値下がりし、厳しい滑り出しとなっています。
単語: {words}
ニュース:'''
    response = openai.Completion.create(
        # engine='text-davinci-003',
        engine='text-curie-001',
        prompt=prompt,
        temperature=0.6,
        max_tokens=256,
    )
    return response['choices'][0]['text'].strip()
