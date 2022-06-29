from loader import bot
from keyboards.admin_company import *
from loader import *
from telebot import types

@bot.message_handler(commands=['admin'])
def start_company_admin(msg):
    user_id = msg.chat.id
    if not admin.is_admin(user_id):
        bot.send_message(user_id, 'Сорри но вы не админ!')
        return
    text = read_rules('company')

    try:
        bot.send_photo(msg.chat.id, photo=open('res\company.jpg', 'rb'))
    except:
        print('Can\'t find the photo :(')

    bot.send_message(msg.chat.id, text=text, reply_markup=admin_markup)

@bot.message_handler(text=['Назад!'])
def back_to_main(msg):
    bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=admin_markup)
'''
    Сценарий работы с отделами
'''
@bot.message_handler(text=['Управление отделами'])
def comp_manage(msg):
    departaments = departament.get_departaments()
    if not departaments:
        bot.send_message(msg.chat.id, 'В вашей компании нет созданных отделов :(', reply_markup=dm_markup)
    else:
        markup = gen_dep_list(departaments, 'dopen')
        bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=dm_markup)
        bot.send_message(msg.chat.id, 'Список отделов:', reply_markup=markup)

@bot.message_handler(text=['Создать отдел'])
def add_departament(msg):
    bot.send_message(msg.chat.id, 'Введите название отдела')
    bot.register_next_step_handler(msg, add_departament_next_step)

def add_departament_next_step(msg):
    departament_name = msg.text
    comp_id = admin.get_company_by_admin(msg.chat.id)
    departament.add(departament_name, comp_id)
    departament.show()
    bot.send_message(msg.chat.id, text='Отдел добавлен!', reply_markup=admin_markup)

@bot.message_handler(text=['Удалить отдел'])
def delete_departament(msg):
    departaments = departament.get_departaments()
    markup = gen_inline_buttons(departaments, 'd_d')
    bot.send_message(msg.chat.id, 'Какой отдел удалить?', reply_markup=markup)

'''
    Сценарий работы с администраторами компаний
'''

@bot.message_handler(text=['Управелние администраторами компании'])
def admin_manage(msg):
    admins = admin_departament.get_admins()
    data = []
    for a in admins:
        if admin_departament.get_dep_name_by_admin(a[0]):
            data.append(
                (user.get_name_by_id(a[0]), a[0])
            )
    inline = gen_inline_buttons(data, 'aopen')
    bot.send_message(msg.chat.id, 'Что делаем?', reply_markup=am_markup)
    bot.send_message(msg.chat.id, text='Список администраторов:', reply_markup=inline)

@bot.message_handler(text=['Убрать администратора'])
def delete_admin(msg):
    admins = admin_departament.get_admins()
    data = []
    for a in admins:
        if admin_departament.get_dep_name_by_admin(a[0]):
            data.append(
                (user.get_name_by_id(a[0]), a[0])
            )
    inline = gen_inline_buttons(data, 'dad')
    bot.send_message(msg.chat.id, 'Кого лишаем прав администратора?', reply_markup=inline)


