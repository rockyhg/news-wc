import os
from datetime import datetime, timedelta

import openai


def jp_time_now():
    return datetime.utcnow() + timedelta(hours=9)


def jp_today():
    return jp_time_now().date()


def generate_news_text(words: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"単語: {words}\nポジティブなニュース:"
    response = openai.Completion.create(
        engine='text-davinci-003',
        # engine="text-curie-001",
        prompt=prompt,
        temperature=0.6,
        max_tokens=256,
    )
    return response["choices"][0]["text"].strip()


if __name__ == "__main__":
    text = generate_news_text("競り 乗用車 大間 豊洲 逮捕")
    print(text)
