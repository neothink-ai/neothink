from pymongo import MongoClient
import logging
import certifi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URI = "mongodb+srv://777:G0DD4HMvoKNjJzL6@neothink.xnzwv.mongodb.net/?retryWrites=true&w=majority"

class Database:
    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            try:
                cls.client = MongoClient(
                    MONGODB_URI,
                    serverSelectionTimeoutMS=5000,
                    tlsCAFile=certifi.where()  # Add SSL certificate verification
                )
                # Ping the server to check the connection
                cls.client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise e
        return cls.client

    @classmethod
    def get_db(cls):
        return cls.get_client()['neothink']

    @classmethod
    def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            logger.info("MongoDB connection closed")
