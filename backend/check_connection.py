from database import Database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_mongodb_connection():
    try:
        client = Database.get_client()
        db = client['neothink']
        collections = db.list_collection_names()
        logger.info(f"Connected successfully. Collections: {collections}")
        return True
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False
    finally:
        Database.close_connection()

if __name__ == "__main__":
    check_mongodb_connection()
