from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to MongoDB
uri = os.getenv('uri_mongodb')
client = MongoClient(uri,server_api=ServerApi('1'))

# Select the database
database = client["bot_telegram"]

# Define the User collection
users = database["users"]

# Define the Chat collection
chats = database["chats"]

def Chat():
    return chats
# Example usage
def create_tb():
    # Ping the MongoDB server
    database.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Create a new user
    user_id = users.insert_one({
        "name": "John Doe",
        "username": "johndoe"
    })

    # Create a new chat
    chat_id = chats.insert_one({
        "user_id": user_id.inserted_id,
        "message": "Hello, world!"
    })

    # Retrieve the chat
    chat = chats.find_one({"_id": chat_id.inserted_id})
    print(chat)

if __name__ == "__main__":
    create_tb()
