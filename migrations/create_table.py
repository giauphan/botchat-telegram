from databases import Database
import orm
import pytz
from datetime import datetime

database = Database("sqlite:///migrations/db.sqlite")
models = orm.ModelRegistry(database=database)


def utc_now():
    return datetime.utcnow()


def convert_to_vietnam_time(utc_time):
    utc_timezone = pytz.timezone("UTC")
    vietnam_timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    utc_time = utc_time.replace(tzinfo=utc_timezone)
    vietnam_time = utc_time.astimezone(vietnam_timezone)
    formatted_time = vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def convert_to_utc(utc_time):
    utc_timezone = pytz.timezone("UTC")
    vietnam_timezone = pytz.timezone("Asia/Ho_Chi_Minh")
    vietnam_time = utc_time.replace(tzinfo=vietnam_timezone)
    utc_time = vietnam_time.astimezone(utc_timezone)
    return utc_time


class User(orm.Model):
    tablename = "users"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=255),
        "email": orm.String(max_length=255, allow_null=True),
        "username": orm.String(max_length=100, unique=True),
        "account_balance": orm.Float(default=0),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


class Chat(orm.Model):
    tablename = "chats"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "message": orm.Text(),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


class Spending(orm.Model):
    tablename = "spends"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "money": orm.Float(),
        "notes": orm.String(max_length=255, allow_null=True),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


class Income(orm.Model):
    tablename = "incomes"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "amount": orm.Float(),
        "source": orm.String(max_length=255, allow_null=True),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


class Diary(orm.Model):
    tablename = "diaries"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "mood": orm.String(max_length=50),
        "main_events": orm.Text(),
        "highlights": orm.Text(),
        "challenges": orm.Text(),
        "gratitude": orm.Text(),
        "goals": orm.Text(),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


class Issue(orm.Model):
    tablename = "issues"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "title": orm.String(max_length=255,index=True),
        "description": orm.Text(),
        "completed":orm.Boolean(default=False),
        "created_at": orm.DateTime(default=utc_now),
        "updated_at": orm.DateTime(default=utc_now),
    }


async def main():
    await models.create_all()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
