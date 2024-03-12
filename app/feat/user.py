from Model.User import UserModel as User
from app.feat.slugify import slugify


async def getInfoUser(username):
    user, created = await User.objects.get_or_create(
        username=slugify(username), defaults={"name": username}
    )

    return user


async def getAllUser():
    user = await User.objects.all()

    return user


async def setUpEmail(username, email):
    user = await User.objects.filter(username=slugify(username)).first()
    await user.update(email=email)


async def setUpName(username, name):
    user = await User.objects.filter(username=slugify(username)).first()
    await user.update(name=name)


def getFullName(user):
    if user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name
