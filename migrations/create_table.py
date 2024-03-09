import databases
import orm , os,sys, pytz
from datetime import datetime
import uuid

database = databases.Database("sqlite:///db.sqlite")

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
    vietnam_time  = utc_time.replace(tzinfo=vietnam_timezone)
    utc_time = vietnam_time.astimezone(utc_timezone)
    return utc_time

class User(orm.Model):
    tablename = "User"
    registry = models
    fields = {
        "id": orm.UUID(primary_key=True,default=uuid.uuid4),
        "name": orm.String(max_length=100),
        "username": orm.String(max_length=100, unique=True), 
        "create_at":orm.DateTime(default=utc_now)
    }
class Chat(orm.Model):
    tablename = "Chat"
    registry = models
    fields = {
        "id": orm.UUID(primary_key=True,default=uuid.uuid4),
        "user_id": orm.ForeignKey(User),
        "message": orm.Text(),
        "create_at":orm.DateTime(default=utc_now)
    }
class Spending(orm.Model):
    tablename = "spending"
    registry = models
    fields = {
        "id": orm.UUID(primary_key=True,default=uuid.uuid4),
        "user_id": orm.ForeignKey(User),
        "money": orm.Float(),
        "create_at":orm.DateTime(default=utc_now)
    }

def checkConnect():
    url = str(database.url)
    if url.startswith("sqlite://"):
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        PARENT_DIR = os.path.dirname(CURRENT_DIR)
        sys.path.append(PARENT_DIR)
        path = PARENT_DIR +url[len("sqlite://"):]
        if os.path.exists(path):
            return "Database file exists and is accessible."
        else:
            return f"Database file does not exist or is not accessible.{path} {PARENT_DIR}"
    else:
        return "Unsupported database type."

async def main():
    await models.create_all()

import asyncio
asyncio.run(main())
