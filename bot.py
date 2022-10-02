from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import randrange
import json, requests, sys, time
import sqlite3

updater = Updater("5449824704:AAGEC-7JT5qIraxTNfl96x3ImDoxAvkHob0",
                  use_context=True)
bot = updater.bot

app_id = '8931547825081ff1a3789851aab073d2'

weather_smiles = {'01': '☀',
                  '02': '🌤',
                  '03': '☁️',
                  '04': '☁️',
                  '09': '🌧',
                  '10': '🌦',
                  '11': '⛈',
                  '13': '❄️',
                  '50': '🌫'}

facts_ru = [
'Метеорология ― самая молодая естественная наука. Вместе с тем, первые прогностические выводы люди научились делать еще в Древней Греции. Известно, что жена Сократа обладала сварливым характером. Однажды она так достала супруга, что тот вышел из дома и сел на порог, взявшись за голову. Тогда она вылила на него ведро воды. «После грома всегда следует дождь!» ― воскликнул философ',
'Люди по-разному воспринимают погоду. Некоторые, в том числе и сильные личности, подвержены метеопатии. Например, Наполеон, при всей своей энергичности, в непогоду терял самообладание, становился вялым и подавленным. Так произошло в окрестностях Ватерлоо, когда многообещающий день начался сильным ливнем, а завершился полным разгромом',
'Самый первый прогноз погоды был опубликован в лондонской Times 1 августа 1861 года. Его автором был Роберт Фицрой — вице-адмирал королевского флота. Ранее Р. Фицрой возглавлял научную экспедицию на корабле «Бигль» с участием Ч. Дарвина',
'Ливневый дождь не дал публике услышать лучшую речь Бернарда Шоу, как считал он сам. Писатель произнес ее в Гайд-парке всего для семи человек: один был секретарем общества, пригласившего Шоу на выступление, а остальные шесть — полицейскими, которые охраняли порядок',
'Нередко капризы погоды оказывали влияние на моду. Так, английский король Эдуард VII, сын королевы Виктории, однажды во время дождя закатал брюки. После этого в моду вошли манжеты',
'Самый первый телевизионный прогноз погоды был показан на телеканале BBC в Англии 11 ноября 1936 года',
'Многие видели хронику, когда под барабанную дробь фашистские флаги бросали к подножью Мавзолея. Но не многие знают, что этому чуть не помешала погода. Пошел дождь, и кожа барабанов намокла — дроби не было! В ГУМе устроили печи: одни барабаны сушились, а в другие — били',
'В Португалии уважительной причиной неявки на работу является ненастная погода',
'В процессе наблюдения за погодой появились разные температурные шкалы. Наибольшее распространение получила шкала Цельсия, где за 0 принята температура замерзания воды. Однако в Северной Америке прижилась шкала Фаренгейта. Любопытно, что в одном значении обе шкалы все-таки сходятся. Температура −40 по Цельсию точно равна температуре −40 по Фаренгейту',
'Для метеорологов самый хороший антициклон хуже самого плохого циклона',
'Из всех народных примет лучше всего оправдываются крещенские морозы и черемуховые холода',
'1 мм осадков — это 1 литр воды на площади 1 кв. м.',
'Одно из самых солнечных мест на планете Земля — это Мертвое море. Здесь около 330 солнечных дней в году! Синоптики с прогнозами особо не парятся. Зато парятся отдыхающие',
'Меньше всего солнца на архипелаге Северная Земля. Там солнце светит всего 12 дней в году'
'В средних широтах погода обладает большой изменчивостью. Она может меняться каждый день и по нескольку раз в день. С этим хорошо знакомы в США. В свое время Марк Твен сказал: «Если вам не нравится погода в Новой Англии, подождите несколько минут». Зато какие возможности для общения! Согласно статистике, если бы погода не менялась, то девять из десяти человек, никогда бы не начали разговора. Да, снег, дождь и ветер, не всегда соответствуют нашим желаниям, и за это погоду часто ругают. Но вот, что говорят на этот счет мудрые шотландцы: «Не бывает плохой погоды, бывает плохая одежда!»',
'В 17 веке в Англии приняли закон о смертной казни синоптика за его неверное предсказание, после чего желающих предсказать погоду практически не осталось',
'В России погодные условия еще более жесткие. Наша страна — самая холодная в мире. Со среднегодовой температурой −5 по суровости климата она опережает Финляндию и Канаду. В таких условиях без шуток не выжить: «Все так жалуются на погоду. Как будто, кроме погоды, у нас все хорошо»',
'В Гидрометцентре у каждого выражения имеется свое значение. «Ожидается дождь» значит то, что он идет не менее 12 ч, «кратковременный дождь» – не более 3 часов, «без существенных осадков» означает, что осадки выпадут не больше 0,3 л на кв.м',
'Недавно изобрели зонт, который предупреждает владельца о приближающемся дожде. При повышении вероятности осадков он тоже повышается, а в ручке зажигается синий свет. Прогноз поступает из Интернета',
'При прогнозе погоды синоптики Сан-Франциско указывают вероятность исполнения прогноза так: «Дождь будет с вероятностью 7/3», поскольку голосование проводят десять работников станции',
'На одном из Интернет-сайтов можно увидеть погоду многих городов мира. В списке 40 крупных городов России и деревня Гадюкино, где всегда один и тот же прогноз: «В деревне Гадюкино дожди…»',
'Крупные туристические агентства в последнее время предоставляют страхование от беспогодицы. Если во время отдыха все время шел дождь, тогда туристу выплачивают солидную неустойку',
'Жительница Сан-Франциско зарабатывает на просмотре прогноза синоптиков до 27 долл в месяц, так как она держит пари с мужем на доллар, что погода не будет соответствовать прогнозу',
]
facts_en = [
'The naming of hurricanes and tropical storms officially began in 1953',
'The wind doesn’t make a sound until it blows against an object',
'Average global temperature is up 0.94°C (1.7°F) since 1880',
'Fire whirls are tornadoes made of fire caused by wildfires',
'At any given time, on average there are about 1800 thunderstorms occurring on Earth with 100 lightning strikes per second',
'For each minute of the day, 1 billion tonnes of rain falls on the Earth',
'A molecule of water will stay in the Earth’s atmosphere for an average duration of 10-12 days',
'Every second around 100 lightning bolts strike the Earth',
'The fastest speed a falling raindrop can hit you is 18 mph',
'It was so cold in 1684 that the Thames River in England froze solid for two months',
'Mawsynram in Meghalaya, India is the wettest place on Earth with an annual rainfall of more than 11 meters',
'Highest Temperature Recorded on Earth is 56.7°C (134°F) at Greenland Ranch in Death Valley, California, on July 10, 1913',
'Lowest Temperature Recorded on Earth is -89.2°C (-128.5°F) at Vostok, Antarctica on July 21, 1983',
'A cubic mile of ordinary fog contains less than a gallon of water',
'In 1899, it was so cold that the Mississippi river froze over its entire length',
'The air located around a lightning bolt is heated to around 30,000°C. This is 5 times hotter than the surface of the sun',
'The average width of a tornado’s funnel averages about 100 to 200 yards, but it may be as wide as a mile',
'Snowflakes falling at 2-4 mph can take up to 1 hour to reach the ground',
'The country most affected by tornadoes is the USA which faces on average 1200 tornadoes every year',
'Commonwealth Bay, Antarctica is the windiest place on Earth with winds of 200mph been recorded',
]

