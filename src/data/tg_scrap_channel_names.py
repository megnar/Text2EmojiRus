from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import InputPeerChannel
import asyncio
import pandas as pd
import csv 

from telethon import TelegramClient

api_id = 'api_id'
api_hash = 'api_hash'
phone_number = "phone_number"

file_path = "/Users/evgeny/Desktop/study/Text2EmojiRus/data/raw/nicknames.txt"
ouput_path = "/Users/evgeny/Desktop/study/Text2EmojiRus/data/processed/channel_names.csv"

client = TelegramClient('session_name', api_id, api_hash)

groups_list = []
async def search_channels(query):
    result = await client(SearchRequest(
        q=query,  # Поисковый запрос
        limit=100  # Ограничение на количество результатов
    ))
    for chat in result.chats:
        groups_list.append(chat.username)


async def main():
    df = pd.read_csv(file_path, sep="\t")  
    names = list(df.iterrows())
    names = [el[1]['_Loo'] for el in names]
    names = names[101:400]

    await client.start(phone=phone_number)
    for name in names:
        await search_channels(name)
    
    await client.disconnect()

    with open(ouput_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["Name"])

        for name in groups_list:
            writer.writerow([name])


asyncio.run(main())

