import datetime as dt
import threading
import time
import os
import schedule
import Interactive

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from functools import wraps

import Chat
import Links
import database3 as db

import telebot
from telebot import types
import User
import Programme
import time as timing

# token = "1406324519:AAGIK0HBMNtZ3IfSZ_iiy0PfM6bv8Ngch7c"  # older token
token_lay = "1413164033:AAH0U93n1FtD9H1y6cdMOGNojfzigzsxu2M"
token_dih = "1716180979:AAHlbkPTJ7FBJvT3GgGUadRQy7G3yTtIt7M"

bot = telebot.TeleBot(token_dih)


def commit():
    # os.system('git add *')
    # os.system('git commit -am "update"')
    print('git updated')

# commit()


def message_to_id_(id_, message, attachment=None):
    bot.send_message(id_, message)
    if attachment is not None:
        bot.send_document(id_, attachment)


db.init()

time_diff = lambda first, second: (first - second + 24) % 24


class threader:

    def __init__(self, user):
        self.user = user

    def run_welcome(self):
        threading.Thread(target=self.welcome).start()

    def welcome(self):
        user = self.user

        def msg(message, markup=None):
            bot.send_message(user.chat_id, message, reply_markup=markup)
            print('sent {0} to {1}'.format(message, user.login))

        def doc(path):
            for i in range(5):
                try:
                    document = open(path, 'rb')
                    if document is not None:
                        bot.send_document(user.chat_id, document)
                    return
                except Exception as e:
                    print(e)
                    time.sleep(5)

        msg('Добро пожаловать в программу! 👋🏼\n\nМы приготовили для вас три простых и очень эффективных ментальных '
            'упражнения, которые можно выполнять в течении дня, чтобы улучшить своё самочувствие, а также снизить '
            'уровень стресса и напряжения.\n\nВизуализация 🌾\nПоможет нам настроиться на день, наполниться силой, '
            'светом и уверенностью.\nПродолжительность 7 минут.\nРекомендую с неё начинать свой день.\n\nДыхание '
            '🌲\nУспокоит наш ум и сердце, восстановит баланс, поможет отвлечься и переключиться.\nПродолжительность '
            '3,5 минуты.\nЛучше выполнять в обед, перерыв или перед началом какого-нибудь важного мероприятия или по '
            'его окончании, чтобы прийти в себя.\n\nРасслабление 🌊\nСнимет напряжение с тела и ума, поможет заснуть '
            'и отдохнуть.\nПродолжительность 12 минут.\nВыполнять можно и в кровати, перед сном, чтобы легче и '
            'быстрее уснуть, расслабиться и сбросить груз прожитого дня.')
        msg('Команда проекта\n\n\nАвтор @saturtim\nТехническая реализация @almosh822\nДизайн и иллюстрации '
            '@aamiamm\nКреативный продюсер @akurtsev')
        msg('Предлагаю вам определиться с выбором времени, когда будет комфортно выполнять упражнения ⏰\n\nУкажите '
            'текущее время в вашем регионе, чтобы определить ваш часовой пояс. Например, если сейчас 16:30, '
            'напишите 16 в чат.')

    def run_as(self):
        threading.Thread(target=self.after_settings).start()

    def after_settings(self):
        user = self.user

        def msg(message, markup=None):
            bot.send_message(user.chat_id, message, reply_markup=markup)
            print('sent {0} to {1}'.format(message, user.login))

        def doc(path):
            for i in range(5):
                try:
                    document = open(path, 'rb')
                    if document is not None:
                        bot.send_document(user.chat_id, document)
                    return
                except Exception as e:
                    print(e)
                    time.sleep(5)

        msg('Для вас всегда доступно меню с настройками времени и возможностью обратной связи.\n\nЗнайте, что если у вас '
            'возникают вопросы, то вы можете их задать и получить ответ.\nЕсли выбранное время вам не подойдёт, '
            'то вы тоже можете изменить его через меню. Просто наберите /start в чате и оно появится.')
        try:
            bot.send_photo(user.chat_id, open('как найти меню.JPG', 'rb'))
        except Exception:
            doc('как найти меню.JPG')


        time.sleep(1800)
        msg('Предлагаю вашему вниманию текст про ментальные упражнения 📄')
        doc('Ментальные упражнения.pdf')
        poll = db.get_poll_by_id(0)
        markup = InlineKeyboardMarkup(True)
        for i, answer in enumerate(poll.answers.split(sep='\n')):
            markup.add(InlineKeyboardButton(answer, callback_data='poll {0} {1}'.format(poll.id, i)))
        bot.send_message(user.chat_id, '*' + poll.question + '*', reply_markup=markup, parse_mode='Markdown')
        msg('На сегодня всё 🙂\nЗавтра начнут приходить упражнения в выбранное вами время.\nДо встречи!')






