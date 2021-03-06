import json
import requests
import time
import urllib
from dbhelper import DBHelper

TOKEN = "330022198:AAGBcFDf19unG_oR8QLrZjAN14Z6ffgqBkg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
        return max(update_ids)


# def echo_all(updates):
#     for update in updates['result']:
#         try:
#             text = update['message']['text']
#             chat = update['message']['chat']['id']
#             send_message(text, chat)
#         except Exception as e:
#             print(e)

def handle_updates(updates):
    for update in updates['result']:
        text = update['message']['text']
        chat = update['message']['chat']['id']
        assignments = db.get_assignments(chat)
        if text == '/done':
            keyboard = build_keyboard(assignments)
            send_message('Which assignment did you complete?', chat, keyboard)
        elif text == "/start":
            send_message(
                "Welcome to your personal Homework list. Send any text to me "
                "and I'll store it as an assignment. Send /done to remove "
                "assignments.",
                chat)
        elif text.startswith("/"):
            continue
        elif text in assignments:
            db.delete_assignment(text, chat)
            assignments = db.get_assignments(chat)
            keyboard = build_keyboard(assignments)
            send_message('Which assignment did you complete?', chat, keyboard)
        else:
            db.add_assignment(text, chat)
            assignments = db.get_assignments(chat)
            message = '\n'.join(assignments)
            send_message(message, chat)


def build_keyboard(assignments):
    keyboard = [[assignment] for assignment in assignments]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(
        text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
