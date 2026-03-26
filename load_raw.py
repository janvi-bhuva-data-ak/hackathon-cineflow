import pandas as pd
import psycopg2
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os
load_dotenv()


#-----------------connect postgres

pg = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

#----------connect snowflake
sf = snowflake.connector.connect(
    account=os.getenv("SF_ACCOUNT"),
    user=os.getenv("SF_USER"),
    password=os.getenv("SF_PASSWORD"),
    warehouse=os.getenv("SF_WAREHOUSE"),
    database=os.getenv("SF_DATABASE"),
    schema=os.getenv("SF_SCHEMA") 
)


tables = [
    "movies",
    "users",
    "theaters",
    "screens",
    "showtime",
    "bookings",
    "payments",
    "reviews"
]

#------------------load data to snowflake 
for table in tables:
    print(f"\n Loading {table}...")
    df = pd.read_sql(f"SELECT * FROM {table}", pg)
    df.columns = [col.upper() for col in df.columns]
    success, nchunks, nrows, _ = write_pandas(
        sf,
        df,
        table.upper(),
        auto_create_table=True,
        overwrite=True
    )

    print(f" {table}: {nrows} rows loaded to Snowflake RAW")


pg.close()
sf.close()

print("\nraw data load complete!")