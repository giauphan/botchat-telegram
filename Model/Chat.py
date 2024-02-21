from pymongo import MongoClient
import os

uri = os.getenv('uri_mongodb')
client = MongoClient(uri, tls=True)
database = client["bot_telegram"]
chats = database["chats"]

class ChatModel:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def Chat():
     return chats

