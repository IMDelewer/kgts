from pymongo import MongoClient
from typing import Optional
from data import set_logger, Config

from .models import NewUser
from json import dumps

class Database():

    def __init__(self, current_collection, **kwargs): 

        self.logger = set_logger(process_name="Database", log_path="data/logs.log")

        client = MongoClient(Config.url)
    
        self.db = client[Config.db_name]

        self.current_collection = current_collection
    

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
        collection:str,
        username:str,
        user_id:int,
        first_name:str,
        second_name:str,
        access_lvl:int | None = None,
        **kwargs
    ):

        self.collection = collection

        self.username = username
        self.user_id = user_id

        self.first_name = first_name
        self.second_name = second_name

        self.access_lvl = access_lvl
                
        super().__init__(current_collection=collection, **kwargs)



    async def insert(self):

        db = self.db[self.collection]
        
        if not db.find_one({"userid": self.user_id}):

            
            base = NewUser(
                username = self.username,
                user_id = self.user_id,
                first_name = self.first_name,
                second_name = self.second_name,
            )

            dump_base = base.model_dump()

            if self.access_lvl != None:      
                dump_base['access_lvl'] = self.access_lvl
            
            db.insert_one(dump_base)
        else:
            pass