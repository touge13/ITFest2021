# -*- coding:utf-8-*-

#Грудинин Михаил Артемович, 15 лет

#Добрый день уважаемое жюри, в первую очередь, я хотел бы выразить вам благодарность за то, что организовали такой конкурс, в нём я впервые столкнулся не только с написанием ботов, но и с телеграммом в прицнипе, про базы данных я вообще молчу. 
#Вы позволили получить бесценный опыт и подтолкнули меня на такие открытия.

ok = 0     #количество верных ответов
bad = 0    #количество неверных ответов


import time
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import urllib.parse as up
import psycopg2





# инициализируем бота
bot = Bot(token="your_bot_token")
dp = Dispatcher(bot)


#Такие отступы (#=====...) я делал для себя, чтобы примерно разделять темы сообщений и не запутаться
#=====================================================================================================================================
button1 = KeyboardButton('Хм, ну привет, где я?')
button2 = KeyboardButton('Что происходит? Где я?')
button3 = KeyboardButton('Хай!')
button4 = KeyboardButton('Стоп')

greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb1.add(button1)
greet_kb1.add(button2)
greet_kb1.add(button3)
greet_kb1.add(button4)

buttonstart = KeyboardButton('/start')
greet_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_start.add(buttonstart)


@dp.message_handler(commands=['help'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, 'https://psv4.userapi.com/c613501//u312306207/audiomsg/d1/04f05d80f2.ogg', reply_to_message_id=message.message_id)
    await bot.send_photo(message.from_user.id, 'https://sun9-4.userapi.com/impg/EWpIEpUdTY7wcD8I_XSCMoJLJqxgZKKJvHIGqA/jXtSpkSnv5w.jpg?size=267x200&quality=96&sign=ee465de9337e6b8375d4c35134f1fdb2&type=album', reply_markup=greet_start)


up.uses_netloc.append("postgres")
conn = psycopg2.connect("dbname='zrmfsvop' user='zrmfsvop' host='dumbo.db.elephantsql.com' password='your_password'")
cur = conn.cursor()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global start_time
    global ok
    global bad
    global cur

    ok=0
    bad=0

    
    cur.execute(f'SELECT user_id FROM Users WHERE user_id = {message.from_user.id}')
    result = cur.fetchone()

    if result is None:

        #дата регистрации
        today = datetime.datetime.today()
        data_reg = today.strftime("%Y.%m.%d %H:%M:%S")

        cur.execute(f"INSERT INTO Users (user_id, user_name, user_record, user_time, user_data_reg) VALUES( {message.from_user.id}, '@{message.from_user.first_name}', 0, '00:00:00', '{data_reg}')")
        conn.commit()

        start_time = time.time()
        await message.reply("Йоу, дружище, привет👋! Меня зовут Миша.")
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8Jgj8BmFYSo0pH3x1Qyv4_xlew39wACBQADO2AkFDwYiAABJUt2MR8E', reply_markup=greet_kb1)
    
    else:
        await bot.send_message(message.chat.id,'Вы уже играли в эту игру, ваши данные уже зарегестрированы, если хотите сбросить свой прогресс, напишите /delete, затем пропишите /start и скорее побейте свой рекорд! (если он, конечно же, уже не максимальный :) )', reply_markup=greet_stop)
    #конец работы с бд /start
    
    


#удаление пользователя из бд
@dp.message_handler(commands=['delete'])
async def process_delete_command(message: types.Message):
    global cur

    cur.execute(f"SELECT user_id FROM Users WHERE user_id = {message.from_user.id}")
    result = cur.fetchone()

    if result is None:
        await bot.send_message(message.chat.id,'Ваших результатов и так не существует! Скорее напишите /start, чтобы исправить ситуацию!')
    else:
        cur.execute(f"DELETE FROM Users WHERE user_id = {message.from_user.id}")
        conn.commit()
        await bot.send_message(message.chat.id, 'Вы удалены из базы данных, можете прописать /start, чтобы побить свой старый рекорд!', reply_markup=greet_start)



kb1 = ['Хм, ну привет, где я?', 'Что происходит? Где я?', 'Хай!', 'Стоп']

@dp.message_handler(lambda message: message.text in kb1)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == "Хм, ну привет, где я?" or message.text == "Что происходит? Где я?":
        await bot.send_message(message.chat.id,'О, не пугайся, ты попал в мою игру! Своеобразный симулятор жизни, либо просто мотивирующая игрушка, где ты должен принимать правильные решения. Твоя задача - добиться успеха в этой виртуальной жизни. По мере прохождения ты должен принимать правильные решения, которые будут влиять на исход твоего сюжета! Быть может, пройдя игру, ты будешь замотивирован развиваться и познавать что-то новое.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Я буду сопровождать тебя всю игру, думаю ты не против.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Твоя задача - ответить правильно на как можно больше вопросов, от этого будет зависить твой рейтинг (процент правильного ответа). Твои результаты сохраняются, но ты сможешь их сохранить только тогда, когда пройдёшь игру полностью, то есть ты не можешь ответить на один вопрос правильно, выйти и получить максимальный рейтинг. Также будет промежуточное сохранение твоего времени игры.')  
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Если ты захочешь выйти из игры, то просто напиши в поле для ввода слово "Стоп", но помни, что ты потеряешь свой рекорд и тебе придётся играть заново!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Ах, да, если ты выберешь неправильный ответ, то просто напиши в поле для ввода другой, верный номер варианта ответа на вопрос, где ты ответил неправильно.', reply_markup=greet_kb2)
        
        ok+=1



    elif message.text == "Хай!":
        await bot.send_message(message.chat.id, 'Ты попал в мою игру! Своеобразный симулятор жизни, либо просто мотивирующая игрушка, где ты должен принимать правильные решения. Твоя задача - добиться успеха в этой виртуальной жизни. По мере прохождения ты должен принимать правильные решения, которые будут влиять на исход твоего сюжета! Быть может, пройдя игру, ты будешь замотивирован развиваться и познавать что-то новое.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Я буду сопровождать тебя всю игру, думаю ты не против.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Твоя задача - ответить правильно на как можно больше вопросов, от этого будет зависить твой рейтинг (процент правильного ответа). Твои результаты сохраняются, но ты сможешь их сохранить только тогда, когда пройдёшь игру полностью, то есть ты не можешь ответить на один вопрос правильно, выйти и получить максимальный рейтинг. Также будет промежуточное сохранение твоего времени игры.')  
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Если ты захочешь выйти из игры, то просто напиши в поле для ввода слово "Стоп", но помни, что ты потеряешь свой рекорд и тебе придётся играть заново!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id,'Ах, да, если ты выберешь неправильный ответ, то просто напиши в поле для ввода другой, верный номер варианта ответа на вопрос, где ты ответил неправильно.', reply_markup=greet_kb2)

        ok+=1



    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb1)
    

