from utils.db_connection import get_db_engine
import pandas as pd

def run_query(sql):
    engine = get_db_engine()
    return pd.read_sql(sql, engine)
