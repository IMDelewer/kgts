from pymongo import MongoClient
from typing import Optional
from data import set_logger

class Database:
    
    def __init__(
        self, 
        db_name: str, 
        uri: Optional[str], 
        **kwargs
    ):  
        self.client = MongoClient(uri, **kwargs)
        self.logger = set_logger(process_name="Database", log_path="data/logs.log")
        self.db = self.client[db_name]
        self.current_collection = None
        self.logger.info(f"Connected to database: {db_name}")

    def use_collection(self, collection_name: str):
        """Устанавливаем текущую коллекцию."""
        self.current_collection = self.db[collection_name]
        self.logger.info(f"Using collection: {collection_name}")
    
    def create_collection(self, collection_name: str):
        """Создаем новую коллекцию."""
        try:
            self.db.create_collection(collection_name)
            self.logger.info(f"Collection '{collection_name}' created successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create collection '{collection_name}': {e}")

    def drop_collection(self, collection_name: str):
        """Удаляем коллекцию."""
        try:
            self.db.drop_collection(collection_name)
            self.logger.info(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            self.logger.error(f"Failed to drop collection '{collection_name}': {e}")
    
    def find(self, query: dict):
        """Ищем все документы в коллекции, соответствующие запросу."""
        try:
            result = self.current_collection.find(query)
            self.logger.info(f"Found documents matching query: {query}")
            return result
        except Exception as e:
            self.logger.error(f"Error finding documents with query {query}: {e}")
            return

    def insert(self, document: dict):
        """Вставляем документ в коллекцию."""
        try:
            result = self.current_collection.insert_one(document)
            self.logger.info(f"Inserted document with _id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")
            return None

    def update(self, filter: dict, update: dict, many: bool = False):
        """Обновляем документы по фильтру. Если many=True, обновляем несколько документов, иначе один."""
        try:
            if many:
                result = self.current_collection.update_many(filter, {"$set": update})
            else:
                result = self.current_collection.update_one(filter, {"$set": update})
            
            self.logger.info(f"Updated {result.modified_count} documents matching filter: {filter}")
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update documents: {e}")
            return 0

    
    def delete(self, query: dict):
        """Удаляем документы по запросу."""
        try:
            result = self.current_collection.delete_many(query)
            self.logger.info(f"Deleted {result.deleted_count} documents matching query: {query}")
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete documents: {e}")
            return 0

    def close_connection(self):
        """Закрываем соединение с MongoDB."""
        try:
            self.client.close()
            self.logger.info("MongoDB connection closed.")
        except Exception as e:
            self.logger.error(f"Failed to close MongoDB connection: {e}")