buttonstop = KeyboardButton('/delete')

greet_stop = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_stop.add(buttonstop)


#=====================================================================================================================================

button21 = KeyboardButton('Но... что произойдёт, если у меня будет плохая концовка?')
button22 = KeyboardButton('Окей, допустим. Поехали!')
button23 = KeyboardButton('Стоп')

greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb2.add(button21)
greet_kb2.add(button22)
greet_kb2.add(button23)

button41 = KeyboardButton('Школа - мой фундамент. Затем я поступлю в институт и по итогу получу образование.')
button42 = KeyboardButton('Зачем мне нужна эта школа? я и без неё всё прекрасно знаю')
button43 = KeyboardButton('Стоп')

greet_kb4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb4.add(button41)
greet_kb4.add(button42)
greet_kb4.add(button43)

button51 = KeyboardButton('90°')
button52 = KeyboardButton('180°')
button53 = KeyboardButton('60°')
button54 = KeyboardButton('Стоп')

greet_kb5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb5.add(button51)
greet_kb5.add(button52)
greet_kb5.add(button53)
greet_kb5.add(button54)

kb2 = ['Но... что произойдёт, если у меня будет плохая концовка?', 'Окей, допустим. Поехали!', 'Стоп']

@dp.message_handler(lambda message: message.text in kb2)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == "Но... что произойдёт, если у меня будет плохая концовка?":
        await bot.send_message(message.chat.id,'Не переживай, это всего лишь игра. В любом случае ты сможешь её перепройти и рано или поздно добиться лучшей концовки. Итак, сейчас я отправлю тебя в саму игру, удачи!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '3...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '2...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '1...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Ох, ну что же, понеслась! Неплохо было бы осмотреться.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Ты осмотрелся и нашёл информацию о своём персонаже:\n1. Тебе 15 лет\n2. ты учишься в 9 классе\n3. Тебе нравится программирование на Python\n4. Ты мечтаешь стать востребованным программистом')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Кажется нужно сделать свой первый серьёзный выбор. Как собираешься провести свои учебные деньки?📘✏️')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8Vgj8EcqpwNwLcm-Yll2C6PLuKMcgACdAEAAs-71A77o37THQ55OB8E', reply_markup=greet_kb4)
        
        ok+=1



    elif message.text == "Окей, допустим. Поехали!":
        await bot.send_message(message.chat.id, 'Мне нравится твой настрой!  Итак, сейчас я отправлю тебя в саму игру, удачи!') 
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '3...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '2...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '1...')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Ох, ну что же, понеслась! Неплохо было бы осмотреться.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Ты осмотрелся и нашёл информацию о своём персонаже:\n1. Тебе 15 лет\n2. ты учишься в 9 классе\n3. Тебе нравится программирование на Python\n4. Ты мечтаешь стать востребованным программистом')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Кажется нужно сделать свой первый серьёзный выбор. Как собираешься провести свои учебные деньки?📘✏️')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8Vgj8EcqpwNwLcm-Yll2C6PLuKMcgACdAEAAs-71A77o37THQ55OB8E', reply_markup=greet_kb4)
        
        ok+=1



    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb2)

#=====================================================================================================================================
kb4 = ['Школа - мой фундамент. Затем я поступлю в институт и по итогу получу образование.', 'Зачем мне нужна эта школа? я и без неё всё прекрасно знаю', 'Стоп']

