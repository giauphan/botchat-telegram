from telebot import types

def buildKeyBoar(message,bot):
    option_buttons = [
        [types.InlineKeyboardButton("⬜ Task 1", callback_data='task1')],
        [types.InlineKeyboardButton("⬜ Task 2", callback_data='task2')]
    ]
    keyboard = types.InlineKeyboardMarkup([option_buttons])
    bot.send_message(chat_id=message.chat.id, text="Please select your options:", reply_markup=keyboard)


