from telebot import types

admin_dep_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_dep_markup.add(types.KeyboardButton(text='Заявки пользователей'))
admin_dep_markup.add(types.KeyboardButton(text='На главную'))

def gen_inline_app(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{name}-{id}'
        inline.add(
            types.InlineKeyboardButton(text=name, callback_data=callback_data)
        )
    return inline

def gen_opened_app(action):
    app_id, user_id, app_id = action.split('-')
    inline = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='Изменить статус заявки', callback_data=f'status-{app_id}')],
        [types.InlineKeyboardButton(text='Написать пользователю', callback_data=f'uwrite-{user_id}-{app_id}')],
        [types.InlineKeyboardButton(text='Назад', callback_data='aback')]
    ])
    return inline