@dp.message_handler(lambda message: message.text in kb4)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Школа - мой фундамент. Затем я поступлю в институт и по итогу получу образование.':
        await bot.send_message(message.chat.id, "Да, молодец, это правильный выбор!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Итак, финишная прямая твоей школьной и студенческой жизни! Осталось лишь сдать экзамены.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "вопрос №1\nКакая величина каждого из углов равностороннего треугольника?")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgEAAxkBAAEBP8tgj8I1m_o_7KrFl-UHMryJMaZ4gQACHgEAAjgOghFGWGjXaYZe_R8E', reply_markup=greet_kb5)
        
        ok+=1
    
    
    elif message.text == "Зачем мне нужна эта школа? я и без неё всё прекрасно знаю":
        await bot.send_message(message.chat.id, "Ты забил на школу, и что? что дальше? ты вырос безответственным и неграмотным человеком, тебя никто не взял на работу и все пошло под откос. Поздравляю, первая плохая концовка открыта, хотя поздравлять тут не с чем.😔 Отматываю время назад! Ответь на вопрос ещё раз.", reply_markup = greet_kb4)
        
        bad+=1

    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb4)   
#=====================================================================================================================================


kb5 = ['90°', '180°', '60°', 'Стоп']

@dp.message_handler(lambda message: message.text in kb5)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == '90°':
        await bot.send_message(message.chat.id, "ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb5)
        
        bad+=1
    
    
    elif message.text == '180°':
        await bot.send_message(message.chat.id, "ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb5)
        
        bad+=1
    

    elif message.text == '60°':
        await bot.send_message(message.chat.id, "Неплохо")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "вопрос №2\nПосчитайте в уме: 5+2-1+7")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP85gj8I_gm-im2RrRbCVda5eoX_pIAAC9wcAAhhC7ghILnc5wsdKCR8E', reply_markup=greet_kb6)

        ok+=1
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb5)   

#=====================================================================================================================================

button61 = KeyboardButton('9')
button62 = KeyboardButton('15')
button63 = KeyboardButton('13')
button64 = KeyboardButton('Стоп')

greet_kb6 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb6.add(button61)
greet_kb6.add(button62)
greet_kb6.add(button63)
greet_kb6.add(button64)

kb6 = ['9', '15', '13', 'Стоп']

@dp.message_handler(lambda message: message.text in kb6)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == '9':
        await bot.send_message(message.chat.id, "Ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb6)
        
        bad+=1
    
    
    
    elif message.text == '15':
        await bot.send_message(message.chat.id, "Ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb6)
        
        bad+=1
    
    
    
    elif message.text == '13':
        await bot.send_message(message.chat.id, "Хорошо")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "вопрос №3\nУвеличь самое маленькое двузначное число на 4")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9Fgj8JbbHS0fuARnRBuctJ1iyCKhAACJgkAAhhC7gijq_JGMfijjh8E', reply_markup=greet_kb7)
        
        ok+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb6) 

#=====================================================================================================================================

button71 = KeyboardButton('14')
button72 = KeyboardButton('23')
button73 = KeyboardButton('11')
button74 = KeyboardButton('Стоп')

greet_kb7 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb7.add(button71)
greet_kb7.add(button72)
greet_kb7.add(button73)
greet_kb7.add(button74)

kb7 = ['14', '23', '11', 'Стоп']

@dp.message_handler(lambda message: message.text in kb7)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == '14':
        await bot.send_message(message.chat.id, "Поздравляем! Вы ответили на все вопросы!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Окей ты получил образование и понял, что чуть не совершил огромную ошибку. Ты понял, что школа нужна не для того, чтобы знать о синусах и косинусах, а для того, чтобы вырасти ответственным и грамотным человеком, способным решать и преодолевать какие-либо трудности.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Сейчас тебе нужно устроиться на работу, но на какую?")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP-lgj8ZwS3EmN2zVFKv2vTRTaSWzhwAC3AAD9wLID1DYvAZ7vfB8HwQ', reply_markup=greet_kb8)
        
        ok+=1
    
    
    
    elif message.text == '23':
        await bot.send_message(message.chat.id, "Ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb7)

        bad+=1
    
    
    
    elif message.text == '11':
        await bot.send_message(message.chat.id, "Ты ошибся, попробуй ещё раз")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP91gj8TGRKxmTPbfGi_ubD3XhlY5bAACfAADUomRI2amgxWSeyF6HwQ', reply_markup=greet_kb7)

        bad+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb7) 

#======================================================================================================================================================

button81 = KeyboardButton('Хочу устроиться программистом, ведь мне нравится этим заниматься.👨‍💻')
button82 = KeyboardButton('Устроюсь на работу, которую терпеть не могу.')
button83 = KeyboardButton('Устроюсь супергероем!')
button84 = KeyboardButton('Стоп')

greet_kb8 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb8.add(button81)
greet_kb8.add(button82)
greet_kb8.add(button83)
greet_kb8.add(button84)

kb8 = ['Хочу устроиться программистом, ведь мне нравится этим заниматься.👨‍💻', 'Устроюсь на работу, которую терпеть не могу.', 'Устроюсь супергероем!', 'Стоп'] 


buttons1 = KeyboardButton('А что если я стану супергероем - программистом?👨‍💻')
buttons2 = KeyboardButton('ладно, это была шутка')
buttons3 = KeyboardButton('Стоп')

