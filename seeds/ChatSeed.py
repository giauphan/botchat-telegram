import orm
import os, sys, pytz
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from migrations.create_table import User, database
from migrations.create_table import convert_to_vietnam_time


async def main():
    # # # Seed Chat data
    user, create = await User.objects.get_or_create(
        username="abc", defaults={"name": "abc"}
    )
    chat_objects = await User.objects.all()
    for chat_obj in chat_objects:
        create_at = chat_obj.create_at
        vietnam_time = convert_to_vietnam_time(create_at)
        print(vietnam_time)


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
