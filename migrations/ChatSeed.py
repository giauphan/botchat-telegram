import os, sys
from pymongo import MongoClient
from pymongo.server_api import ServerApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


uri = os.getenv('uri_mongodb')
client = MongoClient(uri,server_api=ServerApi('1'))
database = client["bot_telegram"]
chats = database["chats"]

def seed():
    database.command('ping')
    all_chats = chats.find_one()
    
    print(all_chats)



if __name__ == "__main__":
    seed()