@bot.message_handler(text=['Добавить администратора'])
def add_admin(msg):
    users = user.get_users()
    data = []
    for u in users:
        if not admin_departament.is_admin(u[1]):
            data.append(u)
    inline = gen_inline_buttons(data, 'gd')
    bot.send_message(msg.chat.id, text='Выберите пользователя:', reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gd'))
def get_user_handler(call):
    action, name, id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    departaments = departament.get_departaments()
    action = f'a_d-{id}'
    inline = gen_inline_buttons(departaments, action)
    
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text('Какой отдел представляет администратор?', chat_id, message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('a_d'))
def get_departament_handler(call):
    print(call.data.split('-'))
    action, user_id, name, dep_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = int(user_id)
    if admin_departament.get_admin_by_departament(dep_id):
        bot.answer_callback_query(call.id, text='У этого отдела уже есть администратор!')
        return
    admin_departament.add(user_id, dep_id)
    admin_name = user.get_name_by_id(user_id)
    text = f'{admin_name}-Является администратором!'
    
    bot.answer_callback_query(call.id, text='')
    bot.send_message(chat_id, text=text, reply_markup=admin_markup)
    admin_departament.show()

@bot.callback_query_handler(func=lambda call: call.data.startswith('d_d'))
def delete_departament_handler(call):
    action, name, id = call.data.split('-')
    departament.delete(id)
    text = f'Департамент "{name}" - удален!'
    message_id = call.message.id
    chat_id = call.message.chat.id
    departaments = departament.get_departaments()
    inline = gen_inline_buttons(departaments, 'dd')
    
    bot.answer_callback_query(call.id, text=text)
    bot.edit_message_text('Какой отдел удалить?', chat_id, message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dad'))
def delete_admin_handler(call):
    action, name, id = call.data.split('-')
    admin_departament.delete(id)
    text = f'Администратор "{name}" - удален!'
    message_id = call.message.id
    chat_id = call.message.chat.id
    admins = admin_departament.get_admins()
    data = []
    for a in admins:
        data.append(
            (user.get_name_by_id(a[0]), a[0])
        )
    inline = gen_inline_buttons(data, 'dad')
    
    bot.answer_callback_query(call.id, text=text)
    bot.edit_message_text('Кого лишаем прав администратора?', chat_id, message_id, reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dopen'))
def open_departament(call):
    action, name, dep_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id

    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text(text=name, chat_id=chat_id, message_id=message_id, reply_markup=gen_actions(dep_id))

@bot.callback_query_handler(func=lambda call: call.data.startswith('dback'))
def go_back(call):
    message_id = call.message.id
    chat_id = call.message.chat.id
    departaments = departament.get_departaments()
    markup = gen_dep_list(departaments, 'dopen')
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text('Список отделов:', chat_id=chat_id,message_id=message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dback'))
def edit_departament(call):
    message_id = call.message.id
    chat_id = call.message.chat.id
    departaments = departament.get_departaments()
    markup = gen_dep_list(departaments, 'dopen')
    bot.answer_callback_query(call.id, text='')
    bot.edit_message_text('Список отделов:', chat_id=chat_id,message_id=message_id, reply_markup=markup)

local_db = {}
@bot.callback_query_handler(func=lambda call: call.data.startswith('dedit'))
def edit_departament(call):
    command, dep_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id
    local_db[chat_id] = { 'dep_id' : dep_id }

    bot.answer_callback_query(call.id, '')
    bot.edit_message_text('Введите новое название отдела', chat_id=chat_id, message_id=message_id)
    bot.register_next_step_handler(call.message, edit_departament_last_step)

def edit_departament_last_step(msg):
    dep_name = msg.text
    rowid = local_db[msg.chat.id]['dep_id']
    departament.edit_departament_name(dep_name, rowid)
    bot.send_message(msg.chat.id, text='Название отдела изменено!', reply_markup=admin_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ddelete'))
def edit_departament(call):
    command, dep_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id

    admin_id = admin_departament.get_admin_by_departament(dep_id)
    admin_departament.delete(admin_id)
    
    bot.answer_callback_query(call.id, '')
    departament.delete(dep_id)
    bot.edit_message_text('Отдел удален!', chat_id=chat_id, message_id=message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('aadd'))
def add_admin(call):
    command, dep_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id

    users = user.get_users()
    data = []
    if admin_departament.get_admin_by_departament(dep_id):
        bot.edit_message_text('У этого отдела уже есть администратор!', chat_id=chat_id, message_id=message_id)
        return

    for u in users:
        if not admin_departament.is_admin(u[1]):
            data.append(u)
    
    inline = gen_inline_buttons(data, f'_aadd-{dep_id}')
    bot.edit_message_text('Выберите пользователя:', chat_id=chat_id, message_id=message_id,reply_markup=inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('_aadd'))
def add_admin_last_step(call):
    command, dep_id, name, user_id = call.data.split('-')
    message_id = call.message.id
    chat_id = call.message.chat.id

    admin_departament.add(user_id, dep_id)
    admin_name = user.get_name_by_id(user_id)
    text = f'{admin_name}-Является администратором!'
    
    bot.answer_callback_query(call.id, text='')
    bot.send_message(chat_id, text, reply_markup=admin_markup)
    admin_departament.show()


@bot.callback_query_handler(func=lambda call: call.data.startswith('aopen'))
def open_admin(call):
    message_id = call.message.id
    chat_id = call.message.chat.id
    command, admin_name, admin_id = call.data.split('-')

    bot.answer_callback_query(call.id, text='')
    
    dep_name = admin_departament.get_dep_name_by_admin(admin_id)
    text = f'{admin_name} - представляет отдел {dep_name}'
    back = types.InlineKeyboardMarkup(keyboard=[[types.InlineKeyboardButton(text='Назад', callback_data='return')]])

    bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=back)
    print(dep_name, admin_name)

@bot.callback_query_handler(func=lambda call: call.data.startswith('return'))
def back_to_admins(call):
    bot.answer_callback_query(call.id, text='')
    admins = admin_departament.get_admins()
    data = []
    for a in admins:
        data.append(
            (user.get_name_by_id(a[0]), a[0])
        )
    inline = gen_inline_buttons(data, 'aopen')
    bot.send_message(call.message.chat.id, text='Список администраторов:', reply_markup=inline)
