from db_utils2 import create_db_connection, load_parquet, optimise_table
import os

engine = create_db_connection()


for file in os.listdir("/home/nosamaj/EAdata"):
    print(f"loading {file}")
    load_parquet(f"/home/nosamaj/EAdata/{file}",engine,"ea_readings")

#optimise_table(engine,"ea_readings","dateTime","measure")

