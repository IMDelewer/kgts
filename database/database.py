from pymongo import MongoClient
from typing import Optional
from data import set_logger

class Database(MongoClient):

    def __init__(
        self, 
        db_name: Optional[str] = None,
        uri: Optional[str] = None, 
        **kwargs
    ):  
        super().__init__(uri, **kwargs)
        self.logger = set_logger(process_name="Database", log_path="data/logs.log")
        self.db_name = db_name
        self.db = self[db_name]
        self.current_collection = None
        
        self.__enter__()

    def use_collection(self, collection_name):
        """Устанавливаем текущую коллекцию."""
        self.current_collection = self.db[collection_name]

    def create_collection(self, collection_name):
        """Создаём новую коллекцию в указанной базе данных."""
        self.db.create_collection(collection_name)

    def drop_collection(self, collection_name):
        """Удаляем коллекцию из указанной базы данных."""
        self.db.drop_collection(collection_name)

    def find(self, query):
        """Находим документы в текущей коллекции по запросу."""
        return self.current_collection.find_one(query)

    def delete(self, query):
        """Удаляем документы из текущей коллекции по запросу."""
        return self.current_collection.delete_many(query)

    def insert(self, data):
        """Вставляем или обновляем документы в текущей коллекции."""
        return self.current_collection.insert_one(data)

    def __enter__(self):
        if self.logger:
            self.logger.info("Connected to MongoDB")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if self.logger:
            self.logger.info("Connection closed")


class User(Database):

    def __init__(
        self,
        username:str,
        user_id:int,
        phone_number:str,
        first_name:str,
        db_name: str | None = None,
        uri: str | None = None,
        **kwargs
    ):

        self._id:int

        self.username: username
        self.user_id: user_id

        self.phone_number = phone_number

        self.first_name = first_name
        self.second_name: str

        self.acces_lvl: int = 0
                
        super().__init__(db_name, uri, **kwargs)



    async def insert(self, data):
        return super().insert(data)