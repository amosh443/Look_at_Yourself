import datetime
import time
import datetime as dt
import types
import telebot

import requests

import User

token = "1256909898:AAF9zQKjvXmaZ3L7HIBJ4P1AvTMMYw7dvIQ"

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

now = datetime.datetime.now()

bot = BotHandler(token)

def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        last_chat_login = last_update['message']['chat']['username']

        def msg(message):
            bot.send_message(last_chat_id, message)

        if not User.is_allowed(last_chat_login):
            msg("У Вас нет доступа к этому чату.")
            new_offset = last_update_id + 1
            continue

        if User.get_user_by_login(last_chat_login) == None: #register new user
            msg('Для начала работы введите информацию о себе')
            msg('Укажите текущее время\nНапример, если сейчас 16:30, напишите 16 в чат')


        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    main()