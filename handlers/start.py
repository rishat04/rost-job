from loader import bot
from loader import user, company, admin
from loader import read_rules
from keyboards.users import user_markup

@bot.message_handler(commands=['start'])
def start_bot(msg):
    username = msg.from_user.username
    user_id = msg.chat.id
    rules = read_rules('users')
    text = f'Привет {username}! Правила пользования:\n\n{rules}'

    if not user.is_user_exists(user_id=user_id):
        user.add(user_id=user_id, username=username)
    
    if user.get_name_by_id(user_id) != username:
        user.update_user_name(username, user_id)


    try:
        bot.send_photo(msg.chat.id, photo=open('res/users.jpg', 'rb'))
    except:
        raise Exception('Can\'t find the photo :(')

    bot.send_message(msg.chat.id, text=text, reply_markup=user_markup['main'])
