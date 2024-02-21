import orm
from create_table_chat import Chat, User

async def main():
    # user = await User.objects.create( name="John Doe", username="john_doe")

    # # # Seed Chat data
    # await Chat.objects.create( user_id=user, message="Hello, World 3!")
    chat_objects  = await Chat.objects.all()
    for chat_obj in chat_objects :
        print(chat_obj.message)

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
