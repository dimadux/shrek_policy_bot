from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from utils.errors import CollectionNotFound


class DB:
    def __init__(self, db_config):
        self._mc = MongoClient(**db_config["auth"])
        self._collections = db_config["collections"]
        self._db = db_config["database"]

    def _get_coll(self, coll_name):
        try:
            return self._mc[self._db][self._collections[coll_name]]
        except KeyError:
            raise CollectionNotFound(coll_name)

    def _get_record(self, coll_name, _id):
        return self._get_coll(coll_name).find_one(_id)

    def _find(self, coll_name, filter, projection=None):
        return self._get_coll(coll_name).find(filter, projection)

    def _insert_doc(self, coll_name, doc):
        return self._get_coll(coll_name).insert_one(doc).inserted_id

    def _update_doc(self, coll_name, doc):
        _id = doc.pop("_id")
        return self._get_coll(coll_name).update_one(
            {"_id":_id},
            {"$set":doc}
        )

    def get_bad_word(self, bad_word):
        bad_word = bad_word.lower()
        item = self._get_record("bad_words", bad_word)
        if item and item.get("confidence", 0) >= 0.5:
            return True

    def insert_bad_word(self, bad_word):
        bad_word = bad_word.lower()
        item = self._get_record("bad_words", bad_word)
        if item:
            confidence = item.get("confidence", 0)
            confidence = confidence + 0.1
            item["confidence"] = confidence
            self._update_doc("bad_words", item)
        else:
            item = {
                "_id": bad_word,
                "confidence": 0.4
            }
            self._insert_doc("bad_words", item)

    def insert_chat(self, chat_doc):
        chat_doc["_id"] = chat_doc["id"]
        del chat_doc["id"]
        try:
            return self._insert_doc("chats",chat_doc)
        except DuplicateKeyError:
            return {
                "ok":0,
                "error": "Chat already exists"
            }

    def get_shrek(self):
        return self._get_coll("stickers").find_one({"type": "shrek_policy"})["_id"]

    def add_token_to_user(self, user_id, token):
        user_tokens = self._get_record("users", user_id).get("tokens", [])
        user_tokens = user_tokens + token
        self._get_coll("users").update_one({"_id":user_id}, {"$set": {
            "tokens":user_tokens
        }})

    def insert_user(self, user):
        user["_id"] = user["id"]
        del user["id"]
        try:
            return self._insert_doc("users", user)
        except DuplicateKeyError:
            return {
                "ok":0,
                "error":"User exists"
            }

    def update_bad_word(self, bad_word, user_id):
        user_info = self._get_record("users", user_id)
        registered_words = user_info.get("registered_words", [])
        if bad_word in registered_words:
            return f"Вы уже добавляли слово {bad_word} в список плохих"
        else:
            registered_words.append(bad_word)
            self._get_coll("users").update_one({"_id": user_id}, {"$set": {"registered_words": registered_words}})
            return f"Слово {bad_word} успешно обновлено в списке плохих слов"