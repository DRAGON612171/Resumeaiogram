from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

but_create = ReplyKeyboardMarkup(
    keyboard=[
        [
          KeyboardButton(text='📄Створити резюме📄')
        ]
    ],
    resize_keyboard=True
)


end_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Так', callback_data='15'),
            InlineKeyboardButton(text='Ні', callback_data='16')
        ]
    ]
)

changes = InlineKeyboardMarkup(
    inline_keyboard= [
            [
             InlineKeyboardButton(text='😃Імя та прізвище😃', callback_data='1' )
            ],
            [
                InlineKeyboardButton(text='☎Номер телефону☎️', callback_data='2')
            ],
            [
                InlineKeyboardButton(text='📧Email📧', callback_data='3')
            ],
            [
                InlineKeyboardButton(text='🧐Освіта🧐', callback_data='4')
            ],
            [
                 InlineKeyboardButton(text='😄Soft Навички😄', callback_data='5' )
            ],
            [
                InlineKeyboardButton(text='😄Tech Навички😄', callback_data='14')
            ],
            [
                InlineKeyboardButton(text='😲Проекти😲', callback_data='6' )
            ],
            [
                InlineKeyboardButton(text='✌Мови✌️', callback_data='7')
            ],
            [
                InlineKeyboardButton(text='🗣Рівень мови🗣', callback_data='8' )
            ],
            [
                InlineKeyboardButton(text="👍Країна👍", callback_data='9')
            ],
            [
                InlineKeyboardButton(text="🤟Місто🤟", callback_data='10')
            ],
            [
                InlineKeyboardButton(text="👨‍🎓Професія👨‍🎓", callback_data='11')
            ],
            [
                InlineKeyboardButton(text="😱Очікування😱", callback_data='12')
            ],
            [
                InlineKeyboardButton(text="🤯Минула посада🤯", callback_data='13'),
            ],
            [
                InlineKeyboardButton(text="😱Ваша робота на минулій посаді😱", callback_data='17'),
            ],
            [
                InlineKeyboardButton(text="🤯Термін вашої минулої роботи🤯", callback_data='18'),
            ]


    ],
)


lists = ReplyKeyboardMarkup(
    keyboard=[
        [
          KeyboardButton(text='stop')
        ]
    ],
    resize_keyboard=True
)