from loader import *
from keyboards.admin_departament import *
from keyboards.users import user_markup
from telebot import types

@bot.message_handler(commands=['meadmin'])
def start_departament(msg):
    user_id = msg.chat.id
    if not admin_departament.is_admin(user_id):
        bot.send_message(user_id, 'Сорри но вы не админ!')
        return
    text = read_rules('departament')
    bot.send_photo(msg.chat.id, photo=open('res/departament.jpg', 'rb'))
    bot.send_message(msg.chat.id, text=text, reply_markup=admin_dep_markup)

@bot.message_handler(text=['Меню администратора'])
def start_departament(msg):
    user_id = msg.chat.id
    if not admin_departament.is_admin(user_id):
        bot.send_message(user_id, 'Сорри но вы не админ!')
        return
    text = read_rules('departament')
    try:
        bot.send_photo(msg.chat.id, photo=open('res/departament.jpg', 'rb'))
    except:
        print('Can\'t find the photo :(')
    bot.send_message(msg.chat.id, text=text, reply_markup=admin_dep_markup)

@bot.message_handler(text=['На главную'])
def go_back(msg):
    
    text = 'Меню пользователя!'
    bot.send_message(msg.chat.id, text=text, reply_markup=user_markup['main'])

@bot.message_handler(text=['Заявки пользователей'])
def get_applications(msg):
    admin_id = msg.chat.id
    applications = application.get_applications_for_admin(admin_id)
    apps = []
    for app in applications:
        apps.append(
            [priority_emoji[app[8]]+' '+app[7],app[0]]
        )
    inline = gen_inline_app(apps, 'apopen')
    text = 'Заявки клиентов:'
    bot.send_message(msg.chat.id, text, reply_markup=inline)
    
local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('apopen'))
def open_application(call):
    action, name, id = call.data.split('-')
    chat_id = call.message.chat.id
    message_id = call.message.id
    admin_id = chat_id

    name = ' '.join(name.split(' ')[1:])

    applications = application.get_applications_for_admin(admin_id)
    for app in applications:
        if name in app:
            text = '\n'.join([
                app[7],
                'Отдел: ' + app[1],
                'Описание: ' + app[5],
                'Приоритет заявки: ' + app[8],
                'Статус заявки: ' + app[6],
                'Дата создания заявки: ' + app[9]
            ])
            action = str(app[0])
            user_id = application.get_user_by_application(name)
            app_id = app[0]
    action += '-' + str(user_id) + '-' + str(app_id)
    inline = gen_opened_app(action)

    local_db[chat_id] = {
        'header' : app[1],
        'user_id' : user_id
    }

    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=inline)

local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('status'))
def edit_status(call):
    status, app_id = call.data.split('-')
    chat_id = call.message.chat.id
    local_db[chat_id] = {
        'app_id' : app_id
    }
    bot.answer_callback_query(call.id, text='')
    bot.send_message(chat_id, text='Введите новое состояние заявки:')
    bot.register_next_step_handler(call.message, edit_status_step)

def edit_status_step(msg):
    new_status = msg.text
    app_id = local_db[msg.chat.id]['app_id']
    application.edit_status(app_id, new_status)
    bot.send_message(msg.chat.id, text='Статус заявки изменен!')

    user_id = application.get_user_id(app_id)
    header = application.get_header(app_id)

    inline = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text=header, callback_data=f'open-{header}-{app_id}')
        ]
    ])

    text = f'{header} - статус заявки изменен!'

    bot.send_message(user_id, text, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('aback'))
def back_to_applications(call):
    chat_id = call.message.chat.id
    message_id = call.message.id
    text = 'Заявки клиентов:'
    applications = application.get_applications_for_admin(chat_id)
    apps = []
    for app in applications:
        apps.append(
            [priority_emoji[app[8]]+' '+app[7],app[0]]
        )
    inline = gen_inline_app(apps, 'apopen')
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=inline)

local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('uwrite'))
def write_to_user(call):
    _, user_id, app_id = call.data.split('-')
    local_db[call.message.chat.id] = {
        'user_id' : int(user_id),
        'app_id':app_id
    }
    bot.answer_callback_query(call.id, text='')
    bot.send_message(call.message.chat.id, 'Введите текст для отправки:')
    bot.register_next_step_handler(call.message, write_to_user_last_step)

def write_to_user_last_step(msg):
    app_id = local_db[msg.chat.id]['app_id']
    header = application.get_header(app_id)
    text = f'Заявка-{header}\n{msg.text}'
    user_id = local_db[msg.chat.id]['user_id']
    inline = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text='Ответить', callback_data=f'awrite-{msg.chat.id}-{app_id}')
        ]
    ])
    bot.send_message(user_id, text, reply_markup=inline)
    bot.send_message(msg.chat.id, 'Сообщение отправлено!')
