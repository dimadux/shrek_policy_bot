
class CollectionNotFound(Exception):
    def __init__(self, coll_name):
        message = f"Collection {coll_name} not found in db"
        super().__init__(message)