import os
import sqlite3 as sql

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

import Chat
import Links
import User
import telebot
import Programme
import threading
import datetime as dt
import time
import Interactive

# token = "1406324519:AAGIK0HBMNtZ3IfSZ_iiy0PfM6bv8Ngch7c"  # older token
token_lay = "1413164033:AAH0U93n1FtD9H1y6cdMOGNojfzigzsxu2M"
token_dih = "1716180979:AAHlbkPTJ7FBJvT3GgGUadRQy7G3yTtIt7M"

bot = telebot.TeleBot(token_dih)


def commit(cur):
    cur.commit()
    bot.send_document(475542187, open('dd.db', 'rb'), caption='db changed')
    # os.system('git add 3 days db.db')
    # print('bot3 git add')
    # os.system('git commit -am "auto-commit"')
    # print('bot3 git commit')


def msg(user, message):
    markup = InlineKeyboardMarkup(True)
    print('bot3 sending {0} to {1} at {2}'.format(message, user.login, dt.datetime.now()))
    tmp = 0
    for link in links:

        if link.name in message:
            if link.name == 'Метта' and 'Метта на себя' in message:
                continue
            markup.add(InlineKeyboardButton('Описание упражнения {0}'.format(link.name if link.name != 'Трёхминутную '
                                                                                                       'дыхательную '
                                                                                                       'медитацию'
                                                                             else 'Трёхминутная дыхательная '
                                                                                  'медитация'), callback_data='link'
                                                                                                              + str(
                tmp)))
            tmp += 1

    if 'Самоотчёт' in message:
        markup.add(InlineKeyboardButton('📝Отправить самоотчет', callback_data='done'))
    bot.send_message(user.chat_id, message, reply_markup=markup)

    if 'хочу попросить вас оставить отзыв' in message:
        def msg(message, markup=None):
            bot.send_message(user.chat_id, message, reply_markup=markup)
            print('bot3 sent {0} to {1}'.format(message, user.login))

        def doc(path):
            for i in range(5):
                try:
                    document = open(path, 'rb')
                    if document is not None:
                        bot.send_document(user.chat_id, document)
                    return
                except Exception as e:
                    print('bot3' + str(e))
                    time.sleep(5)

        def end():
            time.sleep(10)
            msg('Вы можете и дальше практиковать эти медитации, нажав кнопку «Начать '
                'заново» в меню. Там же можно поменять время медитаций или «выключить» '
                'одну из них. Программа запустится опять на 3 дня. Таким образом вы можете '
                'выстроить свою практику на то количество дней, на которое захотите 🙂')
            time.sleep(5)
            doc('Польза ментальных упражнений.pdf')
            time.sleep(5)
            msg('Ознакомиться с полноценным обучающим курсом медитаций осознанности и самопознания можно '
                'здесь:\nhttps://lookatyourself.turbo.site/')
            doc('О курсе.pdf')

        threading.Thread(target=end).start()
        user.done = '1'
        update_user(user)


def doc(user, documents):
    for d in documents.split():
        try:
            bot.send_photo(user.chat_id, d)
        except Exception as e:
            bot.send_document(user.chat_id, d)


def send(user, event):
    try:
        msg(user, event.text)
    except Exception as e:
        print(e)
        if 'blocked' in str(e):
            delete_user(user)

    if event.attachment is not None:
        doc(user, event.attachment)

    for i, poll in enumerate(polls):
        nums = [int(s) for s in poll.event.split()]
        if nums[0] == event.datetime.year:
            if event.id_ == event_for_poll[poll.id]:
                markup = None
                if poll.type == 1:
                    answers = []
                    for i, answer in enumerate(poll.answers.split(sep='\n')):
                        if len(answers) == 0:
                            answers.append([])
                        # answers[0].append(InlineKeyboardButton(answer, callback_data='poll {0} {1}'.format(poll.id, i)))
                        answers[0].append({'text': answer, 'callback_data': 'poll {0} {1}'.format(poll.id, i)})
                    markup = InlineKeyboardMarkup()
                    markup.keyboard = answers
                else:
                    markup = InlineKeyboardMarkup(True)
                    for i, answer in enumerate(poll.answers.split(sep='\n')):
                        markup.add(InlineKeyboardButton(answer, callback_data='poll {0} {1}'.format(poll.id, i)))
                bot.send_message(user.chat_id, '*' + poll.question + '*', reply_markup=markup, parse_mode='Markdown')

    # print('bot3 send successful')
    # return


