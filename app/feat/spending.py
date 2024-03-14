from Model.User import UserModel as User
from Model.Spending import Spending
from app.feat.user import getInfoUser
from datetime import timedelta, datetime


async def getSpending(full_name, date_str):
    user = await getInfoUser(full_name)
    spending = await Spending.objects.filter(user_id=user).all()

    date = datetime.strptime(date_str, "%d/%m/%Y")
    money = sum(
        s.money
        for s in spending
        if s.created_at.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d")
    )

    return money


async def getSpendingDetail(full_name, date_str):
    user = await getInfoUser(full_name)
    spendings = await Spending.objects.filter(user_id=user).all()

    date = datetime.strptime(date_str, "%d/%m/%Y")
    data = []
    response = None
    total = 0
    for spending in spendings:
        if spending.created_at.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            total += spending.money
            data.append((spending.notes, spending.money))

    if len(data) > 0:
        response = f"{full_name} spending on {date_str}:\n"
        for notes, money in data:
            format_money = formatMoney(float(money))
            response += f"Notes: {notes}, Amount: {format_money}\n"
        response += f"Total: {formatMoney(float(total))}"
        return response
    return response


async def sumMoneyLast7Weeks(user_id):

    seven_days_ago = datetime.now() - timedelta(days=7)

    records = await Spending.objects.filter(
        created_at__gte=seven_days_ago, user_id=user_id
    ).all()

    total_money_spent = sum(record.money for record in records)

    return total_money_spent, seven_days_ago


def formatMoney(money):
    format_money = "{:,.3f}".format(float(money)) + "vnđ"
    return format_money
