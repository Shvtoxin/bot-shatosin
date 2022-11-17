from email._header_value_parser import ContentType

from telebot import TeleBot
from telebot import types
from telebot.types import LabeledPrice, ShippingQuery, PreCheckoutQuery

from config import BOT_TOKEN

from config import PAYMENTS_TOKEN

import sqlite3

bot = TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    connect=sqlite3.connect('shop.db')
    cursor=connect.cursor()
    people_id=message.chat.id
    cursor.execute(f"SELECT user_id FROM users WHERE user_id={people_id}")
    data=cursor.fetchone()
    print(data)
    if data is None:
        cursor.execute("""INSERT INTO users (user_id, name) VALUES(?, ?);""",
                       [message.chat.id, message.chat.first_name])
        cursor.close()
        connect.commit()
    connect.close()
    markup_start = types.InlineKeyboardMarkup()
    menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    websait = types.InlineKeyboardButton("Официальный сайт", url="https://mnogolososya.ru")
    markup_start.add(menu, websait)
    mess = f'Добро пожаловать <b>{message.from_user.first_name}</b> в ресторан\n            ' \
           f'       <b>🍣Много Лосося🍱</b>' \
           '\n   Я бот для оформления заказа заказа! ' \
           '\nТыкай на кнопку ниже для простомотра меню!'

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup_start)


