import telebot
from telebot import custom_filters
from models import *

token = '5377139728:AAFFDsknJbQbYrdDWK_wfNiWUuE0wNa1d5Q'
bot = telebot.TeleBot(token=token)

bot.add_custom_filter(custom_filters.TextMatchFilter())

def read_rules(path):
    with open(f'res\{path}.txt', encoding='utf-8') as f:
        return f.read()

rules = read_rules('users')

rules_company = read_rules('company')

rules_departament = read_rules('departament')

priority_dict = {
    1: 'Не важно',
    2: 'Важно',
    3: 'Срочно'
}

priority_emoji = {
    'Не важно': '👩‍🦽',
    'Важно': '👨‍🦯',
    'Срочно': '🏃‍♂️'
}

company = Company()
departament = Departament()
user = User()
admin = AdminCompany('AdminCompany', 'comp_id')
admin_departament = AdminDepartament('AdminDepartament', 'dep_id')
application = Application()