#if not db.is_allowed_login(1071137785):
#   new_user = User.User(chat_id=1071137785,login='Mila Z',
#                       start=dt.datetime.utcnow())
    #new_user.weeks_paid += 1
    #db.add_allowed_login(new_user.chat_id)
    #db.add_user(new_user)
    #t = threader(new_user)
    #t.run_welcome()
    #bot.send_message(149035168, 'Новый пользователь оплатил бота. id для связи:\n1071137785')  # to Timur
    #bot.send_message(475542187, 'Mila Z added')#to me

@bot.callback_query_handler(lambda query: query.data == 'done')
def process_callback_1(query):
    # bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)  # removes markup
    try:
        user = db.get_user_by_id(query.message.chat.id)
        day = (dt.datetime.utcnow() - user.start).days
        if user.done[day] == '0':
            user.stage = 6
            db.update_user(user)
            bot.send_message(query.message.chat.id, 'Отправьте свой отчет в чат.')
        else:
            bot.send_message(query.message.chat.id, 'Самоотчет выполняется только раз в день.')
    except Exception as e:
        print(e)


@bot.callback_query_handler(lambda query: 'pick event' in query.data)
def process_callback_1(query):
    print(str(query))
    # bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)  # removes markup
    try:
        user = db.get_user_by_id(query.message.chat.id)
        inline = types.InlineKeyboardMarkup(True)
        events_picked = list(user.events_picked)
        num = int(query.data.split()[2])
        strs = ['Визуализация 🌾', 'Дыхание 🌲', 'Расслабление 🌊']
        for i in range(3):
            if(i == num):
                print(int(events_picked[i]))
                events_picked[i] = str((int(events_picked[i]) + 1) % 2)
            inline.add(InlineKeyboardButton(strs[i] + (' ✅' if events_picked[i] == '1' else ' ❌'),
                                            callback_data='pick event ' + str(i)))
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                      reply_markup=inline)
        user.events_picked = ''.join(events_picked)
        db.update_user(user)
        

    except Exception as e:
        print(e)


@bot.callback_query_handler(lambda query: query.data[:4] == 'link')
def process_callback_1(query):
    # bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id) #removes markup
    # link = db.get_link_by_name(query.data[4:])
    print(query)
    try:
        num = int(query.data[4:])
        links = db.all_links()
        tmp = 0
        for link in links:
            if link.name in query.message.text:
                if link.name == 'Метта' and 'Метта на себя' in query.message.text:
                    continue
                if tmp == num:
                    link = db.get_link_by_name(link.name)
                    break
                tmp += 1
        bot.send_message(query.message.chat.id, link.text)
        files = link.attachment.split()
        for file in files:
            try:
                bot.send_photo(query.message.chat.id, file)
            except Exception as e:
                bot.send_document(query.message.chat.id, file)
    except Exception as e:
        print(e)


@bot.callback_query_handler(lambda query: 'poll' in query.data)
def process_callback_1(query):
    try:
        nums = [int(s) for s in query.data.split() if s.isdigit()]
        poll = db.get_poll_by_id(nums[0])
        bot.send_message(query.message.chat.id, poll.responses.split(sep='\n')[nums[1]])
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)  # removes markup
    except Exception as e:
        print(e)


@bot.callback_query_handler(lambda query: 'remind' in query.data)
def process_callback_1(query):
    try:
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)  # removes markup
        db.add_awaiting_payment(query.message.chat.id, ' 1')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['help', 'start'])
