from loader import bot
from keyboards.super import *
from loader import admin, user, company

@bot.message_handler(commands=['super'])
def start_super(msg):
    text = 'Введите пароль:'
    bot.send_message(msg.chat.id, text=text)
    bot.register_next_step_handler(msg, login)

def login(msg):
    password = msg.text
    if password == 'super': 
        text = 'Добро пожаловать в панель Супер Администратора!'
        bot.send_message(msg.chat.id, text=text, reply_markup=admin_markup)
    else:
        text = 'Неверный пароль!'
        bot.send_message(msg.chat.id, text=text)

@bot.message_handler(text=['Назад'])
def back_to_main(msg):
    bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=admin_markup)
'''
    Сценарий работы с компаниями
'''
@bot.message_handler(text=['Управление компаниями'])
def comp_manage(msg):
    bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=cm_markup)

@bot.message_handler(text=['Создать компанию'])
def add_company(msg):
    bot.send_message(msg.chat.id, 'Введите название компании')
    bot.register_next_step_handler(msg, add_company_next_step)

def add_company_next_step(msg):
    company_name = msg.text
    company.add(company_name)
    bot.send_message(msg.chat.id, text='Компания добавлена!', reply_markup=admin_markup)

@bot.message_handler(text=['Редактировать тексты приветствия'])
def edit_starting_text(msg):
    bot.send_message(msg.chat.id, 'Что редактируем?', reply_markup=edit_rules_markup)

@bot.message_handler(text=['Удалить компанию'])
def delete_company(msg):
    companies = company.get_companies()
    markup = gen_inline_buttons(companies, 'dc')
    bot.send_message(msg.chat.id, 'Какую компанию удалить?', reply_markup=markup)

'''
    Сценарий работы с администраторами компаний
'''

@bot.message_handler(text=['Управление администраторами'])
def admin_manage(msg):
    bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=am_markup)

@bot.message_handler(text=['Назначить администратора'])
def add_admin(msg):
    users = user.get_users()
    inline = gen_inline_buttons(users, 'gu')
    bot.send_message(msg.chat.id, text='Выберите пользователя', reply_markup=inline)

@bot.message_handler(text=['Удалить администратора'])
def delete_admin(msg):
    admins = admin.get_admins()
    data = []
    for a in admins:
        data.append(
            (user.get_name_by_id(a[0]), a[0])
        )
    inline = gen_inline_buttons(data, 'daa')
    bot.send_message(msg.chat.id, 'Кого лишаем прав администратора?', reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gu'))
def get_user_handler(call):
    action, name, id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    companies = company.get_companies()
    action = f'gc-{id}'
    inline = gen_inline_buttons(companies, action)
    
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text('Какую компанию представляет администратор?', chat_id, message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gc'))
def get_company_handler(call):
    action, user_id, name, id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = int(user_id)
    admin.add(user_id, id)
    admin_name = user.get_name_by_id(user_id)
    text = f'{admin_name}-Является администратором!'
    
    bot.answer_callback_query(call.id, text='')
    bot.send_message(chat_id, text=text, reply_markup=admin_markup)
    admin.show()

@bot.callback_query_handler(func=lambda call: call.data.startswith('dc'))
def delete_company_handler(call):
    action, name, id = call.data.split('-')
    company.delete(id)
    text = f'Компания "{name}" - удалена!'
    message_id = call.message.id
    chat_id = call.message.chat.id
    companies = company.get_companies()
    inline = gen_inline_buttons(companies, 'dc')
    
    bot.answer_callback_query(call.id, text=text)
    bot.edit_message_text('Какую компанию удалить?', chat_id, message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('daa'))
def delete_admin_handler(call):
    action, name, id = call.data.split('-')
    admin.delete(id)
    text = f'Администратор "{name}" - удален!'
    message_id = call.message.id
    chat_id = call.message.chat.id
    admins = admin.get_admins()
    inline = gen_inline_buttons(admins, 'daa')
    
    bot.answer_callback_query(call.id, text=text)
    bot.edit_message_text('Кого лишаем прав администратора?', chat_id, message_id, reply_markup=inline)

local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('rules'))
def edit_rules(call):
    _, profile = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    local_db[call.message.chat.id] = { 'profile' : profile }
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text='Введите текст:\n(Если есть картинка прикрепите ее тем же сообщением)',
                            chat_id=chat_id,
                            message_id=message_id)
    bot.register_next_step_handler(call.message, edit_rules_next_step)

def edit_rules_next_step(msg):
    text = msg.text
    profile = local_db[msg.chat.id]['profile']
    file = bot.get_file(msg.photo[-1].file_id)

    if file:
        downloaded_file = bot.download_file(file.file_path)
        with open(f'res\{profile}.jpg', 'wb') as f:
            f.write(downloaded_file)
        
        text = msg.caption

        with open(f'res\{profile}.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        with open(f'res\{profile}.txt', 'w', encoding='utf-8') as f:
            f.write(text)
    bot.send_message(msg.chat.id, text='Приветствие изменено!')