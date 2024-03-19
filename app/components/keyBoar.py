from telebot import types

def buildKeyBoar():
    option_buttons = [
        types.InlineKeyboardButton("⬜ Task 1", callback_data='option_1'),
        types.InlineKeyboardButton("⬜ Task 2", callback_data='option_2'),
        types.InlineKeyboardButton("⬜ Task 3", callback_data='option_3')
    ]

    keyboard = types.InlineKeyboardMarkup([option_buttons])

    return keyboard
    


def showKeyboardSuccess(user_id,user_choices):
    keyboard = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(f"{choice} ✅" if choice in user_choices[user_id] else f"{choice} ⬜️", callback_data=choice) for choice in ["option_1", "option_2", "option_3"]]])
    return keyboard