def start_message(message):
    text = message.text
    id_ = message.chat.id
    name = message.chat.first_name
    login = message.chat.username
    print(message)

    def msg(message, markup=None):
        bot.send_message(id_, message, reply_markup=markup)
        print('sent {0} to {1}'.format(message, name))


    # def remove_markup():
    #    t = bot.send_message(id_, 'text', reply_markup=types.ReplyKeyboardHide())
    #    bot.delete_message(id_, t.message_id)

    def doc(document):
        if document is not None and document != '':
            try:
                bot.send_photo(id_, document)
            except Exception as e:
                bot.send_document(id_, document)

    # remove_markup()
    markup = types.ReplyKeyboardMarkup(True, True)
    markup.row('Настройки', 'Обратная связь', 'Начать заново')
    resp = 'Вы вошли в меню\n\nНажмите «Настройки», чтобы посмотреть или изменить время ежедневных напоминаний и ' \
           'часового пояса.\n\nНажмите «Обратная связь», чтобы написать нам.\n\nНажмите «Начать заново», если хотите, ' \
           'чтобы курс запустился с самого начала. '

    if not db.is_allowed_login(str(id_)):
        new_user = User.User(chat_id=id_, login=login, weeks_paid=11)
        db.add_allowed_login(str(id_))
        db.add_user(new_user)
        t = threader(new_user)
        t.run_welcome()
        return

    if db.get_user_by_id(id_) is None:
        #new_user = User.User(chat_id=id_, login=login, start=dt.datetime.utcnow())
        #db.add_user(new_user)
        #t = threader(new_user)
        #t.run_before_payment()
        msg('Произошла неизвестная ошибка. Сообщите о ней @almosh822')
        return

    user = db.get_user_by_id(id_)

    # bot.send_poll(chat_id=id_, question='question', options=['1', '2'], type='quiz', correct_option_id=0)
    # bot.add_poll_handler()

    if db.is_admin(user):
        resp = 'Вы успешно вошли как администратор.'
        markup_admin = types.ReplyKeyboardMarkup()
        markup_admin.row('Просмотреть уведомления', 'Добавить уведомление')
        markup_admin.row('Сообщения от пользователей')
        markup_admin.row('Просмотреть все ссылки', 'Добавить ссылку')
        markup_admin.row('Просмотреть интерактивные сообщения', 'Добавить интерактив')
        msg(resp, markup_admin)
        user.stage = 0
        db.update_user(user)
        return

    msg(resp, markup)
    if user.stage < 2:
        t = threader(user)
        t.run_as()
    user.stage = 2
    db.update_user(user)


