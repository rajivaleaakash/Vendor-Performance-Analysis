from sqlalchemy import create_engine, text
import os
import urllib.parse
from logging_setup import setup_logger
logger = setup_logger('data_ingestion')
from dotenv import load_dotenv
load_dotenv()

def create_connection():
    """Create and Return database engine"""
    try:
        # Get the Enviroment Variables
        user = os.getenv('DB_USER')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        password = urllib.parse.quote(os.getenv('DB_PASSWORD'))

        # Create Connection String
        engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
            )

        # Test Connection
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        
        logger.info("Database connection established successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to create database connection: {e}")
        raise


def ingestion_DB(df, tbl_name, engine):
    try:
        clean_tbl_name = tbl_name.replace(' ','_').replace('-','_').replace('.','_')
        logger.info(f"Starting ingestion for table: {clean_tbl_name}")
        logger.info(f"Dataframe shape: Rows:{df.shape[0]} Columns:{df.shape[1]}")
        df.to_sql(
            clean_tbl_name,
            con = engine,
            if_exists = 'replace',
            index = False,
            chunksize = 10000
        )

        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {clean_tbl_name}"))
            count = result.scalar()
            logger.info(f"Successfully ingested {count} records into table '{clean_tbl_name}'")
        return True

    except Exception as e:
        logger.error(f"Failed to ingest data into table '{clean_tbl_name}': {e}")
        return False

if __name__ == "__main__":
    engine = create_connection()
    