users = []
events = []
links = []
polls = []
event_for_poll = []
allowed_logins = []
awaiting_payment = []


def handle_events():
    all_users()
    all_events()
    all_links()
    all_polls()
    all_awaiting_payment()

    def work():
        while True:
            now_server = dt.datetime.utcnow()

            for user in users:
                timing = get_user_timing(user)  # timing = [login, number, hours, minutes]
                now = now_server + dt.timedelta(hours=user.time_diff)
                day = (now - user.start).days

                for event in events:
                    event_time = event.datetime
                    # print(now.hour, event_time.hour, now.minute, event_time.minute)
                    if event.type == 0 and user.events_picked[event.number] == '1':
                        if len(timing) > event.number and timing[event.number][2] == now.hour and now.minute == \
                                timing[event.number][3] \
                                and ((day == event_time.year and now.hour >= timing[0][2]) or (
                                day == event_time.year + 1 and now.hour < timing[0][2])):
                            send(user, event)
                            # print('bot3 sent ok')

                    elif event.type == 1:
                        if day == 4 and user.done == '1':  # end msgs sent before
                            continue
                        if day == event_time.year and now.hour == event_time.hour \
                                and now.minute == event_time.minute:
                            send(user, event)

                    else:
                        # print(now.day, event_time.day, now.hour, event_time.hour, now.minute, event_time.minute)
                        if now.day == event_time.day and now.hour == event_time.hour \
                                and now.minute == event_time.minute:
                            send(user, event)
            time.sleep(60)

    def repeat_work():
        try:
            work()
        except Exception as e:
            print('bot3 ' + str(e))
            time.sleep(60)
            repeat_work()

    repeat_work()


def del_files():
    all_links()
    for link in links:
        link.attachment = ''
        update_link(link)
        print(link.text)
    all_events()
    for event in events:
        event.attachment = ''
        update_event(event)


def init():
    # del_files()
    thread = threading.Thread(target=handle_events)
    thread.start()
    # del_files()


def add_users_timing(user):  # times = [[hour, minute]]
    con = sql.connect('dd.db')
    cur = con.cursor()
    for i, time in enumerate(user.times):
        cur.execute('INSERT INTO users_timings(login, number, hours, minutes) VALUES(?, ?, ?, ?)',
                    [user.chat_id, i, time[0], time[1]])
    for i, u in enumerate(users):
        if u.chat_id == user.chat_id:
            users[i] = user

    commit(con)


def update_user_timing(user):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('DELETE FROM users_timings WHERE login = ?', [str(user.chat_id)])
    commit(con)
    add_users_timing(user)


def get_user_timing(user):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users_timings WHERE login = ?", [str(user.chat_id)])
    rows = cur.fetchall()
    rows.sort(key=lambda x: x[1])
    return rows


def add_allowed_login(login):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('INSERT INTO allowed_logins(login) VALUES(?)', [login])
    commit(con)
    allowed_logins.append(login)


def get_allowed_logins():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM allowed_logins")
    rows = cur.fetchall()
    allowed_logins = [str(row[0]) for row in rows]
    return allowed_logins


def is_allowed_login(login):
    allowed_users = get_allowed_logins()
    return login in allowed_users


def get_user_by_login(login):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE login = ?", [login])
    rows = cur.fetchall()
    if (len(rows) == 0):
        return None
    row = rows[0]
    user = User.from_list(row)
    cur.execute("SELECT * FROM reports WHERE login = ?", [str(user.chat_id)])
    rows = cur.fetchall()
    if len(rows) == 0:
        return user
    row = rows[0]
    user.done = row[1]
    return user