@bot.callback_query_handler(func=lambda call: True)
def najatie(call):

    if call.data == 'menu':
        markup_reply = types.InlineKeyboardMarkup()
        rolls = types.InlineKeyboardButton(text= 'Роллы🍱' ,callback_data = 'rolls' )
        poke = types.InlineKeyboardButton(text= 'Поке🥗' ,callback_data = 'poke' )
        pizza = types.InlineKeyboardButton(text= 'Пицца🍕',callback_data = 'pizza' )
        syps = types.InlineKeyboardButton(text= 'Супы🍜' ,callback_data = 'syps' )
        syshi = types.InlineKeyboardButton(text= 'Суши🍣' ,callback_data = 'syshi' )
        markup_reply.add(rolls,poke, pizza, syps, syshi)
        bot.send_message(call.message.chat.id, 'Представляю Вам категории ⬇️', parse_mode='html',
                         reply_markup=markup_reply)


    if call.data == 'rolls':
        markup_reply = types.InlineKeyboardMarkup()
        fila = types.InlineKeyboardButton(text='Ролл Филадельфия с лососем', callback_data='fila')
        kali = types.InlineKeyboardButton(text='Ролл Калифорния с лососем', callback_data='kali')
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='menu')
        markup_reply.add(fila, kali,nazad)
        bot.send_message(chat_id=call.message.chat.id, text='Какие желаете Роллы?', parse_mode='html',reply_markup=markup_reply)


    if call.data == 'fila':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_fila')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='rolls')
        markup_reply.add(dob, kbjy, nazad)
        photo = open('image menu/fila.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                         '<b>Ролл Филадельфия с лососем</b>\n'
                         '<u>Описание:</u> '
                         '\t Великие роллы. Круговорот нежности лосося, сливочного сыра '
                         'и авокадо. И, как ни крути, вечная классика — никогда не надоест! '
                         '\n<u>Состав:</u>\t' ' рис, лосось, сыр, авокадо, нори, имбирь, васаби. '
                         'Соевый соус 1 шт/40гр, имбирь маринованный 10 гр, васаби 5 гр.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_fila':

        product_id = 1
        user_id=call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад',callback_data='rolls')
        markup_reply.add(pay,nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Ролл Филадельфию с лососем в корзину!',parse_mode='html', reply_markup=markup_reply)



    if call.data == 'kali':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать',callback_data='dob_kali')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='rolls')
        markup_reply.add(dob,kbjy,nazad)
        photo = open('image menu/kali.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                         '<b>Ролл Калифорния с лососем</b>\n'
                         '<u>Описание:</u> '
                         '\t Лосось как праздник. Свежее филе, рис, икра и японский '
                         'майонез — все в круг!'
                         '\n<u>Состав:</u>\t' ' Лосось, рис, огурец, икра тобико, майонез, '
                         'нори, имбирь, васаби. Соевый соус 1 шт/40гр, имбирь маринованный 10 гр, '
                         'васаби 5 гр.', parse_mode='html', reply_markup= markup_reply)

    if call.data == 'dob_kali':

        product_id = 2
        user_id=call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад',callback_data='rolls')
        markup_reply.add(pay,nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Ролл Калифорнию с лососем в корзину!',parse_mode='html', reply_markup=markup_reply)



    if  call.data == 'poke':
        markup_reply = types.InlineKeyboardMarkup()
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='menu')
        poke_los = types.InlineKeyboardButton(text='Поке с лососем', callback_data='poke_los')
        poke_tun = types.InlineKeyboardButton(text='Поке с тунцом', callback_data='poke_tun')
        markup_reply.add(poke_los, poke_tun,nazad)
        bot.send_message(call.message.chat.id, 'Какие желаете Поке?', parse_mode='html', reply_markup=markup_reply)


    if call.data == 'poke_los':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_poke_los')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='poke')
        markup_reply.add(dob, kbjy, nazad)
        photo = open('image menu/poke_los.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                         '<b>Поке с лососем</b>\n'
                         '<u>Описание:</u> '
                         '\t Сочный обед с лососем.Сборная из кусочков рыбы,спелого авокадо,'
                         'свежих овощей и основы на выбор:рис,киноа,салат.Лосось можно выбрать:от классического '
                         'до самого жгучего.'
                         '\n<u>Состав:</u>\t' 'Лосось, рис, огурец, икра тобико, майонез, '
                         'нори, имбирь, васаби. Соевый соус 1 шт/40гр, имбирь маринованный 10 гр, '
                         'васаби 5 гр.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_poke_los':

        product_id = 3
        user_id=call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад',callback_data='poke')
        markup_reply.add(pay,nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Поке с лососем в корзину!',parse_mode='html', reply_markup=markup_reply)



    if call.data == 'poke_tun':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_poke_tun')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='poke')
        markup_reply.add(dob, kbjy, nazad)
        photo = open('image menu/poke_tun.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                         '<b>Поке с тунцом</b>\n'
                         '<u>Описание:</u> '
                         '\tМного тунца.Кубики рыбы,апельсин,бобы эдамаме,икра тобико и другие свежие'
                         ' овощи с одним из трех вариантов основы:рис,киноа,салат.Тунец на выбор:обычный или поострее.'
                         '\n<u>Состав:</u>\t' 'тунец,огурец,апельсин,чука,тобико,редис,бобы Эдамаме,соус '
                         'поке,лук зеленый,кунжут белый.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_poke_tun':
        product_id = 4
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='poke')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Поке с тунцом в корзину!', parse_mode='html',
                         reply_markup=markup_reply)



    if call.data == 'pizza':
        markup_reply = types.InlineKeyboardMarkup()
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='menu')
        mexico = types.InlineKeyboardButton(text='Пицца Мексиканская', callback_data='mexico')
        margo = types.InlineKeyboardButton(text='Пицца Маргарита', callback_data='margo')
        markup_reply.add(mexico, margo,nazad)
        bot.send_message(call.message.chat.id, 'Какие желаете Пиццы?', parse_mode='html', reply_markup=markup_reply)


    if call.data == 'margo':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_mexico')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='pizza')
        markup_reply.add(dob, kbjy, nazad)
        photo = open('image menu/margo.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                         '<b>Пицца Маргарита</b>\n'
                         '<u>Описание:</u> '
                         '\t Мясные остроты. Встретились как-то раз ветчина, пепперони '
                         'и халапеньо. Получилась наша самая жгучая из пицц.'
                         '\n<u>Состав:</u>\t' ' тесто, мука пшеничная из мягких сортов пшеницы,'
                         ' мука из твёрдых сортов пшеницы для пасты, соус томатный, сыр моцарелла,'
                         ' ветчина, колбаса пепперони, перец халапеньо, перец болгарский, масло оливковое, '
                         ' соус фирменный  (майонез, сыр сливочный, петрушка, вода, соль, чеснок сушёный).',
                       parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_margo':
        product_id = 6
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='pizza')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Пиццу Маргариту в корзину!',
                             parse_mode='html', reply_markup=markup_reply)

    if call.data == 'mexico':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_mexico')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='pizza')
        markup_reply.add(dob, kbjy, nazad)
        photo = open('image menu/mexico.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo,
                       '<b>Пицца Мексиканская</b>\n'
                       '<u>Описание:</u> '
                       '\t Мясные остроты. Встретились как-то раз ветчина, пепперони '
                       'и халапеньо. Получилась наша самая жгучая из пицц.'
                       '\n<u>Состав:</u>\t' ' тесто, мука пшеничная из мягких сортов пшеницы,'
                       ' мука из твёрдых сортов пшеницы для пасты, соус томатный, сыр моцарелла,'
                       ' ветчина, колбаса пепперони, перец халапеньо, перец болгарский, масло оливковое, '
                       ' соус фирменный  (майонез, сыр сливочный, петрушка, вода, соль, чеснок сушёный).',
                       parse_mode='html', reply_markup=markup_reply)

    if call.data == 'dob_mexico':
        product_id = 5
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='pizza')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Пиццу Мексиканскую в корзину!',
                         parse_mode='html', reply_markup=markup_reply)





    if call.data == 'syps':
        markup_reply = types.InlineKeyboardMarkup()
        tom_los = types.InlineKeyboardButton(text='Том Ям с лососем', callback_data='tom_los')
        tom_krv = types.InlineKeyboardButton(text='Том Ям с креветками', callback_data='tom_krv')
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='menu')
        markup_reply.add(tom_los, tom_krv,nazad)
        bot.send_message(call.message.chat.id, 'Какие желаете Супы?', parse_mode='html', reply_markup=markup_reply)


    if call.data == 'tom_los':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_tom_los')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syps')
        markup_reply.add(dob, kbjy, nazad)
        bot.send_photo(call.message.chat.id, open('image menu/tom_los.jpg', 'rb'),
                         '<b>Том ям с лососем</b>\n'
                         '<u>Описание:</u> '
                         '\t   Лосось с кислинкой. Традиционный суп с кокосовым молоком,'
                         ' шампиньонами и черри. Только вместо креветок — много лосося.'
                         '\n<u>Состав:</u>\t '
                         '   Лосось, соль, куриный бульон, сахар-песок, масло подсолнечное, лайм, вода,'
                         ' кокосовое молоко, рис, лист лайма, лимонная трава, том ям паста, чили перец, кинза,'
                         ' шампиньоны и помидоры черри.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_tom_los':
        product_id = 7
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syps')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Том ям с лососем в корзину!',
                parse_mode='html', reply_markup=markup_reply)


    if call.data == 'tom_krv':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_tom_krv')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='syps')
        markup_reply.add(dob, kbjy, nazad)
        bot.send_photo(call.message.chat.id, open('image menu/tom_krv.jpg', 'rb'),
                         '<b>Том ям с креветками</b>\n'
                         '<u>Описание:</u> '
                         '\t Зарубежная классика. В бульоне с кислинкой и кокосовым '
                         'молоком креветки, шампиньоны и помидоры черри. А к нему, по традиции,'
                         ' чашка рассыпчатого риса.'
                         '\n<u>Состав:</u>\t' 'Креветки, соль, куриный бульон, сахар-песок, масло подсолнечное,'
                         ' лайм, вода, кокосовое молоко, рис, помидоры черри, лист лайма, лимонная трава, '
                         'том ям паста,чили перец, кинза, шампиньоны.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_tom_krv':
        product_id = 8
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syps')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Том ям с креветками в корзину!',
                parse_mode='html', reply_markup=markup_reply)



    if call.data == 'syshi':
        markup_reply = types.InlineKeyboardMarkup()
        syshi_los = types.InlineKeyboardButton(text='Суши с лососем', callback_data='syshi_los')
        sysmi_los = types.InlineKeyboardButton(text='Сашими с лососем', callback_data='sysmi_los')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='menu')
        markup_reply.add(syshi_los, sysmi_los,nazad)
        bot.send_message(call.message.chat.id, 'Какие желаете Суши?', parse_mode='html', reply_markup=markup_reply)


    if call.data == 'syshi_los':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_syshi_los')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syshi')
        markup_reply.add(dob, kbjy, nazad)
        bot.send_photo(call.message.chat.id, open('image menu\sushi_los.jpg', 'rb'),
                                            '<b>Суши из лососем</b>\n'
                                            '<u>Описание:</u> '
                                            '\tКлассические нигири. '
                                            'Свежий лосось на горке идеально сваренного риса.'
                                            ' Просто вкусно.'
                                            '\n<u>Состав:</u>\t' ' лосось, рис, имбирь,'
                                            ' васаби. Соевый соус 1 шт/40гр, имбирь '
                                            'маринованный 10 гр, васаби 5 гр.', parse_mode='html',reply_markup=markup_reply)
    if call.data == 'dob_syshi_los':
        product_id = 9
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syshi')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Суши из лосося с лососем в корзину!',
                         parse_mode='html', reply_markup=markup_reply)




    if call.data == 'sysmi_los':
        markup_reply = types.InlineKeyboardMarkup()
        dob = types.InlineKeyboardButton(text='Выбрать', callback_data='dob_sysmi_los')
        kbjy = types.InlineKeyboardButton(text='КБЖУ', url='https://mlmenu.ru')
        nazad = types.InlineKeyboardButton(text='Меню', callback_data='syshi')
        markup_reply.add(dob, kbjy, nazad)
        bot.send_photo(call.message.chat.id, open('image menu\sysmi_los.jpg', 'rb'),
                       '<b>Сашими из лососем</b>\n'
                       '<u>Описание:</u> '
                       '\t Лосось как он есть. Сочное и мягкое филе.'
                       '\n<u>Состав:</u>\t' ' лосось, имбирь, васаби.'
                       ' Соевый соус 1 шт/40гр, имбирь маринованный 10 гр,'
                       ' васаби 5 гр.', parse_mode='html',reply_markup=markup_reply)

    if call.data == 'dob_sysmi_los':
        product_id = 10
        user_id = call.message.chat.id

        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        cursor.execute("""INSERT INTO cart (user_id, product_id) VALUES (?, ?);""", [user_id, product_id])
        cursor.close()
        connect.commit()
        connect.close()

        markup_reply = types.InlineKeyboardMarkup()
        pay = types.InlineKeyboardButton(text='Корзина', callback_data='pay')
        nazad = types.InlineKeyboardButton(text='Назад', callback_data='syshi')
        markup_reply.add(pay, nazad)
        bot.send_message(call.message.chat.id, 'Вы добавили Сашими из лосося в корзину!',
                         parse_mode='html', reply_markup=markup_reply)

    if call.data == 'pay':
        connect = sqlite3.connect('shop.db')
        cursor = connect.cursor()
        data = cursor.execute("""SELECT * FROM cart WHERE user_id=(?);""", [call.message.chat.id]).fetchall()
        cursor.close()
        connect.commit()
        cursor = connect.cursor()
        new_data = []
        for i in range(len(data)):
            new_data.append(cursor.execute("""SELECT * FROM products WHERE id=(?);""", [data[i][1]]).fetchall())
        cursor.close()
        connect.commit()
        connect.close()
        new_data = [new_data[i][0] for i in range(len(new_data))]
        prices = [LabeledPrice(label=i[1], amount=i[2]) for i in new_data]
        bot.send_invoice(call.message.chat.id,
                         title='Заказ в Много Лосося',
                         description='Ваш заказ будет доставлен за 60 минут!',
                         provider_token=PAYMENTS_TOKEN,
                         currency='rub',
                         need_email=True,
                         prices=prices,
                         start_parameter='example',
                         need_phone_number=True,
                         need_shipping_address=True,
                         invoice_payload='some_invoice')

@bot.message_handler(commands=['clear_cart'])
def clear_table(message):
    connect = sqlite3.connect('shop.db')
    cursor=connect.cursor()
    cursor.execute("""DELETE FROM cart WHERE user_id=(?);""",[message.chat.id])
    cursor.close()
    connect.commit()
    connect.close()
    bot.send_message(message.chat.id,'Корзина успешно очишена!')
bot.polling(none_stop=True, interval=0)