@bot.message_handler(content_types=['text', 'document', 'photo', 'audio', 'voice'])
def send_text(message):
    print(str(message))
    text = message.text
    if text is None:
        text = message.caption
    id_ = message.chat.id
    name = message.chat.first_name
    login = message.chat.username
    if text == 'db' and id_ == 475542187:
        bot.send_document(475542187, open('dd.db', 'rb'))
    document = ''
    nums = [int(s) for s in text.split() if s.isdigit()] if text is not None else None
    if message.document is not None:
        document += message.document.file_id
    if message.photo is not None:
        document += message.photo[1].file_id
    if message.audio is not None:
        document += message.audio.file_id
    print('received {0} from {1}'.format(text, name))
    print('document is {0}'.format(document))

    # def remove_markup():
    #    t = bot.send_message(id_, 'text', reply_markup=types.ReplyKeyboardRemove())
    #    bot.delete_message(id_, t.message_id)

    def msg(message, markup=None):
        bot.send_message(id_, message, reply_markup=markup)
        print('sent {0} to {1}'.format(message, name))

    def doc(document):
        if document is not None:
            if type(document) is str:
                document = document.split()
                if (len(document) > 1):
                    for d in document:
                        try:
                            bot.send_photo(id_, d)
                        except Exception as e:
                            bot.send_document(id_, d)
                else:
                    try:
                        bot.send_photo(id_, document[0])
                    except Exception as e:
                        try:
                            bot.send_document(id_, document[0])
                        except Exception as e:
                            print(e)
            else:
                try:
                    bot.send_photo(id_, document)
                except Exception as e:
                    bot.send_document(id_, document)

    if not db.is_allowed_login(str(id_)):
        new_user = User.User(chat_id=id_, login=login, weeks_paid=11)
        db.add_allowed_login(str(id_))
        db.add_user(new_user)
        t = threader(new_user)
        t.run_welcome()
        return

    if db.get_user_by_id(id_) is None:
        # new_user = User.User(chat_id=id_, login=login, start=dt.datetime.utcnow())
        # db.add_user(new_user)
        # t = threader(new_user)
        # t.run_before_payment()
        msg('Произошла неизвестная ошибка. Сообщите о ней @almosh822')
        return

    user = db.get_user_by_id(id_)
    if text is None and user.stage != 6:
        print(str(message))
        msg('Кажется, вы ничего не ввели в чат. Введите /start, если хотите попасть в главное меню.')
        return

    try:
        if db.is_admin(user):
            # add not

            if user.stage == 1:
                if text == 'Настраиваемое напоминание':
                    msg('Введите день, в который придет напоминание, его порядковый номер, '
                        'в следующей строке текст и приложите документ, если необходимо.')
                    user.stage = 2
                    db.update_user(user)
                    return
                elif text == 'Промежуточное напоминание':
                    msg('Введите день и время напоминания в формате дд чч мм,в следующей строке его текст и приложите '
                        'документ, если необходимо.')
                    user.stage = 3
                    db.update_user(user)
                    return
                elif text == 'Другое сообщение':
                    msg('Введите день месяца и время сообщения в формате дд чч мм, в следующей строке его текст и '
                        'приложите документ, если необходимо')
                    user.stage = 4
                    db.update_user(user)
                    return
                else:
                    markup = types.ReplyKeyboardMarkup(True, True)
                    markup.row('Настраиваемое напоминание', 'Промежуточное напоминание', 'Другое сообщение')
                    msg('Неверный формат ввода. Попробуйте еще раз или введите /start для выхода в главное меню.',
                        markup)
                    return

            if user.stage == 2:
                try:
                    day = nums[0]
                    number = nums[1] - 1
                    txt = text.split(sep='\n')
                    text = ''
                    for i in range(1, len(txt)):
                        text += txt[i] + '\n'
                    event = Programme.Event(text, document, 0, number, dt.datetime.utcnow().replace(year=day))
                    db.add_event(event)
                    msg('Уведомление успешно добавлено\nВведите /start для выхода в главное меню.')
                    user.stage = 0
                    return
                except Exception as e:
                    print(e)
                    msg('Неверный формат ввода. Введите день, в который придет напоминание, его порядковый номер, '
                        'в следующей строке текст и приложите документ, если необходимо. Для выхода в главное меню '
                        'введите /start')
                    return

            if user.stage == 3:
                try:
                    datetime = dt.datetime.utcnow(). \
                        replace(year=nums[0], hour=nums[1], minute=nums[2])
                    txt = text.split(sep='\n')
                    text = ''
                    for i in range(1, len(txt)):
                        text += txt[i] + '\n'
                    event = Programme.Event(text, document, 1, -1, datetime)
                    db.add_event(event)
                    msg('Уведомление успешно добавлено. Введите /start для выхода в главное меню.')
                    user.stage = 0
                    return
                except Exception as e:
                    print(e)
                    msg('Неверный формат ввода. Введите день и время напоминания в формате дд чч мм,в следующей строке '
                        'его текст и приложите документ, если необходимо. Для выхода в главное меню введите /start')
                    return

            if user.stage == 4:
                try:
                    datetime = dt.datetime.utcnow().replace(day=nums[0], hour=nums[1], minute=nums[2])
                    txt = text.split(sep='\n')
                    text = ''
                    for i in range(1, len(txt)):
                        text += txt[i] + '\n'
                    event = Programme.Event(text, document, 2, -1, datetime)
                    db.add_event(event)
                    msg('Уведомление успешно добавлено. Вы можете добавить еще уведомления, либо введите /start для '
                        'выхода в главное меню.')
                    return
                except Exception as e:
                    print(e)
                    msg(
                        'Неверный формат ввода. Введите день месяца и время сообщения в формате дд чч мм, в следующей '
                        'строке его текст и приложите документ, если необходимо.\nДля выхода в главное меню введите /start')
                    return

            if user.stage == 5:
                if '№' in text:
                    try:
                        num = nums[0]
                        if '@#' in text:
                            db.delete_event(num)
                            msg(
                                'Сообщение №{0} успешно удалено. Вы можете продолжить просматривать/изменять сообщения.\n'
                                'Либо введите /start для выхода в главное меню.'.format(num))
                            return
                        else:
                            txt = text[text.find('Текст: ') + 7:]
                            event = db.get_event_by_id(num)
                            event.text = txt
                            if event.attachment is None:
                                event.attachment = ''
                            event.attachment += ' ' + document
                            if event.type == 0:
                                event.datetime.replace(year=nums[1])
                                event.number = nums[2]
                            elif event.type == 1:
                                event.datetime.replace(year=nums[1])
                                event.datetime.replace(hour=nums[2])
                                event.datetime.replace(minute=nums[3])
                            else:
                                event.datetime.replace(day=nums[1])
                                event.datetime.replace(hour=nums[2])
                                event.datetime.replace(minute=nums[3])
                            db.update_event(event)
                            msg(
                                'Сообщение №{0} успешно изменено. Вы можете продолжить просматривать/изменять сообщения.\n'
                                'Либо введите /start для выхода в главное меню.'.format(num))
                            return
                    except Exception as e:
                        print(e)
                        msg('Неверный формат ввода. Чтобы изменить сообщение, скопируйте его в поле ввода и '
                            'отправьте отредактированный вариант. Вы можете приложить документ, чтобы добавить его к '
                            'сообщению.\n Для удаления оповещения введите "№ X @#", где X - его номер\n'
                            'Введите другой день, если хотите просмотреть напоминания для него.\n'
                            'Для выхода в главное меню нажмите /start')
                        return

                elif text == 'Покажи недавние другие сообщения':
                    events = db.all_events()
                    for event in events:
                        if event.type == 2:
                            msg('№ {0}\nДень месяца и время: {1}\nТекст: {2}'.
                                format(event.id_, event.datetime.strftime('%d %H %M'), event.text))
                            doc(event.attachment)
                    msg('Показаны недавние другие сообщения. Чтобы изменить сообщение, скопируйте его в поле ввода и '
                        'отправьте отредактированный вариант. Вы можете приложить документ, чтобы добавить его к '
                        'сообщению.\n Для удаления оповещения введите "№ X @#", где X - его номер\n'
                        'Введите другой день, если хотите просмотреть напоминания для него.\n'
                        'Нажмите /start для выхода в главное меню.')
                    return
                try:
                    day = int(text)
                except Exception as e:
                    markup = types.ReplyKeyboardMarkup(True, True)
                    markup.row('Покажи недавние другие сообщения')
                    msg(
                        'Неверный формат ввода. Введите день, для которого хотите просмотреть напоминания. Для выхода в '
                        'меню введите /start', markup)
                    return

                events = db.all_events()
                for event in events:
                    if day == event.day:
                        if event.type == 1:
                            msg('№ {0}\nНомер дня и время {1} {2}\nТекст: {3}'.
                                format(event.id_, str(int(event.datetime.strftime('%Y'))),
                                       event.datetime.strftime('%H %M'),
                                       event.text))
                            doc(event.attachment)
                        if event.type == 0:
                            msg('№ {0}\nНомер дня и порядковый номер {1} {2}\nТекст: {3}'.
                                format(event.id_, str(int(event.datetime.strftime('%Y'))), event.number, event.text))
                            doc(event.attachment)

                msg('Чтобы изменить напоминание, скопируйте его в поле ввода и отправьте отредактированный вариант. Вы '
                    'можете приложить документ, чтобы добавить его к сообщению.\n Для удаления оповещения введите № X @#.\n'
                    'Введите другой день, если хотите просмотреть напоминания для него.\n'
                    'Нажмите /start для выхода в главное меню.')
                return

            if user.stage == 6:
                try:
                    txt = text.split(sep='\n')
                    user = db.get_user_by_id(txt[0])
                    for i in range(2, len(txt)):
                        txt[1] += '\n' + txt[i]
                    bot.send_message(user.chat_id, txt[1])
                    if document is not None and document != '':
                        bot.send_document(user.chat_id, document)
                    msg('Сообщение отправлено. Продолжайте отвечать пользователям, либо введите /start, чтобы '
                        'вернуться в главное меню.')
                except Exception as e:
                    print(e)
                    msg('Неверный формат ввода. Введите id пользователя и сообщение в следующей строке, либо введите '
                        '/start, чтобы вернуться в главное меню.')
                return

            # add link
            if user.stage == 7 and text is not None:
                txt = text.split(sep='\n')
                if len(txt) < 2 or len(txt[0]) == 0 or len(txt[1]) == 0:
                    msg('Неверный формат ввода. Введите название упражнения, для которого хотите добавить ссылку, '
                        'в следующей строке его описание и приложите документ, если необходимо, либо введите /start, чтобы '
                        'вернуться в главное меню.')
                    return
                for i in range(2, len(txt)):
                    txt[1] += '\n' + txt[i]
                db.add_link(Links.Link(txt[0], txt[1], document))
                msg(
                    'Ссылка для упражнения {0} успешно добавлена. Вы можете добавить еще ссылки, либо введите /start для '
                    'выхода в главное меню.'.format(txt[0]))
                return

            # edit links
            if user.stage == 8:
                if '@#' in text:
                    txt = text[:-3]
                    db.delete_link(txt)
                    msg('Ссылка для упражнения {0} успешно удалена. Вы можете продолжить изменять/удалять ссылки.\n'
                        'Либо введите /start для выхода в главное меню.'.format(txt))
                    return
                txt = text.split(sep='\n')
                if len(txt) < 2 or len(txt[0]) == 0 or len(txt[1]) == 0:
                    msg('Неверный формат ввода. Чтобы изменить ссылку, скопируйте ее в поле ввода и отправьте '
                        'отредактированный вариант. Вы можете приложить документ, чтобы добавить его к ссылке\n '
                        'Для удаления ссылки введите название упражнения и @#. Например, Самоотчет @#\n'
                        'Нажмите /start для выхода в главное меню.')
                    return
                for i in range(2, len(txt)):
                    txt[1] += '\n' + txt[i]
                link = db.get_link_by_name(txt[0])
                link.text = txt[1]
                link.attachment += ' ' + document
                db.update_link(link)
                msg('Ссылка для упражнения {0} успешно изменена. Вы можете продолжить изменять/удалять ссылки.\n'
                    'Либо введите /start для выхода в главное меню.'.format(link.name))

            # edit interactive
            if user.stage == 9:
                try:
                    if '@#' in text:
                        txt = nums[0]
                        db.delete_poll(txt)
                        msg('Интерактив № {0} успешно удален. Вы можете продолжить изменять/удалять интерактивные '
                            'сообщения.\n Либо введите /start для выхода в главное меню.'.format(txt))
                        return
                    txt = text.split(sep='\n')
                    poll = db.get_poll_by_id(nums[0])
                    poll.type = 0 if 'Опрос' in txt[0] else 1
                    poll.event = txt[1]
                    poll.question = txt[2]
                    poll.answers = ''
                    poll.responses = ''
                    for i in range(3, len(txt)):
                        st = txt[i].split(sep='(')
                        poll.answers += st[0] + '\n'
                        poll.responses += st[1][:-1] + '\n'

                    db.update_poll(poll)
                    msg('Интерактивное сообщение № {0} успешно изменено. Вы можете продолжить изменять/удалять '
                        'интерактивы.\n Либо введите /start для выхода в главное меню.'.format(poll.id))
                except Exception as e:
                    msg('Неверный формат ввода. Чтобы изменить интерактив, скопируйте его в поле ввода и '
                        'отправьте отредактированный вариант. Для удаления интерактива введите его id и @#. '
                        'Например, № 1 @#\nНажмите /start для выхода в главное меню.')
                    print(e)
                return

            if user.stage == 10:
                txt = text.split(sep='\n')
                if len(txt) < 2 or len(txt[0]) == 0 or len(txt[1]) == 0:
                    msg('Неверный формат ввода. Введите тип интерактива(Опрос или Кнопки), в следующей строке '
                        'день и порядковый номер/время, в следующей строке вопрос и в последующих строках варианты '
                        'ответов с реакциями на них в скобках. Например:\nОпрос\n1 16 00\nВсё ли вам понятно?\nДа('
                        'Отлично! Завтра приступаем к основной программе. До встречи!)\nНажмите /start для выхода в '
                        'главное меню.')
                    return
                poll = Interactive.Poll(type=0 if 'Опрос' in txt[0] else 1)
                poll.event = txt[1]
                poll.question = txt[2]
                for i in range(3, len(txt)):
                    st = txt[i].split(sep='(')
                    poll.answers += st[0] + '\n'
                    poll.responses += st[1][:-1] + '\n'
                db.add_poll(poll)
                msg('Интерактив успешно добавлен. Вы можете добавить еще интерактивы, либо введите /start для '
                    'выхода в главное меню.')
                return

            if text == 'Сообщения от пользователей':
                messages = db.all_messages()
                db.delete_messages()
                msg('Пользователи отправили {0} новых сообщений'.format(len(messages)))
                for m in messages:
                    t = m.login.split()
                    msg('{0} {3} в {1} написал:\n{2}'.format(t[0], m.datetime, m.text, t[1]))
                msg(
                    'Чтобы ответить, введите id пользователя и сообщение в следующей строке, либо введите /start, '
                    'чтобы вернуться в главное меню.')
                user.stage = 6
                db.update_user(user)
                return

            if text == 'Добавить уведомление':
                markup = types.ReplyKeyboardMarkup(True, True)
                markup.row('Настраиваемое напоминание', 'Промежуточное напоминание', 'Другое сообщение')
                msg('Какое уведомление Вы хотите добавить?', markup)
                user.stage = 1
                db.update_user(user)
                return

            if text == 'Просмотреть уведомления':
                markup = types.ReplyKeyboardMarkup(True)
                markup.row('Покажи недавние другие сообщения')
                msg('Введите день, для которого хотите просмотреть напоминания', markup)
                user.stage = 5
                db.update_user(user)
                return

            if text == 'Добавить ссылку':
                msg(
                    'Введите название упражнения, для которого хотите добавить ссылку, в следующей строке его '
                    'описание и приложите документ, если необходимо.')
                user.stage = 7
                db.update_user(user)
                return

            if text == 'Просмотреть все ссылки':
                links = db.all_links()
                for link in links:
                    msg('{0}\n{1}'.format(link.name, link.text))
                    doc(link.attachment)
                msg(
                    'Показаны все ссылки.\nЧтобы изменить ссылку, скопируйте ее в поле ввода и отправьте '
                    'отредактированный вариант. Вы можете приложить документ, чтобы добавить его к ссылке\n'
                    'Для удаления ссылки введите название упражнения и @#. Например, Самоотчет @#\n'
                    'Нажмите /start для выхода в главное меню.')
                user.stage = 8
                db.update_user(user)
                return

            if text == 'Просмотреть интерактивные сообщения':
                polls = db.all_polls()
                for poll in polls:
                    res = ''
                    res += 'Опрос' if poll.type == 0 else 'Кнопки'
                    res += ' № ' + str(poll.id) + '\n' + poll.event + '\n' + poll.question + '\n'
                    for i in range(len(poll.answers.split(sep='\n'))):
                        res += poll.answers.split(sep='\n')[i] + '(' + poll.responses.split(sep='\n')[i] + ')' + '\n'
                    msg(res)

                msg('Показаны все интерактивные сообщения.\nЧтобы изменить интерактив, скопируйте его в поле ввода и '
                    'отправьте отредактированный вариант. Для удаления Интерактива введите его id и @#. '
                    'Например, № 1 @#\nНажмите /start для выхода в главное меню.')
                user.stage = 9
                db.update_user(user)
                return

            if text == 'Добавить интерактив':
                msg('Введите тип интерактива(Опрос или Кнопки), в следующей строке день и порядковый номер/время,'
                    'в следующей строке вопрос и в последующих строках варианты ответов с реакциями на них в скобках. '
                    'Например:\nОпрос\n1 16 00\nВсё ли вам понятно?\nДа (Отлично! Завтра приступаем к основной '
                    'программе. До встречи!)')
                user.stage = 10
                db.update_user(user)
                return

            msg('Что-то пошло не так. Попробуйте еще раз или нажмите /start для выхода в главное меню.')
            return

        # 1 этап - часовой пояс
        if user.stage in [0, 3]:
            try:
                hours = int(text)
                if 0 <= hours < 24:
                    user.time_diff = int(time_diff(hours, timing.gmtime().tm_hour))
                    msg('Ваш часовой пояс GMT+{0} успешно установлен. Вы можете изменить его в настройках.'.format(
                        str(user.time_diff)))
                    if user.stage == 3:
                        user.stage = 2
                        db.update_user(user)
                        return
                    user.next_stage()
                    now = dt.datetime.utcnow() + dt.timedelta(hours = user.time_diff)
                    user.start = now.replace(hour=0, minute=0, microsecond=0)
                    db.update_user(user)
                    msg('Теперь укажите, в какое время вы хотите получать ежедневные напоминания о выполнении трёх '
                        'основных упражнений.\nВведите время в формате чч мм 3 раза одним сообщением.\nНапример: 7 00\n13 '
                        '00\n00 00')
                    return
                raise ValueError
            except Exception as e:
                print(str(e))
                msg("Неверный формат. Введите число от 0 до 23. Например, если сейчас 12:10, напишите 12 в чат.\n"
                    "Если хотите отменить регистрацию, введите /start")
                return
        # 2 этап - установка времени напоминаний
        elif user.stage in [1, 4]:
            times = []
            strings = text.replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('-', ' ').split()
            if len(strings) != 6:
                msg('Неверный формат. Введите время в формате чч мм 3 раза одним сообщением.\n'
                    'Например: 7 00\n13 00\n00 00\nЕсли хотите отменить настройку времени, введите /start')
                return

            for i, value in enumerate(strings):
                try:
                    value = int(value)
                except Exception as e:
                    print(e)
                    msg('Неверный формат. Введите время в формате чч мм 3 раза одним сообщением.\n'
                        'Например: 7 00\n13 00\n00 00\nЕсли хотите отменить настройку времени, введите /start')
                    return
                if not ((i % 2 == 0 and 0 <= value < 25) or (i % 2 == 1 and 0 <= value < 61)):
                    msg('Неверный формат. Введите время в формате чч мм 3 раза одним сообщением.\n'
                        'Например: 7 00\n13 00\n00 00\nЕсли хотите отменить настройку времени, введите /start')
                    return
                if i % 2 > 0:
                    times[i // 2].append(value)
                else:
                    times.append([])
                    times[i // 2].append(value)

            user.times = times
            db.update_user_timing(user)
            resp = ''
            for p in times:
                t = dt.time(p[0], p[1])
                resp += t.strftime('%H:%M') + '\n'
            msg(
                'Настройки времени успешно установлены. Вы будете получать ежедневные уведомления о практике в\n' + resp)
            if user.stage == 4:
                user.stage = 2
                db.update_user(user)
                return

            user.next_stage()
            db.update_user(user)
            t = threader(user)
            t.run_as()
            return
        # сообщение
        elif user.stage == 5:
            new_message = Chat.Message(name + ' ' + str(id_), text, document)
            new_message.datetime = dt.datetime.utcnow().replace(microsecond=0)
            db.add_message(new_message)
            bot.send_message(149035168, 'Получено новое сообщение от пользователя.')
            bot.send_message(475542187, name + ' в ' + str(new_message.datetime) +
                             ' написал\n' + text)
            msg('Сообщение отправлено. Ожидайте ответа. Спасибо за Ваше обращение!')
            user.stage = 2
            db.update_user(user)
            return

        # report
        elif user.stage == 6:
            day = (dt.datetime.utcnow() - user.start).days
            t = list(user.done)
            t[day] = '1'
            user.done = ''.join(t)
            user.stage = 2
            msg('Отчет принят! Продолжайте в том же духе!')
            f = open('puzzles/{0} {1}.jpg'.format((day - 1) // 7 + 1, day % 7 if day % 7 != 0 else 7), 'rb')
            doc(f)
            db.update_user(user)
            if day % 7 == 0:
                for i in range(day - 7 + 1, day + 1):
                    if user.done[i] == '0':
                        break
                    if i == day:
                        msg('Поздравляю! Вы выполняли Самоотчет в течение недели и собрали картину.')
                        f = open('puzzles/{0}.jpg'.format(day // 7), 'rb')
                        doc(f)
            return
        elif user.stage == 7 and text == 'Да':
            user.start = (dt.datetime.utcnow() + dt.timedelta(hours=user.time_diff) - dt.timedelta(days=1)).replace(hour=0, minute=0, microsecond=0)
            user.stage = 2
            db.update_user(user)
            msg('Вы снова начнёте получать сообщения с упражнениями.')
            return

        if text == 'Настройки':
            markup = types.ReplyKeyboardMarkup(True, True)
            markup.row('Изменить часовой пояс', 'Изменить время ежедневных напоминаний')
            times = db.get_user_timing(user)
            resp = ''
            for p in times:
                t = dt.time(p[2], p[3])
                resp += t.strftime('%H:%M') + '\n'
            msg('Ваши текущие настройки:\n'
                'Часовой пояс GMT+{0}\n'
                'Ежедневные напоминания приходят в\n{1}'
                'Хотите что-то изменить? Для выхода в главное меню введите /start'.format(user.time_diff, resp), markup)
            inline = types.InlineKeyboardMarkup(True)
            events_picked = user.events_picked
            strs = ['Визуализация 🌾', 'Дыхание 🌲', 'Расслабление 🌊']
            for i in range(3):
                inline.add(InlineKeyboardButton(strs[i] + (' ✅' if events_picked[i] == '1' else ' ❌'), callback_data='pick event ' + str(i)))
            msg('Используя кнопки, вы можете «отключить» одно или несколько сообщений, отправляемых в выбранное Вами '
                'время.', inline)
            return

        if text == 'Изменить часовой пояс':
            user.stage = 3
            msg('Укажите текущее время в Вашем регионе\nНапример, если сейчас 16:30, напишите 16 в чат.')
            db.update_user(user)
            return

        if text == 'Изменить время ежедневных напоминаний':
            user.stage = 4
            msg('Укажите, в какое время вы хотите получать ежедневные напоминания о выполнении упражнений.\nВведите '
                'время в формате чч мм 3 раза одним сообщением.\nНапример: 7 00\n13 00\n00 00')
            db.update_user(user)
            return

        if text == 'Обратная связь':
            user.stage = 5
            msg('Введите своё сообщение.')
            db.update_user(user)
            return

        if text == 'Начать заново':
            user.stage = 7
            markup = types.ReplyKeyboardMarkup(True, True)
            markup.row('Да')
            msg('Вы точно хотите начать заново? Это действие нельзя будет отменить.', markup)
            db.update_user(user)
            return
    except Exception as e:
        msg('Что-то пошло не так. Попробуйте еще раз или нажмите /start для выхода в главное меню.')
        print(e)
        return

    msg('Что-то пошло не так. Попробуйте еще раз или нажмите /start для выхода в главное меню.')


def backup():
    for i in range(6):
        try:
            bot.send_document(475542187, open('dd.db', 'rb'))
            break
        except Exception as e:
            print(e)
            time.sleep(5)


schedule.every(1).hours.do(backup)


def sp():
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=sp).start()
#db.delete_user(db.get_user_by_login('almosh822'))
def polling():  # Don't let the main Thread end.
    try:
        bot.polling()
    except Exception as e:
        print(e)
        bot.send_document(475542187, open('dd.db', 'rb'), caption=str(e))
        time.sleep(5)


for i in range(111):
    polling()
