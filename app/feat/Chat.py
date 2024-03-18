from app.feat.user import getInfoUser,getFullName
from Model.Chat import ChatModel as Chat
from app.feat.SaveLog import log,logger

async def saveChat(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        await Chat.objects.create(user_id=user, message=message.text)
        
    except Exception as e:
        logger.error(f"Error saving chat: {e}")

async def statistics(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        num_messages = await Chat.objects.filter(user_id=user).count()
        return num_messages or 0
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")