greet_skb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_skb1.add(buttons1)
greet_skb1.add(buttons2)
greet_skb1.add(buttons3)

@dp.message_handler(lambda message: message.text in kb8)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Хочу устроиться программистом, ведь мне нравится этим заниматься.👨‍💻':
        await bot.send_message(message.chat.id, "Итак, ты устроился программистом, ты любишь свою работу и добиваешься успехов в своём деле!\nНу что, кажется твои дела идут неплохо, но стоит ли на этом останавливаться?")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_Jgj8eAk2g6AYV9PnKV4ahKm7eexQACRgADUomRI_j-5eQK1QodHwQ', reply_markup=greet_kb9)

        ok+=1
    
    
    
    elif message.text == 'Устроюсь на работу, которую терпеть не могу.':
        await bot.send_message(message.chat.id, "Ты устроился на нелюбимую работу, да, ты способен содержать свою семью, но каждый день ты шёл туда, куда не хочешь идти, и занимался тем, чем не хочешь заниматься, не думаю, что это предел мечтаний. Вторая плохая концовка открыта.🙁 Отматываю время назад! Ответь на вопрос ещё раз.", reply_markup=greet_kb8)

        bad+=1
    
    
    
    elif message.text == 'Устроюсь супергероем!':
        await bot.send_message(message.chat.id, "Хм. Ну, супергероем, так супергероем. Кого спасать собираешься?😄")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBQAFgj8mZSc31QwHluGENB_Qj7XH1bAACegADlp-MDgcT6Kxf6ytCHwQ', reply_markup=greet_skb1)        

        ok+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb8) 

#=====================================================================================================================================

skb1 = ['А что если я стану супергероем - программистом?👨‍💻', 'ладно, это была шутка', 'Стоп']

@dp.message_handler(lambda message: message.text in skb1)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'А что если я стану супергероем - программистом?👨‍💻':
        await bot.send_message(message.chat.id, 'Ладно, звучит заманчиво! Приступим к делу, с чего начнёшь?', reply_markup=greet_s2)

        ok+=1
    
    
    
    elif message.text == 'ладно, это была шутка':
        await bot.send_message(message.chat.id, "Другое дело. Я думаю ты устроишься программистом. Хотя почему 'Думаю?'. Ты устроишься программистом. А то кто его знает, на какую ещё профессию тебя потянет.😑")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Итак, ты устроился программистом, ты любишь свою работу и добиваешься успехов в своём деле!\nНу что, кажется твои дела идут неплохо, но стоит ли на этом останавливаться?")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_Jgj8eAk2g6AYV9PnKV4ahKm7eexQACRgADUomRI_j-5eQK1QodHwQ', reply_markup=greet_kb9)

        ok+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_skb1) 

buttons21 = KeyboardButton('Напишу-ка я программу, при помощи которой я смогу вычислять преступников!')
buttons22 = KeyboardButton('Напишу программу, где люди без страха и риска смогут обмениваться серкретными данными!')
buttons23 = KeyboardButton('А напишу-ка я программу, при помощи которой смогу воровать деньги!🤑 (в шутку)')
buttons24 = KeyboardButton('Стоп')

greet_s2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_s2.add(buttons21)
greet_s2.add(buttons22)
greet_s2.add(buttons23)
greet_s2.add(buttons24)

sk2 = ['Напишу-ка я программу, при помощи которой я смогу вычислять преступников!', 'Напишу программу, где люди без страха и риска смогут обмениваться серкретными данными!', 'А напишу-ка я программу, при помощи которой смогу воровать деньги!🤑 (в шутку)', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in sk2)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Напишу-ка я программу, при помощи которой я смогу вычислять преступников!':
        await bot.send_message(message.chat.id, 'Звучит неплохо')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Итак, став суперпрограммистом ты добился колосального успеха! Ты открыл свою огромную компанию, ты зарабатываешь миллиарды и у тебя всё прекрасно. Значит ли это то, что развиваться и стремиться к большему больше не нужно? Конечно нет! Всю жизнь мы должны ставить себе цели, пусть даже не постигаемые, и пытаться изо всех сил преодолеть их, вне зависимости супергерой ты или нет!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Слушай, я тут подумал, а давай в казино сходим?💰')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9Rgj8M6zQWkLIjaVGboSQABApPe1sAAAugAAyI3jgQHOZSZ2kODqR8E', reply_markup = greet_kb12)
        
        ok+=1
    
    
    elif message.text == 'Напишу программу, где люди без страха и риска смогут обмениваться серкретными данными!':
        await bot.send_message(message.chat.id, 'Звучит неплохо')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Итак, став суперпрограммистом ты добился колосального успеха! Ты открыл свою огромную компанию, ты зарабатываешь миллиарды и у тебя всё прекрасно. Значит ли это то, что развиваться и стремиться к большему больше не нужно? Конечно нет! Всю жизнь мы должны ставить себе цели, пусть даже не постигаемые, и пытаться изо всех сил преодолеть их, вне зависимости супергерой ты или нет!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Слушай, я тут подумал, а давай в казино сходим?💰')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9Rgj8M6zQWkLIjaVGboSQABApPe1sAAAugAAyI3jgQHOZSZ2kODqR8E', reply_markup = greet_kb12)
        
        ok+=1
    
    
    elif message.text == 'А напишу-ка я программу, при помощи которой смогу воровать деньги!🤑 (в шутку)':
        await bot.send_message(message.chat.id, "Чтоооооо?", reply_markup=greet_s3)
        
        ok+=1
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_s2) 

