from migrations.create_table import User

class UserModel(User):
    pass
    async def CheckUser(username : str):
        user = await User.objects.filter(username=username).exists()
        return user
