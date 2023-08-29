from db_utils2 import db_connect

import pandas as pd
import sqlite3
import os
import sys

con = db_connect()

df_all = pd.DataFrame()
datadir = "/home/nosamaj/EAdata/"

for file in os.listdir(datadir):
    df = pd.read_csv(f"{datadir}/{file}")
    df = df.drop(["Unnamed: 0"], axis=1)
  
    df.to_sql("values", con, if_exists='append', index=False)

