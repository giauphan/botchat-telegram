from Model.User import UserModel as User
from app.feat.slugify import slugify

async def get_info_user(username):
    user, created = await User.objects.get_or_create(username=slugify(username), defaults={"name": username})

    return user
