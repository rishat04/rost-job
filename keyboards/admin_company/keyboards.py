from telebot import types

admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(types.KeyboardButton(text='Управление отделами'))
admin_markup.add(types.KeyboardButton(text='Управелние администраторами компании'))
#admin manage  markup
am_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
am_markup.add(types.KeyboardButton(text='Добавить администратора'))
am_markup.add(types.KeyboardButton(text='Убрать администратора'))
am_markup.add(types.KeyboardButton(text='Назад!'))
#departament manage markup
dm_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
dm_markup.add(types.KeyboardButton(text='Создать отдел'))
dm_markup.add(types.KeyboardButton(text='Удалить отдел'))
dm_markup.add(types.KeyboardButton(text='Назад!'))

def gen_inline_buttons(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{str(name)}-{id}'
        inline.add(
            types.InlineKeyboardButton(text=str(name), callback_data=callback_data)
        )
    return inline

def gen_dep_list(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{name}-{id}'
        
        inline.add(
            types.InlineKeyboardButton(text=name, callback_data=callback_data)
        )
    return inline

def gen_actions(id):
    return types.InlineKeyboardMarkup(keyboard=[
            [
                types.InlineKeyboardButton(text='Редактировать название', callback_data=f'dedit-{id}')
            ],
            [
                types.InlineKeyboardButton(text='Удалить отдел', callback_data=f'ddelete-{id}')
            ],
            [
                types.InlineKeyboardButton(text='Назначить администратора', callback_data=f'aadd-{id}')
            ],
            [
                types.InlineKeyboardButton(text='Назад', callback_data='dback')
            ]
        ])