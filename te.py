import asyncio
import databases
import orm

database = databases.Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)


class Note(orm.Model):
    tablename = "notes"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "text": orm.String(max_length=100),
        "completed": orm.Boolean(default=False),
    }


async def main():
    # Create the database and tables
    await models.create_all()

    await Note.objects.create(text="Buy the groceries.", completed=False)

    note = await Note.objects.get(id=1)
    print(note)


if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        print("Event loop is already running. Cannot run asyncio.run()")
    else:
        asyncio.run(main())
