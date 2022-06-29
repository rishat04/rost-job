from telebot import types

admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(types.KeyboardButton(text='Управление компаниями'))
admin_markup.add(types.KeyboardButton(text='Управление администраторами'))
admin_markup.add(types.KeyboardButton(text='Редактировать тексты приветствия'))
#admin manage markup
am_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
am_markup.add(types.KeyboardButton(text='Назначить администратора'))
am_markup.add(types.KeyboardButton(text='Удалить администратора'))
am_markup.add(types.KeyboardButton(text='Назад'))
#companies manage markup
cm_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
cm_markup.add(types.KeyboardButton(text='Создать компанию'))
cm_markup.add(types.KeyboardButton(text='Удалить компанию'))
cm_markup.add(types.KeyboardButton(text='Назад'))

def gen_inline_buttons(object, action):
    inline = types.InlineKeyboardMarkup()
    for name, id in object:
        callback_data = f'{action}-{str(name)}-{id}'
        inline.add(
            types.InlineKeyboardButton(text=str(name), callback_data=callback_data)
        )
    return inline

edit_rules_markup = types.InlineKeyboardMarkup(keyboard=[
    [types.InlineKeyboardButton(text='Пользователи', callback_data='rules-users')],
    [types.InlineKeyboardButton(text='Администраторы компаний', callback_data='rules-company')],
    [types.InlineKeyboardButton(text='Администраторы отделов', callback_data='rules-departament')]
])