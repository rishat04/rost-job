from this import d
from telebot import types

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(
    types.KeyboardButton(text='Создать заявку'),
    types.KeyboardButton(text='Мои заявки'),
)
main_markup.add(types.KeyboardButton(text='Правила пользования'))
main_markup.add(types.KeyboardButton(text='Меню администратора'))

user_markup = {
    'main' : main_markup
}

def gen_inline_buttons(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{id}'
        inline.add(
            types.InlineKeyboardButton(text=name, callback_data=callback_data)
        )
    return inline

def gen_inline_app(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{name}-{id}'
        inline.add(
            types.InlineKeyboardButton(text=name, callback_data=callback_data)
        )
    return inline

def gen_opened_app(admin_id, app_id):
    inline_back = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='Назад', callback_data='back')],
        [types.InlineKeyboardButton(text='Написать администратору', callback_data=f'awrite-{admin_id}-{app_id}')]
    ])
    return inline_back
