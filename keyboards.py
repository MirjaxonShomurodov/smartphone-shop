from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_brends,get_phones_by_brend



def home_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton('Shop🏪'), KeyboardButton('Cart🛒')],
            [KeyboardButton('About👨🏻‍💻'), KeyboardButton('Contact☎️')]
        ],
        resize_keyboard=True
    )

def phones_keyboard(brend:str):
    phones = get_phones_by_brend(brend)

    keyboard = []
    for phone in phones:
        keyboard.append(
            [
                InlineKeyboardButton(text=phone['name'],callback_data=f"phone:{brend}:{phone.doc_id}")
            ]
        )
    return InlineKeyboardMarkup(keyboard)

def brends_keyboard():
    keyboards_btns = []
    row = []
    for brend in get_brends():
        row.append(InlineKeyboardButton(brend,callback_data=f'brend:{brend}'))
        if len(row) == 2:
            keyboards_btns.append(row)
            row = []

    if row:
        keyboards_btns.append(row)
    return InlineKeyboardMarkup(
        keyboards_btns
        )