import os
import sqlite3 as sql

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import Chat
import Links
import User
import telebot
import Programme
import threading
import datetime as dt
import time

#token = "1406324519:AAGIK0HBMNtZ3IfSZ_iiy0PfM6bv8Ngch7c" #older token
token = "1413164033:AAH0U93n1FtD9H1y6cdMOGNojfzigzsxu2M"

bot = telebot.TeleBot(token)
#os.system('git init')
#os.system('git config --global user.email mr.almosh443@mail.ru')
#os.system('git config --global user.name almosh443')
#print('git inited')

def commit(cur):
    cur.commit()
    #os.system('git add test.db')
    #print('git add')
    #os.system('git commit -am "auto-commit"')
    #print('git commit')

def msg(user, message):
    all_links()
    markup = InlineKeyboardMarkup(True)
    print('sending {0} to {1} at {2}'.format(message, user.login, dt.datetime.now()))
    tmp = 0
    for link in links:

        if link.name in message:
            if link.name == 'Метта' and 'Метта на себя' in message:
                continue
            markup.add(InlineKeyboardButton('Описание упражнения {0}'.format(link.name), callback_data='link' + str(tmp)))
            tmp += 1
    if 'Самоотчёт' in message:
        markup.add(InlineKeyboardButton('📝Отправить самоотчет', callback_data='done'))
    bot.send_message(user.chat_id, message, reply_markup=markup)


def doc(user, documents):
    for d in documents.split():
        try:
            bot.send_photo(user.chat_id, d)
        except Exception as e:
            bot.send_document(user.chat_id, d)


def send(user, event):
    msg(user, event.text)
    if event.attachment is not None:
        doc(user, event.attachment)


users = []
events = []
links = []


def handle_events():
    all_users()
    all_events()
    all_links()
    while True:
        now_server = dt.datetime.utcnow()
        for user in users:
            timing = get_user_timing(user)  # timing = [login, number, hours, minutes]
            now = now_server.replace(hour=(now_server.hour + user.time_diff) % 24)
            day = (now - user.start).days
            for event in events:
                event_time = event.datetime
                # print(now.hour, event_time.hour, now.minute, event_time.minute)
                if event.type == 0:
                    if day == event_time.year and len(timing) > event.number and \
                            timing[event.number][2] == now.hour and now.minute == timing[event.number][3]:
                        send(user, event)

                elif event.type == 1:
                    if day == event_time.year and now.hour == event_time.hour \
                            and now.minute == event_time.minute:
                        send(user, event)

                else:
                    # print(now.day, event_time.day, now.hour, event_time.hour, now.minute, event_time.minute)
                    if now.day == event_time.day and now.hour == event_time.hour \
                            and now.minute == event_time.minute:
                        send(user, event)
        time.sleep(60)

def del_files():
    all_links()
    for link in links:
        link.attachment = ''
        update_link(link)
        print(link.text)

def init():

    thread = threading.Thread(target=handle_events)
    thread.start()
    #del_files()


def add_users_timing(user):  # times = [[hour, minute]]
    con = sql.connect('test.db')
    cur = con.cursor()
    for i, time in enumerate(user.times):
        cur.execute('INSERT INTO users_timings(login, number, hours, minutes) VALUES(?, ?, ?, ?)',
                    [user.chat_id, i, time[0], time[1]])
    for i, u in enumerate(users):
        if u.chat_id == user.chat_id:
            users[i] = user

    commit(con)


def update_user_timing(user):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('DELETE FROM users_timings WHERE login = ?', [str(user.chat_id)])
    commit(con)
    add_users_timing(user)


def get_user_timing(user):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users_timings WHERE login = ?", [str(user.chat_id)])
    rows = cur.fetchall()
    rows.sort(key=lambda x: x[1])
    return rows


def add_allowed_login(login):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('INSERT INTO allowed_logins(login) VALUES(?)', [login])
    commit(con)


def get_allowed_logins():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM allowed_logins")
    rows = cur.fetchall()
    result = [row[0] for row in rows]
    return result


