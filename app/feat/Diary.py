from app.feat.user import getInfoUser
from Model.Diary import Diary
from datetime import  datetime

async def getDiaryDetail(full_name,date_str):
    user = await getInfoUser(full_name)
    diarys = await Diary.objects.filter(user_id=user).all()

    date = datetime.strptime(date_str, "%d/%m/%Y")
    response = "\t Your detail diary"

    for diary in diarys:
        if diary.created_at.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            response += f"  \n mood: {diary.mood} \n  main_events:{diary.main_events} \n highlights: {diary.highlights} \n challenges: {diary.challenges} \n gratitude: {diary.gratitude} \n goals: {diary.goals} \n------------- \n"
    
    return response