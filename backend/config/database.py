import os
from pymongo import MongoClient
import logging
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    def __init__(self):
        # Use your existing flowmind database
        self.MONGODB_URI = 'mongodb://localhost:27017/'
        self.DATABASE_NAME = 'flowmind'
        self.client = None
        self.db = None
        self.connected = False
    
    def connect(self):
        try:
            self.client = MongoClient(
                self.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.DATABASE_NAME]
            self.connected = True
            logger.info(f"✅ Connected to MongoDB: {self.DATABASE_NAME}")
            return True
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.connected = False
            return False
    
    def get_database(self):
        if not self.connected or self.db is None:
            if not self.connect():
                return None
        return self.db
    
    def get_users_collection(self):
        """Get users collection - returns None if connection fails"""
        try:
            db = self.get_database()
            if db is not None:
                return db.users
            return None
        except Exception as e:
            logger.error(f"❌ Error getting users collection: {e}")
            return None
    
    def is_connected(self):
        if not self.connected or self.client is None:
            return False
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            self.connected = False
            return False

# Global database instance
db_config = DatabaseConfig()