def is_allowed_login(login):
    allowed_users = get_allowed_logins()
    return login in allowed_users


def get_user_by_login(login):
    con = sql.connect('test.db')
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
    con = sql.connect('test.db')
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
    con = sql.connect('test.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users(time_diff, chat_id, login, stage, start) VALUES(?, ?, ?, ?, ?)",
                    user.list())
        cur.execute("INSERT INTO reports(login, done) VALUES(?, ?)",
                    [str(user.chat_id), user.done])
    except Exception as e:
        print(e)
    commit(con)
    users.append(user)
    update_user_timing(user)


def update_user(user):
    con = sql.connect('test.db')
    cur = con.cursor()
    args = user.list()
    args.append(str(user.chat_id))
    cur.execute('UPDATE users SET time_diff = ?, chat_id = ?, login = ?, stage = ?, start = ? WHERE chat_id = ?',
                args)
    cur.execute('UPDATE reports SET done = ? WHERE login = ?',
                [user.done, str(user.chat_id)])
    commit(con)
    for i, u in enumerate(users):
        if u.chat_id == user.chat_id:
            users[i] = user


def all_users():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    users.clear()
    for row in rows:
        users.append(User.from_list(row))


def add_link(link):
    con = sql.connect('test.db')
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO links(name, text, attachment) VALUES(?, ?, ?)",
                link.list())
        commit(con)
        links.append(link)
    except Exception as e:
        print('adding link({0}, {1}) failed due to {2}'.format(link.name, link.text, e))


def update_link(link):
    con = sql.connect('test.db')
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
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM links')
    rows = cur.fetchall()
    links.clear()
    for row in rows:
        links.append(Links.from_list(row))
    return links


def get_link_by_name(name):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM links WHERE name = ?', [name])
    rows = cur.fetchall()
    try:
        return Links.from_list(rows[0])
    except Exception as e:
        print('selecting link {0} failed due to {1}'.format(name, e))


def delete_link(name):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("DELETE FROM links WHERE name = ?",
                [name])
    commit(con)
    for i, l in enumerate(links):
        if l.name == name:
            links.remove(l)


def add_event(event):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("INSERT INTO events(text, attachment, type, datetime, number) VALUES(?, ?, ?, ?, ?)",
                event.fresh_list())
    commit(con)
    events.append(event)


def add_test_event(event):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("INSERT INTO test_events(text, attachment, type, datetime, number) VALUES(?, ?, ?, ?, ?)",
                event.fresh_list())
    commit(con)


def delete_event(id_):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("DELETE FROM events WHERE id = ?",
                [id_])
    commit(con)
    for i, e in enumerate(events):
        if e.id_ == id_:
            events.remove(e)


def all_events():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM events')
    rows = cur.fetchall()
    events.clear()
    for row in rows:
        events.append(Programme.from_list(row))
    return events


def get_event_by_id(id_):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM events WHERE id = ?', [id_])
    rows = cur.fetchall()
    return Programme.from_list(rows[0])


def update_event(event):
    con = sql.connect('test.db')
    cur = con.cursor()
    args = event.list()
    cur.execute('UPDATE events SET text = ?, attachment = ?, type = ?, datetime = ?, number = ? WHERE id = ?',
                args)
    commit(con)
    for i, e in enumerate(events):
        if e.id_ == event.id_:
            events[i] = event


def add_admin(login):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('INSERT INTO admins(login) VALUES(?)', [login])
    commit(con)


def get_admins():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM admins")
    rows = cur.fetchall()
    result = [row[0] for row in rows]
    return result


def is_admin(user):
    admins = get_admins()
    return user.login in admins


def add_message(message):
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute("INSERT INTO messages(login, text, attachment, datetime) VALUES(?, ?, ?, ?)",
                message.list())
    commit(con)


def all_messages():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM messages')
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append(Chat.from_list(row))
    return result


def delete_messages():
    con = sql.connect('test.db')
    cur = con.cursor()
    cur.execute('DELETE FROM messages')
    commit(con)
