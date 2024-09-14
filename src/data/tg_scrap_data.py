from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import InputPeerChannel
import asyncio
import pandas as pd
import csv 

from telethon import TelegramClient
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

from telethon import TelegramClient, events
import asyncio

DetectorFactory.seed = 0


api_id = 'api_id'
api_hash = 'api_hash'
phone_number = "phone_number"



file_path = "/Users/evgeny/Desktop/study/Text2EmojiRus/data/raw/nicknames.txt"
ouput_path = "/Users/evgeny/Desktop/study/Text2EmojiRus/data/processed/channel_names.csv"
result_path = "/Users/evgeny/Desktop/study/Text2EmojiRus/data/processed/text_and_emoji.csv"


def contains_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # смайлики
        "\U0001F300-\U0001F5FF"  # символы и пиктограммы
        "\U0001F680-\U0001F6FF"  # транспорт и символы
        "\U0001F700-\U0001F77F"  # дополнительные символы
        "\U0001F780-\U0001F7FF"  # геометрические символы
        "\U0001F800-\U0001F8FF"  # дополнительные символы
        "\U0001F900-\U0001F9FF"  # дополнительные символы
        "\U0001FA00-\U0001FA6F"  # дополнительные символы
        "\U0001FA70-\U0001FAFF"  # дополнительные символы
        "\U00002702-\U000027B0"  # символы
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def check_all_not_emoji(elements):
    return all(not contains_emoji(element.text) for element in elements if isinstance(element.text, str))


def is_russian(text_list):
    for text in text_list:
        try:
            language = detect(text)
            if language != 'ru':
                return False
        except LangDetectException:
            # Если не удалось определить язык, возвращаем False
            return False
    return True

def check_is_russian(elements):
    count = 0
    for element in elements: 
        if isinstance(element.text, str) and is_russian(element.text):
          count += 1
    return count == 3


client = TelegramClient('session_name', api_id, api_hash)
result = []
df = pd.read_csv(ouput_path)  
df = df.dropna()

async def scrape_channel(channel_username):
    channel = await client.get_entity(channel_username)
    messages = await client.get_messages(channel, limit=3) 
    if not check_all_not_emoji(messages) and check_is_russian(messages):
      messages = await client.get_messages(channel, limit=3000)
      for message in messages:
        result.append(message.text)

async def main():
    await client.start(phone=phone_number)

    channels_to_scrape = [el[1]["Name"] for el in  list(df.iterrows())[200:250]]
    
    for channel in channels_to_scrape:
        await scrape_channel(channel)
      
    await client.disconnect()

    result2 = [x for x in result if x]

    with open(result_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        for name in result2:
            writer.writerow([name])


asyncio.run(main())

