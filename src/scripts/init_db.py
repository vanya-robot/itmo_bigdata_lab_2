import logging
from src.db.database import engine, Base
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info(f"Initializing database on {settings.database_url}")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()