buttons311 = KeyboardButton('Да я шучу! Напишу программу, которая поможет работать аппаратам в медицине безошибочно!')
buttons322 = KeyboardButton('Стоп')

greet_s3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_s3.add(buttons311)
greet_s3.add(buttons322)

#=====================================================================================================================================

s3 = ['Да я шучу! Напишу программу, которая поможет работать аппаратам в медицине безошибочно!', 'Стоп']

@dp.message_handler(lambda message: message.text in s3)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Да я шучу! Напишу программу, которая поможет работать аппаратам в медицине безошибочно!':
        await bot.send_message(message.chat.id, 'Фух, а то я уж испугался, неплохая идея, кстати!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Итак, став суперпрограммистом ты добился колосального успеха! Ты открыл свою огромную компанию, ты зарабатываешь миллиарды и у тебя всё прекрасно. Значит ли это то, что развиваться и стремиться к большему больше не нужно? Конечно нет! Всю жизнь мы должны ставить себе цели, пусть даже не постигаемые, и пытаться изо всех сил преодолеть их, вне зависимости супергерой ты или нет!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Слушай, я тут подумал, а давай в казино сходим?💰')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9Rgj8M6zQWkLIjaVGboSQABApPe1sAAAugAAyI3jgQHOZSZ2kODqR8E', reply_markup = greet_kb12)
        
        ok+=1
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_s3) 


button91 = KeyboardButton('Конечно нет! Я всегда буду стремиться к чему-то большему!')
button92 = KeyboardButton('Буду работать и жить также, как и жил до этого, мне не хочется ничего менять в своей жизни.')
button93 = KeyboardButton('Стоп')

greet_kb9 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb9.add(button91)
greet_kb9.add(button92)
greet_kb9.add(button93)

kb9 = ['Конечно нет! Я всегда буду стремиться к чему-то большему!', 'Буду работать и жить также, как и жил до этого, мне не хочется ничего менять в своей жизни.', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in kb9)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Конечно нет! Я всегда буду стремиться к чему-то большему!':
        await bot.send_message(message.chat.id, 'у тебя появилась возможность создать что-то большее и значимое, чем ты создавал до этого и тобой заинтересовались большие компании, такие как "Яндекс" и "Майкрософт". Сейчас ты должен доказать, что способен работать в таких компаниях, ты пришёл на собеседование и тебя решили проверить.')        
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Добрый день. Для того, чтобы мы могли устроить Вас на работу, вы должны ответить на несколько вопросов.')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, '1.Что выведет следующая программа?\na = "10"\nb = "10"\nprint(a+b)')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP-Ngj8TiDcA_3VXDhAj2A3xM1wguuwACIAkAAhhC7gjhiiCooToK2R8E', reply_markup=greet_kb10)
        
        ok+=1
    
    
    
    elif message.text == 'Буду работать и жить также, как и жил до этого, мне не хочется ничего менять в своей жизни.':
        await bot.send_message(message.chat.id, "Это нельзя назвать плохой концовкой, но твоя жизнь будет скучной и однообразной, ты всегда должен стремиться к чему то, ты должен действовать всегда и везде. Подумай над этим! Отматываю время назад! Ответь на вопрос ещё раз.")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBQARgj8nBRSG2t433WzNpgMAs9Bgr-gACBwEAAiI3jgREgTHWw4j1vx8E', reply_markup=greet_kb9)

        bad+=1
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb9) 


button101 = KeyboardButton('10')
button102 = KeyboardButton('20')
button103 = KeyboardButton('1010')
button104 = KeyboardButton('Стоп')

greet_kb10 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb10.add(button101)
greet_kb10.add(button102)
greet_kb10.add(button103)
greet_kb10.add(button104)

