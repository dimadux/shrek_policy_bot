from utils.db import DB
from telebot import TeleBot
from copy import deepcopy
import re

class Api:

    def __init__(self, config):
        self.db = DB(config["mongo"])
        self.bot = TeleBot(token=config["token"])
        self.event_loop()


    def event_loop(self):
        updated_ids = set([r.update_id for r in self.bot.get_updates()])
        while True:
            updates = self.bot.get_updates(offset=max(updated_ids))
            for update in updates:
                if update.update_id in updated_ids:
                    continue
                else:
                    updated_ids.add(update.update_id)
                self.process(update.message.json)

    def check_bad_word(self, update):
        update = deepcopy(update)
        chat = update.get("chat")
        chat_id = chat.get("id")
        self.save_chat(chat)
        message_id = update.get("message_id")
        text = update.get("text", "")
        user = update.get("from")
        self.save_user(user)
        tokens = re.split(r"[?,.!\s\n]", text.lower())
        for token in tokens:
            if self.db.get_bad_word(token):
                self.user_report(user.get("id"), token)
                self.bot.send_sticker(chat_id=chat_id, reply_to_message_id=message_id,
                                      data=self.db.get_shrek())
            break

    def save_user(self, user):
        self.db.insert_user(user)

    def save_chat(self, chat):
        self.db.insert_chat(chat)

    def user_report(self, user_id, token):
        self.db.add_token_to_user(user_id, token)


    def check_register(self, update):
        text = update.get("text")
        chat_id = update.get("chat").get("id")
        user = update.get("from").get("id")
        if "/register" in text:
            tokens = re.split(r"[,.\n\s!]", text)
            tokens = [i for i in tokens if len(i) > 2 and i not in "/register"]
            if not len(tokens) == 1:
                self.bot.send_message(chat_id=chat_id, text="Должно быть только одно слово длины > 2")
            else:
                message = self.db.update_bad_word(tokens[0], user)
                self.bot.send_message(chat_id=chat_id, text=message)

    def check_unregister(self, update):
        pass

    def check_stats(self, update):
        pass

    def process(self, update):
        self.check_bad_word(deepcopy(update))
        self.check_register(deepcopy(update))
        self.check_unregister(deepcopy(update))
        self.check_stats(deepcopy(update))