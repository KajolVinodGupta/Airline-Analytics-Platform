import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def get_engine(user="root", password="admin", host="localhost", port=3306, db="airline_analytics"):
    """
    Creates a SQLAlchemy engine for MySQL.
    """
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


def upload_dataframe(df: pd.DataFrame, table_name: str, engine=None, if_exists="append"):
    """
    Uploads a Pandas DataFrame to a MySQL table using SQLAlchemy.

    Args:
        df (pd.DataFrame): DataFrame to upload
        table_name (str): MySQL table name
        engine: SQLAlchemy engine object
        if_exists: append / replace / fail (default: append)

    Returns:
        bool: True if success, False if failed
    """
    if engine is None:
        raise ValueError("Engine cannot be None")

    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        print(f"[SUCCESS] Uploaded {len(df)} rows to '{table_name}' table.")
        return True

    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to upload to {table_name}: {e}")
        return False
