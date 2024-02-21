import orm
import databases
import sys
import os

# Add the parent directory of 'database.migrations' to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)

# Import Chat model from 'create_table_chat.py' module
from migrations.create_table_chat import Chat

database = databases.Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)

async def main():
    await Chat.objects.create(id=1)
    chat_obj = await Chat.objects.get(id=1)
    print(chat_obj)

    # Call main function from ChatSeed.py
    await seed_main()

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
