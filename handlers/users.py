from loader import bot, company, departament, application, admin_departament, priority_dict, priority_emoji
from keyboards.users import *
from telebot import types
from datetime import date

local_db = {}

@bot.message_handler(text=['Создать заявку'])
def create_application(msg):
    text = 'Выберите компанию:'
    companies = company.get_companies()
    action = 'company'
    inline = gen_inline_buttons(companies, action)
    bot.send_message(msg.chat.id, text, reply_markup=inline)

@bot.message_handler(text=['Мои заявки'])
def show_applications(msg):
    text = 'Ваши текущие заявки:'
    applications = application.get_applications(msg.chat.id)
    apps = []
    for app in applications:
        apps.append(
            [app[7],app[0]]
        )
    inline = gen_inline_app(apps, 'open')
    bot.send_message(msg.chat.id, text, reply_markup=inline)

@bot.message_handler(text=['Правила пользования'])
def show_rules(msg):
    text = msg.text
    bot.send_message(msg.chat.id, text)

'''
    Create Application сценарий
'''
@bot.callback_query_handler(func=lambda call: call.data.startswith('company'))
def create_application_set_company(call):
    action, comp_id = call.data.split('-')
    text = 'Выберите Отдел:'
    #departaments = departament.get_departaments()
    departaments = departament.get_departaments_by_company(comp_id)
    action = f'departament-{comp_id}'
    inline = gen_inline_buttons(departaments, action)
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(
        text=text, 
        chat_id=call.message.chat.id, 
        message_id=call.message.id, 
        reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('departament'))
def create_application_set_departament(call):
    user_id = call.message.chat.id
    action, comp_id, dep_id = call.data.split('-')
    chat_id = call.message.chat.id
    message_id = call.message.id

    local_db[user_id] = {
        'comp_id' : comp_id,
        'dep_id'  : dep_id
    }
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text('Введите заголовок заявки:', chat_id, message_id)
    bot.register_next_step_handler(call.message, create_application_set_header)

def create_application_set_header(msg):
    header = msg.text
    user_id = msg.chat.id
    local_db[user_id]['header'] = header
    bot.send_message(user_id, 'Введите описание заявки:')
    bot.register_next_step_handler(msg, create_application_set_description)

def create_application_set_description(msg):
    description = msg.text
    user_id = msg.chat.id
    local_db[user_id]['description'] = description

    inline = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='Не важно', callback_data='priority-1')],
        [types.InlineKeyboardButton(text='Важно', callback_data='priority-2')],
        [types.InlineKeyboardButton(text='Срочно', callback_data='priority-3')],
    ])
    bot.send_message(user_id, 'Выберите приоритет важности заявки:', reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('priority'))
def create_application_last_step(call):
    _, priority_position = call.data.split('-')
    priority_position = int(priority_position)
    msg = call.message
    user_id = msg.chat.id
    #print(local_db[user_id]['dep_id'])
    admin_id = admin_departament.get_admin_by_departament(local_db[user_id]['dep_id'])
    today = date.today().strftime("%d.%m.%Y")
    application.add(
        dep_id=local_db[user_id]['dep_id'],
        comp_id=local_db[user_id]['comp_id'],
        user_id=msg.chat.id,
        admin_id=admin_id,
        description=local_db[user_id]['description'],
        header=local_db[user_id]['header'],
        priority=priority_dict[priority_position],
        date_now=today
    )
    application.show()
    bot.answer_callback_query(call.id, text='')
    bot.send_message(msg.chat.id, text='Заявка создана!')

    applications = application.get_applications(msg.chat.id)
    apps = []
    header=local_db[user_id]['header']
    for app in applications:
        if header in app:
            apps.append(
                [priority_emoji[app[8]]+' '+app[7],app[0]]
            )
    inline = gen_inline_app(apps, 'apopen')

    bot.send_message(admin_id, 'Создана новая заявка!', reply_markup=inline)
    

'''
    Работа с заявками
'''
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('open'))
def open_application(call):
    #print(call.data.split('-'))
    action, name, id = call.data.split('-')
    chat_id = call.message.chat.id
    message_id = call.message.id
    user_id = chat_id

    applications = application.get_applications(user_id)
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
            dep_id = departament.get_id_by_name(app[1])
            admin_id = admin_departament.get_admin_by_departament(dep_id)
            app_id = app[0]
    inline = gen_opened_app(admin_id, app_id)

    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
def back_to_applications(call):
    chat_id = call.message.chat.id
    message_id = call.message.id
    text = 'Ваши заявки:'
    applications = application.get_applications(chat_id)
    apps = []
    for app in applications:
        apps.append(
            [app[7],app[0]]
        )
    inline = gen_inline_app(apps, 'open')
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=inline)

local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('awrite'))
def write_to_admin(call):
    _, admin_id, app_id = call.data.split('-')
    local_db[call.message.chat.id] = {
        'admin_id' : int(admin_id),
        'app_id' : app_id
    }
    bot.answer_callback_query(call.id, text='')
    bot.send_message(call.message.chat.id, 'Введите текст для отправки:')
    bot.register_next_step_handler(call.message, write_to_admin_last_step)

def write_to_admin_last_step(msg):
    app_id = local_db[msg.chat.id]['app_id']
    header = application.get_header(app_id)
    text = f'Заявка-{header}\n{msg.text}'
    admin_id = local_db[msg.chat.id]['admin_id']
    inline = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text='Ответить', callback_data=f'uwrite-{msg.chat.id}-{app_id}')
        ]
    ])
    bot.send_message(admin_id, text, reply_markup=inline)
    bot.send_message(msg.chat.id, 'Сообщение отправлено!')