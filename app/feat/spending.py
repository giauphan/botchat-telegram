from Model.User import UserModel as User
from Model.Spending import SpendingModel as Spending
from datetime import datetime
from app.feat.user import get_info_user

async def getSpending(full_name,date_str):
    user = await get_info_user(full_name)
    spending = await Spending.objects.filter(user_id=user).all()

    date = datetime.strptime(date_str, "%d/%m/%Y")
    money = sum(s.money for s in spending if s.created_at.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"))

    return money