def get_user_by_id(id_):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE chat_id = ?", [id_])
    rows = cur.fetchall()
    if (len(rows) == 0):
        return None
    row = rows[0]
    user = User.from_list(row)
    cur.execute("SELECT * FROM reports WHERE login = ?", [str(user.chat_id)])
    rows = cur.fetchall()
    if len(rows) == 0:
        return user
    row = rows[0]
    user.done = row[1]
    return user


def add_user(user):
    con = sql.connect('dd.db')
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO users(time_diff, chat_id, login, stage, start, weeks_paid, events_picked) VALUES(?, ?, ?, ?, ?, ?, ?)",
            user.list())
        cur.execute("INSERT INTO reports(login, done) VALUES(?, ?)",
                    [str(user.chat_id), user.done])
    except Exception as e:
        print('bot3 ' + str(e))
    commit(con)
    users.append(user)
    update_user_timing(user)


def delete_user(user):
    con = sql.connect('dd.db')
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM users WHERE chat_id = ?", [user.chat_id])
        cur.execute("DELETE FROM reports WHERE login = ?",
                    [str(user.chat_id)])
    except Exception as e:
        print('bot3 ' + str(e))
    commit(con)


def update_user(user):
    con = sql.connect('dd.db')
    cur = con.cursor()
    args = user.list()
    args.append(str(user.chat_id))
    cur.execute('UPDATE users SET time_diff = ?, chat_id = ?, login = ?, stage = ?, start = ?, weeks_paid = ?, '
                'events_picked = ? WHERE chat_id = ?', args)
    cur.execute('UPDATE reports SET done = ? WHERE login = ?',
                [user.done, str(user.chat_id)])
    commit(con)
    for i, u in enumerate(users):
        if u.chat_id == user.chat_id:
            users[i] = user


def all_users():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    users.clear()
    for row in rows:
        users.append(User.from_list(row))


def add_link(link):
    con = sql.connect('dd.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO links(name, text, attachment) VALUES(?, ?, ?)",
                    link.list())
        commit(con)
        links.append(link)
    except Exception as e:
        print('bot3 adding link({0}, {1}) failed due to {2}'.format(link.name, link.text, e))


def update_link(link):
    con = sql.connect('dd.db')
    cur = con.cursor()
    args = link.list()
    args.append(link.name)
    cur.execute('UPDATE links SET name = ?, text = ?, attachment = ? WHERE name = ?',
                args)
    commit(con)
    for i, l in enumerate(links):
        if l.name == link.name:
            links[i] = link


def all_links():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM links')
    rows = cur.fetchall()
    links.clear()
    for row in rows:
        links.append(Links.from_list(row))
    return links


def get_link_by_name(name):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM links WHERE name = ?', [name])
    rows = cur.fetchall()
    try:
        return Links.from_list(rows[0])
    except Exception as e:
        print('bot3 selecting link {0} failed due to {1}'.format(name, e))


def delete_link(name):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("DELETE FROM links WHERE name = ?",
                [name])
    commit(con)
    for i, l in enumerate(links):
        if l.name == name:
            links.remove(l)


def add_event(event):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO events(text, attachment, type, datetime, number) VALUES(?, ?, ?, ?, ?)",
                event.fresh_list())
    event.id_ = cur.lastrowid
    commit(con)
    events.append(event)


def add_test_event(event):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO test_events(text, attachment, type, datetime, number) VALUES(?, ?, ?, ?, ?)",
                event.fresh_list())
    commit(con)


def delete_event(id_):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("DELETE FROM events WHERE id = ?",
                [id_])
    commit(con)
    for i, e in enumerate(events):
        if e.id_ == id_:
            events.remove(e)


def all_events():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM events')
    rows = cur.fetchall()
    events.clear()
    for row in rows:
        events.append(Programme.from_list(row))
    return events