kb10 = ['10', '20', '1010', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in kb10)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == '10':
        await bot.send_message(message.chat.id, "хм.. у нас появляются сомнения на ваш счёт, докажите обратное!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgEAAxkBAAEBP-Bgj8TeozvJoORv6eIoDtuc1nlZxwACFQEAAjgOghGqOtb4EGwFOx8E', reply_markup=greet_kb10)

        bad+=1
    
    
    
    elif message.text == '20':
        await bot.send_message(message.chat.id, "хм.. у нас появляются сомнения на ваш счёт, докажите обратное!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgEAAxkBAAEBP-Bgj8TeozvJoORv6eIoDtuc1nlZxwACFQEAAjgOghGqOtb4EGwFOx8E', reply_markup=greet_kb10)

        bad+=1
    


    elif message.text == '1010':
        await bot.send_message(message.chat.id, "Хорошо, перейдём к следующему вопросу.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Скажите, какой тип данных соответствует float?", reply_markup=greet_kb11)

        ok+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb10) 


button111 = KeyboardButton('4.0')
button112 = KeyboardButton('"25"')
button113 = KeyboardButton('76')
button114 = KeyboardButton('Стоп')

greet_kb11 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb11.add(button111)
greet_kb11.add(button112)
greet_kb11.add(button113)
greet_kb11.add(button114)

kb11 = ['4.0', '"25"', '76', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in kb11)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == '4.0':
        await bot.send_message(message.chat.id, "Вы справились с нашими вопросами, мы готовы принять Вас на работу.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Итак, ты устроился в престижную компанию,ты любишь свою работу и имеешь материальный достаток. Это ли не чудесно? Значит ли это то, что развиваться и стремиться к большему больше не нужно? Конечно нет! Всю жизнь мы должны ставить себе цели, пусть даже не постигаемые, и пытаться изо всех сил преодолеть их.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Слушай, я тут подумал, а давай в казино сходим?💰")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9Rgj8M6zQWkLIjaVGboSQABApPe1sAAAugAAyI3jgQHOZSZ2kODqR8E', reply_markup=greet_kb12)

        ok+=1
    
    
    
    elif message.text == '"25"':
        await bot.send_message(message.chat.id, "хм.. у нас появляются сомнения на ваш счёт, докажите обратное!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgEAAxkBAAEBP-Bgj8TeozvJoORv6eIoDtuc1nlZxwACFQEAAjgOghGqOtb4EGwFOx8E', reply_markup=greet_kb11)

        bad+=1
    
    
    
    elif message.text == '76':
        await bot.send_message(message.chat.id, "хм.. у нас появляются сомнения на ваш счёт, докажите обратное!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgEAAxkBAAEBP-Bgj8TeozvJoORv6eIoDtuc1nlZxwACFQEAAjgOghGqOtb4EGwFOx8E', reply_markup=greet_kb11)

        bad+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb11) 


button121 = KeyboardButton('А давай!')
button122 = KeyboardButton('нет, я откажусь')
button123 = KeyboardButton('Стоп')

greet_kb12 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb12.add(button121)
greet_kb12.add(button122)
greet_kb12.add(button123)

kb12 = ['А давай!', 'нет, я откажусь', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in kb12)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'А давай!':
        await bot.send_message(message.chat.id, "Так, мы пришли в казино и... Кажется, сегодня не твой день, ты проиграл всё своё состояние, идти в казино было огромной ошибкой... Отматываю время назад! Ответь на вопрос ещё раз.")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP9dgj8P7m0lm_KPf_aMGDozzYbr5hAACZgEAAladvQrYDLaLXKq1Wx8E', reply_markup=greet_kb12)
        
        bad+=1

    
    
    
    
    elif message.text == 'нет, я откажусь':
        await bot.send_message(message.chat.id, 'Ты сделал правильный выбор! Азартные игры до добра не доведут! Ну что же, очередное правильное решение, ты прошёл все мои испытания, поздравляю!')
        time.sleep(0.2)
        await bot.send_message(message.chat.id, 'Хотя подожди, тебе предстоит сразить главного босса (то есть меня :>), сыграем в "камень, ножницы, бумага"?')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP-Zgj8XvBkHKYuA4wSF3-UWpzqRUiAACXQIAAladvQp6NSgg1ryRux8E', reply_markup=greet_kkk)
        
        ok+=1
    
    
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb12) 



buttonkkk1 = KeyboardButton('Давай сыграем, я тебя обязательно выиграю!')
buttonkkk2 = KeyboardButton('Да нет, как то не хочется')
buttonkkk3 = KeyboardButton('Стоп')
    
greet_kkk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kkk.add(buttonkkk1)
greet_kkk.add(buttonkkk2)
greet_kkk.add(buttonkkk3)

k = ['Давай сыграем, я тебя обязательно выиграю!', 'Да нет, как то не хочется', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in k)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Давай сыграем, я тебя обязательно выиграю!':
        await bot.send_message(message.chat.id, "Это мы ещё посмотрим! Камень, ножницы, бумага, раз... два... три...", reply_markup=greet_0)

        ok+=1
    
    
    elif message.text == 'Да нет, как то не хочется':
        await bot.send_message(message.chat.id, "Ну как хочешь, кажется в этом мире ты сделал всё, что должен был сделать, сейчас я тебя телепортирую тебя обратно, держись крепче!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "хэй, ну как ты?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "понравилось?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "судя по твоему довольному лицу ты прошёл игру на хорошую концовку?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Хээййй, поздравляю!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_tgj8gdVzQMLlaVcwLseVL6434sxAACCwEAAvcCyA_F9DuYlapx2x8E', reply_markup=greet_kb13)

        ok+=1
    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kkk) 


button01 = KeyboardButton('Камень')
button02 = KeyboardButton('Ножницы')
button03 = KeyboardButton('Бумага')
button04 = KeyboardButton('Стоп')

greet_0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_0.add(button01)
greet_0.add(button02)
greet_0.add(button03)
greet_0.add(button04)

k0 = ['Камень', 'Ножницы', 'Бумага', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in k0)
async def text(message: types.Message):
    global cur
    global start_time

    #обновляем user_time в бд
    a = time.time() - start_time
    time_format = time.strftime("%H:%M:%S", time.gmtime(a))
    
    cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
    conn.commit()

    global ok
    global bad

    if message.text == 'Камень':
        await bot.send_message(message.chat.id, "Бумага! Что, не получается выиграть? А вот тебе и урок. Проигрывать – не страшно. Страшно – впасть в дизмораль. Всю жизнь нас будут преследовать неудачи, это нормально.") 
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Кажется в этом измерении ты сделал всё, что должен был, сейчас я отправлю тебя обратно, держись крепче!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "хэй, ну как ты?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "понравилось?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "судя по твоему довольному лицу ты прошёл игру на хорошую концовку?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Хээййй, поздравляю!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_tgj8gdVzQMLlaVcwLseVL6434sxAACCwEAAvcCyA_F9DuYlapx2x8E', reply_markup=greet_kb13)

        ok+=1
    
    
    
    
    elif message.text == 'Ножницы':
        await bot.send_message(message.chat.id, "Камень! Что, не получается выиграть? А вот тебе и урок. Проигрывать – не страшно. Страшно – впасть в дизмораль. Всю жизнь нас будут преследовать неудачи, это нормально.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Кажется в этом измерении ты сделал всё, что должен был, сейчас я отправлю тебя обратно, держись крепче!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "хэй, ну как ты?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "понравилось?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "судя по твоему довольному лицу ты прошёл игру на хорошую концовку?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Хээййй, поздравляю!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_tgj8gdVzQMLlaVcwLseVL6434sxAACCwEAAvcCyA_F9DuYlapx2x8E', reply_markup=greet_kb13)

        ok+=1
    
    
    
    
    
    
    elif message.text == 'Бумага':
        await bot.send_message(message.chat.id, "Ножницы! Что, не получается выиграть? А вот тебе и урок. Проигрывать – не страшно. Страшно – впасть в дизмораль. Всю жизнь нас будут преследовать неудачи, это нормально.")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Кажется в этом измерении ты сделал всё, что должен был, сейчас я отправлю тебя обратно, держись крепче!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "БУХ! ТУХ! ФЫХ! ...звуки телепортации... ЧУХ! БЫХ! ФУХ!")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "хэй, ну как ты?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "понравилось?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "судя по твоему довольному лицу ты прошёл игру на хорошую концовку?")
        time.sleep(0.2)
        await bot.send_message(message.chat.id, "Хээййй, поздравляю!")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_tgj8gdVzQMLlaVcwLseVL6434sxAACCwEAAvcCyA_F9DuYlapx2x8E', reply_markup=greet_kb13)

        ok+=1




    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_0) 


