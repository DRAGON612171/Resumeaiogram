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
    inline_keyboard=[
            [
             InlineKeyboardButton(text='😃Імя та прізвище😃', callback_data='name_surname' )
            ],
            [
                InlineKeyboardButton(text='☎Номер телефону☎️', callback_data='phone')
            ],
            [
                InlineKeyboardButton(text='📧Email📧', callback_data='email')
            ],
            [
                InlineKeyboardButton(text='🧐Освіта🧐', callback_data='education')
            ],
            [
                 InlineKeyboardButton(text='😄Soft Навички😄', callback_data='soft_skills' )
            ],
            [
                InlineKeyboardButton(text='😄Tech Навички😄', callback_data='tech_skills')
            ],
            [
                InlineKeyboardButton(text='😲Проекти😲', callback_data='projects' )
            ],
            [
                InlineKeyboardButton(text='✌Мови✌️', callback_data='lang')
            ],
            [
                InlineKeyboardButton(text='🗣Рівень мови🗣', callback_data='lang_level' )
            ],
            [
                InlineKeyboardButton(text="👍Країна👍", callback_data='country')
            ],
            [
                InlineKeyboardButton(text="🤟Місто🤟", callback_data='city')
            ],
            [
                InlineKeyboardButton(text="👨‍🎓Професія👨‍🎓", callback_data='profession')
            ],
            [
                InlineKeyboardButton(text="😱Очікування😱", callback_data='description')
            ],
            [
                InlineKeyboardButton(text="🤯Минула посада🤯", callback_data='past_work'),
            ],
            [
                InlineKeyboardButton(text="😱Що ви робили на минулій посаді😱", callback_data='job_description'),
            ],
            [
                InlineKeyboardButton(text="🤯Термін вашої минулої роботи🤯", callback_data='how_long'),
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

confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Підтвердити', callback_data='confirm'),
            InlineKeyboardButton(text='Скасувати', callback_data='cancel')
        ]
    ]
)