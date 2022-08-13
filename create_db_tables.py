from db_utils import db_connect

con = db_connect()
cur = con.cursor()

readings_sql = """
    CREATE TABLE readings (
    id integer PRIMARY KEY,
    date_time text NOT NULL,
    measure text NOT NULL, 
    value real NOT NULL)"""

cur.execute(readings_sql)