button131 = KeyboardButton('Да, мне понравилось!')
button132 = KeyboardButton('Ну да, прошёл, честно сказать игра так себе')
button133 = KeyboardButton('Не с первой попытки конечно, но дошёл, мне понравилось!')
button134 = KeyboardButton('Стоп')
    
greet_kb13 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb13.add(button131)
greet_kb13.add(button132)
greet_kb13.add(button133)
greet_kb13.add(button134)

kb13 = ['Да, мне понравилось!', 'Ну да, прошёл, честно сказать игра так себе', 'Не с первой попытки конечно, но дошёл, мне понравилось!', 'Стоп']

#=====================================================================================================================================

@dp.message_handler(lambda message: message.text in kb13)
async def text(message: types.Message):
    global cur
    global start_time

    global ok
    global bad

    if message.text == 'Да, мне понравилось!':
        await bot.send_message(message.chat.id, 'Я рад! Ну что же, кажется нам надо прощаться? Неплохо провели время, до скорых встреч! Надеюсь ты усвоил мораль, которую я пытался донести и всё то время, что я потратил, пошло тебе на пользу.😊')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_5gj8ikqfeIfpIXIfQ47OHgTwy5VQACxwADMNSdEbWf7Uv9DdzuHwQ')
        ok+=1
        

        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Вы прошли игру за: %s' % time_format)
        

        await bot.send_message(message.chat.id, 'Количество верных ответов: %s ' % ok)
        await bot.send_message(message.chat.id, 'Количество неверных ответов: %s ' % bad)
        TotalAnswers = ok + bad 
        await bot.send_message(message.chat.id, 'Общее количество вопросов: %s ' % TotalAnswers)

        #найдём процент верных ответов
        z = ok*100
        correctAnswersPercent = int(z/TotalAnswers)
        await bot.send_message(message.chat.id, 'Процент верных ответов: %s' % correctAnswersPercent)


        #обновляем user_record в бд
        cur.execute(f"UPDATE Users SET user_record = {correctAnswersPercent} WHERE user_id = {message.from_user.id}")
        conn.commit()


        #обновляем user_time в бд
        cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
        conn.commit()

        await bot.send_message(message.chat.id, 'Если захочешь пройти игру ещё раз - напиши /delete, чтобы удалить свой прежний рекорд, а затем напиши /start, чтобы поставить новый!')
        await bot.send_photo(message.from_user.id, 'https://static.vecteezy.com/system/resources/previews/000/359/980/original/chat-bot-free-wallpaper-the-robot-holds-the-phone-responds-to-messages-vector-flat-illustration.jpg', reply_markup=greet_stop)
    
    
    
    
    
    elif message.text == 'Ну да, прошёл, честно сказать игра так себе':
        await bot.send_message(message.chat.id, "Всем не угодить, но я буду безумно рад, если ты расскажешь о всех нюансах подробнее, спасибо, что уделил своё время. Обещаю, в следующий раз я тебя не огорчу! Но в любом случае я надеюсь ты усвоил мораль, которую я пытался донести и всё то время, что я потратил, пошло тебе на пользу.😊")
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_5gj8ikqfeIfpIXIfQ47OHgTwy5VQACxwADMNSdEbWf7Uv9DdzuHwQ')
        ok+=1

        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Вы прошли игру за: %s' % time_format)

 
    
        await bot.send_message(message.chat.id, 'Количество верных ответов: %s ' % ok)
        await bot.send_message(message.chat.id, 'Количество неверных ответов: %s ' % bad)
        TotalAnswers = ok + bad 
        await bot.send_message(message.chat.id, 'Общее количество вопросов: %s ' % TotalAnswers)

        #найдём процент верных ответов
        z = ok*100
        correctAnswersPercent = int(z/TotalAnswers)
        await bot.send_message(message.chat.id, 'Процент верных ответов: %s' % correctAnswersPercent)


        #обновляем user_record в бд
        cur.execute(f"UPDATE Users SET user_record = {correctAnswersPercent} WHERE user_id = {message.from_user.id}")
        conn.commit()


        #обновляем user_time в бд
        cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
        conn.commit()

        await bot.send_message(message.chat.id, 'Если захочешь пройти игру ещё раз - напиши /delete, чтобы удалить свой прежний рекорд, а затем напиши /start, чтобы поставить новый!')
        await bot.send_photo(message.from_user.id, 'https://static.vecteezy.com/system/resources/previews/000/359/980/original/chat-bot-free-wallpaper-the-robot-holds-the-phone-responds-to-messages-vector-flat-illustration.jpg', reply_markup=greet_stop)
    
    
    
    elif message.text == 'Не с первой попытки конечно, но дошёл, мне понравилось!':
        await bot.send_message(message.chat.id, 'Я рад! Ну что же, кажется нам надо прощаться? Неплохо провели время, до скорых встреч! Надеюсь ты усвоил мораль, которую я пытался донести и всё то время, что я потратил, пошло тебе на пользу.😊')
        time.sleep(0.2)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP_5gj8ikqfeIfpIXIfQ47OHgTwy5VQACxwADMNSdEbWf7Uv9DdzuHwQ')
        ok+=1


        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Вы прошли игру за: %s' % time_format)


        await bot.send_message(message.chat.id, 'Количество верных ответов: %s ' % ok)
        await bot.send_message(message.chat.id, 'Количество неверных ответов: %s ' % bad)
        TotalAnswers = ok + bad 
        await bot.send_message(message.chat.id, 'Общее количество вопросов: %s ' % TotalAnswers)

        #найдём процент верных ответов
        z = ok*100
        correctAnswersPercent = int(z/TotalAnswers)
        await bot.send_message(message.chat.id, 'Процент верных ответов: %s' % correctAnswersPercent)

        #обновляем user_record в бд
        cur.execute(f"UPDATE Users SET user_record = {correctAnswersPercent} WHERE user_id = {message.from_user.id}")
        conn.commit()


        #обновляем user_time в бд
        cur.execute(f"UPDATE Users SET user_time = '{time_format}' WHERE user_id = {message.from_user.id}")
        conn.commit()

        
        await bot.send_message(message.chat.id, 'Если захочешь пройти игру ещё раз - напиши /delete, чтобы удалить свой прежний рекорд, а затем напиши /start, чтобы поставить новый!')
        await bot.send_photo(message.from_user.id, 'https://static.vecteezy.com/system/resources/previews/000/359/980/original/chat-bot-free-wallpaper-the-robot-holds-the-phone-responds-to-messages-vector-flat-illustration.jpg', reply_markup=greet_stop)



    
    
    
    elif message.text == 'Стоп':
        await bot.send_message(message.chat.id, 'Твой результат - 0%. Ты должен пройти игру полностью, чтобы сохранить свой настоящий результат.')
        await bot.send_message(message.chat.id, 'Если захочешь оставить след в истории и поставить рекорд - пиши /delete, чтобы удалить свой нулевой результат, а затем напиши /start, чтобы начать игру заново и поставить рекорд!', reply_markup=greet_stop)
        await message.answer_sticker(r'CAACAgIAAxkBAAEBP8hgj8GLaIbzfCpPhjQF4CfXMCpxXgACZwIAAladvQoH52ys787IPx8E')
        a = time.time() - start_time
        time_format = time.strftime("%H:%M:%S", time.gmtime(a))
        await bot.send_message(message.chat.id, 'Ваше время игры: %s' % time_format)
    else:
        await bot.send_message(message.chat.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...", reply_markup=greet_kb13) 

#=====================================================================================================================================


#это я на всякий случай сделал, тут мы фильтруем вообще все сообщения в чате :)
@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Постарайся вводить то, что было предложено, я всего лишь глупая машина, не телепат...")


if __name__ == '__main__':
    executor.start_polling(dp)