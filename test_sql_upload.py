import pandas as pd
from utils.upload_to_sql import get_engine, upload_dataframe

engine = get_engine(password="admin")

df = pd.DataFrame({
    "test_col": ["A", "B", "C"]
})

upload_dataframe(df, "test_table", engine, if_exists="replace")
