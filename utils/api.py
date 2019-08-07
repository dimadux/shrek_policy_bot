from utils.db import DB
from telebot import TeleBot
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
                self.process(update)

    def check_bad_word(self, update):
        chat_id = update.message.json.get("chat", {}).get("id")
        message_id = update.message.json.get("message_id")
        text = update.message.json.get("text", "")
        tokens = re.split(r"[?,.!\s\n]", text.lower())
        for token in tokens:
            if self.db.get_bad_word(token):
                self.bot.send_sticker(chat_id=chat_id, reply_to_message_id=message_id,
                                      data=self.db.get_shrek())
            break

    def check_register(self, update):
        pass

    def check_unregister(self, update):
        pass

    def check_stats(self, update):
        pass

    def process(self, update):
        self.check_bad_word(update)
        self.check_register(update)
        self.check_unregister(update)
        self.check_stats()