def get_weather(location, lang):
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                 params={'q': location + ',RU', 'type': 'like', 'units': 'metric', 'APPID': app_id, 'lang': lang})
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    weather_data = json.loads(response.text)
    return weather_data

def get_language(chat_id):
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute('select * from user_data01 where chat_id=%s;'%chat_id)
    data = cur.fetchone()
    database.close()
    if data:
        return data[1]
    return 'ru'

def set_language(chat_id, lang):
    database = sqlite3.connect("database.db")
    try:
        database.execute('insert into user_data01 (chat_id, language) values (%s, "%s")' %(chat_id, lang))
    except:
        database.execute('update user_data01 set language="%s" where chat_id=%s' %(lang, chat_id))
    database.commit()
    database.close()

def start(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    if lang == 'ru':
        bot.send_message(chat_id=update.effective_chat.id, text='''
Привет!
Я - новый бот для простого и качественного определения погоды
Просто введите название города или населённого пункта России
Я покажу вам подробные данные о погоде в ближайшее время
''')
    else:
        bot.send_message(chat_id=update.effective_chat.id, text='''
Hi!
I'm a new bot for simple and high-quality weather determination
Just input the location in Russia where you need to determine the weather
I'll show you weather forecast for soon
''')

def lang(update: Update, context: CallbackContext):
    button_list = [[InlineKeyboardButton("Русский🇷🇺", callback_data="language_ru"),
    InlineKeyboardButton("English🇬🇧", callback_data="language_en")]]
    bot.send_message(chat_id=update.effective_chat.id, text="Выберите ваш язык/Choose your language", reply_markup=InlineKeyboardMarkup(button_list))

def language_ru(update: Update, context: CallbackContext):
    set_language(update.effective_chat.id, 'ru')
    bot.send_message(chat_id=update.effective_chat.id, text="Русский язык успешно установлен")

def language_en(update: Update, context: CallbackContext):
    set_language(update.effective_chat.id, 'en')
    bot.send_message(chat_id=update.effective_chat.id, text="English has changed successfully")

def show_fact(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    button_list = [[InlineKeyboardButton(("Ещё😎" if lang == 'ru' else "Show more😎"), callback_data="show_fact")]]
    bot.send_message(chat_id=update.effective_chat.id, text=("А вы знали, что...\n%s" %facts_ru[randrange(len(facts_ru))] if lang == 'ru' else "Did you know...\n%s" %facts_en[randrange(len(facts_en))]), reply_markup=InlineKeyboardMarkup(button_list))

def show_help(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    if lang == 'ru':
        bot.send_message(chat_id=update.effective_chat.id, text='''
/start - Запуск бота
/lang - Выбор языка
/ru - Установить русский язык
/en - Установить английсикй язык
/fact - Показать интересный факт
/help - Показать список доступных команд
''')
    else:
        bot.send_message(chat_id=update.effective_chat.id, text='''
/start - Launch the bot
/lang - Choose the language
/ru - Change Russian language
/en - Change English language
/fact - Show an intresting fact
/help - Show a list of commands
''')

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == 'language_ru':
        language_ru(update, context)
    if variant == 'language_en':
        language_en(update, context)
    if variant == 'show_fact':
        show_fact(update, context)

def start_weather(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    city = update.message.text.title()
    weather_data = get_weather(city, lang)
    if weather_data is None:
        button_list = [[InlineKeyboardButton(("Хочу интересный факт😁" if lang == 'ru' else "I want to know an interesting fact😁"), callback_data="show_fact")]]
        bot.send_message(chat_id=update.effective_chat.id, text=("Населённый пункт *%s* не найден🤨" if lang == 'ru' else "Location *%s* not found🤨") %city, parse_mode='markdown', reply_markup=InlineKeyboardMarkup(button_list))
    else:
        button_list = [[InlineKeyboardButton(("Хочу интересный факт😁" if lang == 'ru' else "I want to know an interesting fact😁"), callback_data="show_fact")]]
        time_add = weather_data['city']['timezone'] // 3600
        w = weather_data['list']
        t = time.gmtime()
        #bot.send_location(chat_id=update.effective_chat.id, latitude=weather_data['city']['coord']['lat'], longitude=weather_data['city']['coord']['lon'], horizontal_accuracy=1500) 
        bot.send_message(chat_id=update.effective_chat.id, text=("Погода в *%s*\nЧасовой пояс (UTC+%s) %02d:%02d" if lang == 'ru' else "Weather in *%s*\nTimezone (UTC+%s) %02d:%02d") %(city, time_add, (t.tm_hour + time_add) % 24, t.tm_min), parse_mode='markdown')
        day = (time.time() // 3600 + time_add) // 24
        text = ''
        for i in range(len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day:
                break
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Сегодня*:\n%s' if lang == 'ru' else '*Today*:\n%s') %text, parse_mode='markdown')
        text = ''
        for i in range(i, len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day + 1:
                break 
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Завтра*:\n%s' if lang == 'ru' else '*Tomorrow*:\n%s') %text, parse_mode='markdown')
        text = ''
        for i in range(i, len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day + 2:
                break 
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Послезавтра*:\n%s' if lang == 'ru' else '*Day after tomorrow*:\n%s') %text, parse_mode='markdown', reply_markup=InlineKeyboardMarkup(button_list))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('lang', lang))
updater.dispatcher.add_handler(CommandHandler('ru', language_ru))
updater.dispatcher.add_handler(CommandHandler('en', language_en))
updater.dispatcher.add_handler(CommandHandler('fact', show_fact))
updater.dispatcher.add_handler(CommandHandler('help', show_help))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), start_weather))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()

'В 17 веке в Англии приняли закон о смертной казни синоптика за его неверное предсказание, после чего желающих предсказать погоду практически не осталось',
'В России погодные условия еще более жесткие. Наша страна — самая холодная в мире. Со среднегодовой температурой −5 по суровости климата она опережает Финляндию и Канаду. В таких условиях без шуток не выжить: «Все так жалуются на погоду. Как будто, кроме погоды, у нас все хорошо»',
'В Гидрометцентре у каждого выражения имеется свое значение. «Ожидается дождь» значит то, что он идет не менее 12 ч, «кратковременный дождь» – не более 3 часов, «без существенных осадков» означает, что осадки выпадут не больше 0,3 л на кв.м',
'Недавно изобрели зонт, который предупреждает владельца о приближающемся дожде. При повышении вероятности осадков он тоже повышается, а в ручке зажигается синий свет. Прогноз поступает из Интернета',
'При прогнозе погоды синоптики Сан-Франциско указывают вероятность исполнения прогноза так: «Дождь будет с вероятностью 7/3», поскольку голосование проводят десять работников станции',
'На одном из Интернет-сайтов можно увидеть погоду многих городов мира. В списке 40 крупных городов России и деревня Гадюкино, где всегда один и тот же прогноз: «В деревне Гадюкино дожди…»',
'Крупные туристические агентства в последнее время предоставляют страхование от беспогодицы. Если во время отдыха все время шел дождь, тогда туристу выплачивают солидную неустойку',
'Жительница Сан-Франциско зарабатывает на просмотре прогноза синоптиков до 27 долл в месяц, так как она держит пари с мужем на доллар, что погода не будет соответствовать прогнозу',
]
facts_en = [
'The naming of hurricanes and tropical storms officially began in 1953',
'The wind doesn’t make a sound until it blows against an object',
'Average global temperature is up 0.94°C (1.7°F) since 1880',
'Fire whirls are tornadoes made of fire caused by wildfires',
'At any given time, on average there are about 1800 thunderstorms occurring on Earth with 100 lightning strikes per second',
'For each minute of the day, 1 billion tonnes of rain falls on the Earth',
'A molecule of water will stay in the Earth’s atmosphere for an average duration of 10-12 days',
'Every second around 100 lightning bolts strike the Earth',
'The fastest speed a falling raindrop can hit you is 18 mph',
'It was so cold in 1684 that the Thames River in England froze solid for two months',
'Mawsynram in Meghalaya, India is the wettest place on Earth with an annual rainfall of more than 11 meters',
'Highest Temperature Recorded on Earth is 56.7°C (134°F) at Greenland Ranch in Death Valley, California, on July 10, 1913',
'Lowest Temperature Recorded on Earth is -89.2°C (-128.5°F) at Vostok, Antarctica on July 21, 1983',
'A cubic mile of ordinary fog contains less than a gallon of water',
'In 1899, it was so cold that the Mississippi river froze over its entire length',
'The air located around a lightning bolt is heated to around 30,000°C. This is 5 times hotter than the surface of the sun',
'The average width of a tornado’s funnel averages about 100 to 200 yards, but it may be as wide as a mile',
'Snowflakes falling at 2-4 mph can take up to 1 hour to reach the ground',
'The country most affected by tornadoes is the USA which faces on average 1200 tornadoes every year',
'Commonwealth Bay, Antarctica is the windiest place on Earth with winds of 200mph been recorded',
]

def get_weather(location, lang):
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                 params={'q': location + ',RU', 'type': 'like', 'units': 'metric', 'APPID': app_id, 'lang': lang})
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    weather_data = json.loads(response.text)
    return weather_data

def get_language(chat_id):
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    cur.execute('select * from user_data01 where chat_id=%s;'%chat_id)
    data = cur.fetchone()
    database.close()
    if data:
        return data[1]
    return 'ru'

def set_language(chat_id, lang):
    database = sqlite3.connect("database.db")
    try:
        database.execute('insert into user_data01 (chat_id, language) values (%s, "%s")' %(chat_id, lang))
    except:
        database.execute('update user_data01 set language="%s" where chat_id=%s' %(lang, chat_id))
    database.commit()
    database.close()

def start(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    if lang == 'ru':
        bot.send_message(chat_id=update.effective_chat.id, text='''
Привет!
Я - новый бот для простого и качественного определения погоды
Просто введите название города или населённого пункта России
Я покажу вам подробные данные о погоде в ближайшее время
''')
    else:
        bot.send_message(chat_id=update.effective_chat.id, text='''
Hi!
I'm a new bot for simple and high-quality weather determination
Just input the location in Russia where you need to determine the weather
I'll show you weather forecast for soon
''')

def lang(update: Update, context: CallbackContext):
    button_list = [[InlineKeyboardButton("Русский🇷🇺", callback_data="language_ru"),
    InlineKeyboardButton("English🇬🇧", callback_data="language_en")]]
    bot.send_message(chat_id=update.effective_chat.id, text="Выберите ваш язык/Choose your language", reply_markup=InlineKeyboardMarkup(button_list))

def language_ru(update: Update, context: CallbackContext):
    set_language(update.effective_chat.id, 'ru')
    bot.send_message(chat_id=update.effective_chat.id, text="Русский язык успешно установлен")

def language_en(update: Update, context: CallbackContext):
    set_language(update.effective_chat.id, 'en')
    bot.send_message(chat_id=update.effective_chat.id, text="English has changed successfully")

def show_fact(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    button_list = [[InlineKeyboardButton(("Ещё😎" if lang == 'ru' else "Show more😎"), callback_data="show_fact")]]
    bot.send_message(chat_id=update.effective_chat.id, text=("А вы знали, что...\n%s" %facts_ru[randrange(len(facts_ru))] if lang == 'ru' else "Did you know...\n%s" %facts_en[randrange(len(facts_en))]), reply_markup=InlineKeyboardMarkup(button_list))

def show_help(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    if lang == 'ru':
        bot.send_message(chat_id=update.effective_chat.id, text='''
/start - Запуск бота
/lang - Выбор языка
/ru - Установить русский язык
/en - Установить английсикй язык
/fact - Показать интересный факт
/help - Показать список доступных команд
''')
    else:
        bot.send_message(chat_id=update.effective_chat.id, text='''
/start - Launch the bot
/lang - Choose the language
/ru - Change Russian language
/en - Change English language
/fact - Show an intresting fact
/help - Show a list of commands
''')

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == 'language_ru':
        language_ru(update, context)
    if variant == 'language_en':
        language_en(update, context)
    if variant == 'show_fact':
        show_fact(update, context)

def start_weather(update: Update, context: CallbackContext):
    lang = get_language(update.effective_chat.id)
    global xxx
    city = update.message.text.title()
    weather_data = get_weather(city, lang)
    if weather_data is None:
        button_list = [[InlineKeyboardButton(("Хочу интересный факт😁" if lang == 'ru' else "I want to know an interesting fact😁"), callback_data="show_fact")]]
        bot.send_message(chat_id=update.effective_chat.id, text=("Населённый пункт *%s* не найден🤨" if lang == 'ru' else "Location *%s* not found🤨") %city, parse_mode='markdown', reply_markup=InlineKeyboardMarkup(button_list))
    else:
        button_list = [[InlineKeyboardButton(("Хочу интересный факт😁" if lang == 'ru' else "I want to know an interesting fact😁"), callback_data="show_fact")]]
        time_add = weather_data['city']['timezone'] // 3600
        xxx = weather_data
        w = weather_data['list']
        t = time.gmtime()
        #bot.send_location(chat_id=update.effective_chat.id, latitude=weather_data['city']['coord']['lat'], longitude=weather_data['city']['coord']['lon'], horizontal_accuracy=1500) 
        bot.send_message(chat_id=update.effective_chat.id, text=("Погода в *%s*\nЧасовой пояс (UTC+%s) %02d:%02d" if lang == 'ru' else "Weather in *%s*\nTimezone (UTC+%s) %02d:%02d") %(city, time_add, (t.tm_hour + time_add) % 24, t.tm_min), parse_mode='markdown')
        day = (time.time() // 3600 + time_add) // 24
        text = ''
        for i in range(len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day:
                break
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Сегодня*:\n%s' if lang == 'ru' else '*Today*:\n%s') %text, parse_mode='markdown')
        text = ''
        for i in range(i, len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day + 1:
                break 
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Завтра*:\n%s' if lang == 'ru' else '*Tomorrow*:\n%s') %text, parse_mode='markdown')
        text = ''
        for i in range(i, len(w)):
            date, main, weather = w[i]['dt'], w[i]['main'], w[i]['weather']
            if (date // 3600 + time_add) // 24 != day + 2:
                break 
            t = time.gmtime(date + time_add * 3600)
            text = text + ("%02d:00: Температура %+.1f C° (ощущается как %+.1f С°), %s%s\n" if lang == 'ru' else "%02d:00: Temperature %+.1f C° (feels like %+.1f С°), %s%s\n") %(t.tm_hour, main['temp'], main['feels_like'], weather[0]['description'], weather_smiles[weather[0]['icon'][:2]])
        if text:
            bot.send_message(chat_id=update.effective_chat.id, text=('*Послезавтра*:\n%s' if lang == 'ru' else '*Day after tomorrow*:\n%s') %text, parse_mode='markdown', reply_markup=InlineKeyboardMarkup(button_list))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('lang', lang))
updater.dispatcher.add_handler(CommandHandler('ru', language_ru))
updater.dispatcher.add_handler(CommandHandler('en', language_en))
updater.dispatcher.add_handler(CommandHandler('fact', show_fact))
updater.dispatcher.add_handler(CommandHandler('help', show_help))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), start_weather))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
