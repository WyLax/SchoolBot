from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

def button(list, num):

    keyboard_rows = [
        [InlineKeyboardButton(text=c, callback_data=c) for c in list[i:i + num]]
        for i in range(0, len(list), num)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
