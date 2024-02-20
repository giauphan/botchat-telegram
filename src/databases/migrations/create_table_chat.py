import databases
import orm

database = databases.Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)


class Chat(orm.Model):
    tablename = "chats"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
    }

models.create_all()