from migrations.create_table import User,database

class UserModel(User):
    database.connect()
    pass
    database.disconnect
    async def CheckUser(username : str):
        user = await User.objects.filter(username=username).exists()
        return user
