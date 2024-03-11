from databases import Database
import orm
import os
import sys
import pytz
from datetime import datetime


database = Database("sqlite:///migrations/db.sqlite")
models = orm.ModelRegistry(database=database)


def utc_now():
    return datetime.utcnow()


def convert_to_vietnam_time(utc_time):
    utc_timezone = pytz.timezone('UTC')
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    utc_time = utc_time.replace(tzinfo=utc_timezone)
    vietnam_time = utc_time.astimezone(vietnam_timezone)
    formatted_time = vietnam_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def convert_to_utc(utc_time):
    utc_timezone = pytz.timezone('UTC')
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = utc_time.replace(tzinfo=vietnam_timezone)
    utc_time = vietnam_time.astimezone(utc_timezone)
    return utc_time


class User(orm.Model):
    tablename = "users"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=255),
        "username": orm.String(max_length=100, unique=True),
    }


class Chat(orm.Model):
    tablename = "chats"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "message": orm.Text(),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now)
    }


class Spending(orm.Model):
    tablename = "spends"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "money": orm.Float(),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now)
    }


def check_connect():
    url = str(database.url)
    if url.startswith("mysql+mysqlconnector://"):
        return "Connected to MySQL database."
    else:
        return "Unsupported database type."

async def main():
    await models.create_all()
    
    await database.connect()
    try:
        user,create =await User.objects.get_or_create(username="abc2",defaults={'name':'ab2c'})
    finally:
        await database.disconnect()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())