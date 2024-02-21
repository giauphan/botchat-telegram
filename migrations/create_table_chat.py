import databases
import orm

database = databases.Database("sqlite:///db.sqlite")

models = orm.ModelRegistry(database=database)

class Chat(orm.Model):
    __tablename__ = "chats"
    id = orm.Integer(primary_key=True)

async def main():
    await models.create_all()

# Run the main function
import asyncio
asyncio.run(main())
