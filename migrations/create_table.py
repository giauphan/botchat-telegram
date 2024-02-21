import databases
import orm

database = databases.Database("sqlite:///db.sqlite")

models = orm.ModelRegistry(database=database)

class User(orm.Model):
    tablename = "User"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=100),
        "username": orm.String(max_length=100, unique=True), 
    }
class Chat(orm.Model):
    tablename = "Chat"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "user_id": orm.ForeignKey(User),
        "message": orm.String(max_length=255),
    }

async def main():
    await models.create_all()

import asyncio
asyncio.run(main())
