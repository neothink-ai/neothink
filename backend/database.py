from pymongo import MongoClient
import logging
import certifi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URI = "mongodb+srv://777:G0DD4HMvoKNjJzL6@neothink.xnzwv.mongodb.net/neothink?retryWrites=true&w=majority"

class Database:
    client = None
    db = None

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
                
                # Initialize database
                cls.db = cls.client['neothink']
                logger.info(f"Connected to database: {cls.db.name}")
                
                # Create Tasks collection if it doesn't exist
                if 'tasks' not in cls.db.list_collection_names():
                    cls.db.create_collection('tasks')
                    logger.info("Created tasks collection")
                
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise e
        return cls.client

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.get_client()
        return cls.db

    @classmethod
    def close_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            logger.info("MongoDB connection closed")
