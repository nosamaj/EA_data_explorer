
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect



def create_db_connection():
    with open("/home/nosamaj/timescale.conf","r") as f:
        u = f.readline().rstrip()
        p = f.readline().rstrip()
        
        db_uri = f"postgresql://{u}:{p}@localhost:5432/tsdb"
        engine = create_engine(db_uri)

    return engine

def load_parquet(path,engine,table_name):

    parquet_file_path = path
    print(f"Attempting to read {path}")
    df2 = pd.read_parquet(parquet_file_path) 
    df = df2[['datetime','measure','value']]
    del df2
    print(f"Read {path}")

    inspector = inspect(engine)
    table_exists = table_name in inspector.get_table_names()
    
    print(f"table_exists = {table_exists}")

    if not table_exists:
# Create the table using the schema of the DataFrame
        print(f"loading {path} into new table named {table_name}")
        df.to_sql(table_name, con=engine, index=False,chunksize=8000)
        print("load complete")
    else:
    # Append data to the existing table
        print(f"loading {path} into existing table named {table_name}")
        df.to_sql(table_name, con=engine, index=False, if_exists='append',chunksize=8000)
        print("load complete")

def optimise_table(engine,table,timestamp_col,id_col):
    create_hypertable_query = f"""
    SELECT create_hypertable({table}, {timestamp_col});
    """
    engine.execute(create_hypertable_query)

    create_index_query = f"""
    CREATE INDEX your_index_name ON your_table_name ({timestamp_col}, {id_col});
    """
    engine.execute(create_index_query)



def select_timeseries(engine,table,measures,start_time,end_time):
    # Construct the SQL query
    query = f"""
    SELECT *
    FROM %s
    WHERE measure IN ({', '.join(['%s'] * len(measures))})
        AND timestamp_column BETWEEN %s AND %s
    """
    
    # Execute the query and fetch results into a DataFrame
    with engine.connect() as conn:
        results = conn.execute(query, table, tuple(measures), start_time, end_time)
        df = pd.DataFrame(results.fetchall(), columns=results.keys())
    
    return df

if __name__ == "__main__":

    con = create_db_connection()
    import pandas as pd

    load_parquet('/home/nosamaj/EAdata/2023-07.parquet',con,'test_table2')