def get_event_by_id(id_):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM events WHERE id = ?', [id_])
    rows = cur.fetchall()
    return Programme.from_list(rows[0])


def update_event(event):
    con = sql.connect('dd.db')
    cur = con.cursor()
    args = event.list()
    cur.execute('UPDATE events SET text = ?, attachment = ?, type = ?, datetime = ?, number = ? WHERE id = ?',
                args)
    commit(con)
    for i, e in enumerate(events):
        if e.id_ == event.id_:
            events[i] = event


def add_admin(login):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('INSERT INTO admins(login) VALUES(?)', [login])
    commit(con)


def get_admins():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM admins")
    rows = cur.fetchall()
    result = [row[0] for row in rows]
    return result


def is_admin(user):
    admins = get_admins()
    return user.login in admins


def add_message(message):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO messages(login, text, attachment, datetime) VALUES(?, ?, ?, ?)",
                message.list())
    commit(con)


def all_messages():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM messages')
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append(Chat.from_list(row))
    return result


def delete_messages():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('DELETE FROM messages')
    commit(con)


def map_poll_to_event(poll):
    nums = [int(s) for s in poll.event.split()]
    while len(event_for_poll) < poll.id + 1:
        event_for_poll.append(0)
    for event in events:
        if nums[0] == event.datetime.year:
            if (len(nums) == 2 and event.type == 0 and nums[1] == event.number) or \
                    (len(nums) == 3 and event.type == 1 and nums[1] == event.datetime.hour and nums[
                        2] == event.datetime.minute):
                event_for_poll[poll.id] = event.id_


def all_polls():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM polls')
    rows = cur.fetchall()
    polls.clear()
    for row in rows:
        poll = Interactive.from_list(row)
        polls.append(poll)
        map_poll_to_event(poll)

    return polls


def delete_poll(id_):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("DELETE FROM polls WHERE id = ?", [id_])
    commit(con)
    for i, e in enumerate(polls):
        if e.id == id_:
            polls.remove(e)


def get_poll_by_id(id_):
    all_polls()
    for poll in polls:
        if poll.id == id_:
            return poll


def update_poll(poll):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('UPDATE polls SET event = ?, question = ?, type = ?, answers = ?, responses = ? WHERE id = ?',
                poll.list())
    commit(con)

    for i, e in enumerate(polls):
        if e.id == poll.id:
            polls[i] = poll
    map_poll_to_event(poll)


def add_poll(poll):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute('INSERT INTO polls(event, question, type, answers, responses) VALUES (?, ?, ?, ?, ?)',
                poll.list_to_add())
    poll.id = cur.lastrowid
    commit(con)
    polls.append(poll)
    map_poll_to_event(poll)


def add_awaiting_payment(id_, type):  # type = ' 0/1'
    try:
        con = sql.connect('dd.db')
        cur = con.cursor()
        id_ = str(id_) + type
        now = dt.datetime.utcnow().replace(hour=0, minute=0, microsecond=0)
        for ap in awaiting_payment:
            if ap[0] == id_:
                return
        cur.execute('INSERT INTO awaiting_payment(chat_id, date) VALUES (?, ?)',
                    [id_, now])
        commit(con)
        awaiting_payment.append([id_, now])
    except Exception as e:
        print(str(e) + '\nin add_awaiting_payment bot3')


def delete_awaiting_payment(ap):
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("DELETE FROM awaiting_payment WHERE chat_id = ?", [ap[0]])
    commit(con)
    awaiting_payment.remove(ap)


def all_awaiting_payment():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM awaiting_payment")
    rows = cur.fetchall()
    awaiting_payment.clear()
    for row in rows:
        awaiting_payment.append([row[0], dt.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')])

def count_relaunch():
    con = sql.connect('dd.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM stats")
    current = int(cur.fetchall()[0][0])
    cur.execute("UPDATE stats SET relaunches = ? WHERE relaunches = ?", [current + 1, current])