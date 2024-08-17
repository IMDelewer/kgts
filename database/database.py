from pymongo import MongoClient
from typing import Optional, Dict, Any, List
from data import set_logger, Config

from .models import *
from json import dumps

class Database:

    def __init__(self, current_collection, **kwargs): 
        self.logger = set_logger(process_name="Database", log_path="data/logs.log")
        client = MongoClient(Config.url)
        self.db = client[Config.db_name]
        self.current_collection = self.db[current_collection]
    

    def find(self, filter, value, collection):
        
        db = self.db[collection].find_one({filter:value})
        
        return db   

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
        collection: str,
        username: str,
        user_id: int,
        first_name: str,
        second_name: str,
        access_lvl: Optional[int] = None,
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
        
        if not db.find_one({"user_id": self.user_id}):
            base = NewUser(
                username=self.username,
                user_id=self.user_id,
                first_name=self.first_name,
                second_name=self.second_name,
            )

            dump_base = base.model_dump()

            if self.access_lvl is not None:      
                dump_base['access_lvl'] = self.access_lvl
            
            user = db.insert_one(dump_base)

            return user
        else:
            pass

    async def delete(self, query: Dict[str, Any]):
        db = self.db[self.collection]

        user = db.delete_many(query)

        return user

    async def update(self, query: Dict[str, Any], new_data: Dict[str, Any]):
        db = self.db[self.collection]

        user = db.update_one(query, {'$set': new_data})

        return user

    async def find(self, query):
        db = self.db[self.collection]

        user = db.find_one(query)

        return user
    
class Support(Database):

    def __init__(
        self,
        collection: str,
        request: str,
        status: str,
        support_name: str,
        userid: int,
        operid: int,
        rate: int,
        cancels: int,
        cancel_ids: list[int],
        **kwargs
    ):
        self.collection = collection
        self.request = request
        self.status = status
        self.support_name = support_name
        self.userid = userid
        self.operid = operid
        self.rate = rate
        self.cancels = cancels
        self.cancel_ids = cancel_ids
        super().__init__(current_collection=collection, **kwargs)

    async def insert(self):
        db = self.db[self.collection]
        
        base = NewSupport(
            request=self.request,
            status=self.status,
            support_name=self.support_name,
            userid=self.userid,
            operid=self.operid,
            rate=self.rate,
            cancels=self.cancels
        )

        dump_base = base.model_dump()
            
        support = db.insert_one(dump_base)

        return support  

    async def delete(self, query: Dict[str, Any]):
        db = self.db[self.collection]

        support = db.delete_many(query)

        return support

    async def update(self, query: Dict[str, Any], new_data: Dict[str, Any]):
        db = self.db[self.collection]

        support = db.update_one(query, {'$set': new_data})

        return support
    
    async def find(self, query):
        db = self.db[self.collection]

        support = db.find_one(query)

        return support